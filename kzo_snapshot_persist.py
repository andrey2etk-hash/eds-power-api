"""Stage 8A — insert-only persistence for frozen `KZO_MVP_SNAPSHOT_V1`.

Calculation truth stays in ``prepare_calculation``; this module validates shape
and stores rows. No BOM/pricing/engineering recomputation.

Stage 8B.1A — L3/L4 validation ladder, logic_version traceability vs
``request_metadata``, unified reject codes (see governance plan)."""

from __future__ import annotations

import os
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

try:
    from supabase import Client, create_client
except ImportError:
    Client = Any  # type: ignore[misc, assignment]
    create_client = None  # type: ignore[misc, assignment]

_KZO_SNAPSHOT_V1_VERSION = "KZO_MVP_SNAPSHOT_V1"
# Root table name is system-neutral; KZO is indicated on the row (product_type).
_TABLE = "calculation_snapshots"
_PRODUCT_TYPE_KZO = "KZO"

# Strict allow-list: reject unknown top-level keys (anti-drift).
_ALLOWED_TOP_KEYS = frozenset(
    {
        "snapshot_version",
        "run_status",
        "timestamp_basis",
        "logic_version",
        "request_metadata",
        "normalized_input",
        "structural_composition_summary",
        "physical_summary",
        "physical_topology_summary",
        "engineering_class_summary",
        "engineering_burden_summary",
        "failure",
    }
)

_SUCCESS_LAYER_KEYS = (
    "structural_composition_summary",
    "physical_summary",
    "physical_topology_summary",
    "engineering_class_summary",
    "engineering_burden_summary",
)

_REQUEST_METADATA_REQUIRED_KEYS = (
    "request_id",
    "api_version",
    "logic_version",
    "execution_time_ms",
)

_client: Client | None = None


def get_supabase_client() -> tuple[Client | None, str | None]:
    """Return cached Supabase client or (None, error_code)."""
    global _client
    if _client is not None:
        return _client, None

    url = os.environ.get("SUPABASE_URL", "").strip()
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "").strip()
    if not url or not key:
        return None, "SNAPSHOT_PERSISTENCE_UNAVAILABLE"
    if create_client is None:
        return None, "SNAPSHOT_PERSISTENCE_UNAVAILABLE"
    _client = create_client(url, key)
    return _client, None


def _parse_timestamp_basis(raw: Any) -> tuple[datetime | None, str | None]:
    if raw is None:
        return None, "SNAPSHOT_MISSING_TIMESTAMP"
    if isinstance(raw, datetime):
        dt = raw
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=UTC)
        return dt, None
    if isinstance(raw, str):
        ts = raw.strip()
        if ts.endswith("Z"):
            ts = ts[:-1] + "+00:00"
        try:
            parsed = datetime.fromisoformat(ts)
        except ValueError:
            return None, "SNAPSHOT_TIMESTAMP_INVALID"
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=UTC)
        return parsed, None
    return None, "SNAPSHOT_TIMESTAMP_INVALID"


def _validate_failure_contract(failure: dict[str, Any]) -> str | None:
    code = failure.get("error_code")
    if not isinstance(code, str) or code.strip() == "":
        return "SNAPSHOT_FAILURE_ERROR_CODE_REQUIRED"
    msg = failure.get("message")
    if not isinstance(msg, str):
        return "SNAPSHOT_FAILURE_MESSAGE_REQUIRED"
    return None


def _validate_request_metadata_l4(meta: Any) -> str | None:
    """L4 — SUCCESS path only; aligns with ``prepare_calculation`` metadata keys."""
    if not isinstance(meta, dict):
        return "SNAPSHOT_REQUEST_METADATA_REQUIRED"
    for key in _REQUEST_METADATA_REQUIRED_KEYS:
        if key not in meta:
            return "SNAPSHOT_REQUEST_METADATA_SUBKEY_MISSING"
    rid = meta.get("request_id")
    if not isinstance(rid, str) or rid.strip() == "":
        return "SNAPSHOT_REQUEST_METADATA_REQUEST_ID_INVALID"
    api_ver = meta.get("api_version")
    if not isinstance(api_ver, str) or api_ver.strip() == "":
        return "SNAPSHOT_REQUEST_METADATA_API_VERSION_INVALID"
    rlv = meta.get("logic_version")
    if not isinstance(rlv, str) or rlv.strip() == "":
        return "SNAPSHOT_REQUEST_METADATA_LOGIC_VERSION_INVALID"
    etm = meta.get("execution_time_ms")
    if isinstance(etm, bool) or not isinstance(etm, int):
        return "SNAPSHOT_REQUEST_METADATA_EXECUTION_TIME_INVALID"
    if etm < 0:
        return "SNAPSHOT_REQUEST_METADATA_EXECUTION_TIME_INVALID"
    return None


