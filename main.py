import hashlib
import json
import os
import secrets
from datetime import UTC, datetime, timedelta
from time import perf_counter
from typing import Any
from uuid import UUID, uuid4

from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError, VerificationError

from kzo_snapshot_persist import (
    find_snapshot_by_request_id,
    insert_snapshot_row,
    validate_kzo_mvp_snapshot_v1,
)
from services.menu_registry_service import MenuRegistryService, resolve_menu_environment_scope
import services.menu_registry_service as _menu_registry_svc

try:
    from supabase import Client, create_client
except ImportError:
    Client = Any  # type: ignore[misc, assignment]
    create_client = None  # type: ignore[misc, assignment]

app = FastAPI()


KZO_REQUIRED_FIELDS = (
    "object_number",
    "product_type",
    "logic_version",
    "voltage_class",
    "busbar_current",
    "configuration_type",
    "quantity_total",
    "cell_distribution",
    "status",
)

KZO_VOLTAGE_CLASSES = {"VC_06", "VC_10", "VC_20", "VC_35"}
KZO_CONFIGURATION_TYPES = {"CFG_SINGLE_BUS", "CFG_SINGLE_BUS_SECTION"}
KZO_CELL_TYPES = {
    "CELL_INCOMER",
    "CELL_OUTGOING",
    "CELL_PT",
    "CELL_BUS_SECTION",
}
KZO_CELL_COMPOSITION_FIELDS = {
    "CELL_INCOMER": "incoming",
    "CELL_OUTGOING": "outgoing",
    "CELL_PT": "pt",
    "CELL_BUS_SECTION": "sectionalizer",
}
KZO_VOLTAGE_CLASS_LABELS = {
    "VC_06": "6kV",
    "VC_10": "10kV",
    "VC_20": "20kV",
    "VC_35": "35kV",
}
KZO_CONFIGURATION_SECTION_COUNTS = {
    "CFG_SINGLE_BUS": 1,
    "CFG_SINGLE_BUS_SECTION": 2,
}
# Stage 5B MVP — rough lineup width only (not detailed engineering / not CAD)
KZO_STAGE_5B_MVP_STANDARD_CELL_WIDTH_MM = 800
KZO_OBJECT_STATUSES = {
    "DRAFT",
    "VALIDATED",
    "LOCKED",
    "SENT_TO_NEXT_MODULE",
    "ARCHIVED",
    "ERROR",
}

EDS_CLIENT_TYPES = frozenset({"GAS", "WEB", "MOBILE", "AGENT", "UNKNOWN"})
DEMO_ALLOWED_CLIENT_TYPE = "GAS_DEMO"
DEMO_ALLOWED_MODE = "MODULE_01_DEMO"
DEMO_ALLOWED_PRODUCT_TYPE = "KZO"
DEMO_ALLOWED_DEMO_ID = "MODULE_01_KZO_DEMO_001"
DEMO_ALLOWED_OUTPUT_BLOCKS = frozenset(
    {
        "demo_status",
        "status_flow",
        "node_results",
        "fastener_decisions",
        "kit_issue_lines",
        "traceability",
        "boundary_note",
        "management_summary",
        "registry_versions",
    }
)
DEMO_FORBIDDEN_FLAGS = frozenset(
    {
        "pricing",
        "procurement",
        "warehouse",
        "erp",
        "cad",
        "production",
        "db_write",
        "supabase_write",
    }
)
DEMO_REQUIRED_REQUEST_FIELDS = (
    "request_id",
    "client_type",
    "mode",
    "product_type",
    "demo_id",
    "requested_output_blocks",
    "operator_context",
)

DEMO_ERROR_INVALID_REQUEST_ID = "ERR_INVALID_REQUEST_ID"
DEMO_ERROR_INVALID_CLIENT_TYPE = "ERR_INVALID_CLIENT_TYPE"
DEMO_ERROR_INVALID_MODE = "ERR_INVALID_MODE"
DEMO_ERROR_INVALID_PRODUCT_TYPE = "ERR_INVALID_PRODUCT_TYPE"
DEMO_ERROR_INVALID_DEMO_ID = "ERR_INVALID_DEMO_ID"
DEMO_ERROR_UNSUPPORTED_OUTPUT_BLOCK = "ERR_UNSUPPORTED_OUTPUT_BLOCK"
DEMO_ERROR_FORBIDDEN_FLAG = "ERR_FORBIDDEN_FLAG"
DEMO_ERROR_RUNNER_FAILURE = "ERR_DEMO_RUNNER_FAILURE"
DEMO_ERROR_LOGIC_CHAIN_FAILURE = "ERR_LOGIC_CHAIN_FAILURE"
DEMO_ERROR_FIXTURE_MUTATION = "ERR_FIXTURE_MUTATION_DETECTED"
DEMO_ERROR_DEMO_VERSION_MISMATCH = "ERR_DEMO_VERSION_MISMATCH"
DEMO_ERROR_BOUNDARY_VIOLATION = "ERR_BOUNDARY_VIOLATION"
DEMO_MISSING_FIELD_ERRORS = {
    "request_id": DEMO_ERROR_INVALID_REQUEST_ID,
    "client_type": DEMO_ERROR_INVALID_CLIENT_TYPE,
    "mode": DEMO_ERROR_INVALID_MODE,
    "product_type": DEMO_ERROR_INVALID_PRODUCT_TYPE,
    "demo_id": DEMO_ERROR_INVALID_DEMO_ID,
    "requested_output_blocks": DEMO_ERROR_UNSUPPORTED_OUTPUT_BLOCK,
}

AUTH_MODULE_NAME = "MODULE_01_AUTH"
AUTH_ALLOWED_ACTIONS_TEST_OPERATOR = ["auth.login", "auth.refresh_menu"]
AUTH_FAILURE_MESSAGE = "Authentication failed"
AUTH_FAILURE_CODE = "AUTH_FAILED"
AUTH_REQUIRED_ENV_KEYS = ("SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY", "AUTH_SESSION_TTL_HOURS")
AUTH_MENU_MOCK_RESPONSE_VERSION = "EDS_POWER_MENU_V1"
AUTH_MENU_ACTION = "menu"
_AUTH_LOGIN_DIAG_ALLOWED_KEYS: frozenset[str] = frozenset(
    {
        "request_id",
        "auth_stage",
        "email_present",
        "email_domain",
        "spreadsheet_id_present",
        "spreadsheet_id_suffix",
        "supabase_query_user_found",
        "user_status",
        "supabase_query_terminal_found",
        "terminal_status",
        "terminal_spreadsheet_match",
        "supabase_query_auth_row_found",
        "password_algorithm",
        "password_hash_present",
        "locked_until_present",
        "password_verify_result",
        "final_auth_result",
        "request_spreadsheet_len",
        "stored_spreadsheet_len",
        "request_spreadsheet_suffix_12",
        "stored_spreadsheet_suffix_12",
        "request_spreadsheet_md5",
        "stored_spreadsheet_md5",
        "request_spreadsheet_normalized_len",
        "stored_spreadsheet_normalized_len",
        "request_spreadsheet_normalized_md5",
        "stored_spreadsheet_normalized_md5",
    }
)

AUTH_MENU_MOCK_ITEMS = [
    {
        "menu_id": "refresh_menu",
        "menu_label": "Оновити меню",
        "action_key": "REFRESH_MENU",
        "action_type": "REFRESH_MENU",
        "visibility": "VISIBLE",
        "enabled": True,
        "sort_order": 10,
    },
    {
        "menu_id": "session_status",
        "menu_label": "Статус сесії",
        "action_key": "SESSION_STATUS",
        "action_type": "SESSION_STATUS",
        "visibility": "VISIBLE",
        "enabled": True,
        "sort_order": 20,
    },
    {
        "menu_id": "module_01_placeholder",
        "module_id": "MODULE_01",
        "module_name": "Module 01",
        "menu_label": "Module 01 — Розрахунки (planned)",
        "action_key": "MODULE_01_PLACEHOLDER",
        "action_type": "PLACEHOLDER_DISABLED",
        "visibility": "VISIBLE",
        "enabled": False,
        "module_status": "PLANNED",
        "sort_order": 30,
    },
    {
        "menu_id": "logout",
        "menu_label": "Вийти",
        "action_key": "LOGOUT",
        "action_type": "LOGOUT",
        "visibility": "VISIBLE",
        "enabled": True,
        "sort_order": 90,
    },
]

_auth_supabase_client: Client | None = None
_password_hasher = PasswordHasher()

KZO_PROTOTYPE_CONSTRUCTIVE_FAMILY = "KZO_WELDED"
KZO_PROTOTYPE_CELL_ROLE = "VACUUM_BREAKER"
KZO_PROTOTYPE_CELL_POSITION = "LEFT_END"
KZO_PROTOTYPE_NODE = "INSULATOR_SYSTEM"

