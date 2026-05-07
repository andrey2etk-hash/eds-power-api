"""Tests for POST /api/module01/calculations/create."""

import ast
import json
import unittest
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

from main import module01_calculations_create


def _decode(response):
    return response.status_code, json.loads(response.body.decode("utf-8"))


class Module01CalculationsCreateEndpointTests(unittest.TestCase):
    def test_missing_token_returns_create_auth_required(self):
        response = module01_calculations_create(None, {})
        status_code, body = _decode(response)
        self.assertEqual(status_code, 200)
        self.assertEqual(body["status"], "error")
        self.assertEqual(body["error"]["error_code"], "MODULE01_CREATE_AUTH_REQUIRED")

    def test_invalid_token_returns_create_auth_required(self):
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
            response = module01_calculations_create("Bearer bad", {})
        _, body = _decode(response)
        self.assertEqual(body["status"], "error")
        self.assertEqual(body["error"]["error_code"], "MODULE01_CREATE_AUTH_REQUIRED")

    def test_invalid_product_type(self):
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
                return {"id": "09ca45e0-56f7-414d-85ff-6f69bfdab621", "email": "t@e.l", "status": "ACTIVE"}
            if table == "module01_user_terminals":
                return {
                    "id": "10578103-6c44-4eaf-a825-402d1fc5f7a6",
                    "user_id": "09ca45e0-56f7-414d-85ff-6f69bfdab621",
                    "status": "ACTIVE",
                    "spreadsheet_id": "sheet-abc",
                }
            return None

        mock_client = MagicMock()

        with (
            patch.dict(
                "os.environ",
                {
                    "SUPABASE_URL": "https://example.supabase.co",
                    "SUPABASE_SERVICE_ROLE_KEY": "k",
                    "AUTH_SESSION_TTL_HOURS": "12",
                    "EDS_MENU_ENVIRONMENT_SCOPE": "PRODUCTION",
                },
                clear=False,
            ),
            patch("main._auth_get_supabase_client", return_value=mock_client),
            patch("main._auth_fetch_single", side_effect=_fetch_single),
        ):
            body = {
                "source_client": "GAS_TERMINAL_V1",
                "terminal_id": "10578103-6c44-4eaf-a825-402d1fc5f7a6",
                "spreadsheet_id": "sheet-abc",
                "payload": {
                    "calculation_title": "T",
                    "potential_customer": "P",
                    "product_type": "OTHER",
                },
            }
            response = module01_calculations_create("Bearer tok", body)

        _, out = _decode(response)
        self.assertEqual(out["status"], "error")
        self.assertEqual(out["error"]["error_code"], "MODULE01_CREATE_PRODUCT_TYPE_UNSUPPORTED")

    def test_missing_title(self):
        future = (datetime.now(UTC) + timedelta(hours=1)).isoformat()

        def _fetch_single(_client, table: str, *, select: str, filters: dict):
            if table == "module01_user_sessions":
                return {
                    "user_id": "u1",
                    "terminal_id": "t1",
                    "expires_at": future,
                    "revoked_at": None,
                }
            if table == "module01_users":
                return {"id": "u1", "status": "ACTIVE"}
            if table == "module01_user_terminals":
                return {"id": "t1", "user_id": "u1", "status": "ACTIVE", "spreadsheet_id": "s1"}
            return None

        mock_client = MagicMock()
        with (
            patch.dict("os.environ", {"SUPABASE_URL": "https://x.co", "SUPABASE_SERVICE_ROLE_KEY": "k", "AUTH_SESSION_TTL_HOURS": "12"}, clear=False),
            patch("main._auth_get_supabase_client", return_value=mock_client),
            patch("main._auth_fetch_single", side_effect=_fetch_single),
        ):
            response = module01_calculations_create(
                "Bearer tok",
                {
                    "source_client": "GAS_TERMINAL_V1",
                    "terminal_id": "t1",
                    "spreadsheet_id": "s1",
                    "payload": {"potential_customer": "P", "product_type": "KZO"},
                },
            )
        _, out = _decode(response)
        self.assertEqual(out["error"]["error_code"], "MODULE01_CREATE_INVALID_PAYLOAD")

    def test_permission_denied_when_service_returns_denied(self):
        future = (datetime.now(UTC) + timedelta(hours=1)).isoformat()

        def _fetch_single(_client, table: str, *, select: str, filters: dict):
            if table == "module01_user_sessions":
                return {"user_id": "u1", "terminal_id": "t1", "expires_at": future, "revoked_at": None}
            if table == "module01_users":
                return {"id": "u1", "status": "ACTIVE"}
            if table == "module01_user_terminals":
                return {"id": "t1", "user_id": "u1", "status": "ACTIVE", "spreadsheet_id": "s1"}
            return None

        mock_client = MagicMock()
        with (
            patch.dict("os.environ", {"SUPABASE_URL": "https://x.co", "SUPABASE_SERVICE_ROLE_KEY": "k", "AUTH_SESSION_TTL_HOURS": "12"}, clear=False),
            patch("main._auth_get_supabase_client", return_value=mock_client),
            patch("main._auth_fetch_single", side_effect=_fetch_single),
            patch("main.create_calculation_v1", return_value=(None, "MODULE01_CREATE_PERMISSION_DENIED")),
        ):
            response = module01_calculations_create(
                "Bearer tok",
                {
                    "source_client": "GAS_TERMINAL_V1",
                    "terminal_id": "t1",
                    "spreadsheet_id": "s1",
                    "payload": {
                        "calculation_title": "T",
                        "potential_customer": "P",
                        "product_type": "KZO",
                    },
                },
            )
        _, out = _decode(response)
        self.assertEqual(out["error"]["error_code"], "MODULE01_CREATE_PERMISSION_DENIED")

    def test_success_envelope_shape(self):
        future = (datetime.now(UTC) + timedelta(hours=1)).isoformat()

        def _fetch_single(_client, table: str, *, select: str, filters: dict):
            if table == "module01_user_sessions":
                return {"user_id": "u1", "terminal_id": "t1", "expires_at": future, "revoked_at": None}
            if table == "module01_users":
                return {"id": "u1", "status": "ACTIVE"}
            if table == "module01_user_terminals":
                return {"id": "t1", "user_id": "u1", "status": "ACTIVE", "spreadsheet_id": "s1"}
            return None

        mock_client = MagicMock()
        payload_ok = {
            "calculation": {
                "calculation_id": "cid",
                "calculation_base_number": "202605071200",
                "calculation_display_number": "202605071200-00",
                "version": "-00",
                "status": "DRAFT",
                "product_type": "KZO",
                "title": "T",
                "potential_customer": "P",
                "created_at": "2026-05-07T12:00:00Z",
            },
            "sidebar_update": {"active_calculation_id": "cid", "active_calculation_display": "d"},
        }
        with (
            patch.dict("os.environ", {"SUPABASE_URL": "https://x.co", "SUPABASE_SERVICE_ROLE_KEY": "k", "AUTH_SESSION_TTL_HOURS": "12"}, clear=False),
            patch("main._auth_get_supabase_client", return_value=mock_client),
            patch("main._auth_fetch_single", side_effect=_fetch_single),
            patch("main.create_calculation_v1", return_value=(payload_ok, None)),
        ):
            response = module01_calculations_create(
                "Bearer tok",
                {
                    "source_client": "GAS_TERMINAL_V1",
                    "terminal_id": "t1",
                    "spreadsheet_id": "s1",
                    "payload": {
                        "calculation_title": "T",
                        "potential_customer": "P",
                        "product_type": "KZO",
                    },
                },
            )
        _, out = _decode(response)
        self.assertEqual(out["status"], "success")
        self.assertEqual(out["data"]["calculation"]["calculation_base_number"], "202605071200")
        self.assertIn("sidebar_update", out["data"])

    def test_main_create_route_is_thin(self):
        root = Path(__file__).resolve().parent.parent
        main_src = (root / "main.py").read_text(encoding="utf-8")
        tree = ast.parse(main_src)
        fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "module01_calculations_create")
        body_lines = [n for n in fn.body if not isinstance(n, ast.Expr) or not isinstance(n.value, ast.Constant)]
        self.assertLessEqual(len(body_lines), 45, "module01_calculations_create should delegate to service")


if __name__ == "__main__":
    unittest.main()
