"""Tests for GET /api/module01/sidebar/context (static sidebar shell context)."""

import ast
import json
import unittest
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

from main import module01_sidebar_context


def _decode_response(response):
    return response.status_code, json.loads(response.body.decode("utf-8"))


class Module01SidebarContextEndpointTests(unittest.TestCase):
    def test_missing_token_returns_auth_error(self):
        response = module01_sidebar_context(None)
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
            response = module01_sidebar_context("Bearer invalid-token")

        status_code, body = _decode_response(response)
        self.assertEqual(status_code, 200)
        self.assertEqual(body["status"], "auth_error")
        self.assertEqual(body["error"]["error_code"], "AUTH_INVALID_TOKEN")

    def test_valid_session_returns_success_with_sidebar(self):
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

        role_links = MagicMock()
        role_links.data = [{"role_id": "role-uuid-1", "is_active": True}]

        user_row = MagicMock()
        user_row.data = [
            {
                "id": "09ca45e0-56f7-414d-85ff-6f69bfdab621",
                "email": "test.auth@eds.local",
                "display_name": "Test User",
                "status": "ACTIVE",
            }
        ]

        def _table(name: str):
            m = MagicMock()
            if name == "module01_user_roles":
                m.select.return_value.eq.return_value.execute.return_value = role_links
            elif name == "module01_users":
                m.select.return_value.eq.return_value.limit.return_value.execute.return_value = user_row
            elif name == "module01_calculations":
                empty_calc = MagicMock()
                empty_calc.data = []
                m.select.return_value.eq.return_value.eq.return_value.order.return_value.limit.return_value.execute.return_value = empty_calc
            return m

        mock_client = MagicMock()
        mock_client.table.side_effect = _table

        def _fetch_role(_client, table: str, *, select: str, filters: dict):
            if table == "module01_roles" and filters.get("id") == "role-uuid-1":
                return {"id": "role-uuid-1", "role_code": "TEST_OPERATOR", "is_active": True}
            return _fetch_single(_client, table, select=select, filters=filters)

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
            patch("main._auth_get_supabase_client", return_value=mock_client),
            patch("main._auth_fetch_single", side_effect=_fetch_role),
        ):
            response = module01_sidebar_context("Bearer valid-token-pattern")

        status_code, body = _decode_response(response)
        self.assertEqual(status_code, 200)
        self.assertEqual(body["status"], "success")
        self.assertIsNone(body["error"])
        sidebar = body["data"]["sidebar"]
        self.assertEqual(sidebar["module_code"], "MODULE_01")
        self.assertEqual(sidebar["sidebar_id"], "MODULE_01_CALCULATION_SIDEBAR")
        self.assertIn("user", sidebar)
        self.assertEqual(sidebar["user"]["user_id"], "09ca45e0-56f7-414d-85ff-6f69bfdab621")
        self.assertIsNone(sidebar["active_calculation"])
        self.assertIn("session", sidebar)
        self.assertTrue(sidebar["session"]["authenticated"])
        self.assertIn("remaining_seconds", sidebar["session"])
        meta = body.get("metadata") or {}
        self.assertEqual(meta.get("menu_source"), "registry")

    def test_no_roles_returns_permission_denied(self):
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

        role_links = MagicMock()
        role_links.data = []

        def _table(name: str):
            m = MagicMock()
            if name == "module01_user_roles":
                m.select.return_value.eq.return_value.execute.return_value = role_links
            return m

        mock_client = MagicMock()
        mock_client.table.side_effect = _table

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
            patch("main._auth_get_supabase_client", return_value=mock_client),
            patch("main._auth_fetch_single", side_effect=_fetch_single),
        ):
            response = module01_sidebar_context("Bearer valid-token-pattern")

        status_code, body = _decode_response(response)
        self.assertEqual(status_code, 200)
        self.assertEqual(body["status"], "error")
        self.assertEqual(body["error"]["error_code"], "MODULE01_PERMISSION_DENIED")

    def test_main_py_sidebar_route_is_thin(self):
        """Sidebar assembly lives in services/module01_sidebar_service.py, not large inline trees in main."""
        root = Path(__file__).resolve().parent.parent
        main_src = (root / "main.py").read_text(encoding="utf-8")
        tree = ast.parse(main_src)
        fn = next(
            n
            for n in tree.body
            if isinstance(n, ast.FunctionDef) and n.name == "module01_sidebar_context"
        )
        body_lines = [n for n in fn.body if not isinstance(n, ast.Expr) or not isinstance(n.value, ast.Constant)]
        self.assertLessEqual(len(body_lines), 40, "module01_sidebar_context should delegate to service")
        self.assertNotIn(
            "MODULE_01_CALCULATION_SIDEBAR",
            main_src.split("def module01_sidebar_context")[1].split("def ", 1)[0],
            "sidebar payload constants should not be inlined in main.py",
        )


if __name__ == "__main__":
    unittest.main()
