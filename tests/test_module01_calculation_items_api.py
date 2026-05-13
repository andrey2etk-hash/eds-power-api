"""Tests for Module 01 calculation items API V1 (add + list + delete)."""

import json
import unittest
from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock, patch

from main import (
    module01_calculation_items_add,
    module01_calculation_items_delete,
    module01_calculation_items_list,
)
from services.module01_calculation_items_service import (
    add_calculation_item_v1,
    delete_calculation_item_v1,
    is_child_only_item_type,
    list_calculation_items_v1,
    parent_required_for_child_item_message,
    validate_items_add_payload,
    validate_items_delete_payload,
)

UID = "09ca45e0-56f7-414d-85ff-6f69bfdab621"
CID = "11111111-1111-1111-1111-111111111111"
VID = "22222222-2222-2222-2222-222222222222"
PID = "33333333-3333-3333-3333-333333333333"
LEAF_ID = "66666666-6666-6666-6666-666666666666"
OTHER_VID = "99999999-9999-9999-9999-999999999999"


def _decode(response):
    return response.status_code, json.loads(response.body.decode("utf-8"))


def _norm(body: dict):
    n, e, f = validate_items_add_payload(body)
    assert e is None and n is not None
    return n


class Module01CalculationItemsServiceTests(unittest.TestCase):
    def test_strict_reject_child_only_types_helpers(self):
        for t in ("KZO_CELL", "kzo_cell", "KZO", "SHOS_CABINET", "SHCHO", "SERVICE_ITEM"):
            self.assertTrue(is_child_only_item_type(t), t)
        self.assertFalse(is_child_only_item_type("MEDIUM_VOLTAGE_SWITCHGEAR_10KV"))
        self.assertFalse(is_child_only_item_type("KTP"))
        msg_kzo = parent_required_for_child_item_message("KZO_CELL")
        self.assertIn("KZO_CELL cannot be created as root", msg_kzo)
        self.assertIn("SHOS_CABINET cannot be created as root", parent_required_for_child_item_message("SHCHO"))
        self.assertIn("SERVICE_ITEM cannot be created as root", parent_required_for_child_item_message("SERVICE_ITEM"))

    def test_valid_root_parent_mv_10kv(self):
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
                            "item_type": "MEDIUM_VOLTAGE_SWITCHGEAR_10KV",
                            "item_name": "Root",
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
                    "item_type": "MEDIUM_VOLTAGE_SWITCHGEAR_10KV",
                    "item_name": "Root",
                    "local_quantity": 1,
                }
            )
            data, err, _ = add_calculation_item_v1(client=mock_client, user_id=UID, normalized=n)

        self.assertIsNone(err)
        assert data is not None
        self.assertEqual(data["item"]["item_type"], "MEDIUM_VOLTAGE_SWITCHGEAR_10KV")

    def test_valid_root_parent_ktp(self):
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
                            "item_type": "KTP",
                            "item_name": "KTP root",
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
                    "item_type": "KTP",
                    "item_name": "KTP root",
                    "local_quantity": 1,
                }
            )
            data, err, _ = add_calculation_item_v1(client=mock_client, user_id=UID, normalized=n)

        self.assertIsNone(err)
        assert data is not None
        self.assertEqual(data["item"]["item_type"], "KTP")

    def test_strict_reject_root_kzo_cell(self):
        mock_client = MagicMock()
        with patch(
            "services.module01_calculation_items_service._table_fetch_single",
            side_effect=[
                {"id": CID, "created_by_user_id": UID},
                {"id": VID, "calculation_id": CID, "status": "DRAFT"},
            ],
        ):
            n = _norm(
                {
                    "calculation_id": CID,
                    "calculation_version_id": VID,
                    "parent_item_id": None,
                    "item_kind": "PRODUCT",
                    "item_type": "KZO_CELL",
                    "item_name": "Bad root",
                    "local_quantity": 1,
                }
            )
            _, err, f = add_calculation_item_v1(client=mock_client, user_id=UID, normalized=n)

        self.assertEqual(err, "PARENT_REQUIRED_FOR_CHILD_ITEM")
        self.assertEqual(f, "parent_item_id")
        mock_client.table.assert_not_called()

    def test_strict_reject_root_legacy_kzo(self):
        mock_client = MagicMock()
        with patch(
            "services.module01_calculation_items_service._table_fetch_single",
            side_effect=[
                {"id": CID, "created_by_user_id": UID},
                {"id": VID, "calculation_id": CID, "status": "DRAFT"},
            ],
        ):
            n = _norm(
                {
                    "calculation_id": CID,
                    "calculation_version_id": VID,
                    "parent_item_id": None,
                    "item_kind": "CONTAINER",
                    "item_type": "KZO",
                    "item_name": "Legacy root",
                    "local_quantity": 1,
                }
            )
            _, err, f = add_calculation_item_v1(client=mock_client, user_id=UID, normalized=n)

        self.assertEqual(err, "PARENT_REQUIRED_FOR_CHILD_ITEM")
        self.assertEqual(f, "parent_item_id")

    def test_strict_reject_root_shos_cabinet(self):
        mock_client = MagicMock()
        with patch(
            "services.module01_calculation_items_service._table_fetch_single",
            side_effect=[
                {"id": CID, "created_by_user_id": UID},
                {"id": VID, "calculation_id": CID, "status": "DRAFT"},
            ],
        ):
            n = _norm(
                {
                    "calculation_id": CID,
                    "calculation_version_id": VID,
                    "parent_item_id": None,
                    "item_kind": "PRODUCT",
                    "item_type": "SHOS_CABINET",
                    "item_name": "Bad",
                    "local_quantity": 1,
                }
            )
            _, err, _ = add_calculation_item_v1(client=mock_client, user_id=UID, normalized=n)

        self.assertEqual(err, "PARENT_REQUIRED_FOR_CHILD_ITEM")

    def test_strict_reject_root_shcho_alias(self):
        mock_client = MagicMock()
        with patch(
            "services.module01_calculation_items_service._table_fetch_single",
            side_effect=[
                {"id": CID, "created_by_user_id": UID},
                {"id": VID, "calculation_id": CID, "status": "DRAFT"},
            ],
        ):
            n = _norm(
                {
                    "calculation_id": CID,
                    "calculation_version_id": VID,
                    "parent_item_id": None,
                    "item_kind": "PRODUCT",
                    "item_type": "SHCHO",
                    "item_name": "Bad",
                    "local_quantity": 1,
                }
            )
            _, err, _ = add_calculation_item_v1(client=mock_client, user_id=UID, normalized=n)

        self.assertEqual(err, "PARENT_REQUIRED_FOR_CHILD_ITEM")

    def test_strict_reject_root_service_item(self):
        mock_client = MagicMock()
        with patch(
            "services.module01_calculation_items_service._table_fetch_single",
            side_effect=[
                {"id": CID, "created_by_user_id": UID},
                {"id": VID, "calculation_id": CID, "status": "DRAFT"},
            ],
        ):
            n = _norm(
                {
                    "calculation_id": CID,
                    "calculation_version_id": VID,
                    "parent_item_id": None,
                    "item_kind": "SERVICE",
                    "item_type": "SERVICE_ITEM",
                    "item_name": "Bad",
                    "local_quantity": 1,
                }
            )
            _, err, _ = add_calculation_item_v1(client=mock_client, user_id=UID, normalized=n)

        self.assertEqual(err, "PARENT_REQUIRED_FOR_CHILD_ITEM")

    def test_valid_child_kzo_cell_under_mv_parent(self):
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
                            "item_type": "KZO_CELL",
                            "item_name": "Cell",
                            "local_quantity": 2.0,
                            "total_quantity": 4.0,
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
                        "item_type": "MEDIUM_VOLTAGE_SWITCHGEAR_10KV",
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
                    "item_type": "KZO_CELL",
                    "item_name": "Cell",
                    "local_quantity": 2,
                }
            )
            data, err, _ = add_calculation_item_v1(client=mock_client, user_id=UID, normalized=n)

        self.assertIsNone(err)
        assert data is not None
        self.assertEqual(data["item"]["item_type"], "KZO_CELL")
        self.assertEqual(data["item"]["total_quantity"], 4.0)

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