_SNAPSHOT_ERROR_MESSAGES: dict[str, str] = {
    "SNAPSHOT_BODY_NOT_OBJECT": "Request body must be a JSON object.",
    "SNAPSHOT_UNKNOWN_FIELDS": "Snapshot JSON contains unsupported top-level fields.",
    "SNAPSHOT_VERSION_INVALID": "snapshot_version must be KZO_MVP_SNAPSHOT_V1.",
    "SNAPSHOT_RUN_STATUS_INVALID": "run_status must be SUCCESS or FAILED.",
    "SNAPSHOT_MISSING_TIMESTAMP": "timestamp_basis is required.",
    "SNAPSHOT_TIMESTAMP_INVALID": "timestamp_basis is not a valid ISO-8601 timestamp.",
    "SNAPSHOT_SUCCESS_LAYER_INVALID": "SUCCESS snapshots require non-empty engineering layer objects.",
    "SNAPSHOT_LOGIC_VERSION_REQUIRED": "logic_version is required for SUCCESS snapshots.",
    "SNAPSHOT_REQUEST_METADATA_REQUIRED": "request_metadata must be an object.",
    "SNAPSHOT_REQUEST_METADATA_TYPE_INVALID": "FAILED snapshots require request_metadata to be an object or omitted.",
    "SNAPSHOT_NORMALIZED_INPUT_TYPE_INVALID": "FAILED snapshots require normalized_input to be an object or null.",
    "SNAPSHOT_REQUEST_METADATA_SUBKEY_MISSING": "request_metadata must include request_id, api_version, logic_version, execution_time_ms.",
    "SNAPSHOT_REQUEST_METADATA_REQUEST_ID_INVALID": "request_metadata.request_id must be a non-empty string.",
    "SNAPSHOT_REQUEST_METADATA_API_VERSION_INVALID": "request_metadata.api_version must be a non-empty string.",
    "SNAPSHOT_REQUEST_METADATA_LOGIC_VERSION_INVALID": "request_metadata.logic_version must be a non-empty string.",
    "SNAPSHOT_REQUEST_METADATA_EXECUTION_TIME_INVALID": "request_metadata.execution_time_ms must be a non-negative integer.",
    "SNAPSHOT_NORMALIZED_INPUT_REQUIRED": "SUCCESS snapshots require normalized_input object.",
    "SNAPSHOT_SUCCESS_MUST_NOT_HAVE_FAILURE": "SUCCESS snapshots must not include failure.",
    "SNAPSHOT_FAILURE_DETAIL_REQUIRED": "FAILED snapshots require a failure object.",
    "SNAPSHOT_FAILURE_ERROR_CODE_REQUIRED": "failure.error_code is required for FAILED snapshots.",
    "SNAPSHOT_FAILURE_MESSAGE_REQUIRED": "failure.message is required for FAILED snapshots.",
    "SNAPSHOT_LOGIC_VERSION_METADATA_MISMATCH": "logic_version must match request_metadata.logic_version.",
    "SNAPSHOT_INSERT_FAILED": "Snapshot row could not be stored.",
    "SNAPSHOT_DUPLICATE_CHECK_FAILED": "Duplicate protection check failed.",
    "SNAPSHOT_DUPLICATE_REJECTED": "Duplicate snapshot save request rejected.",
    "SNAPSHOT_PERSISTENCE_UNAVAILABLE": "Persistence service is not configured.",
}


def normalize_eds_client_type(raw: str | None) -> str:
    if raw is None or str(raw).strip() == "":
        return "UNKNOWN"
    cand = str(raw).strip().upper()
    return cand if cand in EDS_CLIENT_TYPES else "UNKNOWN"


def _failure_envelope(code: str) -> dict[str, Any]:
    return {
        "error_code": code,
        "message": _SNAPSHOT_ERROR_MESSAGES.get(code, "Snapshot request rejected."),
        "details": {},
    }


def save_snapshot_http_response_success(
    *,
    snapshot_id: str,
    client_type: str,
    created_at: str | None,
) -> dict[str, Any]:
    created = created_at
    if not created:
        created = datetime.now(UTC).isoformat()
    return {
        "status": "SUCCESS",
        "snapshot_id": snapshot_id,
        "persistence_status": "STORED",
        "snapshot_version": "KZO_MVP_SNAPSHOT_V1",
        "created_at": created,
        "client_type": client_type,
        "failure": None,
        "error_code": None,
    }


def save_snapshot_http_response_failure(
    *,
    client_type: str,
    persistence_status: str,
    response_snapshot_version: str | None,
    error_code: str,
    snapshot_id: str | None = None,
    created_at: str | None = None,
    legacy_flat_error: bool = True,
) -> dict[str, Any]:
    """validation → REJECTED; insert/infrastructure → ERROR."""
    fb = _failure_envelope(error_code)
    out: dict[str, Any] = {
        "status": "FAILED",
        "snapshot_id": snapshot_id,
        "persistence_status": persistence_status,
        "snapshot_version": response_snapshot_version,
        "created_at": created_at,
        "client_type": client_type,
        "failure": fb,
    }
    if legacy_flat_error:
        out["error_code"] = error_code
    return out


def _response_metadata(meta: dict[str, Any] | None, logic_version: str | None, started_at: float) -> dict[str, Any]:
    return {
        "request_id": (meta or {}).get("request_id") or str(uuid4()),
        "api_version": "0.1.0",
        "logic_version": logic_version,
        "execution_time_ms": int((perf_counter() - started_at) * 1000),
    }


def _validation_error(
    *,
    message: str,
    source_field: str,
    error_code: str,
    meta: dict[str, Any] | None,
    logic_version: str | None,
    started_at: float,
) -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content={
            "status": "validation_error",
            "data": None,
            "error": {
                "error_code": error_code,
                "message": message,
                "source_field": source_field,
                "module": "CALC_CONFIGURATOR",
                "action": "prepare_calculation",
            },
            "metadata": _response_metadata(meta, logic_version, started_at),
        },
    )


