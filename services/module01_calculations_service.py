"""Module 01 — Create Calculation V1 (header + version -00 + status history). No engineering/product logic."""

from __future__ import annotations

import re
from datetime import UTC, datetime, timedelta
from typing import Any

try:
    from supabase import Client
except ImportError:  # pragma: no cover
    Client = Any  # type: ignore[misc, assignment]

from services.menu_registry_service import MenuRegistryService, resolve_menu_environment_scope

MODULE01_CREATE_ACTION_KEY = "MODULE01_CREATE_CALCULATION"

ALLOWED_SOURCE_CLIENTS = frozenset({"GAS_TERMINAL_V1"})

TITLE_MAX_LEN = 500
POTENTIAL_CUSTOMER_MAX_LEN = 500
COMMENT_MAX_LEN = 4000
EXTERNAL_REFERENCE_MAX_LEN = 500

CALC_NUMBER_MAX_ATTEMPTS = 5

_REASON_CREATE = "CREATE_CALCULATION"
_HISTORY_NOTE_INITIAL = "initial calculation created"


def _table_fetch_single(client: Client, table: str, *, select: str, filters: dict[str, Any]) -> dict[str, Any] | None:
    q = client.table(table).select(select)
    for k, v in filters.items():
        q = q.eq(k, v)
    result = q.limit(1).execute()
    rows = getattr(result, "data", None)
    if isinstance(rows, list) and rows and isinstance(rows[0], dict):
        return rows[0]
    return None


def build_structured_notes_v1(
    *,
    product_type: str,
    comment: str | None,
    external_reference: str | None,
) -> str:
    """Strict V1 template (no JSON)."""
    lines = ["EDS_POWER_CALC_NOTES_V1", f"PRODUCT_TYPE: {product_type.strip()}"]
    ext = (external_reference or "").strip()
    if ext:
        lines.append(f"EXTERNAL_REFERENCE: {ext}")
    cmt = (comment or "").strip()
    if cmt:
        lines.append(f"COMMENT: {cmt}")
    return "\n".join(lines) + "\n"


def _utc_base_number(*, minute_offset: int = 0) -> str:
    """12-digit YYYYMMDDHHMM in UTC."""
    dt = datetime.now(UTC) + timedelta(minutes=minute_offset)
    return dt.strftime("%Y%m%d%H%M")


def _display_number(base: str, version_suffix: str) -> str:
    """e.g. base 202605071904 + suffix '-00' -> 202605071904-00."""
    digits = version_suffix.lstrip("-") if version_suffix.startswith("-") else version_suffix
    return f"{base}-{digits}"


def _is_unique_violation(exc: BaseException) -> bool:
    s = str(exc).lower()
    return "duplicate" in s or "unique" in s or "23505" in s


def user_has_create_calculation_permission(
    *,
    client: Client,
    user_id: str,
    environment_scope: str,
) -> bool:
    """True if registry grants MODULE01_CREATE_CALCULATION for user's primary role."""
    links = client.table("module01_user_roles").select("role_id,is_active").eq("user_id", user_id).execute()
    link_rows = getattr(links, "data", None)
    if not isinstance(link_rows, list):
        return False
    active_role_ids = [
        row.get("role_id")
        for row in link_rows
        if isinstance(row, dict) and row.get("is_active") is True and isinstance(row.get("role_id"), str)
    ]
    if not active_role_ids:
        return False
    roles: list[dict[str, Any]] = []
    for rid in active_role_ids:
        role = _table_fetch_single(client, "module01_roles", select="id,role_code,is_active", filters={"id": rid})
        if role and role.get("is_active") is True and isinstance(role.get("id"), str):
            roles.append(role)
    if not roles:
        return False
    by_code = {str(r["role_code"]): str(r["id"]) for r in roles if isinstance(r.get("role_code"), str) and r.get("id")}
    role_id = by_code.get("TEST_OPERATOR") or str(sorted(roles, key=lambda r: str(r.get("role_code") or ""))[0]["id"])

    msvc = MenuRegistryService(client)
    modules, err = msvc.fetch_menu_modules(role_id, environment_scope)
    if err or not modules:
        return False
    for mod in modules:
        for act in mod.get("actions") or []:
            if not isinstance(act, dict):
                continue
            if act.get("action_key") == MODULE01_CREATE_ACTION_KEY:
                return True
    return False


