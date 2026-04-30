"""Stage 8A — insert-only persistence for frozen `KZO_MVP_SNAPSHOT_V1`.

Calculation truth stays in ``prepare_calculation``; this module validates shape
and stores rows. No BOM/pricing/engineering recomputation."""

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


def validate_kzo_mvp_snapshot_v1(body: Any) -> tuple[dict[str, Any] | None, str | None]:
    """Return sanitized row-shaped dict ready for DB, or (None, error_code)."""
    if not isinstance(body, dict):
        return None, "SNAPSHOT_BODY_NOT_OBJECT"

    extra = set(body.keys()) - _ALLOWED_TOP_KEYS
    if extra:
        return None, "SNAPSHOT_UNKNOWN_FIELDS"

    if body.get("snapshot_version") != _KZO_SNAPSHOT_V1_VERSION:
        return None, "SNAPSHOT_VERSION_INVALID"

    run_status = body.get("run_status")
    if run_status not in ("SUCCESS", "FAILED"):
        return None, "SNAPSHOT_RUN_STATUS_INVALID"

    ts_parsed, ts_err = _parse_timestamp_basis(body.get("timestamp_basis"))
    if ts_err:
        return None, ts_err
    assert ts_parsed is not None
    timestamp_iso = ts_parsed.isoformat()

    if run_status == "SUCCESS":
        for key in (
            "structural_composition_summary",
            "physical_summary",
            "physical_topology_summary",
            "engineering_class_summary",
            "engineering_burden_summary",
        ):
            if not isinstance(body.get(key), dict):
                return None, "SNAPSHOT_SUCCESS_LAYER_MISSING"
        lv = body.get("logic_version")
        if lv is None or not isinstance(lv, str) or lv.strip() == "":
            return None, "SNAPSHOT_LOGIC_VERSION_REQUIRED"
        if not isinstance(body.get("request_metadata"), dict):
            return None, "SNAPSHOT_REQUEST_METADATA_REQUIRED"
        if not isinstance(body.get("normalized_input"), dict):
            return None, "SNAPSHOT_NORMALIZED_INPUT_REQUIRED"
        if body.get("failure") is not None:
            return None, "SNAPSHOT_SUCCESS_MUST_NOT_HAVE_FAILURE"

    elif run_status == "FAILED":
        if not isinstance(body.get("failure"), dict):
            return None, "SNAPSHOT_FAILURE_DETAIL_REQUIRED"

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
    return row, None


def insert_snapshot_row(row: dict[str, Any]) -> tuple[str | None, str | None]:
    """Insert single row via Supabase REST.

    Uses a server-generated-compatible UUID supplied by the caller so the HTTP
    response can echo ``snapshot_id`` without depending on INSERT returning body.
    """
    client, code = get_supabase_client()
    if client is None:
        return None, code or "SNAPSHOT_PERSISTENCE_UNAVAILABLE"

    snapshot_pk = str(uuid4())
    payload = {**row, "id": snapshot_pk}

    try:
        client.table(_TABLE).insert(payload).execute()
    except Exception:
        return None, "SNAPSHOT_INSERT_FAILED"

    return snapshot_pk, None
