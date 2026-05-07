import json
import unittest
from unittest.mock import patch

from main import module01_auth_login


class _InsertRecorder:
    def __init__(self) -> None:
        self.rows: list[dict] = []

    def table(self, table_name: str):
        return _InsertTable(table_name, self.rows)


class _InsertTable:
    def __init__(self, table_name: str, rows: list[dict]) -> None:
        self.table_name = table_name
        self.rows = rows
        self._insert_payload: dict | None = None

    def insert(self, payload: dict):
        self._insert_payload = payload
        return self

    def execute(self):
        if self.table_name == "module01_user_sessions" and self._insert_payload is not None:
            self.rows.append(self._insert_payload)
        return type("Result", (), {"data": [{"id": "row-1"}]})()


def _decode_response(response) -> tuple[int, dict]:
    return response.status_code, json.loads(response.body.decode("utf-8"))


class Module01AuthLoginEndpointTests(unittest.TestCase):
    def test_valid_login_returns_success_and_stores_hash_only(self):
        recorder = _InsertRecorder()
        payload = {
            "email": "test.auth@eds.local",
            "password": "secret-password",
            "spreadsheet_id": "sheet-1",
        }

        def _fetch_single(_client, table: str, *, select: str, filters: dict):
            if table == "module01_users":
                return {
                    "id": "09ca45e0-56f7-414d-85ff-6f69bfdab621",
                    "email": "test.auth@eds.local",
                    "display_name": "Test Auth User",
                    "status": "ACTIVE",
                }
            if table == "module01_user_auth":
                return {"password_hash": "$argon2id$v=19$m=65536,t=3,p=4$abc$def", "locked_until": None}
            if table == "module01_user_terminals":
                if filters.get("spreadsheet_id") == "sheet-1":
                    return {
                        "id": "10578103-6c44-4eaf-a825-402d1fc5f7a6",
                        "status": "ACTIVE",
                        "spreadsheet_id": "sheet-1",
                    }
                return None
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
            patch("main._auth_get_supabase_client", return_value=recorder),
            patch("main._auth_fetch_single", side_effect=_fetch_single),
            patch("main._auth_fetch_active_roles", return_value=["TEST_OPERATOR"]),
            patch("main._auth_verify_password", return_value=True),
        ):
            response = module01_auth_login(payload)

        status_code, body = _decode_response(response)
        self.assertEqual(status_code, 200)
        self.assertEqual(body["status"], "success")
        self.assertEqual(body["error"], None)
        self.assertEqual(body["data"]["user"]["email"], "test.auth@eds.local")
        self.assertEqual(body["data"]["allowed_actions"], ["auth.login", "auth.refresh_menu"])
        self.assertTrue(body["data"]["session"]["session_token"])

        self.assertEqual(len(recorder.rows), 1)
        inserted = recorder.rows[0]
        self.assertIn("session_token_hash", inserted)
        self.assertEqual(len(inserted["session_token_hash"]), 64)
        self.assertNotIn("session_token", inserted)

    def test_wrong_password_returns_auth_failed(self):
        payload = {
            "email": "test.auth@eds.local",
            "password": "wrong-password",
            "spreadsheet_id": "sheet-1",
        }

        def _fetch_single(_client, table: str, *, select: str, filters: dict):
            if table == "module01_users":
                return {
                    "id": "09ca45e0-56f7-414d-85ff-6f69bfdab621",
                    "email": "test.auth@eds.local",
                    "display_name": "Test Auth User",
                    "status": "ACTIVE",
                }
            if table == "module01_user_auth":
                return {"password_hash": "$argon2id$v=19$m=65536,t=3,p=4$abc$def", "locked_until": None}
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
            patch("main._auth_get_supabase_client", return_value=_InsertRecorder()),
            patch("main._auth_fetch_single", side_effect=_fetch_single),
            patch("main._auth_verify_password", return_value=False),
        ):
            response = module01_auth_login(payload)

        status_code, body = _decode_response(response)
        self.assertEqual(status_code, 200)
        self.assertEqual(body["status"], "auth_failed")
        self.assertEqual(body["error"]["error_code"], "AUTH_FAILED")

    def test_wrong_spreadsheet_id_returns_auth_failed(self):
        payload = {
            "email": "test.auth@eds.local",
            "password": "secret-password",
            "spreadsheet_id": "wrong-sheet",
        }

        def _fetch_single(_client, table: str, *, select: str, filters: dict):
            if table == "module01_users":
                return {
                    "id": "09ca45e0-56f7-414d-85ff-6f69bfdab621",
                    "email": "test.auth@eds.local",
                    "display_name": "Test Auth User",
                    "status": "ACTIVE",
                }
            if table == "module01_user_auth":
                return {"password_hash": "$argon2id$v=19$m=65536,t=3,p=4$abc$def", "locked_until": None}
            if table == "module01_user_terminals":
                return None
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
            patch("main._auth_get_supabase_client", return_value=_InsertRecorder()),
            patch("main._auth_fetch_single", side_effect=_fetch_single),
            patch("main._auth_fetch_active_roles", return_value=["TEST_OPERATOR"]),
            patch("main._auth_verify_password", return_value=True),
        ):
            response = module01_auth_login(payload)

        status_code, body = _decode_response(response)
        self.assertEqual(status_code, 200)
        self.assertEqual(body["status"], "auth_failed")
        self.assertEqual(body["error"]["error_code"], "AUTH_FAILED")

    def test_missing_required_env_fails_closed(self):
        payload = {
            "email": "test.auth@eds.local",
            "password": "secret-password",
            "spreadsheet_id": "sheet-1",
        }

        with patch.dict(
            "os.environ",
            {
                "SUPABASE_URL": "https://example.supabase.co",
                "SUPABASE_SERVICE_ROLE_KEY": "",
                "AUTH_SESSION_TTL_HOURS": "12",
            },
            clear=False,
        ):
            response = module01_auth_login(payload)

        status_code, body = _decode_response(response)
        self.assertEqual(status_code, 500)
        self.assertEqual(body["status"], "error")
        self.assertEqual(body["error"]["error_code"], "AUTH_CONFIG_ERROR")
