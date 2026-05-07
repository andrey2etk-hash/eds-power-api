"""DB-driven dynamic menu registry reader (SQL Registry S01 tables)."""

from __future__ import annotations

import os
from typing import Any

try:
    from supabase import Client
except ImportError:  # pragma: no cover - typed fallback when supabase not installed
    Client = Any  # type: ignore[misc, assignment]

MENU_REGISTRY_ALLOWED_SCOPES = frozenset({"PRODUCTION", "ADMIN_TEST", "DEV", "TEMPLATE"})


def resolve_menu_environment_scope() -> tuple[str | None, str | None]:
    """Return (scope, error_code). MVP default PRODUCTION via env default."""
    raw = os.environ.get("EDS_MENU_ENVIRONMENT_SCOPE", "PRODUCTION").strip().upper()
    if raw not in MENU_REGISTRY_ALLOWED_SCOPES:
        return None, "MENU_ENVIRONMENT_SCOPE_INVALID"
    return raw, None


class MenuRegistryService:
    """Read normalized menu structure from eds_power_* registry via Supabase (service role)."""

    def __init__(self, client: Client) -> None:
        self._client = client

    def fetch_menu_modules(self, role_id: str, environment_scope: str) -> tuple[list[dict[str, Any]] | None, str | None]:
        """
        Return (modules list, error_code).
        On success error_code is None. On failure modules is None and error_code is set.
        """
        select_cols = (
            "role_id,module_id,action_id,visible,enabled,environment_scope,"
            "eds_power_modules(module_code,module_name,module_status,sort_order,is_active),"
            "eds_power_module_actions(action_key,action_type,menu_label,enabled,sort_order,metadata,visibility),"
            "module01_roles!inner(id,role_code)"
        )
        try:
            q = (
                self._client.table("eds_power_role_module_access")
                .select(select_cols)
                .eq("role_id", role_id)
                .eq("visible", True)
                .eq("enabled", True)
                .eq("environment_scope", environment_scope)
            )
            result = q.execute()
        except Exception:  # noqa: BLE001
            return None, "MENU_REGISTRY_QUERY_FAILED"

        rows = getattr(result, "data", None)
        if not isinstance(rows, list):
            return None, "MENU_REGISTRY_QUERY_FAILED"

        modules_accum: dict[str, dict[str, Any]] = {}
        actions_by_module: dict[str, list[dict[str, Any]]] = {}

        for row in rows:
            if not isinstance(row, dict):
                continue
            mod = row.get("eds_power_modules")
            act = row.get("eds_power_module_actions")
            role = row.get("module01_roles")
            if not isinstance(mod, dict) or not isinstance(act, dict):
                continue
            if not isinstance(role, dict) or role.get("id") != role_id:
                continue
            if not mod.get("is_active"):
                continue
            if not act.get("enabled"):
                continue

            module_code = mod.get("module_code")
            if not isinstance(module_code, str) or not module_code:
                continue

            if module_code not in modules_accum:
                modules_accum[module_code] = {
                    "module_code": module_code,
                    "module_name": mod.get("module_name"),
                    "module_status": mod.get("module_status"),
                    "sort_order": mod.get("sort_order"),
                }
                actions_by_module[module_code] = []

            action_key = act.get("action_key")
            if not isinstance(action_key, str) or not action_key:
                continue

            meta = act.get("metadata")
            if meta is None:
                meta = {}
            if not isinstance(meta, dict):
                meta = {}

            vis = act.get("visibility")
            if not isinstance(vis, str) or not vis:
                vis = "VISIBLE"

            actions_by_module[module_code].append(
                {
                    "action_key": action_key,
                    "action_type": act.get("action_type"),
                    "menu_label": act.get("menu_label"),
                    "enabled": bool(act.get("enabled")),
                    "sort_order": act.get("sort_order"),
                    "metadata": meta,
                    "visibility": vis,
                    "_module_code": module_code,
                    "_module_name": mod.get("module_name"),
                    "_module_status": mod.get("module_status"),
                    "_module_sort": mod.get("sort_order"),
                }
            )

        modules_out: list[dict[str, Any]] = []
        for code, m in sorted(
            modules_accum.items(),
            key=lambda kv: (kv[1].get("sort_order") if isinstance(kv[1].get("sort_order"), int) else 10_000, kv[0]),
        ):
            actions = actions_by_module.get(code, [])
            actions.sort(
                key=lambda a: (
                    a.get("sort_order") if isinstance(a.get("sort_order"), int) else 10_000,
                    a.get("action_key") or "",
                )
            )
            m_out = dict(m)
            m_out["actions"] = actions
            modules_out.append(m_out)

        return modules_out, None

    @staticmethod
    def menu_has_any_action(modules: list[dict[str, Any]]) -> bool:
        for m in modules:
            acts = m.get("actions")
            if isinstance(acts, list) and len(acts) > 0:
                return True
        return False