def _calc_ver_draft():
    return (
        {"id": CID, "created_by_user_id": UID},
        {"id": VID, "calculation_id": CID, "status": "DRAFT"},
    )


def _mock_items_table_for_delete(*, child_check_rows: list, delete_return_rows: list | None):
    """select/eq/eq/limit/execute -> child_check_rows; delete/eq/eq/eq/execute -> delete_return_rows."""
    items_mock = MagicMock()
    sel = items_mock.select.return_value
    sel.eq.return_value.eq.return_value.limit.return_value.execute.return_value = MagicMock(data=child_check_rows)
    delchain = items_mock.delete.return_value
    delchain.eq.return_value.eq.return_value.eq.return_value.execute.return_value = MagicMock(
        data=delete_return_rows or []
    )
    return items_mock


class Module01CalculationItemsDeleteServiceTests(unittest.TestCase):
    def test_validate_delete_payload_invalid_item_id(self):
        _, err, field = validate_items_delete_payload(
            {"calculation_id": CID, "calculation_version_id": VID, "item_id": "not-a-uuid"}
        )
        self.assertEqual(err, "ITEM_DELETE_FAILED")
        self.assertEqual(field, "item_id")

    def test_delete_leaf_success(self):
        item_row = {
            "id": LEAF_ID,
            "calculation_id": CID,
            "calculation_version_id": VID,
            "parent_item_id": PID,
            "display_index": "1.1",
            "item_type": "KZO_CELL",
            "item_name": "Cell",
            "sort_order": 100,
        }
        items_mock = _mock_items_table_for_delete(child_check_rows=[], delete_return_rows=[item_row])
        mock_client = MagicMock()

        def _tbl(name: str):
            if name == "module01_calculation_items":
                return items_mock
            return MagicMock()

        mock_client.table.side_effect = _tbl

        with patch(
            "services.module01_calculation_items_service._table_fetch_single",
            side_effect=[
                _calc_ver_draft()[0],
                _calc_ver_draft()[1],
                item_row,
            ],
        ):
            n, e, _ = validate_items_delete_payload(
                {"calculation_id": CID, "calculation_version_id": VID, "item_id": LEAF_ID}
            )
            self.assertIsNone(e)
            assert n is not None
            data, err, sf = delete_calculation_item_v1(client=mock_client, user_id=UID, normalized=n)

        self.assertIsNone(err)
        assert data is not None
        self.assertEqual(data["deleted_item_id"], LEAF_ID)
        self.assertEqual(data["refresh_required"], True)
        self.assertEqual(data["parent_item_id"], PID)
        self.assertEqual(data["deleted_display_index"], "1.1")
        items_mock.update.assert_not_called()

    def test_delete_empty_root_parent_success(self):
        item_row = {
            "id": PID,
            "calculation_id": CID,
            "calculation_version_id": VID,
            "parent_item_id": None,
            "display_index": "1",
            "item_type": "MEDIUM_VOLTAGE_SWITCHGEAR_10KV",
            "item_name": "Root",
            "sort_order": 100,
        }
        items_mock = _mock_items_table_for_delete(child_check_rows=[], delete_return_rows=[item_row])
        mock_client = MagicMock()

        def _tbl(name: str):
            if name == "module01_calculation_items":
                return items_mock
            return MagicMock()

        mock_client.table.side_effect = _tbl

        with patch(
            "services.module01_calculation_items_service._table_fetch_single",
            side_effect=[_calc_ver_draft()[0], _calc_ver_draft()[1], item_row],
        ):
            n, _, _ = validate_items_delete_payload(
                {"calculation_id": CID, "calculation_version_id": VID, "item_id": PID}
            )
            assert n is not None
            data, err, _ = delete_calculation_item_v1(client=mock_client, user_id=UID, normalized=n)

        self.assertIsNone(err)
        assert data is not None
        self.assertIsNone(data["parent_item_id"])

    def test_delete_parent_with_children_rejected(self):
        parent_row = {
            "id": PID,
            "calculation_id": CID,
            "calculation_version_id": VID,
            "parent_item_id": None,
            "display_index": "1",
            "item_type": "MEDIUM_VOLTAGE_SWITCHGEAR_10KV",
            "item_name": "Root",
            "sort_order": 100,
        }
        items_mock = _mock_items_table_for_delete(child_check_rows=[{"id": LEAF_ID}], delete_return_rows=[])
        mock_client = MagicMock()

        def _tbl(name: str):
            if name == "module01_calculation_items":
                return items_mock
            return MagicMock()

        mock_client.table.side_effect = _tbl

        with patch(
            "services.module01_calculation_items_service._table_fetch_single",
            side_effect=[_calc_ver_draft()[0], _calc_ver_draft()[1], parent_row],
        ):
            n, _, _ = validate_items_delete_payload(
                {"calculation_id": CID, "calculation_version_id": VID, "item_id": PID}
            )
            assert n is not None
            _, err, sf = delete_calculation_item_v1(client=mock_client, user_id=UID, normalized=n)

        self.assertEqual(err, "ITEM_HAS_CHILDREN")
        self.assertEqual(sf, "item_id")
        items_mock.delete.assert_not_called()

    def test_delete_version_not_draft(self):
        item_row = {
            "id": LEAF_ID,
            "calculation_id": CID,
            "calculation_version_id": VID,
            "parent_item_id": PID,
            "display_index": "1.1",
            "item_type": "KZO_CELL",
            "item_name": "Cell",
            "sort_order": 100,
        }
        mock_client = MagicMock()
        with patch(
            "services.module01_calculation_items_service._table_fetch_single",
            side_effect=[
                {"id": CID, "created_by_user_id": UID},
                {"id": VID, "calculation_id": CID, "status": "LOCKED"},
                item_row,
            ],
        ):
            n, _, _ = validate_items_delete_payload(
                {"calculation_id": CID, "calculation_version_id": VID, "item_id": LEAF_ID}
            )
            assert n is not None
            _, err, _ = delete_calculation_item_v1(client=mock_client, user_id=UID, normalized=n)

        self.assertEqual(err, "VERSION_NOT_DRAFT")
        mock_client.table.assert_not_called()

    def test_delete_item_wrong_version_privacy_not_found(self):
        item_row = {
            "id": LEAF_ID,
            "calculation_id": CID,
            "calculation_version_id": OTHER_VID,
            "parent_item_id": None,
            "display_index": "1",
            "item_type": "KZO_CELL",
            "item_name": "x",
            "sort_order": 100,
        }
        mock_client = MagicMock()
        with patch(
            "services.module01_calculation_items_service._table_fetch_single",
            side_effect=[_calc_ver_draft()[0], _calc_ver_draft()[1], item_row],
        ):
            n, _, _ = validate_items_delete_payload(
                {"calculation_id": CID, "calculation_version_id": VID, "item_id": LEAF_ID}
            )
            assert n is not None
            _, err, sf = delete_calculation_item_v1(client=mock_client, user_id=UID, normalized=n)

        self.assertEqual(err, "ITEM_NOT_FOUND")
        self.assertEqual(sf, "item_id")
        mock_client.table.assert_not_called()

    def test_delete_same_item_twice(self):
        item_row = {
            "id": LEAF_ID,
            "calculation_id": CID,
            "calculation_version_id": VID,
            "parent_item_id": PID,
            "display_index": "1.1",
            "item_type": "KZO_CELL",
            "item_name": "Cell",
            "sort_order": 100,
        }

        def _make_client():
            im = _mock_items_table_for_delete(child_check_rows=[], delete_return_rows=[item_row])
            mc = MagicMock()

            def _tbl(name: str):
                if name == "module01_calculation_items":
                    return im
                return MagicMock()

            mc.table.side_effect = _tbl
            return mc

        n, _, _ = validate_items_delete_payload(
            {"calculation_id": CID, "calculation_version_id": VID, "item_id": LEAF_ID}
        )
        assert n is not None

        client1 = _make_client()
        with patch(
            "services.module01_calculation_items_service._table_fetch_single",
            side_effect=[_calc_ver_draft()[0], _calc_ver_draft()[1], item_row],
        ):
            data1, err1, _ = delete_calculation_item_v1(client=client1, user_id=UID, normalized=n)
        self.assertIsNone(err1)
        assert data1 is not None

        client2 = _make_client()
        with patch(
            "services.module01_calculation_items_service._table_fetch_single",
            side_effect=[_calc_ver_draft()[0], _calc_ver_draft()[1], None],
        ):
            _, err2, _ = delete_calculation_item_v1(client=client2, user_id=UID, normalized=n)
        self.assertEqual(err2, "ITEM_NOT_FOUND")

    def test_delete_legacy_orphan_root_kzo_no_children(self):
        item_row = {
            "id": LEAF_ID,
            "calculation_id": CID,
            "calculation_version_id": VID,
            "parent_item_id": None,
            "display_index": "1",
            "item_type": "KZO",
            "item_name": "Legacy",
            "sort_order": 100,
        }
        items_mock = _mock_items_table_for_delete(child_check_rows=[], delete_return_rows=[item_row])
        mock_client = MagicMock()

        def _tbl(name: str):
            if name == "module01_calculation_items":
                return items_mock
            return MagicMock()

        mock_client.table.side_effect = _tbl

        with patch(
            "services.module01_calculation_items_service._table_fetch_single",
            side_effect=[_calc_ver_draft()[0], _calc_ver_draft()[1], item_row],
        ):
            n, _, _ = validate_items_delete_payload(
                {"calculation_id": CID, "calculation_version_id": VID, "item_id": LEAF_ID}
            )
            assert n is not None
            data, err, _ = delete_calculation_item_v1(client=mock_client, user_id=UID, normalized=n)

        self.assertIsNone(err)
        assert data is not None
        self.assertEqual(data["deleted_item_type"], "KZO")

    def test_no_reindex_side_effects_no_update_calls(self):
        victim = {
            "id": LEAF_ID,
            "calculation_id": CID,
            "calculation_version_id": VID,
            "parent_item_id": None,
            "display_index": "2",
            "item_type": "PRODUCT",
            "item_name": "P2",
            "sort_order": 101,
        }
        items_mock = _mock_items_table_for_delete(child_check_rows=[], delete_return_rows=[victim])
        mock_client = MagicMock()

        def _tbl(name: str):
            if name == "module01_calculation_items":
                return items_mock
            return MagicMock()

        mock_client.table.side_effect = _tbl

        with patch(
            "services.module01_calculation_items_service._table_fetch_single",
            side_effect=[_calc_ver_draft()[0], _calc_ver_draft()[1], victim],
        ):
            n, _, _ = validate_items_delete_payload(
                {"calculation_id": CID, "calculation_version_id": VID, "item_id": LEAF_ID}
            )
            assert n is not None
            _, err, _ = delete_calculation_item_v1(client=mock_client, user_id=UID, normalized=n)

        self.assertIsNone(err)
        items_mock.update.assert_not_called()