def _is_uuid4(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = UUID(value)
    except (TypeError, ValueError):
        return False
    return parsed.version == 4 and str(parsed) == value.lower()


def _demo_metadata(request_id: str, client_type: Any) -> dict[str, Any]:
    return {
        "request_id": request_id if isinstance(request_id, str) else str(request_id),
        "client_type": client_type if isinstance(client_type, str) else str(client_type),
        "generated_at": datetime.now(UTC).isoformat(),
    }


def _demo_error_response(
    *,
    request_id: Any,
    client_type: Any,
    error_code: str,
    message: str,
    source_field: str,
    notes: list[str] | None = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=200,
        headers={"X-EDS-Power-Mode": "DEMO"},
        content={
            "status": "error",
            "data": None,
            "error": {
                "error_code": error_code,
                "message": message,
                "source_field": source_field,
                "notes": notes or [],
            },
            "metadata": _demo_metadata(request_id=request_id, client_type=client_type),
        },
    )


def _collect_registry_versions(node: Any, collector: list[Any]) -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "registry_version" or key.endswith("_registry_version"):
                collector.append(value)
            _collect_registry_versions(value, collector)
    elif isinstance(node, list):
        for item in node:
            _collect_registry_versions(item, collector)


def _run_module_01_demo_in_memory() -> dict[str, Any]:
    from src.runners.module_01_demo_runner import run_module_01_local_demo

    return run_module_01_local_demo(write_output=False)


def _validate_kzo_payload(payload: dict[str, Any]) -> tuple[dict[str, Any] | None, tuple[str, str, str] | None]:
    for field in KZO_REQUIRED_FIELDS:
        if field not in payload or payload[field] is None:
            return None, (
                "KZO_REQUIRED_FIELD_MISSING",
                f"Required field {field} is missing",
                field,
            )

    if payload["product_type"] != "KZO":
        return None, ("KZO_UNSUPPORTED_CONFIGURATION", "Only KZO product_type is supported", "product_type")

    if payload["voltage_class"] not in KZO_VOLTAGE_CLASSES:
        return None, ("KZO_INVALID_VOLTAGE_CLASS", "Invalid voltage_class", "voltage_class")

    if payload["configuration_type"] not in KZO_CONFIGURATION_TYPES:
        return None, ("KZO_UNSUPPORTED_CONFIGURATION", "Unsupported configuration_type", "configuration_type")

    if payload["status"] not in KZO_OBJECT_STATUSES:
        return None, ("KZO_UNSUPPORTED_CONFIGURATION", "Unsupported object status", "status")

    if not isinstance(payload["quantity_total"], int) or payload["quantity_total"] <= 0:
        return None, ("KZO_CELL_QUANTITY_MISMATCH", "quantity_total must be a positive integer", "quantity_total")

    cell_distribution = payload["cell_distribution"]
    if not isinstance(cell_distribution, dict):
        return None, ("KZO_CELL_QUANTITY_MISMATCH", "cell_distribution must be an object", "cell_distribution")

    for cell_type, quantity in cell_distribution.items():
        if cell_type not in KZO_CELL_TYPES:
            return None, ("KZO_UNSUPPORTED_CONFIGURATION", "Unsupported cell_type", "cell_distribution")
        if not isinstance(quantity, int) or quantity < 0:
            return None, ("KZO_CELL_QUANTITY_MISMATCH", "Cell quantities must be non-negative integers", "cell_distribution")

    if sum(cell_distribution.values()) != payload["quantity_total"]:
        return None, (
            "KZO_CELL_QUANTITY_MISMATCH",
            "Cell distribution sum must match quantity_total",
            "cell_distribution",
        )

    normalized_payload = {field: payload[field] for field in KZO_REQUIRED_FIELDS}
    normalized_payload["status"] = "VALIDATED"
    normalized_payload["breaker_type"] = payload.get("breaker_type")
    normalized_payload["notes"] = payload.get("notes")

    return normalized_payload, None


def _build_kzo_structural_composition_summary(normalized_payload: dict[str, Any]) -> dict[str, Any]:
    cell_distribution = normalized_payload["cell_distribution"]
    cell_composition = {
        summary_field: cell_distribution.get(cell_type, 0)
        for cell_type, summary_field in KZO_CELL_COMPOSITION_FIELDS.items()
    }
    total_cells = normalized_payload["quantity_total"]
    section_cells = cell_composition["sectionalizer"]
    sections = KZO_CONFIGURATION_SECTION_COUNTS[normalized_payload["configuration_type"]]
    structural_flags = []

    if cell_composition["incoming"] >= 2:
        structural_flags.append("dual_incoming")
    if total_cells > 0 and cell_composition["outgoing"] / total_cells >= 0.5:
        structural_flags.append("high_outgoing_density")
    if cell_composition["pt"] > 0:
        structural_flags.append("pt_present")
    if section_cells > 0:
        structural_flags.append("sectionalized_lineup")

    return {
        "summary_version": "KZO_STAGE_5A_STRUCTURAL_COMPOSITION_V1",
        "product_type": normalized_payload["product_type"],
        "lineup_summary": {
            "total_cells": total_cells,
            "sections": sections,
            "primary_voltage_class": KZO_VOLTAGE_CLASS_LABELS[normalized_payload["voltage_class"]],
            "busbar_current": f"{normalized_payload['busbar_current']}A",
            "configuration_type": normalized_payload["configuration_type"],
        },
        "cell_composition": cell_composition,
        "functional_lineup_composition": {
            "incoming_cells": cell_composition["incoming"],
            "outgoing_cells": cell_composition["outgoing"],
            "voltage_transformer_cells": cell_composition["pt"],
            "sectionalizer_cells": cell_composition["sectionalizer"],
        },
        "structural_flags": structural_flags,
        "interpretation_scope": "STRUCTURAL_COMPOSITION_ONLY",
    }


def _kzo_footprint_class_mvp(total_cells: int) -> str:
    """Deterministic MVP bucket from cell count; not product catalog truth."""
    if total_cells <= 12:
        return "compact_lineup"
    if total_cells <= 18:
        return "standard_lineup"
    if total_cells <= 26:
        return "large_lineup"
    return "extended_lineup"


def _build_kzo_physical_footprint_summary(structural_composition_summary: dict[str, Any]) -> dict[str, Any]:
    lineup = structural_composition_summary["lineup_summary"]
    total_cells: int = lineup["total_cells"]
    section_count: int = lineup["sections"]
    w_mm = KZO_STAGE_5B_MVP_STANDARD_CELL_WIDTH_MM
    estimated_width_mm = total_cells * w_mm
    return {
        "summary_version": "KZO_STAGE_5B_PHYSICAL_FOOTPRINT_MVP_V1",
        "estimated_total_width_mm": estimated_width_mm,
        "section_count": section_count,
        "footprint_class": _kzo_footprint_class_mvp(total_cells),
        "basis": "total_cells x standard_cell_width_mvp",
        "mvp_standard_cell_width_mm": w_mm,
        "interpretation_scope": "PHYSICAL_SCALE_ESTIMATE_MVP_ONLY",
    }


def _build_kzo_physical_topology_summary(structural_composition_summary: dict[str, Any]) -> dict[str, Any]:
    lineup = structural_composition_summary["lineup_summary"]
    total_cells: int = lineup["total_cells"]
    total_sections: int = lineup["sections"]

    if total_sections == 1:
        topology_type = "TOPOLOGY_SINGLE_SECTION"
        section_distribution = [{"section_id": "A", "cell_count": total_cells}]
    elif total_sections == 2:
        a_cells = (total_cells + 1) // 2
        b_cells = total_cells // 2
        topology_type = "TOPOLOGY_BALANCED_SPLIT" if a_cells == b_cells else "TOPOLOGY_UNEVEN_SPLIT"
        section_distribution = [
            {"section_id": "A", "cell_count": a_cells},
            {"section_id": "B", "cell_count": b_cells},
        ]
    else:
        # Invariant: MVP configuration types map to 1–2 sections only; keep safe single-bucket output.
        topology_type = "TOPOLOGY_UNSUPPORTED_SECTION_COUNT_MVP"
        section_distribution = [{"section_id": "A", "cell_count": total_cells}]

    section_cell_counts = [bucket["cell_count"] for bucket in section_distribution]

    basis = (
        "distribution from lineup_summary.total_cells and lineup_summary.sections "
        "(Stage 5A structural composition); scale context from Stage 5B physical footprint MVP (same request)"
    )

    return {
        "topology_version": "KZO_STAGE_5C_TOPOLOGY_MVP_V1",
        "total_sections": total_sections,
        "topology_type": topology_type,
        "section_distribution": section_distribution,
        "section_cell_counts": section_cell_counts,
        "interpretation_scope": "PHYSICAL_TOPOLOGY_MVP_ONLY",
        "basis": basis,
    }


def _kzo_lineup_scale_class(total_cells: int) -> str:
    """Planning-grade scale bucket from cell count; not manufacturing truth."""
    if total_cells <= 8:
        return "COMPACT"
    if total_cells <= 16:
        return "STANDARD"
    if total_cells <= 26:
        return "LARGE"
    return "EXTENDED"


def _kzo_section_complexity_piece_mvp(section_cell_count: int) -> str:
    """Per-section planning label for engineering_class_summary."""
    if section_cell_count <= 6:
        return "LIGHT"
    if section_cell_count <= 14:
        return "STANDARD"
    return "HEAVY"


def _build_kzo_engineering_class_summary(
    structural_composition_summary: dict[str, Any],
    physical_topology_summary: dict[str, Any],
) -> dict[str, Any]:
    """Stage 6B — planning intelligence only (no mass, BOM, price, CAD)."""
    lineup = structural_composition_summary["lineup_summary"]
    structural_flags = structural_composition_summary.get("structural_flags") or []
    total_cells = int(lineup["total_cells"])
    total_sections = physical_topology_summary.get("total_sections", 1)
    topology_type = str(physical_topology_summary.get("topology_type") or "TOPOLOGY_SINGLE_SECTION")

    lineup_scale_class = _kzo_lineup_scale_class(total_cells)

    counts = physical_topology_summary.get("section_cell_counts")
    if not isinstance(counts, list):
        counts = [total_cells]
    section_complexity_profile = [_kzo_section_complexity_piece_mvp(int(c)) for c in counts]

    dual_incoming = "dual_incoming" in structural_flags
    high_outgoing_density = "high_outgoing_density" in structural_flags
    uneven_topology = topology_type == "TOPOLOGY_UNEVEN_SPLIT"

    if total_cells >= 27 or uneven_topology:
        lineup_complexity_class = "EXTENDED"
    elif (
        isinstance(total_sections, int)
        and total_sections >= 2
        and (dual_incoming or high_outgoing_density)
    ):
        lineup_complexity_class = "HEAVY"
    elif total_sections == 1 and total_cells <= 8:
        lineup_complexity_class = "LIGHT"
    else:
        lineup_complexity_class = "STANDARD"

    return {
        "classification_version": "KZO_STAGE_6B_ENGINEERING_CLASS_MVP_V1",
        "lineup_complexity_class": lineup_complexity_class,
        "lineup_scale_class": lineup_scale_class,
        "section_complexity_profile": section_complexity_profile,
        "total_cells_basis": total_cells,
        "topology_basis": topology_type,
        "interpretation_scope": "ENGINEERING_CLASSIFICATION_ONLY_MVP",
    }


def _build_kzo_engineering_burden_summary(
    engineering_class_summary: dict[str, Any],
    physical_topology_summary: dict[str, Any],
    structural_composition_summary: dict[str, Any],
) -> dict[str, Any]:
    """Stage 6C — planning burden only (no kg, BOM, price, CAD)."""
    lc = str(engineering_class_summary.get("lineup_complexity_class") or "STANDARD")
    ls = str(engineering_class_summary.get("lineup_scale_class") or "STANDARD")
    topology_type = str(physical_topology_summary.get("topology_type") or "TOPOLOGY_SINGLE_SECTION")
    total_sections = int(physical_topology_summary.get("total_sections") or 1)
    structural_flags = structural_composition_summary.get("structural_flags") or []
    dual_incoming = "dual_incoming" in structural_flags

    complexity_basis = f"COMPLEXITY_{lc}"
    footprint_basis = f"SCALE_{ls}"

    if lc == "EXTENDED" or ls == "EXTENDED":
        structural_burden_class = "BURDEN_EXTENDED"
    elif lc == "HEAVY" and total_sections >= 2:
        structural_burden_class = "BURDEN_HEAVY"
    elif ls == "LARGE" and lc == "STANDARD":
        structural_burden_class = "BURDEN_STANDARD"
    elif ls == "LARGE" or lc == "HEAVY":
        structural_burden_class = "BURDEN_HEAVY"
    elif lc == "LIGHT" and ls == "COMPACT":
        structural_burden_class = "BURDEN_LIGHT"
    else:
        structural_burden_class = "BURDEN_STANDARD"

    if total_sections >= 2 and topology_type == "TOPOLOGY_UNEVEN_SPLIT":
        assembly_burden_class = "ASSEMBLY_COMPLEX"
    elif total_sections >= 2 and lc in ("HEAVY", "EXTENDED"):
        assembly_burden_class = "ASSEMBLY_COMPLEX"
    elif total_sections == 1 and lc == "LIGHT":
        assembly_burden_class = "ASSEMBLY_SIMPLE"
    elif dual_incoming:
        assembly_burden_class = "ASSEMBLY_COMPLEX"
    else:
        assembly_burden_class = "ASSEMBLY_STANDARD"

    tier_order = ("MASS_LITE", "MASS_STANDARD", "MASS_HEAVY", "MASS_EXTENDED")
    scale_mass_idx = {"COMPACT": 0, "STANDARD": 1, "LARGE": 2, "EXTENDED": 3}.get(ls, 1)
    mass_idx = scale_mass_idx
    if lc == "HEAVY":
        mass_idx = min(mass_idx + 1, 3)
    if lc == "EXTENDED":
        mass_idx = 3
    estimated_mass_class = tier_order[mass_idx]

    return {
        "burden_version": "KZO_STAGE_6C_ENGINEERING_BURDEN_MVP_V1",
        "structural_burden_class": structural_burden_class,
        "assembly_burden_class": assembly_burden_class,
        "estimated_mass_class": estimated_mass_class,
        "complexity_basis": complexity_basis,
        "topology_basis": topology_type,
        "footprint_basis": footprint_basis,
        "interpretation_scope": "ENGINEERING_BURDEN_ONLY_MVP",
    }


def _build_kzo_layered_node_summary(payload: dict[str, Any]) -> dict[str, Any] | None:
    """Stage prototype: one bounded family/role/position/node planning output."""
    family = payload.get("constructive_family")
    role = payload.get("cell_role")
    position = payload.get("cell_position")
    node = payload.get("node")
    if not all(isinstance(v, str) for v in (family, role, position, node)):
        return None
    if (
        family != KZO_PROTOTYPE_CONSTRUCTIVE_FAMILY
        or role != KZO_PROTOTYPE_CELL_ROLE
        or position != KZO_PROTOTYPE_CELL_POSITION
        or node != KZO_PROTOTYPE_NODE
    ):
        return None

    placement_points = [
        "PP_FRAME_LEFT_PRIMARY",
        "PP_INSULATOR_SUPPORT_A",
        "PP_INSULATOR_SUPPORT_B",
        "PP_BREAKER_INTERFACE_LEFT",
    ]
    presence_rules_result = {
        "family_rule": "ACTIVE",
        "role_rule": "ACTIVE",
        "position_rule": "ACTIVE",
        "node_rule": "ACTIVE",
    }
    primary_components = [
        {"component": "INSULATOR_BASE", "qty": 1},
        {"component": "WELDED_SUPPORT_BRACKET_SET", "qty": 1},
        {"component": "PRIMARY_FASTENING_INTERFACE", "qty": 1},
    ]
    dependent_hardware = [
        {"component": "BOLT_M10", "qty": 4},
        {"component": "WASHER_M10", "qty": 8},
        {"component": "NUT_M10", "qty": 4},
    ]
    aggregate_bom = {
        "line_items": len(primary_components) + len(dependent_hardware),
        "primary_qty_total": sum(int(item["qty"]) for item in primary_components),
        "dependent_qty_total": sum(int(item["qty"]) for item in dependent_hardware),
    }
    return {
        "prototype_version": "KZO_LAYERED_NODE_PROTOTYPE_MVP_V1",
        "constructive_family": family,
        "cell_role": role,
        "cell_position": position,
        "node": node,
        "placement_points": placement_points,
        "presence_rules_result": presence_rules_result,
        "primary_components": primary_components,
        "dependent_hardware": dependent_hardware,
        "aggregate_bom": aggregate_bom,
        "interpretation_scope": "PROTOTYPE_DEMO_CASE_ONLY",
    }


@app.get("/")
def root():
    return {"message": "EDS Power API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/demo/module-01/kzo/run")
def run_module_01_demo_api(request: dict[str, Any]):
    request_id = request.get("request_id")
    client_type = request.get("client_type")

    for field in DEMO_REQUIRED_REQUEST_FIELDS:
        if field not in request:
            error_code = DEMO_MISSING_FIELD_ERRORS.get(field, DEMO_ERROR_LOGIC_CHAIN_FAILURE)
            message = f"Required field {field} is missing."
            if field == "request_id":
                message = "request_id is required and must be UUID v4."
            return _demo_error_response(
                request_id=request_id or str(uuid4()),
                client_type=client_type or "UNKNOWN",
                error_code=error_code,
                message=message,
                source_field=field,
            )

    if not _is_uuid4(request_id):
        return _demo_error_response(
            request_id=request_id or str(uuid4()),
            client_type=client_type or "UNKNOWN",
            error_code=DEMO_ERROR_INVALID_REQUEST_ID,
            message="request_id must be a valid UUID v4.",
            source_field="request_id",
        )
    if client_type != DEMO_ALLOWED_CLIENT_TYPE:
        return _demo_error_response(
            request_id=request_id,
            client_type=client_type,
            error_code=DEMO_ERROR_INVALID_CLIENT_TYPE,
            message=f"client_type must be {DEMO_ALLOWED_CLIENT_TYPE}.",
            source_field="client_type",
        )
    if request.get("mode") != DEMO_ALLOWED_MODE:
        return _demo_error_response(
            request_id=request_id,
            client_type=client_type,
            error_code=DEMO_ERROR_INVALID_MODE,
            message=f"mode must be {DEMO_ALLOWED_MODE}.",
            source_field="mode",
        )
    if request.get("product_type") != DEMO_ALLOWED_PRODUCT_TYPE:
        return _demo_error_response(
            request_id=request_id,
            client_type=client_type,
            error_code=DEMO_ERROR_INVALID_PRODUCT_TYPE,
            message=f"product_type must be {DEMO_ALLOWED_PRODUCT_TYPE}.",
            source_field="product_type",
        )
    if request.get("demo_id") != DEMO_ALLOWED_DEMO_ID:
        return _demo_error_response(
            request_id=request_id,
            client_type=client_type,
            error_code=DEMO_ERROR_INVALID_DEMO_ID,
            message=f"demo_id must be {DEMO_ALLOWED_DEMO_ID}.",
            source_field="demo_id",
        )

    requested_output_blocks = request.get("requested_output_blocks")
    if not isinstance(requested_output_blocks, list) or len(requested_output_blocks) == 0:
        return _demo_error_response(
            request_id=request_id,
            client_type=client_type,
            error_code=DEMO_ERROR_UNSUPPORTED_OUTPUT_BLOCK,
            message="requested_output_blocks must be a non-empty array.",
            source_field="requested_output_blocks",
        )
    if any((not isinstance(block, str)) or block not in DEMO_ALLOWED_OUTPUT_BLOCKS for block in requested_output_blocks):
        return _demo_error_response(
            request_id=request_id,
            client_type=client_type,
            error_code=DEMO_ERROR_UNSUPPORTED_OUTPUT_BLOCK,
            message="requested_output_blocks contains unsupported values.",
            source_field="requested_output_blocks",
        )

    operator_context = request.get("operator_context")
    if not isinstance(operator_context, dict):
        return _demo_error_response(
            request_id=request_id,
            client_type=client_type,
            error_code=DEMO_ERROR_LOGIC_CHAIN_FAILURE,
            message="operator_context must be an object.",
            source_field="operator_context",
        )

    for flag in DEMO_FORBIDDEN_FLAGS:
        if flag in request or flag in operator_context:
            return _demo_error_response(
                request_id=request_id,
                client_type=client_type,
                error_code=DEMO_ERROR_FORBIDDEN_FLAG,
                message=f"Forbidden flag detected: {flag}.",
                source_field=flag,
            )

    try:
        demo_output = _run_module_01_demo_in_memory()
    except AssertionError as error:
        error_code = DEMO_ERROR_FIXTURE_MUTATION if "mutat" in str(error).lower() else DEMO_ERROR_RUNNER_FAILURE
        return _demo_error_response(
            request_id=request_id,
            client_type=client_type,
            error_code=error_code,
            message=str(error),
            source_field="demo_runner",
        )
    except Exception as error:  # noqa: BLE001
        return _demo_error_response(
            request_id=request_id,
            client_type=client_type,
            error_code=DEMO_ERROR_RUNNER_FAILURE,
            message=f"Demo runner execution failed: {error}",
            source_field="demo_runner",
        )

    if demo_output.get("status") != "PASS":
        return _demo_error_response(
            request_id=request_id,
            client_type=client_type,
            error_code=DEMO_ERROR_LOGIC_CHAIN_FAILURE,
            message="Module 01 demo chain did not return PASS.",
            source_field="status",
        )

    collected_versions: list[Any] = []
    _collect_registry_versions(demo_output.get("registry_versions"), collected_versions)
    _collect_registry_versions(demo_output.get("kit_issue_lines"), collected_versions)
    if not collected_versions or any(version != "demo_v1" for version in collected_versions):
        return _demo_error_response(
            request_id=request_id,
            client_type=client_type,
            error_code=DEMO_ERROR_DEMO_VERSION_MISMATCH,
            message="Registry versions must be demo_v1 across response data.",
            source_field="registry_versions",
        )

    fastener_rows = demo_output.get("fastener_decisions")
    if not isinstance(fastener_rows, list) or not fastener_rows:
        return _demo_error_response(
            request_id=request_id,
            client_type=client_type,
            error_code=DEMO_ERROR_LOGIC_CHAIN_FAILURE,
            message="fastener_decisions block is empty.",
            source_field="fastener_decisions",
        )
    if any(
        (not isinstance(row, dict))
        or row.get("decision") not in {"SELECTED", "REJECTED"}
        for row in fastener_rows
    ):
        return _demo_error_response(
            request_id=request_id,
            client_type=client_type,
            error_code=DEMO_ERROR_LOGIC_CHAIN_FAILURE,
            message="fastener_decisions rows must contain SELECTED/REJECTED decisions.",
            source_field="fastener_decisions",
        )

    management_summary = demo_output.get("management_summary")
    if not isinstance(management_summary, str) or not management_summary.strip():
        return _demo_error_response(
            request_id=request_id,
            client_type=client_type,
            error_code=DEMO_ERROR_LOGIC_CHAIN_FAILURE,
            message="management_summary is required for demo success response.",
            source_field="management_summary",
        )

    boundary_note = demo_output.get("boundary_note")
    boundary_required_markers = (
        "local demo only",
        "not production data",
        "not final erp bom",
        "not procurement",
        "not warehouse",
        "not erp/1c",
        "not pricing",
        "not cad",
        "no api/gas/db",
    )
    boundary_lower = str(boundary_note).lower()
    if not isinstance(boundary_note, str) or any(marker not in boundary_lower for marker in boundary_required_markers):
        return _demo_error_response(
            request_id=request_id,
            client_type=client_type,
            error_code=DEMO_ERROR_BOUNDARY_VIOLATION,
            message="boundary_note is missing required demo boundary statements.",
            source_field="boundary_note",
        )

    output_blob = str(demo_output).lower()
    for forbidden_token in ("erp_posting", "warehouse_reservation", "purchase_request", "stock_movement"):
        if forbidden_token in output_blob:
            return _demo_error_response(
                request_id=request_id,
                client_type=client_type,
                error_code=DEMO_ERROR_BOUNDARY_VIOLATION,
                message=f"Forbidden production token detected in response: {forbidden_token}.",
                source_field="data",
            )

    available_blocks: dict[str, Any] = {
        "demo_status": demo_output.get("status"),
        "status_flow": demo_output.get("status_flow"),
        "node_results": demo_output.get("node_results"),
        "fastener_decisions": fastener_rows,
        "kit_issue_lines": demo_output.get("kit_issue_lines"),
        "traceability": {
            "source_node_ids": demo_output.get("source_node_ids"),
            "source_line_ids": demo_output.get("source_line_ids"),
            "traceability_refs": demo_output.get("traceability_refs"),
        },
        "boundary_note": boundary_note,
        "management_summary": management_summary,
        "registry_versions": demo_output.get("registry_versions"),
    }

    data = {"demo_id": demo_output.get("demo_id")}
    for block_name in requested_output_blocks:
        data[block_name] = available_blocks[block_name]
    data["boundary_note"] = boundary_note
    data["management_summary"] = management_summary

    response_payload = {
        "status": "success",
        "data": data,
        "error": None,
        "metadata": {
            "request_id": request_id,
            "logic_version": "MODULE_01_LOCAL_DEMO_CHAIN_V1",
            "demo_version": "demo_v1",
            "generated_at": datetime.now(UTC).isoformat(),
            "client_type": client_type,
            "response_source": "MODULE_01_LOCAL_DEMO_RUNNER",
        },
    }
    return JSONResponse(status_code=200, headers={"X-EDS-Power-Mode": "DEMO"}, content=response_payload)


@app.post("/api/calc/prepare_calculation")
def prepare_calculation(request: dict[str, Any]):
    started_at = perf_counter()
    meta = request.get("meta") if isinstance(request.get("meta"), dict) else None
    payload = request.get("payload") if isinstance(request.get("payload"), dict) else None
    logic_version = payload.get("logic_version") if payload else None

    for field in ("meta", "module", "action", "payload"):
        if field not in request:
            return _validation_error(
                message=f"Required envelope field {field} is missing",
                source_field=field,
                error_code="KZO_REQUIRED_FIELD_MISSING",
                meta=meta,
                logic_version=logic_version,
                started_at=started_at,
            )

    if request["module"] != "CALC_CONFIGURATOR":
        return _validation_error(
            message="module must be CALC_CONFIGURATOR",
            source_field="module",
            error_code="KZO_UNSUPPORTED_CONFIGURATION",
            meta=meta,
            logic_version=logic_version,
            started_at=started_at,
        )

    if request["action"] != "prepare_calculation":
        return _validation_error(
            message="action must be prepare_calculation",
            source_field="action",
            error_code="KZO_UNSUPPORTED_CONFIGURATION",
            meta=meta,
            logic_version=logic_version,
            started_at=started_at,
        )

    if payload is None:
        return _validation_error(
            message="payload must be an object",
            source_field="payload",
            error_code="KZO_REQUIRED_FIELD_MISSING",
            meta=meta,
            logic_version=logic_version,
            started_at=started_at,
        )

    normalized_payload, error = _validate_kzo_payload(payload)
    if error:
        error_code, message, source_field = error
        return _validation_error(
            message=message,
            source_field=source_field,
            error_code=error_code,
            meta=meta,
            logic_version=logic_version,
            started_at=started_at,
        )

    cell_type_summary = {
        cell_type: normalized_payload["cell_distribution"][cell_type]
        for cell_type in sorted(normalized_payload["cell_distribution"])
    }
    structural_composition_summary = _build_kzo_structural_composition_summary(normalized_payload)
    physical_summary = _build_kzo_physical_footprint_summary(structural_composition_summary)
    physical_topology_summary = _build_kzo_physical_topology_summary(structural_composition_summary)
    engineering_class_summary = _build_kzo_engineering_class_summary(
        structural_composition_summary,
        physical_topology_summary,
    )
    engineering_burden_summary = _build_kzo_engineering_burden_summary(
        engineering_class_summary,
        physical_topology_summary,
        structural_composition_summary,
    )

    data = {
        "validation_status": "VALIDATED",
        "logic_version": normalized_payload["logic_version"],
        "status": normalized_payload["status"],
        "normalized_payload": normalized_payload,
        "basic_result_summary": {
            "summary_version": "KZO_MVP_V1",
            "product_type": normalized_payload["product_type"],
            "logic_version": normalized_payload["logic_version"],
            "voltage_class": normalized_payload["voltage_class"],
            "busbar_current": normalized_payload["busbar_current"],
            "configuration_type": normalized_payload["configuration_type"],
            "quantity_total": normalized_payload["quantity_total"],
            "cell_type_summary": cell_type_summary,
            "validation_status": "VALIDATED",
        },
        "structural_composition_summary": structural_composition_summary,
        "physical_summary": physical_summary,
        "physical_topology_summary": physical_topology_summary,
        "engineering_class_summary": engineering_class_summary,
        "engineering_burden_summary": engineering_burden_summary,
    }
    layered_node_summary = _build_kzo_layered_node_summary(payload)
    if layered_node_summary is not None:
        data["layered_node_summary"] = layered_node_summary

    return {
        "status": "success",
        "data": data,
        "error": None,
        "metadata": _response_metadata(meta, normalized_payload["logic_version"], started_at),
    }


@app.post("/api/kzo/save_snapshot")
def save_snapshot(
    body: dict[str, Any],
    x_eds_client_type: str | None = Header(default=None, alias="X-EDS-Client-Type"),
):
    """Insert-only persistence for frozen ``KZO_MVP_SNAPSHOT_V1`` (Stage 8A / hardened 8B.1A).

    Does **not** recalculate engineering truth — validates contract shape and stores one row.
    Configure ``SUPABASE_URL`` + ``SUPABASE_SERVICE_ROLE_KEY`` + table ``calculation_snapshots``.
    Canonical response includes ``created_at``, ``client_type`` (echo of ``X-EDS-Client-Type``), unified ``failure``."""
    client_type = normalize_eds_client_type(x_eds_client_type)

    normalized, validate_code, aux = validate_kzo_mvp_snapshot_v1(body)
    sv_response: str | None = "KZO_MVP_SNAPSHOT_V1" if aux.get("l1_snapshot_version_ok") else None

    if validate_code:
        return save_snapshot_http_response_failure(
            client_type=client_type,
            persistence_status="REJECTED",
            response_snapshot_version=sv_response,
            error_code=validate_code,
        )

    req_meta = normalized.get("request_metadata")
    req_id = (
        req_meta.get("request_id").strip()
        if isinstance(req_meta, dict) and isinstance(req_meta.get("request_id"), str)
        else None
    )
    if req_id:
        existing_snapshot_id, existing_created_at, duplicate_check_code = find_snapshot_by_request_id(req_id)
        if duplicate_check_code:
            return save_snapshot_http_response_failure(
                client_type=client_type,
                persistence_status="ERROR",
                response_snapshot_version=sv_response,
                error_code=duplicate_check_code,
            )
        if existing_snapshot_id:
            return save_snapshot_http_response_failure(
                client_type=client_type,
                persistence_status="DUPLICATE_REJECTED",
                response_snapshot_version=sv_response,
                error_code="SNAPSHOT_DUPLICATE_REJECTED",
                snapshot_id=existing_snapshot_id,
                created_at=existing_created_at,
            )

    snapshot_id, created_at_iso, insert_code = insert_snapshot_row(normalized)
    if insert_code:
        return save_snapshot_http_response_failure(
            client_type=client_type,
            persistence_status="ERROR",
            response_snapshot_version=sv_response,
            error_code=insert_code,
        )

    assert snapshot_id is not None
    return save_snapshot_http_response_success(
        snapshot_id=snapshot_id,
        client_type=client_type,
        created_at=created_at_iso,
    )


def _auth_response_metadata(request_id: str) -> dict[str, str]:
    return {"request_id": request_id, "module": AUTH_MODULE_NAME}


def _auth_timed_metadata(request_id: str, started_at: float) -> dict[str, Any]:
    return _response_metadata({"request_id": request_id}, None, started_at)


def _auth_failed_response(request_id: str) -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content={
            "status": "auth_failed",
            "data": None,
            "error": {"error_code": AUTH_FAILURE_CODE, "message": AUTH_FAILURE_MESSAGE},
            "metadata": _auth_response_metadata(request_id),
        },
    )