def validate_create_payload(body: Any) -> tuple[dict[str, Any] | None, str | None, str | None]:
    """Return (normalized_body, error_code, field)."""
    if not isinstance(body, dict):
        return None, "MODULE01_CREATE_INVALID_PAYLOAD", None
    src = body.get("source_client")
    if not isinstance(src, str) or src.strip() not in ALLOWED_SOURCE_CLIENTS:
        return None, "MODULE01_CREATE_INVALID_PAYLOAD", "source_client"
    terminal_id = body.get("terminal_id")
    spreadsheet_id = body.get("spreadsheet_id")
    if not isinstance(terminal_id, str) or not terminal_id.strip():
        return None, "MODULE01_CREATE_INVALID_PAYLOAD", "terminal_id"
    if not isinstance(spreadsheet_id, str) or not spreadsheet_id.strip():
        return None, "MODULE01_CREATE_INVALID_PAYLOAD", "spreadsheet_id"
    payload = body.get("payload")
    if not isinstance(payload, dict):
        return None, "MODULE01_CREATE_INVALID_PAYLOAD", "payload"
    title = payload.get("calculation_title")
    pc = payload.get("potential_customer")
    pt = payload.get("product_type")
    comment = payload.get("comment")
    ext_ref = payload.get("external_reference")
    if not isinstance(title, str) or not title.strip():
        return None, "MODULE01_CREATE_INVALID_PAYLOAD", "calculation_title"
    if not isinstance(pc, str) or not pc.strip():
        return None, "MODULE01_CREATE_INVALID_PAYLOAD", "potential_customer"
    if not isinstance(pt, str) or pt.strip() != "KZO":
        return None, "MODULE01_CREATE_PRODUCT_TYPE_UNSUPPORTED", "product_type"
    if comment is not None and not isinstance(comment, str):
        return None, "MODULE01_CREATE_INVALID_PAYLOAD", "comment"
    if ext_ref is not None and not isinstance(ext_ref, str):
        return None, "MODULE01_CREATE_INVALID_PAYLOAD", "external_reference"
    title_s = title.strip()
    pc_s = pc.strip()
    if len(title_s) > TITLE_MAX_LEN or len(pc_s) > POTENTIAL_CUSTOMER_MAX_LEN:
        return None, "MODULE01_CREATE_INVALID_PAYLOAD", None
    cmt_s = (comment or "").strip() if isinstance(comment, str) else ""
    ref_s = (ext_ref or "").strip() if isinstance(ext_ref, str) else ""
    if len(cmt_s) > COMMENT_MAX_LEN or len(ref_s) > EXTERNAL_REFERENCE_MAX_LEN:
        return None, "MODULE01_CREATE_INVALID_PAYLOAD", None
    notes = build_structured_notes_v1(product_type="KZO", comment=cmt_s or None, external_reference=ref_s or None)
    if len(notes) > 12000:
        return None, "MODULE01_CREATE_INVALID_PAYLOAD", None

    normalized = {
        "source_client": src.strip(),
        "terminal_id": terminal_id.strip(),
        "spreadsheet_id": spreadsheet_id.strip(),
        "payload": {
            "calculation_title": title_s,
            "potential_customer": pc_s,
            "product_type": "KZO",
            "comment": cmt_s,
            "external_reference": ref_s,
        },
        "_notes_v1": notes,
    }
    return normalized, None, None


def verify_terminal_spreadsheet(
    client: Client,
    *,
    session_terminal_id: str,
    session_user_id: str,
    payload_terminal_id: str,
    payload_spreadsheet_id: str,
) -> bool:
    if payload_terminal_id != session_terminal_id:
        return False
    term = _table_fetch_single(
        client,
        "module01_user_terminals",
        select="id,user_id,status,spreadsheet_id",
        filters={"id": session_terminal_id},
    )
    if term is None or term.get("status") != "ACTIVE" or term.get("user_id") != session_user_id:
        return False
    sid = term.get("spreadsheet_id")
    return isinstance(sid, str) and sid == payload_spreadsheet_id