class Module01CalculationItemsDeleteEndpointTests(unittest.TestCase):
    def test_delete_success_envelope(self):
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

        payload = {
            "deleted_item_id": LEAF_ID,
            "calculation_id": CID,
            "calculation_version_id": VID,
            "parent_item_id": PID,
            "deleted_display_index": "1.1",
            "refresh_required": True,
        }
        with (
            patch.dict(
                "os.environ",
                {"SUPABASE_URL": "https://x.co", "SUPABASE_SERVICE_ROLE_KEY": "k", "AUTH_SESSION_TTL_HOURS": "12"},
                clear=False,
            ),
            patch("main._auth_get_supabase_client", return_value=MagicMock()),
            patch("main._auth_fetch_single", side_effect=_fetch_single),
            patch("main.delete_calculation_item_v1", return_value=(payload, None, None)),
        ):
            response = module01_calculation_items_delete(
                "Bearer tok",
                {
                    "calculation_id": CID,
                    "calculation_version_id": VID,
                    "item_id": LEAF_ID,
                },
            )

        _, body = _decode(response)
        self.assertEqual(body["status"], "success")
        self.assertEqual(body["data"]["deleted_item_id"], LEAF_ID)
        self.assertTrue(body["data"]["refresh_required"])
        self.assertIsNone(body["error"])

    def test_delete_missing_token_returns_auth_error(self):
        response = module01_calculation_items_delete(None, {})
        _, body = _decode(response)
        self.assertEqual(body["status"], "auth_error")
        self.assertEqual(body["error"]["error_code"], "AUTH_MISSING_TOKEN")

    def test_delete_item_has_children_envelope(self):
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

        with (
            patch.dict(
                "os.environ",
                {"SUPABASE_URL": "https://x.co", "SUPABASE_SERVICE_ROLE_KEY": "k", "AUTH_SESSION_TTL_HOURS": "12"},
                clear=False,
            ),
            patch("main._auth_get_supabase_client", return_value=MagicMock()),
            patch("main._auth_fetch_single", side_effect=_fetch_single),
            patch(
                "main.delete_calculation_item_v1",
                return_value=(None, "ITEM_HAS_CHILDREN", "item_id"),
            ),
        ):
            response = module01_calculation_items_delete(
                "Bearer tok",
                {
                    "calculation_id": CID,
                    "calculation_version_id": VID,
                    "item_id": PID,
                },
            )

        _, body = _decode(response)
        self.assertEqual(body["status"], "error")
        self.assertEqual(body["error"]["error_code"], "ITEM_HAS_CHILDREN")
        self.assertEqual(body["error"]["source_field"], "item_id")
        self.assertIn("Delete children first", body["error"]["message"])


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

    def test_add_parent_required_error_message_on_endpoint(self):
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
            patch(
                "main.add_calculation_item_v1",
                return_value=(None, "PARENT_REQUIRED_FOR_CHILD_ITEM", "parent_item_id"),
            ),
        ):
            response = module01_calculation_items_add(
                "Bearer tok",
                {
                    "calculation_id": CID,
                    "calculation_version_id": VID,
                    "item_kind": "PRODUCT",
                    "item_type": "SHCHO",
                    "item_name": "x",
                    "local_quantity": 1,
                },
            )

        _, body = _decode(response)
        self.assertEqual(body["status"], "error")
        self.assertEqual(body["error"]["error_code"], "PARENT_REQUIRED_FOR_CHILD_ITEM")
        self.assertEqual(body["error"]["source_field"], "parent_item_id")
        self.assertIn("SHOS_CABINET cannot be created as root", body["error"]["message"])
        self.assertEqual(body["error"]["module"], "MODULE_01")

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