def _auth_config_error_response(request_id: str) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "data": None,
            "error": {"error_code": "AUTH_CONFIG_ERROR", "message": "Authentication service unavailable"},
            "metadata": _auth_response_metadata(request_id),
        },
    )


def _auth_validate_request_shape(payload: Any) -> tuple[str, str, str] | None:
    if not isinstance(payload, dict):
        return None
    email = payload.get("email")
    password = payload.get("password")
    spreadsheet_id = payload.get("spreadsheet_id")
    if not isinstance(email, str) or not email.strip():
        return None
    if not isinstance(password, str) or not password:
        return None
    if not isinstance(spreadsheet_id, str) or not spreadsheet_id.strip():
        return None
    return email.strip().lower(), password, spreadsheet_id.strip()


def _auth_redact_email_domain(email: Any) -> str | None:
    if not isinstance(email, str):
        return None
    normalized = email.strip().lower()
    if "@" not in normalized:
        return None
    domain = normalized.split("@", 1)[-1].strip()
    return domain or None


def _auth_redact_spreadsheet_suffix(spreadsheet_id: Any) -> str | None:
    if not isinstance(spreadsheet_id, str):
        return None
    s = spreadsheet_id.strip()
    if not s:
        return None
    return s[-6:] if len(s) >= 6 else s


