import json
import unittest
from datetime import UTC, datetime, timedelta
from unittest.mock import patch

from main import module01_auth_session_status


def _decode_response(response):
    return response.status_code, json.loads(response.body.decode("utf-8"))


class Module01AuthSessionStatusEndpointTests(unittest.TestCase):
    def test_valid_token_returns_authenticated_success(self):
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
            patch("main._auth_fetch_active_roles", return_value=["TEST_OPERATOR"]),
        ):
            response = module01_auth_session_status("Bearer token-123")

        status_code, body = _decode_response(response)
        self.assertEqual(status_code, 200)
        self.assertEqual(body["status"], "success")
        self.assertEqual(body["data"]["authenticated"], True)
        self.assertEqual(body["data"]["user_id"], "09ca45e0-56f7-414d-85ff-6f69bfdab621")
        self.assertEqual(body["data"]["terminal_id"], "10578103-6c44-4eaf-a825-402d1fc5f7a6")
        self.assertIsNone(body["error"])

    def test_missing_token_returns_auth_missing_token(self):
        response = module01_auth_session_status(None)
        status_code, body = _decode_response(response)
        self.assertEqual(status_code, 200)
        self.assertEqual(body["status"], "auth_error")
        self.assertEqual(body["error"]["error_code"], "AUTH_MISSING_TOKEN")

    def test_invalid_token_returns_auth_invalid_token(self):
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
            response = module01_auth_session_status("Bearer invalid-token")

        status_code, body = _decode_response(response)
        self.assertEqual(status_code, 200)
        self.assertEqual(body["status"], "auth_error")
        self.assertEqual(body["error"]["error_code"], "AUTH_INVALID_TOKEN")