def create_calculation_v1(
    *,
    client: Client,
    user_id: str,
    session_terminal_id: str,
    normalized: dict[str, Any],
    request_id: str,
) -> tuple[dict[str, Any] | None, str | None]:
    """
    Insert header + version -00 + status history.
    PostgREST has no single multi-insert transaction in this client; use compensating deletes on failure.
    """
    env_scope, escope_err = resolve_menu_environment_scope()
    if escope_err:
        return None, "MODULE01_CREATE_BACKEND_UNAVAILABLE"

    if not user_has_create_calculation_permission(client=client, user_id=user_id, environment_scope=env_scope):
        return None, "MODULE01_CREATE_PERMISSION_DENIED"

    if not verify_terminal_spreadsheet(
        client,
        session_terminal_id=session_terminal_id,
        session_user_id=user_id,
        payload_terminal_id=normalized["terminal_id"],
        payload_spreadsheet_id=normalized["spreadsheet_id"],
    ):
        return None, "MODULE01_CREATE_TERMINAL_MISMATCH"

    payload = normalized["payload"]
    notes = normalized["_notes_v1"]
    version_suffix = "-00"

    for attempt in range(CALC_NUMBER_MAX_ATTEMPTS):
        calc_id = None
        version_id = None
        base = _utc_base_number(minute_offset=attempt)
        if not re.match(r"^[0-9]{12}$", base):
            continue
        ver_num = _display_number(base, version_suffix)

        try:
            ins_calc = (
                client.table("module01_calculations")
                .insert(
                    {
                        "calculation_base_number": base,
                        "title": payload["calculation_title"],
                        "potential_customer": payload["potential_customer"],
                        "created_by_user_id": user_id,
                        "current_status": "DRAFT",
                        "is_archived": False,
                    }
                )
                .execute()
            )
            calc_rows = getattr(ins_calc, "data", None)
            if not isinstance(calc_rows, list) or not calc_rows or not isinstance(calc_rows[0], dict):
                return None, "MODULE01_CREATE_BACKEND_UNAVAILABLE"
            cid = calc_rows[0].get("id")
            if not isinstance(cid, str):
                return None, "MODULE01_CREATE_BACKEND_UNAVAILABLE"
            calc_id = cid

            try:
                ins_ver = (
                    client.table("module01_calculation_versions")
                    .insert(
                        {
                            "calculation_id": calc_id,
                            "version_suffix": version_suffix,
                            "calculation_version_number": ver_num,
                            "status": "DRAFT",
                            "created_by_user_id": user_id,
                            "notes": notes,
                        }
                    )
                    .execute()
                )
                ver_rows = getattr(ins_ver, "data", None)
                if not isinstance(ver_rows, list) or not ver_rows or not isinstance(ver_rows[0], dict):
                    _delete_calculation_cascade(client, calc_id, None)
                    return None, "MODULE01_CREATE_VERSION_CREATE_FAILED"
                vid = ver_rows[0].get("id")
                if not isinstance(vid, str):
                    _delete_calculation_cascade(client, calc_id, None)
                    return None, "MODULE01_CREATE_VERSION_CREATE_FAILED"
                version_id = vid
            except Exception as exc:  # noqa: BLE001
                if _is_unique_violation(exc) and attempt < CALC_NUMBER_MAX_ATTEMPTS - 1:
                    if calc_id:
                        client.table("module01_calculations").delete().eq("id", calc_id).execute()
                    calc_id = None
                    continue
                if calc_id:
                    client.table("module01_calculations").delete().eq("id", calc_id).execute()
                if _is_unique_violation(exc):
                    return None, "MODULE01_CREATE_NUMBER_COLLISION"
                return None, "MODULE01_CREATE_VERSION_CREATE_FAILED"

            try:
                ins_hist = (
                    client.table("module01_calculation_status_history")
                    .insert(
                        {
                            "calculation_version_id": version_id,
                            "new_status": "DRAFT",
                            "changed_by_user_id": user_id,
                            "reason": _REASON_CREATE,
                            "notes": _HISTORY_NOTE_INITIAL,
                            "request_id": request_id,
                            "source_client": normalized["source_client"],
                        }
                    )
                    .execute()
                )
                hist_rows = getattr(ins_hist, "data", None)
                if not isinstance(hist_rows, list) or not hist_rows:
                    _delete_calculation_cascade(client, calc_id, version_id)
                    return None, "MODULE01_CREATE_STATUS_HISTORY_FAILED"
            except Exception:  # noqa: BLE001
                _delete_calculation_cascade(client, calc_id, version_id)
                return None, "MODULE01_CREATE_STATUS_HISTORY_FAILED"

            created_row = _table_fetch_single(
                client,
                "module01_calculations",
                select="id,calculation_base_number,title,potential_customer,current_status,created_at",
                filters={"id": calc_id},
            )
            created_at = ""
            if isinstance(created_row, dict):
                ca = created_row.get("created_at")
                if isinstance(ca, str):
                    created_at = ca

            display = _display_number(base, version_suffix)
            sidebar_line = f"{display} — KZO — DRAFT"

            data = {
                "calculation": {
                    "calculation_id": calc_id,
                    "calculation_base_number": base,
                    "calculation_display_number": display,
                    "version": version_suffix,
                    "status": "DRAFT",
                    "product_type": "KZO",
                    "title": payload["calculation_title"],
                    "potential_customer": payload["potential_customer"],
                    "created_at": created_at,
                },
                "sidebar_update": {
                    "active_calculation_id": calc_id,
                    "active_calculation_display": sidebar_line,
                },
            }
            return data, None

        except Exception as exc:  # noqa: BLE001
            if calc_id:
                try:
                    client.table("module01_calculations").delete().eq("id", calc_id).execute()
                except Exception:  # noqa: BLE001
                    pass
                calc_id = None
            if _is_unique_violation(exc) and attempt < CALC_NUMBER_MAX_ATTEMPTS - 1:
                continue
            if _is_unique_violation(exc):
                return None, "MODULE01_CREATE_NUMBER_COLLISION"
            return None, "MODULE01_CREATE_BACKEND_UNAVAILABLE"

    return None, "MODULE01_CREATE_NUMBER_COLLISION"


def _delete_calculation_cascade(client: Client, calculation_id: str, version_id: str | None) -> None:
    """Best-effort cleanup (version FK from history)."""
    if version_id:
        try:
            client.table("module01_calculation_status_history").delete().eq("calculation_version_id", version_id).execute()
        except Exception:  # noqa: BLE001
            pass
        try:
            client.table("module01_calculation_versions").delete().eq("id", version_id).execute()
        except Exception:  # noqa: BLE001
            pass
    try:
        client.table("module01_calculations").delete().eq("id", calculation_id).execute()
    except Exception:  # noqa: BLE001
        pass