def _auth_normalize_login_spreadsheet_id(value: Any) -> str:
    """Normalize Sheet file id for comparison (trim + strip common invisible copy/paste characters)."""
    if not isinstance(value, str):
        return ""
    s = value.strip()
    for ch in ("\ufeff", "\u200b", "\u200e", "\u200f"):
        s = s.strip(ch)
    return s.strip()


def _auth_login_spreadsheet_id_diag(request_sheet: str, stored_raw: Any) -> dict[str, Any]:
    """Safe compare metadata for stdout login diagnostics (no full ids)."""
    raw_req = request_sheet if isinstance(request_sheet, str) else ""
    if isinstance(stored_raw, str):
        raw_sto = stored_raw
    elif stored_raw is None:
        raw_sto = ""
    else:
        raw_sto = str(stored_raw)

    norm_req = _auth_normalize_login_spreadsheet_id(raw_req)
    norm_sto = _auth_normalize_login_spreadsheet_id(raw_sto)
    match = bool(norm_sto) and norm_req == norm_sto

    def _suffix12(s: str) -> str:
        if not s:
            return ""
        return s[-12:] if len(s) >= 12 else s

    def _md5_utf8(s: str) -> str:
        return hashlib.md5(s.encode("utf-8")).hexdigest()

    return {
        "request_spreadsheet_len": len(raw_req),
        "stored_spreadsheet_len": len(raw_sto),
        "request_spreadsheet_suffix_12": _suffix12(raw_req),
        "stored_spreadsheet_suffix_12": _suffix12(raw_sto),
        "request_spreadsheet_md5": _md5_utf8(raw_req),
        "stored_spreadsheet_md5": _md5_utf8(raw_sto),
        "request_spreadsheet_normalized_len": len(norm_req),
        "stored_spreadsheet_normalized_len": len(norm_sto),
        "request_spreadsheet_normalized_md5": _md5_utf8(norm_req),
        "stored_spreadsheet_normalized_md5": _md5_utf8(norm_sto),
        "terminal_spreadsheet_match": match,
    }


def _auth_login_shape_flags(payload: Any) -> tuple[bool, bool, str | None, str | None]:
    if not isinstance(payload, dict):
        return False, False, None, None
    email = payload.get("email")
    sid = payload.get("spreadsheet_id")
    email_present = isinstance(email, str) and bool(email.strip())
    spreadsheet_present = isinstance(sid, str) and bool(sid.strip())
    return (
        email_present,
        spreadsheet_present,
        _auth_redact_email_domain(email) if isinstance(email, str) else None,
        _auth_redact_spreadsheet_suffix(sid) if isinstance(sid, str) else None,
    )


def _auth_emit_login_diagnostic(line: dict[str, Any]) -> None:
    payload = {k: line[k] for k in _AUTH_LOGIN_DIAG_ALLOWED_KEYS if k in line}
    # stdout (not logging.info): Uvicorn/Render often omit app INFO unless root is configured;
    # unbuffered flush ensures the line appears with access logs.
    print("EDS_POWER_AUTH_LOGIN_DIAG " + json.dumps(payload, sort_keys=True), flush=True)


