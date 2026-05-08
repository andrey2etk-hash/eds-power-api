"""Tests for Module 01 calculation items API V1 (add + list)."""

import json
import unittest
from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock, patch

from main import module01_calculation_items_add, module01_calculation_items_list
from services.module01_calculation_items_service import (
    add_calculation_item_v1,
    list_calculation_items_v1,
    validate_items_add_payload,
)

UID = "09ca45e0-56f7-414d-85ff-6f69bfdab621"
CID = "11111111-1111-1111-1111-111111111111"
VID = "22222222-2222-2222-2222-222222222222"
PID = "33333333-3333-3333-3333-333333333333"


def _decode(response):
    return response.status_code, json.loads(response.body.decode("utf-8"))


def _norm(body: dict):
    n, e, f = validate_items_add_payload(body)
    assert e is None and n is not None
    return n


class Module01CalculationItemsServiceTests(unittest.TestCase):
    def test_add_top_level_container(self):
        def _table(name: str):
            m = MagicMock()
            if name == "module01_calculation_items":
                m.insert.return_value.execute.return_value = MagicMock(
                    data=[
                        {
                            "id": PID,
                            "calculation_id": CID,
                            "calculation_version_id": VID,
                            "parent_item_id": None,
                            "item_kind": "CONTAINER",
                            "item_type": "T",
                            "item_name": "N",
                            "local_quantity": 1.0,
                            "total_quantity": 1.0,
                            "item_status": "DRAFT",
                            "sort_order": 100,
                            "display_index": "1",
                            "payload_json": {},
                            "result_summary_json": {},
                            "created_at": "2026-05-08T00:00:00Z",
                            "updated_at": "2026-05-08T00:00:00Z",
                        }
                    ]
                )
            return m

        mock_client = MagicMock()
        mock_client.table.side_effect = _table

        with (
            patch(
                "services.module01_calculation_items_service._table_fetch_single",
                side_effect=[
                    {"id": CID, "created_by_user_id": UID},
                    {"id": VID, "calculation_id": CID, "status": "DRAFT"},
                ],
            ),
            patch("services.module01_calculation_items_service._max_sibling_sort_order", return_value=None),
            patch("services.module01_calculation_items_service._count_siblings", return_value=0),
        ):
            n = _norm(
                {
                    "calculation_id": CID,
                    "calculation_version_id": VID,
                    "parent_item_id": None,
                    "item_kind": "CONTAINER",
                    "item_type": "T",
                    "item_name": "N",
                    "local_quantity": 1,
                }
            )
            data, err, _ = add_calculation_item_v1(client=mock_client, user_id=UID, normalized=n)

        self.assertIsNone(err)
        assert data is not None
        self.assertEqual(data["item"]["total_quantity"], 1.0)
        self.assertEqual(data["item"]["display_index"], "1")

    def test_add_second_top_level_product_display_index(self):
        def _table(name: str):
            m = MagicMock()
            if name == "module01_calculation_items":
                m.insert.return_value.execute.return_value = MagicMock(
                    data=[
                        {
                            "id": "44444444-4444-4444-4444-444444444444",
                            "calculation_id": CID,
                            "calculation_version_id": VID,
                            "parent_item_id": None,
                            "item_kind": "PRODUCT",
                            "item_type": "P",
                            "item_name": "P2",
                            "local_quantity": 2.0,
                            "total_quantity": 2.0,
                            "item_status": "DRAFT",
                            "sort_order": 101,
                            "display_index": "2",
                            "payload_json": {},
                            "result_summary_json": {},
                            "created_at": "2026-05-08T00:00:00Z",
                            "updated_at": "2026-05-08T00:00:00Z",
                        }
                    ]
                )
            return m

        mock_client = MagicMock()
        mock_client.table.side_effect = _table

        with (
            patch(
                "services.module01_calculation_items_service._table_fetch_single",
                side_effect=[
                    {"id": CID, "created_by_user_id": UID},
                    {"id": VID, "calculation_id": CID, "status": "DRAFT"},
                ],
            ),
            patch("services.module01_calculation_items_service._max_sibling_sort_order", return_value=100),
            patch("services.module01_calculation_items_service._count_siblings", return_value=1),
        ):
            n = _norm(
                {
                    "calculation_id": CID,
                    "calculation_version_id": VID,
                    "item_kind": "PRODUCT",
                    "item_type": "P",
                    "item_name": "P2",
                    "local_quantity": 2,
                }
            )
            data, err, _ = add_calculation_item_v1(client=mock_client, user_id=UID, normalized=n)

        self.assertIsNone(err)
        assert data is not None
        self.assertEqual(data["item"]["display_index"], "2")

    def test_add_child_product_under_container(self):
        def _table(name: str):
            m = MagicMock()
            if name == "module01_calculation_items":
                m.insert.return_value.execute.return_value = MagicMock(
                    data=[
                        {
                            "id": "55555555-5555-5555-5555-555555555555",
                            "calculation_id": CID,
                            "calculation_version_id": VID,
                            "parent_item_id": PID,
                            "item_kind": "PRODUCT",
                            "item_type": "K",
                            "item_name": "Child",
                            "local_quantity": 3.0,
                            "total_quantity": 6.0,
                            "item_status": "DRAFT",
                            "sort_order": 100,
                            "display_index": "1.1",
                            "payload_json": {},
                            "result_summary_json": {},
                            "created_at": "2026-05-08T00:00:00Z",
                            "updated_at": "2026-05-08T00:00:00Z",
                        }
                    ]
                )
            return m

        mock_client = MagicMock()
        mock_client.table.side_effect = _table

        with (
            patch(
                "services.module01_calculation_items_service._table_fetch_single",
                side_effect=[
                    {"id": CID, "created_by_user_id": UID},
                    {"id": VID, "calculation_id": CID, "status": "DRAFT"},
                    {
                        "id": PID,
                        "calculation_id": CID,
                        "calculation_version_id": VID,
                        "parent_item_id": None,
                        "item_kind": "CONTAINER",
                        "total_quantity": 2.0,
                        "display_index": "1",
                    },
                ],
            ),
            patch("services.module01_calculation_items_service._max_sibling_sort_order", return_value=None),
            patch("services.module01_calculation_items_service._count_siblings", return_value=0),
        ):
            n = _norm(
                {
                    "calculation_id": CID,
                    "calculation_version_id": VID,
                    "parent_item_id": PID,
                    "item_kind": "PRODUCT",
                    "item_type": "K",
                    "item_name": "Child",
                    "local_quantity": 3,
                }
            )
            data, err, _ = add_calculation_item_v1(client=mock_client, user_id=UID, normalized=n)

        self.assertIsNone(err)
        assert data is not None
        self.assertEqual(data["item"]["total_quantity"], 6.0)
        self.assertEqual(data["item"]["display_index"], "1.1")

    def test_reject_child_under_product(self):
        mock_client = MagicMock()
        with patch(
            "services.module01_calculation_items_service._table_fetch_single",
            side_effect=[
                {"id": CID, "created_by_user_id": UID},
                {"id": VID, "calculation_id": CID, "status": "DRAFT"},
                {
                    "id": PID,
                    "calculation_id": CID,
                    "calculation_version_id": VID,
                    "parent_item_id": None,
                    "item_kind": "PRODUCT",
                    "total_quantity": 1.0,
                    "display_index": "1",
                },
            ],
        ):
            n = _norm(
                {
                    "calculation_id": CID,
                    "calculation_version_id": VID,
                    "parent_item_id": PID,
                    "item_kind": "PRODUCT",
                    "item_type": "K",
                    "item_name": "Child",
                    "local_quantity": 1,
                }
            )
            _, err, f = add_calculation_item_v1(client=mock_client, user_id=UID, normalized=n)

        self.assertEqual(err, "ITEM_PARENT_NOT_CONTAINER")
        self.assertEqual(f, "parent_item_id")

    def test_reject_depth_three(self):
        mock_client = MagicMock()
        with patch(
            "services.module01_calculation_items_service._table_fetch_single",
            side_effect=[
                {"id": CID, "created_by_user_id": UID},
                {"id": VID, "calculation_id": CID, "status": "DRAFT"},
                {
                    "id": PID,
                    "calculation_id": CID,
                    "calculation_version_id": VID,
                    "parent_item_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                    "item_kind": "CONTAINER",
                    "total_quantity": 1.0,
                    "display_index": "1.1",
                },
            ],
        ):
            n = _norm(
                {
                    "calculation_id": CID,
                    "calculation_version_id": VID,
                    "parent_item_id": PID,
                    "item_kind": "PRODUCT",
                    "item_type": "K",
                    "item_name": "Deep",
                    "local_quantity": 1,
                }
            )
            _, err, _ = add_calculation_item_v1(client=mock_client, user_id=UID, normalized=n)

        self.assertEqual(err, "ITEM_DEPTH_LIMIT_EXCEEDED")

    def test_reject_version_not_draft(self):
        mock_client = MagicMock()
        with patch(
            "services.module01_calculation_items_service._table_fetch_single",
            side_effect=[
                {"id": CID, "created_by_user_id": UID},
                {"id": VID, "calculation_id": CID, "status": "LOCKED"},
            ],
        ):
            n = _norm(
                {
                    "calculation_id": CID,
                    "calculation_version_id": VID,
                    "item_kind": "CONTAINER",
                    "item_type": "T",
                    "item_name": "N",
                    "local_quantity": 1,
                }
            )
            _, err, _ = add_calculation_item_v1(client=mock_client, user_id=UID, normalized=n)

        self.assertEqual(err, "VERSION_NOT_DRAFT")

    def test_reject_parent_version_mismatch(self):
        mock_client = MagicMock()
        other_vid = "99999999-9999-9999-9999-999999999999"
        with patch(
            "services.module01_calculation_items_service._table_fetch_single",
            side_effect=[
                {"id": CID, "created_by_user_id": UID},
                {"id": VID, "calculation_id": CID, "status": "DRAFT"},
                {
                    "id": PID,
                    "calculation_id": CID,
                    "calculation_version_id": other_vid,
                    "parent_item_id": None,
                    "item_kind": "CONTAINER",
                    "total_quantity": 1.0,
                    "display_index": "1",
                },
            ],
        ):
            n = _norm(
                {
                    "calculation_id": CID,
                    "calculation_version_id": VID,
                    "parent_item_id": PID,
                    "item_kind": "PRODUCT",
                    "item_type": "K",
                    "item_name": "Child",
                    "local_quantity": 1,
                }
            )
            _, err, _ = add_calculation_item_v1(client=mock_client, user_id=UID, normalized=n)

        self.assertEqual(err, "ITEM_PARENT_VERSION_MISMATCH")

    def test_reject_invalid_quantity(self):
        _, err, field = validate_items_add_payload(
            {
                "calculation_id": CID,
                "calculation_version_id": VID,
                "item_kind": "CONTAINER",
                "item_type": "T",
                "item_name": "N",
                "local_quantity": 0,
            }
        )
        self.assertEqual(err, "ITEM_INVALID_QUANTITY")
        self.assertEqual(field, "local_quantity")

    def test_list_items_tree_order(self):
        rows = [
            {
                "id": "c1",
                "calculation_id": CID,
                "calculation_version_id": VID,
                "parent_item_id": "p1",
                "item_kind": "PRODUCT",
                "item_type": "x",
                "item_name": "child",
                "local_quantity": 1.0,
                "total_quantity": 1.0,
                "item_status": "DRAFT",
                "sort_order": 100,
                "display_index": "1.1",
                "payload_json": {},
                "result_summary_json": {},
                "created_at": "a",
                "updated_at": "b",
            },
            {
                "id": "p1",
                "calculation_id": CID,
                "calculation_version_id": VID,
                "parent_item_id": None,
                "item_kind": "CONTAINER",
                "item_type": "x",
                "item_name": "root",
                "local_quantity": 1.0,
                "total_quantity": 1.0,
                "item_status": "DRAFT",
                "sort_order": 100,
                "display_index": "1",
                "payload_json": {},
                "result_summary_json": {},
                "created_at": "a",
                "updated_at": "b",
            },
        ]

        def _table(name: str):
            m = MagicMock()
            if name == "module01_calculation_items":
                m.select.return_value.eq.return_value.execute.return_value = MagicMock(data=rows)
            return m

        mock_client = MagicMock()
        mock_client.table.side_effect = _table

        with patch(
            "services.module01_calculation_items_service._table_fetch_single",
            side_effect=[
                {"id": CID, "created_by_user_id": UID},
                {"id": VID, "calculation_id": CID},
            ],
        ):
            items, err = list_calculation_items_v1(
                client=mock_client,
                user_id=UID,
                calculation_id=CID,
                version_id=VID,
            )

        self.assertIsNone(err)
        assert items is not None
        self.assertEqual([x["id"] for x in items], ["p1", "c1"])
        self.assertEqual(items[0]["display_index"], "1")
        self.assertEqual(items[1]["parent_item_id"], "p1")

    def test_sort_conflict_returns_code(self):
        mock_client = MagicMock()

        def _table(name: str):
            m = MagicMock()
            if name == "module01_calculation_items":

                def _raise(*_a, **_k):
                    raise Exception('duplicate key value violates unique constraint "uq_module01_calculation_items_sibling_sort"')

                m.insert.return_value.execute.side_effect = _raise
            return m

        mock_client.table.side_effect = _table

        with (
            patch(
                "services.module01_calculation_items_service._table_fetch_single",
                side_effect=[
                    {"id": CID, "created_by_user_id": UID},
                    {"id": VID, "calculation_id": CID, "status": "DRAFT"},
                ],
            ),
            patch("services.module01_calculation_items_service._max_sibling_sort_order", return_value=None),
            patch("services.module01_calculation_items_service._count_siblings", return_value=0),
        ):
            n = _norm(
                {
                    "calculation_id": CID,
                    "calculation_version_id": VID,
                    "item_kind": "CONTAINER",
                    "item_type": "T",
                    "item_name": "N",
                    "local_quantity": 1,
                }
            )
            _, err, _ = add_calculation_item_v1(client=mock_client, user_id=UID, normalized=n)

        self.assertEqual(err, "ITEM_SORT_CONFLICT")


