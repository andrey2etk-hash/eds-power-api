from time import perf_counter
from typing import Any
from uuid import uuid4

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from kzo_snapshot_persist import insert_snapshot_row, validate_kzo_mvp_snapshot_v1

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


@app.get("/")
def root():
    return {"message": "EDS Power API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}


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

    return {
        "status": "success",
        "data": {
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
        },
        "error": None,
        "metadata": _response_metadata(meta, normalized_payload["logic_version"], started_at),
    }


@app.post("/api/kzo/save_snapshot")
def save_snapshot(body: dict[str, Any]):
    """Insert-only persistence for frozen ``KZO_MVP_SNAPSHOT_V1`` (Stage 8A).

    Does **not** recalculate engineering truth — validates contract shape and stores one row.
    Configure ``SUPABASE_URL`` + ``SUPABASE_SERVICE_ROLE_KEY`` + table ``calculation_snapshots`` (``product_type`` = KZO for MVP)."""
    normalized, validate_code = validate_kzo_mvp_snapshot_v1(body)
    if validate_code:
        return {
            "status": "FAILED",
            "persistence_status": "REJECTED",
            "error_code": validate_code,
        }

    snapshot_id, insert_code = insert_snapshot_row(normalized)
    if insert_code:
        return {
            "status": "FAILED",
            "persistence_status": "REJECTED",
            "error_code": insert_code,
        }

    return {
        "status": "SUCCESS",
        "snapshot_id": snapshot_id,
        "snapshot_version": "KZO_MVP_SNAPSHOT_V1",
        "persistence_status": "STORED",
    }