def _auth_parse_session_ttl_hours() -> int | None:
    raw = os.environ.get("AUTH_SESSION_TTL_HOURS", "").strip()
    if not raw:
        return None
    try:
        parsed = int(raw)
    except ValueError:
        return None
    if parsed <= 0:
        return None
    return parsed


def _auth_get_supabase_client() -> Client | None:
    global _auth_supabase_client
    if _auth_supabase_client is not None:
        return _auth_supabase_client
    if create_client is None:
        return None
    url = os.environ.get("SUPABASE_URL", "").strip()
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "").strip()
    if not url or not key:
        return None
    _auth_supabase_client = create_client(url, key)
    return _auth_supabase_client


def _auth_env_ready() -> bool:
    for key in AUTH_REQUIRED_ENV_KEYS:
        if not os.environ.get(key, "").strip():
            return False
    return _auth_parse_session_ttl_hours() is not None


def _auth_fetch_single(client: Client, table: str, *, select: str, filters: dict[str, Any]) -> dict[str, Any] | None:
    query = client.table(table).select(select)
    for key, value in filters.items():
        query = query.eq(key, value)
    result = query.limit(1).execute()
    rows = getattr(result, "data", None)
    if isinstance(rows, list) and rows and isinstance(rows[0], dict):
        return rows[0]
    return None


def _auth_fetch_active_roles(client: Client, user_id: str) -> list[str]:
    links = client.table("module01_user_roles").select("role_id,is_active").eq("user_id", user_id).execute()
    link_rows = getattr(links, "data", None)
    if not isinstance(link_rows, list):
        return []
    active_role_ids = [
        row.get("role_id")
        for row in link_rows
        if isinstance(row, dict) and row.get("is_active") is True and isinstance(row.get("role_id"), str)
    ]
    if not active_role_ids:
        return []
    role_codes: list[str] = []
    for role_id in active_role_ids:
        role = _auth_fetch_single(
            client,
            "module01_roles",
            select="role_code,is_active",
            filters={"id": role_id},
        )
        if not role or role.get("is_active") is not True:
            continue
        role_code = role.get("role_code")
        if isinstance(role_code, str) and role_code:
            role_codes.append(role_code)
    return sorted(set(role_codes))


def _auth_resolve_primary_role_id(client: Client, user_id: str) -> str | None:
    """Resolve single role UUID for menu/registry use (TEST_OPERATOR preferred, else lexicographic)."""
    links = client.table("module01_user_roles").select("role_id,is_active").eq("user_id", user_id).execute()
    link_rows = getattr(links, "data", None)
    if not isinstance(link_rows, list):
        return None
    active_role_ids = [
        row.get("role_id")
        for row in link_rows
        if isinstance(row, dict) and row.get("is_active") is True and isinstance(row.get("role_id"), str)
    ]
    if not active_role_ids:
        return None
    roles: list[dict[str, Any]] = []
    for rid in active_role_ids:
        role = _auth_fetch_single(
            client,
            "module01_roles",
            select="id,role_code,is_active",
            filters={"id": rid},
        )
        if role and role.get("is_active") is True and isinstance(role.get("id"), str):
            roles.append(role)
    if not roles:
        return None
    by_code = {str(r["role_code"]): str(r["id"]) for r in roles if isinstance(r.get("role_code"), str) and r.get("id")}
    if "TEST_OPERATOR" in by_code:
        return by_code["TEST_OPERATOR"]
    sorted_roles = sorted(roles, key=lambda r: str(r.get("role_code") or ""))
    first_id = sorted_roles[0].get("id")
    return str(first_id) if first_id else None


def _truthy_env(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in ("1", "true", "yes", "on")


def _auth_verify_password(hash_value: Any, password: str) -> bool:
    if not isinstance(hash_value, str) or not hash_value:
        return False
    try:
        return _password_hasher.verify(hash_value, password)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False


def _auth_error_response(
    *,
    request_id: str,
    started_at: float,
    error_code: str,
    message: str,
    source_field: str = "Authorization",
    action: str = "session_status",
) -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content={
            "status": "auth_error",
            "data": None,
            "error": {
                "error_code": error_code,
                "message": message,
                "source_field": source_field,
                "module": AUTH_MODULE_NAME,
                "action": action,
            },
            "metadata": _auth_timed_metadata(request_id, started_at),
        },
    )


def _menu_registry_error_response(
    *,
    request_id: str,
    started_at: float,
    error_code: str,
    message: str,
) -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content={
            "status": "error",
            "data": None,
            "error": {
                "error_code": error_code,
                "message": message,
                "source_field": None,
                "module": AUTH_MODULE_NAME,
                "action": AUTH_MENU_ACTION,
            },
            "metadata": _auth_timed_metadata(request_id, started_at),
        },
    )


def _auth_extract_bearer_token(authorization: str | None) -> str | None:
    if not isinstance(authorization, str):
        return None
    raw = authorization.strip()
    if not raw:
        return None
    parts = raw.split(" ", 1)
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    token = parts[1].strip()
    return token if token else None


def _auth_mock_menu_payload() -> dict[str, Any]:
    return {
        "menu_version": AUTH_MENU_MOCK_RESPONSE_VERSION,
        "user_context": {
            "display_name": "Mock User",
            "primary_role": "MOCK_OPERATOR",
            "is_admin": False,
        },
        "terminal_context": {
            "terminal_id": "TERMINAL_TEMPLATE",
            "terminal_status": "TEMPLATE",
        },
        "core_compatibility": {
            "required_core_version": "EDS_POWER_CORE_FOUNDATION_V1",
            "compatibility_status": "COMPATIBLE",
        },
        "menus": AUTH_MENU_MOCK_ITEMS,
    }