def validate_kzo_mvp_snapshot_v1(
    body: Any,
) -> tuple[dict[str, Any] | None, str | None, dict[str, Any]]:
    """Return (sanitized row for DB, error_code, aux).

    ``aux`` includes ``l1_snapshot_version_ok`` for HTTP response shaping
    (``snapshot_version`` echo on reject when L1 version check passed).
    """
    aux: dict[str, Any] = {"l1_snapshot_version_ok": False}

    if not isinstance(body, dict):
        return None, "SNAPSHOT_BODY_NOT_OBJECT", aux

    extra = set(body.keys()) - _ALLOWED_TOP_KEYS
    if extra:
        return None, "SNAPSHOT_UNKNOWN_FIELDS", aux

    if body.get("snapshot_version") != _KZO_SNAPSHOT_V1_VERSION:
        return None, "SNAPSHOT_VERSION_INVALID", aux

    aux["l1_snapshot_version_ok"] = True

    run_status = body.get("run_status")
    if run_status not in ("SUCCESS", "FAILED"):
        return None, "SNAPSHOT_RUN_STATUS_INVALID", aux

    ts_parsed, ts_err = _parse_timestamp_basis(body.get("timestamp_basis"))
    if ts_err:
        return None, ts_err, aux
    assert ts_parsed is not None
    timestamp_iso = ts_parsed.isoformat()

    if run_status == "SUCCESS":
        for key in _SUCCESS_LAYER_KEYS:
            layer = body.get(key)
            if not isinstance(layer, dict) or len(layer) == 0:
                return None, "SNAPSHOT_SUCCESS_LAYER_INVALID", aux

        lv = body.get("logic_version")
        if lv is None or not isinstance(lv, str) or lv.strip() == "":
            return None, "SNAPSHOT_LOGIC_VERSION_REQUIRED", aux
        top_lv = lv.strip()

        meta_err = _validate_request_metadata_l4(body.get("request_metadata"))
        if meta_err:
            return None, meta_err, aux
        rm = body.get("request_metadata")
        assert isinstance(rm, dict)
        rm_lv = rm.get("logic_version")
        assert isinstance(rm_lv, str)
        if top_lv != rm_lv.strip():
            return None, "SNAPSHOT_LOGIC_VERSION_METADATA_MISMATCH", aux

        if not isinstance(body.get("normalized_input"), dict):
            return None, "SNAPSHOT_NORMALIZED_INPUT_REQUIRED", aux

        if body.get("failure") is not None:
            return None, "SNAPSHOT_SUCCESS_MUST_NOT_HAVE_FAILURE", aux

    elif run_status == "FAILED":
        rm = body.get("request_metadata")
        if rm is not None and not isinstance(rm, dict):
            return None, "SNAPSHOT_REQUEST_METADATA_TYPE_INVALID", aux
        ni = body.get("normalized_input")
        if ni is not None and not isinstance(ni, dict):
            return None, "SNAPSHOT_NORMALIZED_INPUT_TYPE_INVALID", aux
        failure = body.get("failure")
        if not isinstance(failure, dict):
            return None, "SNAPSHOT_FAILURE_DETAIL_REQUIRED", aux
        ferr = _validate_failure_contract(failure)
        if ferr:
            return None, ferr, aux

    row: dict[str, Any] = {
        "product_type": _PRODUCT_TYPE_KZO,
        "snapshot_version": body["snapshot_version"],
        "run_status": body["run_status"],
        "timestamp_basis": timestamp_iso,
        "logic_version": body.get("logic_version"),
        "request_metadata": body.get("request_metadata"),
        "normalized_input": body.get("normalized_input"),
        "structural_composition_summary": body.get("structural_composition_summary"),
        "physical_summary": body.get("physical_summary"),
        "physical_topology_summary": body.get("physical_topology_summary"),
        "engineering_class_summary": body.get("engineering_class_summary"),
        "engineering_burden_summary": body.get("engineering_burden_summary"),
        "failure": body.get("failure"),
    }
    return row, None, aux


def _format_created_at(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        dt = value
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=UTC)
        return dt.isoformat()
    if isinstance(value, str):
        return value
    return str(value)


def insert_snapshot_row(row: dict[str, Any]) -> tuple[str | None, str | None, str | None]:
    """Insert single row via Supabase REST.

    Returns ``(snapshot_id, created_at_iso, error_code)``.
    ``created_at_iso`` is read from the persisted row when the API supports it.
    """
    client, code = get_supabase_client()
    if client is None:
        return None, None, code or "SNAPSHOT_PERSISTENCE_UNAVAILABLE"

    snapshot_pk = str(uuid4())
    payload = {**row, "id": snapshot_pk}

    try:
        ins = client.table(_TABLE).insert(payload).execute()
    except Exception:
        return None, None, "SNAPSHOT_INSERT_FAILED"

    created_iso: str | None = None
    data = getattr(ins, "data", None)
    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
        created_iso = _format_created_at(data[0].get("created_at"))

    if created_iso is None:
        try:
            sel = client.table(_TABLE).select("created_at").eq("id", snapshot_pk).single().execute()
            sd = getattr(sel, "data", None)
            if isinstance(sd, dict):
                created_iso = _format_created_at(sd.get("created_at"))
        except Exception:
            created_iso = None

    return snapshot_pk, created_iso, None
