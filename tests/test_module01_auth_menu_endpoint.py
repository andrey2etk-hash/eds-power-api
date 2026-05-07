"""Tests for GET /api/module01/auth/menu (DB registry + auth)."""

import json
import unittest
from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock, patch

from main import module01_auth_menu


def _decode_response(response):
    return response.status_code, json.loads(response.body.decode("utf-8"))


class Module01AuthMenuEndpointTests(unittest.TestCase):
    def test_missing_token_returns_auth_error_not_registry(self):
        response = module01_auth_menu(None)
        status_code, body = _decode_response(response)
        self.assertEqual(status_code, 200)
        self.assertEqual(body["status"], "auth_error")
        self.assertEqual(body["error"]["error_code"], "AUTH_MISSING_TOKEN")

    def test_invalid_token_returns_auth_error(self):
        with (
            patch.dict(
                "os.environ",
                {
                    "SUPABASE_URL": "https://example.supabase.co",
                    "SUPABASE_SERVICE_ROLE_KEY": "service-role-key",
                    "AUTH_SESSION_TTL_HOURS": "12",
                },
                clear=False,
            ),
            patch("main._auth_get_supabase_client", return_value=object()),
            patch("main._auth_fetch_single", return_value=None),
        ):
            response = module01_auth_menu("Bearer invalid-token")

        status_code, body = _decode_response(response)
        self.assertEqual(status_code, 200)
        self.assertEqual(body["status"], "auth_error")
        self.assertEqual(body["error"]["error_code"], "AUTH_INVALID_TOKEN")

    def test_authenticated_returns_registry_modules_and_menus(self):
        future = (datetime.now(UTC) + timedelta(hours=1)).isoformat()

        def _fetch_single(_client, table: str, *, select: str, filters: dict):
            if table == "module01_user_sessions":
                return {
                    "id": "session-1",
                    "user_id": "09ca45e0-56f7-414d-85ff-6f69bfdab621",
                    "terminal_id": "10578103-6c44-4eaf-a825-402d1fc5f7a6",
                    "expires_at": future,
                    "revoked_at": None,
                }
            if table == "module01_users":
                return {
                    "id": "09ca45e0-56f7-414d-85ff-6f69bfdab621",
                    "email": "test.auth@eds.local",
                    "status": "ACTIVE",
                }
            if table == "module01_user_terminals":
                return {
                    "id": "10578103-6c44-4eaf-a825-402d1fc5f7a6",
                    "user_id": "09ca45e0-56f7-414d-85ff-6f69bfdab621",
                    "status": "ACTIVE",
                }
            return None

        sample_modules = [
            {
                "module_code": "SYSTEM_SHELL",
                "module_name": "System shell",
                "module_status": "RELEASED",
                "sort_order": 10,
                "actions": [
                    {
                        "action_key": "REFRESH_MENU",
                        "action_type": "REFRESH_MENU",
                        "menu_label": "Оновити меню",
                        "enabled": True,
                        "sort_order": 10,
                        "metadata": {},
                        "visibility": "VISIBLE",
                    },
                    {
                        "action_key": "SESSION_STATUS",
                        "action_type": "SESSION_STATUS",
                        "menu_label": "Статус сесії",
                        "enabled": True,
                        "sort_order": 20,
                        "metadata": {},
                        "visibility": "VISIBLE",
                    },
                    {
                        "action_key": "LOGOUT",
                        "action_type": "LOGOUT",
                        "menu_label": "Вийти",
                        "enabled": True,
                        "sort_order": 30,
                        "metadata": {},
                        "visibility": "VISIBLE",
                    },
                ],
            },
            {
                "module_code": "MODULE_01",
                "module_name": "Module 01",
                "module_status": "PLANNED",
                "sort_order": 20,
                "actions": [
                    {
                        "action_key": "MODULE_01_PLACEHOLDER",
                        "action_type": "PLACEHOLDER_DISABLED",
                        "menu_label": "Module 01 — Розрахунки (planned)",
                        "enabled": False,
                        "sort_order": 10,
                        "metadata": {},
                        "visibility": "VISIBLE",
                    }
                ],
            },
        ]

        with (
            patch.dict(
                "os.environ",
                {
                    "SUPABASE_URL": "https://example.supabase.co",
                    "SUPABASE_SERVICE_ROLE_KEY": "service-role-key",
                    "AUTH_SESSION_TTL_HOURS": "12",
                    "EDS_MENU_ENVIRONMENT_SCOPE": "PRODUCTION",
                },
                clear=False,
            ),
            patch("main._auth_get_supabase_client", return_value=object()),
            patch("main._auth_fetch_single", side_effect=_fetch_single),
            patch("main._auth_resolve_primary_role_id", return_value="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"),
            patch("main.MenuRegistryService") as msvc,
        ):
            inst = msvc.return_value
            inst.fetch_menu_modules = MagicMock(return_value=(sample_modules, None))
            response = module01_auth_menu("Bearer valid-token")

        status_code, body = _decode_response(response)
        self.assertEqual(status_code, 200)
        self.assertEqual(body["status"], "success")
        data = body["data"]
        self.assertIn("modules", data)
        self.assertIn("menus", data)
        codes = [m["module_code"] for m in data["modules"]]
        self.assertIn("SYSTEM_SHELL", codes)
        self.assertIn("MODULE_01", codes)
        ak = {item["action_key"] for item in data["menus"]}
        self.assertEqual({"REFRESH_MENU", "SESSION_STATUS", "LOGOUT", "MODULE_01_PLACEHOLDER"}, ak)
        self.assertNotIn("role_module_access", json.dumps(data))
        self.assertEqual(body["metadata"].get("environment_scope"), "PRODUCTION")
        self.assertEqual(body["metadata"].get("menu_source"), "registry")

    def test_registry_query_failure_returns_error_envelope(self):
        future = (datetime.now(UTC) + timedelta(hours=1)).isoformat()

        def _fetch_single(_client, table: str, *, select: str, filters: dict):
            if table == "module01_user_sessions":
                return {
                    "id": "session-1",
                    "user_id": "09ca45e0-56f7-414d-85ff-6f69bfdab621",
                    "terminal_id": "10578103-6c44-4eaf-a825-402d1fc5f7a6",
                    "expires_at": future,
                    "revoked_at": None,
                }
            if table == "module01_users":
                return {
                    "id": "09ca45e0-56f7-414d-85ff-6f69bfdab621",
                    "email": "test.auth@eds.local",
                    "status": "ACTIVE",
                }
            if table == "module01_user_terminals":
                return {
                    "id": "10578103-6c44-4eaf-a825-402d1fc5f7a6",
                    "user_id": "09ca45e0-56f7-414d-85ff-6f69bfdab621",
                    "status": "ACTIVE",
                }
            return None

        with (
            patch.dict(
                "os.environ",
                {
                    "SUPABASE_URL": "https://example.supabase.co",
                    "SUPABASE_SERVICE_ROLE_KEY": "service-role-key",
                    "AUTH_SESSION_TTL_HOURS": "12",
                },
                clear=False,
            ),
            patch("main._auth_get_supabase_client", return_value=object()),
            patch("main._auth_fetch_single", side_effect=_fetch_single),
            patch("main._auth_resolve_primary_role_id", return_value="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"),
            patch("main.MenuRegistryService") as msvc,
        ):
            inst = msvc.return_value
            inst.fetch_menu_modules = MagicMock(return_value=(None, "MENU_REGISTRY_QUERY_FAILED"))
            response = module01_auth_menu("Bearer valid-token")

        status_code, body = _decode_response(response)
        self.assertEqual(status_code, 200)
        self.assertEqual(body["status"], "error")
        self.assertIsNone(body["data"])
        self.assertEqual(body["error"]["error_code"], "MENU_REGISTRY_QUERY_FAILED")

    def test_no_allowed_actions_returns_menu_no_allowed_actions(self):
        future = (datetime.now(UTC) + timedelta(hours=1)).isoformat()

        def _fetch_single(_client, table: str, *, select: str, filters: dict):
            if table == "module01_user_sessions":
                return {
                    "id": "session-1",
                    "user_id": "09ca45e0-56f7-414d-85ff-6f69bfdab621",
                    "terminal_id": "10578103-6c44-4eaf-a825-402d1fc5f7a6",
                    "expires_at": future,
                    "revoked_at": None,
                }
            if table == "module01_users":
                return {
                    "id": "09ca45e0-56f7-414d-85ff-6f69bfdab621",
                    "email": "test.auth@eds.local",
                    "status": "ACTIVE",
                }
            if table == "module01_user_terminals":
                return {
                    "id": "10578103-6c44-4eaf-a825-402d1fc5f7a6",
                    "user_id": "09ca45e0-56f7-414d-85ff-6f69bfdab621",
                    "status": "ACTIVE",
                }
            return None

        with (
            patch.dict(
                "os.environ",
                {
                    "SUPABASE_URL": "https://example.supabase.co",
                    "SUPABASE_SERVICE_ROLE_KEY": "service-role-key",
                    "AUTH_SESSION_TTL_HOURS": "12",
                },
                clear=False,
            ),
            patch("main._auth_get_supabase_client", return_value=object()),
            patch("main._auth_fetch_single", side_effect=_fetch_single),
            patch("main._auth_resolve_primary_role_id", return_value="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"),
            patch("main.MenuRegistryService") as msvc,
        ):
            inst = msvc.return_value
            inst.fetch_menu_modules = MagicMock(return_value=([{"module_code": "X", "actions": []}], None))
            response = module01_auth_menu("Bearer valid-token")

        status_code, body = _decode_response(response)
        self.assertEqual(status_code, 200)
        self.assertEqual(body["status"], "error")
        self.assertEqual(body["error"]["error_code"], "MENU_NO_ALLOWED_ACTIONS")


if __name__ == "__main__":
    unittest.main()
