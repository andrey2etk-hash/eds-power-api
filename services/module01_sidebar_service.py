"""Module 01 sidebar static context assembly (no calculation or product logic)."""

from __future__ import annotations

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
        "active_calculation": None,
        "sections": [
            {
                "section_key": "CURRENT_CONTEXT",
                "title": "Поточний розрахунок",
                "status_text": "No active calculation",
            },
            {
                "section_key": "PRIMARY_ACTIONS",
                "title": "Основні дії",
            },
        ],
    }
    return {"sidebar": sidebar}