class Module01CalculationItemsEndpointTests(unittest.TestCase):
    def test_add_missing_token_returns_auth_error(self):
        response = module01_calculation_items_add(None, {})
        status_code, body = _decode(response)
        self.assertEqual(status_code, 200)
        self.assertEqual(body["status"], "auth_error")
        self.assertEqual(body["error"]["error_code"], "AUTH_MISSING_TOKEN")

    def test_list_missing_token_returns_auth_error(self):
        response = module01_calculation_items_list(
            "not-a-uuid",
            "also-bad",
            None,
        )
        status_code, body = _decode(response)
        self.assertEqual(status_code, 200)
        self.assertEqual(body["status"], "auth_error")
        self.assertEqual(body["error"]["error_code"], "AUTH_MISSING_TOKEN")

    def test_list_invalid_path_uuid_returns_calc_not_found_after_auth(self):
        future = (datetime.now(UTC) + timedelta(hours=1)).isoformat()

        def _fetch_single(_client, table: str, *, select: str, filters: dict):
            if table == "module01_user_sessions":
                return {
                    "user_id": UID,
                    "terminal_id": "10578103-6c44-4eaf-a825-402d1fc5f7a6",
                    "expires_at": future,
                    "revoked_at": None,
                }
            if table == "module01_users":
                return {"id": UID, "status": "ACTIVE"}
            if table == "module01_user_terminals":
                return {
                    "id": "10578103-6c44-4eaf-a825-402d1fc5f7a6",
                    "user_id": UID,
                    "status": "ACTIVE",
                }
            return None

        mock_client = MagicMock()
        with (
            patch.dict(
                "os.environ",
                {"SUPABASE_URL": "https://x.co", "SUPABASE_SERVICE_ROLE_KEY": "k", "AUTH_SESSION_TTL_HOURS": "12"},
                clear=False,
            ),
            patch("main._auth_get_supabase_client", return_value=mock_client),
            patch("main._auth_fetch_single", side_effect=_fetch_single),
        ):
            response = module01_calculation_items_list("not-a-uuid", VID, "Bearer tok")

        _, body = _decode(response)
        self.assertEqual(body["error"]["error_code"], "CALCULATION_NOT_FOUND")

    def test_add_success_envelope(self):
        future = (datetime.now(UTC) + timedelta(hours=1)).isoformat()

        def _fetch_single(_client, table: str, *, select: str, filters: dict):
            if table == "module01_user_sessions":
                return {
                    "user_id": UID,
                    "terminal_id": "10578103-6c44-4eaf-a825-402d1fc5f7a6",
                    "expires_at": future,
                    "revoked_at": None,
                }
            if table == "module01_users":
                return {"id": UID, "status": "ACTIVE"}
            if table == "module01_user_terminals":
                return {
                    "id": "10578103-6c44-4eaf-a825-402d1fc5f7a6",
                    "user_id": UID,
                    "status": "ACTIVE",
                }
            return None

        mock_client = MagicMock()
        item_payload = {"item": {"id": PID, "display_index": "1", "total_quantity": 1.0}}

        with (
            patch.dict(
                "os.environ",
                {"SUPABASE_URL": "https://x.co", "SUPABASE_SERVICE_ROLE_KEY": "k", "AUTH_SESSION_TTL_HOURS": "12"},
                clear=False,
            ),
            patch("main._auth_get_supabase_client", return_value=mock_client),
            patch("main._auth_fetch_single", side_effect=_fetch_single),
            patch("main.add_calculation_item_v1", return_value=(item_payload, None, None)),
        ):
            response = module01_calculation_items_add(
                "Bearer tok",
                {
                    "calculation_id": CID,
                    "calculation_version_id": VID,
                    "item_kind": "CONTAINER",
                    "item_type": "t",
                    "item_name": "n",
                    "local_quantity": 1,
                },
            )

        _, body = _decode(response)
        self.assertEqual(body["status"], "success")
        self.assertEqual(body["data"]["item"]["id"], PID)


if __name__ == "__main__":
    unittest.main()