def _menu_flatten_for_gas(modules: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Flatten registry modules/actions into legacy `data.menus` list for GAS EDSPowerCore."""
    flat: list[dict[str, Any]] = []
    for m in modules:
        if not isinstance(m, dict):
            continue
        code = m.get("module_code")
        if not isinstance(code, str) or not code:
            continue
        mname = m.get("module_name")
        mstat = m.get("module_status")
        msort = m.get("sort_order") if isinstance(m.get("sort_order"), int) else 100
        for a in m.get("actions") or []:
            if not isinstance(a, dict):
                continue
            ak = a.get("action_key")
            if not isinstance(ak, str) or not ak:
                continue
            asort = a.get("sort_order") if isinstance(a.get("sort_order"), int) else 0
            global_sort = msort * 1000 + asort
            vis = a.get("visibility")
            if not isinstance(vis, str) or not vis:
                vis = "VISIBLE"
            item: dict[str, Any] = {
                "menu_id": ak.lower(),
                "menu_label": a.get("menu_label"),
                "action_key": ak,
                "action_type": a.get("action_type"),
                "visibility": vis,
                "enabled": bool(a.get("enabled")),
                "sort_order": global_sort,
            }
            if code != "SYSTEM_SHELL":
                item["module_id"] = code
                item["module_name"] = mname
                item["module_status"] = mstat
            flat.append(item)
    flat.sort(key=lambda x: (x.get("sort_order") or 0, str(x.get("action_key") or "")))
    return flat


def _auth_validate_session_context(
    authorization: str | None,
    *,
    action: str,
) -> tuple[dict[str, Any] | None, JSONResponse | None]:
    """Validate Bearer session; return context dict or auth error response."""
    started_at = perf_counter()
    request_id = str(uuid4())
    bearer_token = _auth_extract_bearer_token(authorization)
    if not bearer_token:
        return None, _auth_error_response(
            request_id=request_id,
            started_at=started_at,
            error_code="AUTH_MISSING_TOKEN",
            message="Authorization token is missing.",
            action=action,
        )

    if not _auth_env_ready():
        return None, _auth_config_error_response(request_id)
    client = _auth_get_supabase_client()
    if client is None:
        return None, _auth_config_error_response(request_id)

    try:
        token_hash = hashlib.sha256(bearer_token.encode("utf-8")).hexdigest()
        session_row = _auth_fetch_single(
            client,
            "module01_user_sessions",
            select="id,user_id,terminal_id,expires_at,revoked_at",
            filters={"session_token_hash": token_hash},
        )
        if session_row is None:
            return None, _auth_error_response(
                request_id=request_id,
                started_at=started_at,
                error_code="AUTH_INVALID_TOKEN",
                message="Authentication failed.",
                action=action,
            )

        if session_row.get("revoked_at") is not None:
            return None, _auth_error_response(
                request_id=request_id,
                started_at=started_at,
                error_code="AUTH_SESSION_REVOKED",
                message="Session is revoked.",
                action=action,
            )

        expires_raw = session_row.get("expires_at")
        if not isinstance(expires_raw, str) or not expires_raw.strip():
            return None, _auth_error_response(
                request_id=request_id,
                started_at=started_at,
                error_code="AUTH_INVALID_TOKEN",
                message="Authentication failed.",
                action=action,
            )
        expires_str = expires_raw.strip()
        if expires_str.endswith("Z"):
            expires_str = expires_str[:-1] + "+00:00"
        try:
            expires_at_dt = datetime.fromisoformat(expires_str)
        except ValueError:
            return None, _auth_error_response(
                request_id=request_id,
                started_at=started_at,
                error_code="AUTH_INVALID_TOKEN",
                message="Authentication failed.",
                action=action,
            )
        now_dt = datetime.now(UTC)
        if expires_at_dt <= now_dt:
            return None, _auth_error_response(
                request_id=request_id,
                started_at=started_at,
                error_code="AUTH_SESSION_EXPIRED",
                message="Session is expired.",
                action=action,
            )

        user_id = session_row.get("user_id")
        terminal_id = session_row.get("terminal_id")
        if not isinstance(user_id, str) or not user_id or not isinstance(terminal_id, str) or not terminal_id:
            return None, _auth_error_response(
                request_id=request_id,
                started_at=started_at,
                error_code="AUTH_INVALID_TOKEN",
                message="Authentication failed.",
                action=action,
            )

        user = _auth_fetch_single(
            client,
            "module01_users",
            select="id,email,status",
            filters={"id": user_id},
        )
        if user is None or user.get("status") != "ACTIVE":
            return None, _auth_error_response(
                request_id=request_id,
                started_at=started_at,
                error_code="AUTH_USER_NOT_FOUND",
                message="User is not available.",
                action=action,
            )

        terminal = _auth_fetch_single(
            client,
            "module01_user_terminals",
            select="id,user_id,status",
            filters={"id": terminal_id},
        )
        if (
            terminal is None
            or terminal.get("status") != "ACTIVE"
            or terminal.get("user_id") != user_id
        ):
            return None, _auth_error_response(
                request_id=request_id,
                started_at=started_at,
                error_code="AUTH_TERMINAL_MISMATCH",
                message="Terminal is not valid for this session.",
                action=action,
            )

        return {
            "client": client,
            "user_id": user_id,
            "request_id": request_id,
            "started_at": started_at,
            "terminal_id": terminal_id,
            "expires_at_dt": expires_at_dt,
            "user_email": user.get("email"),
        }, None
    except Exception:  # noqa: BLE001
        return None, _auth_error_response(
            request_id=request_id,
            started_at=started_at,
            error_code="AUTH_INVALID_TOKEN",
            message="Authentication failed.",
            action=action,
        )


@app.post("/api/module01/auth/login")
def module01_auth_login(payload: dict[str, Any]):
    request_id = str(uuid4())
    email_present, spreadsheet_id_present, email_domain, spreadsheet_id_suffix = _auth_login_shape_flags(payload)
    parsed = _auth_validate_request_shape(payload)
    if parsed is None:
        _auth_emit_login_diagnostic(
            {
                "request_id": request_id,
                "auth_stage": "LOGIN_REQUEST_RECEIVED",
                "email_present": email_present,
                "email_domain": email_domain,
                "spreadsheet_id_present": spreadsheet_id_present,
                "spreadsheet_id_suffix": spreadsheet_id_suffix,
                "final_auth_result": "AUTH_FAILED",
            }
        )
        return _auth_failed_response(request_id)
    email, password, spreadsheet_id = parsed
    email_domain = _auth_redact_email_domain(email)
    spreadsheet_id_suffix = _auth_redact_spreadsheet_suffix(spreadsheet_id)

    def _base_diag() -> dict[str, Any]:
        return {
            "request_id": request_id,
            "email_present": True,
            "email_domain": email_domain,
            "spreadsheet_id_present": True,
            "spreadsheet_id_suffix": spreadsheet_id_suffix,
        }

    if not _auth_env_ready():
        _auth_emit_login_diagnostic(
            {**_base_diag(), "auth_stage": "LOGIN_REQUEST_RECEIVED", "final_auth_result": "AUTH_FAILED"}
        )
        return _auth_config_error_response(request_id)
    ttl_hours = _auth_parse_session_ttl_hours()
    if ttl_hours is None:
        _auth_emit_login_diagnostic(
            {**_base_diag(), "auth_stage": "LOGIN_REQUEST_RECEIVED", "final_auth_result": "AUTH_FAILED"}
        )
        return _auth_config_error_response(request_id)
    client = _auth_get_supabase_client()
    if client is None:
        _auth_emit_login_diagnostic(
            {**_base_diag(), "auth_stage": "LOGIN_REQUEST_RECEIVED", "final_auth_result": "AUTH_FAILED"}
        )
        return _auth_config_error_response(request_id)

    try:
        _auth_emit_login_diagnostic(
            {**_base_diag(), "auth_stage": "USER_LOOKUP_STARTED", "final_auth_result": "AUTH_FAILED"}
        )
        user = _auth_fetch_single(
            client,
            "module01_users",
            select="id,email,display_name,status",
            filters={"email": email},
        )
        if user is None:
            _auth_emit_login_diagnostic(
                {
                    **_base_diag(),
                    "auth_stage": "USER_LOOKUP_FAILED",
                    "supabase_query_user_found": False,
                    "final_auth_result": "AUTH_FAILED",
                }
            )
            return _auth_failed_response(request_id)
        if user.get("status") != "ACTIVE":
            _auth_emit_login_diagnostic(
                {
                    **_base_diag(),
                    "auth_stage": "USER_INACTIVE",
                    "supabase_query_user_found": True,
                    "user_status": str(user.get("status") or ""),
                    "final_auth_result": "AUTH_FAILED",
                }
            )
            return _auth_failed_response(request_id)
        user_id = user.get("id")
        if not isinstance(user_id, str) or not user_id:
            _auth_emit_login_diagnostic(
                {
                    **_base_diag(),
                    "auth_stage": "USER_LOOKUP_FAILED",
                    "supabase_query_user_found": True,
                    "user_status": "ACTIVE",
                    "final_auth_result": "AUTH_FAILED",
                }
            )
            return _auth_failed_response(request_id)

        _auth_emit_login_diagnostic(
            {
                **_base_diag(),
                "auth_stage": "USER_FOUND",
                "supabase_query_user_found": True,
                "user_status": "ACTIVE",
                "final_auth_result": "AUTH_FAILED",
            }
        )

        _auth_emit_login_diagnostic(
            {
                **_base_diag(),
                "auth_stage": "AUTH_ROW_LOOKUP_STARTED",
                "supabase_query_user_found": True,
                "user_status": "ACTIVE",
                "final_auth_result": "AUTH_FAILED",
            }
        )
        auth_row = _auth_fetch_single(
            client,
            "module01_user_auth",
            select="password_hash,locked_until,password_algorithm",
            filters={"user_id": user_id},
        )
        if auth_row is None:
            _auth_emit_login_diagnostic(
                {
                    **_base_diag(),
                    "auth_stage": "AUTH_ROW_MISSING",
                    "supabase_query_user_found": True,
                    "user_status": "ACTIVE",
                    "supabase_query_auth_row_found": False,
                    "final_auth_result": "AUTH_FAILED",
                }
            )
            return _auth_failed_response(request_id)

        ph_raw = auth_row.get("password_hash")
        password_hash_present = isinstance(ph_raw, str) and bool(ph_raw.strip())
        palg = auth_row.get("password_algorithm")
        password_algorithm = str(palg) if isinstance(palg, str) and palg.strip() else None
        locked_until = auth_row.get("locked_until")
        locked_until_present = locked_until is not None and (
            not isinstance(locked_until, str) or bool(locked_until.strip())
        )

        _auth_emit_login_diagnostic(
            {
                **_base_diag(),
                "auth_stage": "AUTH_ROW_FOUND",
                "supabase_query_user_found": True,
                "user_status": "ACTIVE",
                "supabase_query_auth_row_found": True,
                "password_algorithm": password_algorithm,
                "password_hash_present": password_hash_present,
                "locked_until_present": locked_until_present,
                "final_auth_result": "AUTH_FAILED",
            }
        )

        if isinstance(locked_until, str) and locked_until.strip():
            locked_ts = locked_until.strip()
            if locked_ts.endswith("Z"):
                locked_ts = locked_ts[:-1] + "+00:00"
            try:
                if datetime.fromisoformat(locked_ts) > datetime.now(UTC):
                    _auth_emit_login_diagnostic(
                        {
                            **_base_diag(),
                            "auth_stage": "USER_LOCKED",
                            "supabase_query_user_found": True,
                            "user_status": "ACTIVE",
                            "supabase_query_auth_row_found": True,
                            "password_algorithm": password_algorithm,
                            "password_hash_present": password_hash_present,
                            "locked_until_present": True,
                            "final_auth_result": "AUTH_FAILED",
                        }
                    )
                    return _auth_failed_response(request_id)
            except ValueError:
                _auth_emit_login_diagnostic(
                    {
                        **_base_diag(),
                        "auth_stage": "USER_LOCKED",
                        "supabase_query_user_found": True,
                        "user_status": "ACTIVE",
                        "supabase_query_auth_row_found": True,
                        "password_algorithm": password_algorithm,
                        "password_hash_present": password_hash_present,
                        "locked_until_present": True,
                        "final_auth_result": "AUTH_FAILED",
                    }
                )
                return _auth_failed_response(request_id)

        _auth_emit_login_diagnostic(
            {
                **_base_diag(),
                "auth_stage": "PASSWORD_VERIFY_STARTED",
                "supabase_query_user_found": True,
                "user_status": "ACTIVE",
                "supabase_query_auth_row_found": True,
                "password_algorithm": password_algorithm,
                "password_hash_present": password_hash_present,
                "locked_until_present": locked_until_present,
                "final_auth_result": "AUTH_FAILED",
            }
        )
        if not _auth_verify_password(auth_row.get("password_hash"), password):
            _auth_emit_login_diagnostic(
                {
                    **_base_diag(),
                    "auth_stage": "PASSWORD_VERIFY_FAILED",
                    "supabase_query_user_found": True,
                    "user_status": "ACTIVE",
                    "supabase_query_auth_row_found": True,
                    "password_algorithm": password_algorithm,
                    "password_hash_present": password_hash_present,
                    "locked_until_present": locked_until_present,
                    "password_verify_result": False,
                    "final_auth_result": "AUTH_FAILED",
                }
            )
            return _auth_failed_response(request_id)

        role_codes = _auth_fetch_active_roles(client, user_id)
        if "TEST_OPERATOR" not in role_codes:
            _auth_emit_login_diagnostic(
                {
                    **_base_diag(),
                    "auth_stage": "USER_FOUND",
                    "supabase_query_user_found": True,
                    "user_status": "ACTIVE",
                    "supabase_query_auth_row_found": True,
                    "password_algorithm": password_algorithm,
                    "password_hash_present": password_hash_present,
                    "locked_until_present": locked_until_present,
                    "password_verify_result": True,
                    "final_auth_result": "AUTH_FAILED",
                }
            )
            return _auth_failed_response(request_id)

        _auth_emit_login_diagnostic(
            {
                **_base_diag(),
                "auth_stage": "TERMINAL_LOOKUP_STARTED",
                "supabase_query_user_found": True,
                "user_status": "ACTIVE",
                "supabase_query_auth_row_found": True,
                "password_algorithm": password_algorithm,
                "password_hash_present": password_hash_present,
                "locked_until_present": locked_until_present,
                "password_verify_result": True,
                "final_auth_result": "AUTH_FAILED",
            }
        )
        norm_request_sheet = _auth_normalize_login_spreadsheet_id(spreadsheet_id)
        terminal = _auth_fetch_single(
            client,
            "module01_user_terminals",
            select="id,status,spreadsheet_id",
            filters={"user_id": user_id},
        )
        if terminal is None:
            _auth_emit_login_diagnostic(
                {
                    **_base_diag(),
                    "auth_stage": "TERMINAL_LOOKUP_FAILED",
                    "supabase_query_user_found": True,
                    "user_status": "ACTIVE",
                    "supabase_query_auth_row_found": True,
                    "password_algorithm": password_algorithm,
                    "password_hash_present": password_hash_present,
                    "locked_until_present": locked_until_present,
                    "password_verify_result": True,
                    "supabase_query_terminal_found": False,
                    "terminal_spreadsheet_match": False,
                    "final_auth_result": "AUTH_FAILED",
                }
            )
            return _auth_failed_response(request_id)

        norm_stored_sheet = _auth_normalize_login_spreadsheet_id(terminal.get("spreadsheet_id"))
        terminal_match = bool(norm_stored_sheet) and norm_stored_sheet == norm_request_sheet
        _sheet_diag = _auth_login_spreadsheet_id_diag(spreadsheet_id, terminal.get("spreadsheet_id"))
        if not terminal_match:
            _auth_emit_login_diagnostic(
                {
                    **_base_diag(),
                    "auth_stage": "SPREADSHEET_ID_MISMATCH",
                    "supabase_query_user_found": True,
                    "user_status": "ACTIVE",
                    "supabase_query_auth_row_found": True,
                    "password_algorithm": password_algorithm,
                    "password_hash_present": password_hash_present,
                    "locked_until_present": locked_until_present,
                    "password_verify_result": True,
                    "supabase_query_terminal_found": True,
                    "final_auth_result": "AUTH_FAILED",
                    **_sheet_diag,
                }
            )
            return _auth_failed_response(request_id)

        if terminal.get("status") != "ACTIVE":
            _auth_emit_login_diagnostic(
                {
                    **_base_diag(),
                    "auth_stage": "TERMINAL_INACTIVE",
                    "supabase_query_user_found": True,
                    "user_status": "ACTIVE",
                    "supabase_query_auth_row_found": True,
                    "password_algorithm": password_algorithm,
                    "password_hash_present": password_hash_present,
                    "locked_until_present": locked_until_present,
                    "password_verify_result": True,
                    "supabase_query_terminal_found": True,
                    "terminal_status": str(terminal.get("status") or ""),
                    "terminal_spreadsheet_match": terminal_match,
                    "final_auth_result": "AUTH_FAILED",
                }
            )
            return _auth_failed_response(request_id)
        terminal_id = terminal.get("id")
        if not isinstance(terminal_id, str) or not terminal_id:
            _auth_emit_login_diagnostic(
                {
                    **_base_diag(),
                    "auth_stage": "TERMINAL_LOOKUP_FAILED",
                    "supabase_query_user_found": True,
                    "user_status": "ACTIVE",
                    "supabase_query_auth_row_found": True,
                    "password_algorithm": password_algorithm,
                    "password_hash_present": password_hash_present,
                    "locked_until_present": locked_until_present,
                    "password_verify_result": True,
                    "supabase_query_terminal_found": True,
                    "terminal_status": str(terminal.get("status") or ""),
                    "terminal_spreadsheet_match": terminal_match,
                    "final_auth_result": "AUTH_FAILED",
                }
            )
            return _auth_failed_response(request_id)

        _auth_emit_login_diagnostic(
            {
                **_base_diag(),
                "auth_stage": "TERMINAL_FOUND",
                "supabase_query_user_found": True,
                "user_status": "ACTIVE",
                "supabase_query_auth_row_found": True,
                "password_algorithm": password_algorithm,
                "password_hash_present": password_hash_present,
                "locked_until_present": locked_until_present,
                "password_verify_result": True,
                "supabase_query_terminal_found": True,
                "terminal_status": "ACTIVE",
                "terminal_spreadsheet_match": terminal_match,
                "final_auth_result": "AUTH_FAILED",
                **_auth_login_spreadsheet_id_diag(spreadsheet_id, terminal.get("spreadsheet_id")),
            }
        )

        raw_session_token = secrets.token_urlsafe(32)
        session_token_hash = hashlib.sha256(raw_session_token.encode("utf-8")).hexdigest()
        issued_at = datetime.now(UTC)
        expires_at = issued_at + timedelta(hours=ttl_hours)
        session_id = str(uuid4())

        insert_payload = {
            "id": session_id,
            "user_id": user_id,
            "terminal_id": terminal_id,
            "session_token_hash": session_token_hash,
            "issued_at": issued_at.isoformat(),
            "expires_at": expires_at.isoformat(),
            "revoked_at": None,
            "last_seen_at": None,
            "created_at": issued_at.isoformat(),
            "updated_at": issued_at.isoformat(),
        }
        client.table("module01_user_sessions").insert(insert_payload).execute()

        _auth_emit_login_diagnostic(
            {
                **_base_diag(),
                "auth_stage": "LOGIN_SUCCESS",
                "supabase_query_user_found": True,
                "user_status": "ACTIVE",
                "supabase_query_auth_row_found": True,
                "password_algorithm": password_algorithm,
                "password_hash_present": password_hash_present,
                "locked_until_present": locked_until_present,
                "password_verify_result": True,
                "supabase_query_terminal_found": True,
                "terminal_status": "ACTIVE",
                "terminal_spreadsheet_match": terminal_match,
                "final_auth_result": "LOGIN_SUCCESS",
            }
        )

        response_payload = {
            "status": "success",
            "data": {
                "user": {
                    "user_id": user_id,
                    "email": user.get("email"),
                    "display_name": user.get("display_name"),
                    "role_codes": role_codes,
                },
                "session": {
                    "session_token": raw_session_token,
                    "expires_at": expires_at.isoformat(),
                },
                "allowed_actions": AUTH_ALLOWED_ACTIONS_TEST_OPERATOR,
            },
            "error": None,
            "metadata": _auth_response_metadata(request_id),
        }
        return JSONResponse(status_code=200, content=response_payload)
    except Exception:  # noqa: BLE001
        _auth_emit_login_diagnostic(
            {
                **_base_diag(),
                "auth_stage": "USER_LOOKUP_FAILED",
                "final_auth_result": "AUTH_FAILED",
            }
        )
        return _auth_failed_response(request_id)


@app.get("/api/module01/auth/session/status")
def module01_auth_session_status(authorization: str | None = Header(default=None, alias="Authorization")):
    ctx, err = _auth_validate_session_context(authorization, action="session_status")
    if err is not None:
        return err

    client = ctx["client"]
    user_id = ctx["user_id"]
    request_id = ctx["request_id"]
    started_at = ctx["started_at"]
    terminal_id = ctx["terminal_id"]
    expires_at_dt = ctx["expires_at_dt"]
    user_email = ctx["user_email"]

    role_codes = _auth_fetch_active_roles(client, user_id)
    if not role_codes:
        return _auth_error_response(
            request_id=request_id,
            started_at=started_at,
            error_code="AUTH_FORBIDDEN_ROLE",
            message="Role is not allowed for this action.",
            action="session_status",
        )
    primary_role = "TEST_OPERATOR" if "TEST_OPERATOR" in role_codes else role_codes[0]

    now_dt = datetime.now(UTC)
    response_payload = {
        "status": "success",
        "data": {
            "authenticated": True,
            "user_id": user_id,
            "email": user_email,
            "role": primary_role,
            "terminal_id": terminal_id,
            "expires_at": expires_at_dt.isoformat(),
            "remaining_seconds": max(0, int((expires_at_dt - now_dt).total_seconds())),
        },
        "error": None,
        "metadata": _auth_timed_metadata(request_id, started_at),
    }
    return JSONResponse(status_code=200, content=response_payload)


@app.get("/api/module01/auth/menu")
def module01_auth_menu(authorization: str | None = Header(default=None, alias="Authorization")):
    ctx, err = _auth_validate_session_context(authorization, action=AUTH_MENU_ACTION)
    if err is not None:
        return err

    client = ctx["client"]
    user_id = ctx["user_id"]
    request_id = ctx["request_id"]
    started_at = ctx["started_at"]

    if _truthy_env("EDS_MENU_FORCE_MOCK"):
        metadata = _auth_timed_metadata(request_id, started_at)
        metadata["logic_version"] = None
        metadata["menu_source"] = "mock_dev_fallback"
        metadata["auth_enforcement"] = "authenticated"
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "data": _auth_mock_menu_payload(),
                "error": None,
                "metadata": metadata,
            },
        )

    if not _auth_env_ready() or client is None:
        return _menu_registry_error_response(
            request_id=request_id,
            started_at=started_at,
            error_code="MENU_REGISTRY_UNAVAILABLE",
            message="Menu registry is not available.",
        )

    env_scope, escope_err = resolve_menu_environment_scope()
    if escope_err:
        return _menu_registry_error_response(
            request_id=request_id,
            started_at=started_at,
            error_code=escope_err,
            message="Menu environment scope is not configured validly.",
        )

    role_id = _auth_resolve_primary_role_id(client, user_id)
    if not role_id:
        return _menu_registry_error_response(
            request_id=request_id,
            started_at=started_at,
            error_code="MENU_ROLE_NOT_FOUND",
            message="No active role resolved for menu registry.",
        )

    try:
        service = MenuRegistryService(client)
        modules, svc_err = service.fetch_menu_modules(role_id, env_scope)
    except Exception:  # noqa: BLE001
        return _menu_registry_error_response(
            request_id=request_id,
            started_at=started_at,
            error_code="MENU_REGISTRY_QUERY_FAILED",
            message="Menu registry query failed.",
        )

    if svc_err:
        return _menu_registry_error_response(
            request_id=request_id,
            started_at=started_at,
            error_code=svc_err,
            message="Menu registry query failed.",
        )

    if modules is None:
        return _menu_registry_error_response(
            request_id=request_id,
            started_at=started_at,
            error_code="MENU_REGISTRY_UNAVAILABLE",
            message="Menu registry returned no data.",
        )

    if not _menu_registry_svc.MenuRegistryService.menu_has_any_action(modules):
        return _menu_registry_error_response(
            request_id=request_id,
            started_at=started_at,
            error_code="MENU_NO_ALLOWED_ACTIONS",
            message="No menu actions are allowed for this role in the current environment.",
        )

    menus_flat = _menu_flatten_for_gas(modules)

    metadata = _auth_timed_metadata(request_id, started_at)
    metadata["logic_version"] = None
    metadata["menu_source"] = "registry"
    metadata["environment_scope"] = env_scope
    metadata["auth_enforcement"] = "authenticated"

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": {
                "modules": modules,
                "menus": menus_flat,
            },
            "error": None,
            "metadata": metadata,
        },
    )
