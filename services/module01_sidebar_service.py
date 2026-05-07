"""Module 01 sidebar static context assembly (no calculation or product logic)."""

from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import Any

try:
    from supabase import Client
except ImportError:  # pragma: no cover
    Client = Any  # type: ignore[misc, assignment]


def _fetch_active_user_profile(client: Client, user_id: str) -> dict[str, Any] | None:
    try:
        res = (
            client.table("module01_users")
            .select("id,email,display_name,status")
            .eq("id", user_id)
            .limit(1)
            .execute()
        )
        rows = getattr(res, "data", None)
        if isinstance(rows, list) and rows and isinstance(rows[0], dict):
            return rows[0]
    except Exception:  # noqa: BLE001
        return None
    return None


def _parse_product_type_from_notes_v1(notes: str | None) -> str | None:
    if not isinstance(notes, str) or not notes.strip():
        return None
    for line in notes.splitlines():
        m = re.match(r"^PRODUCT_TYPE:\s*(\S+)\s*$", line.strip(), re.IGNORECASE)
        if m:
            return m.group(1).upper()
    return None


def _fetch_latest_active_calculation_bundle(
    client: Client, user_id: str
) -> dict[str, Any] | None:
    """Latest non-archived calculation for user + its -00 version row if present."""
    try:
        cr = (
            client.table("module01_calculations")
            .select("id,calculation_base_number,title,potential_customer,current_status,created_at")
            .eq("created_by_user_id", user_id)
            .eq("is_archived", False)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
        crows = getattr(cr, "data", None)
        if not isinstance(crows, list) or not crows or not isinstance(crows[0], dict):
            return None
        calc = crows[0]
        cid = calc.get("id")
        if not isinstance(cid, str):
            return None
        vr = (
            client.table("module01_calculation_versions")
            .select("calculation_version_number,status,notes")
            .eq("calculation_id", cid)
            .eq("version_suffix", "-00")
            .limit(1)
            .execute()
        )
        vrows = getattr(vr, "data", None)
        ver: dict[str, Any] | None = None
        if isinstance(vrows, list) and vrows and isinstance(vrows[0], dict):
            ver = vrows[0]
        disp = None
        if ver and isinstance(ver.get("calculation_version_number"), str):
            disp = ver["calculation_version_number"]
        elif isinstance(calc.get("calculation_base_number"), str):
            disp = f"{calc['calculation_base_number']}-00"
        pt = _parse_product_type_from_notes_v1(ver.get("notes") if ver else None) if ver else None
        if not pt:
            pt = "KZO"
        st = calc.get("current_status")
        stat = st if isinstance(st, str) else "DRAFT"
        return {
            "calculation_id": cid,
            "calculation_display_number": disp,
            "status": stat,
            "product_type": pt,
            "title": calc.get("title"),
            "potential_customer": calc.get("potential_customer"),
            "created_at": calc.get("created_at"),
        }
    except Exception:  # noqa: BLE001
        return None


def build_module01_sidebar_data(
    *,
    client: Client,
    user_id: str,
    user_email: str | None,
    terminal_id: str,
    expires_at_dt: datetime,
    role_codes: list[str],
    environment_scope: str,
) -> dict[str, Any]:
    """Return `data` object for GET /api/module01/sidebar/context success envelope (only `sidebar` key)."""
    _ = terminal_id  # reserved for future context; not exposed in V1 static shell
    row = _fetch_active_user_profile(client, user_id)
    if row is None or row.get("status") != "ACTIVE":
        raise ValueError("user_not_active")

    display_raw = row.get("display_name")
    email_raw = row.get("email")
    display_name = display_raw.strip() if isinstance(display_raw, str) and display_raw.strip() else None
    email = email_raw.strip() if isinstance(email_raw, str) and email_raw.strip() else None
    fallback = display_name or email or (user_email.strip() if isinstance(user_email, str) and user_email.strip() else "")

    primary_role = "TEST_OPERATOR" if "TEST_OPERATOR" in role_codes else sorted(role_codes)[0]
    now_dt = datetime.now(UTC)
    remaining = max(0, int((expires_at_dt - now_dt).total_seconds()))

    active = _fetch_latest_active_calculation_bundle(client, user_id)
    current_status_text = "No active calculation"
    if active:
        disp = active.get("calculation_display_number") or ""
        pst = active.get("status") or "DRAFT"
        pt = active.get("product_type") or "KZO"
        current_status_text = f"{disp} — {pt} — {pst}" if disp else f"{pt} — {pst}"

    sidebar: dict[str, Any] = {
        "sidebar_id": "MODULE_01_CALCULATION_SIDEBAR",
        "module_code": "MODULE_01",
        "module_name": "Module 01 — Розрахунки",
        "environment_scope": environment_scope,
        "user": {
            "user_id": user_id,
            "display_name": fallback,
            "role_code": primary_role,
        },
        "session": {
            "authenticated": True,
            "expires_at": expires_at_dt.isoformat(),
            "remaining_seconds": remaining,
        },
        "active_calculation": active,
        "sections": [
            {
                "section_key": "CURRENT_CONTEXT",
                "title": "Поточний розрахунок",
                "status_text": current_status_text,
            },
            {
                "section_key": "PRIMARY_ACTIONS",
                "title": "Основні дії",
            },
        ],
    }
    return {"sidebar": sidebar}
