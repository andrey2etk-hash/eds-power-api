"""Unit tests for services/module01_calculations_service.py."""

import unittest
from unittest.mock import MagicMock, patch

from services.module01_calculations_service import (
    build_structured_notes_v1,
    create_calculation_v1,
    validate_create_payload,
)


class Module01CalculationsServiceTests(unittest.TestCase):
    def test_structured_notes_v1(self):
        n = build_structured_notes_v1(product_type="KZO", comment="c", external_reference="r")
        self.assertIn("EDS_POWER_CALC_NOTES_V1", n)
        self.assertIn("PRODUCT_TYPE: KZO", n)
        self.assertIn("EXTERNAL_REFERENCE: r", n)
        self.assertIn("COMMENT: c", n)

    def test_validate_ok(self):
        body, err, _ = validate_create_payload(
            {
                "source_client": "GAS_TERMINAL_V1",
                "terminal_id": "t1",
                "spreadsheet_id": "s1",
                "payload": {
                    "calculation_title": " Title ",
                    "potential_customer": " P ",
                    "product_type": "KZO",
                },
            }
        )
        self.assertIsNone(err)
        assert body is not None
        self.assertEqual(body["payload"]["calculation_title"], "Title")

    def test_validate_missing_customer(self):
        _, err, field = validate_create_payload(
            {
                "source_client": "GAS_TERMINAL_V1",
                "terminal_id": "t1",
                "spreadsheet_id": "s1",
                "payload": {"calculation_title": "T", "product_type": "KZO"},
            }
        )
        self.assertEqual(err, "MODULE01_CREATE_INVALID_PAYLOAD")
        self.assertEqual(field, "potential_customer")

    def test_create_success_mock_client(self):
        calc_insert = MagicMock()
        calc_insert.data = [{"id": "calc-uuid-1"}]
        ver_insert = MagicMock()
        ver_insert.data = [{"id": "ver-uuid-1"}]
        hist_insert = MagicMock()
        hist_insert.data = [{"id": "h1"}]

        fetch_after = {
            "id": "calc-uuid-1",
            "calculation_base_number": "202601011200",
            "title": "T",
            "potential_customer": "P",
            "current_status": "DRAFT",
            "created_at": "2026-01-01T12:00:00+00:00",
        }

        calc_calls = {"n": 0}

        def _table(name: str):
            m = MagicMock()
            if name == "module01_calculations":
                if calc_calls["n"] == 0:
                    calc_calls["n"] += 1
                    ins = MagicMock()
                    ins.execute.return_value = calc_insert
                    m.insert.return_value = ins
                else:
                    sel = MagicMock()
                    sel.eq.return_value.limit.return_value.execute.return_value = MagicMock(data=[fetch_after])
                    m.select.return_value = sel
            elif name == "module01_calculation_versions":
                ins = MagicMock()
                ins.execute.return_value = ver_insert
                m.insert.return_value = ins
            elif name == "module01_calculation_status_history":
                ins = MagicMock()
                ins.execute.return_value = hist_insert
                m.insert.return_value = ins
            return m

        client = MagicMock()
        client.table.side_effect = _table

        norm = {
            "source_client": "GAS_TERMINAL_V1",
            "terminal_id": "term-1",
            "spreadsheet_id": "spread-1",
            "payload": {
                "calculation_title": "T",
                "potential_customer": "P",
                "product_type": "KZO",
                "comment": "",
                "external_reference": "",
            },
            "_notes_v1": build_structured_notes_v1(product_type="KZO", comment=None, external_reference=None),
        }

        with (
            patch(
                "services.module01_calculations_service.verify_terminal_spreadsheet",
                return_value=True,
            ),
            patch(
                "services.module01_calculations_service.user_has_create_calculation_permission",
                return_value=True,
            ),
            patch(
                "services.module01_calculations_service._utc_base_number",
                return_value="202601011200",
            ),
        ):
            data, err = create_calculation_v1(
                client=client,
                user_id="u1",
                session_terminal_id="term-1",
                normalized=norm,
                request_id="00000000-0000-0000-0000-000000000099",
            )

        self.assertIsNone(err)
        assert data is not None
        self.assertEqual(data["calculation"]["status"], "DRAFT")
        self.assertEqual(data["calculation"]["product_type"], "KZO")
        self.assertEqual(len(data["calculation"]["calculation_base_number"]), 12)
        self.assertIn("sidebar_update", data)


if __name__ == "__main__":
    unittest.main()
