import inspect
import json
import unittest
from copy import deepcopy
from uuid import uuid4
from unittest.mock import patch

import main


def _valid_request(**overrides):
    payload = {
        "request_id": str(uuid4()),
        "client_type": "GAS_DEMO",
        "mode": "MODULE_01_DEMO",
        "product_type": "KZO",
        "demo_id": "MODULE_01_KZO_DEMO_001",
        "requested_output_blocks": [
            "demo_status",
            "status_flow",
            "node_results",
            "fastener_decisions",
            "kit_issue_lines",
            "traceability",
            "boundary_note",
            "management_summary",
            "registry_versions",
        ],
        "operator_context": {
            "sheet_name": "Stage4A_MVP",
            "operator_id": "DEMO_OPERATOR_001",
        },
    }
    payload.update(overrides)
    return payload


def _run_endpoint(payload: dict):
    response = main.run_module_01_demo_api(payload)
    body = json.loads(response.body.decode("utf-8"))
    return response, body


class Module01DemoApiEndpointTests(unittest.TestCase):
    def test_valid_request_returns_success_and_header(self):
        response, body = _run_endpoint(_valid_request())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("X-EDS-Power-Mode"), "DEMO")
        self.assertEqual(body["status"], "success")
        self.assertEqual(body["data"]["demo_id"], "MODULE_01_KZO_DEMO_001")
        self.assertTrue(body["data"]["management_summary"])
        self.assertTrue(body["data"]["boundary_note"])

    def test_invalid_request_id_rejects(self):
        _, body = _run_endpoint(_valid_request(request_id="invalid"))
        self.assertEqual(body["status"], "error")
        self.assertEqual(body["error"]["error_code"], "ERR_INVALID_REQUEST_ID")

    def test_missing_request_id_rejects(self):
        req = _valid_request()
        del req["request_id"]
        response, body = _run_endpoint(req)
        self.assertEqual(body["status"], "error")
        self.assertEqual(body["error"]["error_code"], "ERR_INVALID_REQUEST_ID")
        self.assertEqual(response.headers.get("X-EDS-Power-Mode"), "DEMO")

    def test_missing_client_type_rejects_with_specific_code(self):
        req = _valid_request()
        del req["client_type"]
        _, body = _run_endpoint(req)
        self.assertEqual(body["error"]["error_code"], "ERR_INVALID_CLIENT_TYPE")

    def test_missing_mode_rejects_with_specific_code(self):
        req = _valid_request()
        del req["mode"]
        _, body = _run_endpoint(req)
        self.assertEqual(body["error"]["error_code"], "ERR_INVALID_MODE")

    def test_missing_product_type_rejects_with_specific_code(self):
        req = _valid_request()
        del req["product_type"]
        _, body = _run_endpoint(req)
        self.assertEqual(body["error"]["error_code"], "ERR_INVALID_PRODUCT_TYPE")

    def test_missing_demo_id_rejects_with_specific_code(self):
        req = _valid_request()
        del req["demo_id"]
        _, body = _run_endpoint(req)
        self.assertEqual(body["error"]["error_code"], "ERR_INVALID_DEMO_ID")

    def test_invalid_client_type_rejects(self):
        _, body = _run_endpoint(_valid_request(client_type="WEB"))
        self.assertEqual(body["error"]["error_code"], "ERR_INVALID_CLIENT_TYPE")

    def test_invalid_mode_rejects(self):
        _, body = _run_endpoint(_valid_request(mode="PROD"))
        self.assertEqual(body["error"]["error_code"], "ERR_INVALID_MODE")

    def test_invalid_product_type_rejects(self):
        _, body = _run_endpoint(_valid_request(product_type="ABC"))
        self.assertEqual(body["error"]["error_code"], "ERR_INVALID_PRODUCT_TYPE")

    def test_invalid_demo_id_rejects(self):
        _, body = _run_endpoint(_valid_request(demo_id="OTHER_DEMO"))
        self.assertEqual(body["error"]["error_code"], "ERR_INVALID_DEMO_ID")

    def test_requested_output_blocks_unknown_rejects(self):
        req = _valid_request(requested_output_blocks=["node_results", "unknown_block"])
        _, body = _run_endpoint(req)
        self.assertEqual(body["error"]["error_code"], "ERR_UNSUPPORTED_OUTPUT_BLOCK")

    def test_requested_output_blocks_empty_rejects(self):
        _, body = _run_endpoint(_valid_request(requested_output_blocks=[]))
        self.assertEqual(body["error"]["error_code"], "ERR_UNSUPPORTED_OUTPUT_BLOCK")

    def test_forbidden_pricing_flag_rejects(self):
        response, body = _run_endpoint(_valid_request(pricing=True))
        self.assertEqual(body["error"]["error_code"], "ERR_FORBIDDEN_FLAG")
        self.assertEqual(response.headers.get("X-EDS-Power-Mode"), "DEMO")

    def test_forbidden_procurement_flag_rejects(self):
        _, body = _run_endpoint(_valid_request(procurement=True))
        self.assertEqual(body["error"]["error_code"], "ERR_FORBIDDEN_FLAG")

    def test_forbidden_warehouse_erp_cad_db_flags_reject(self):
        for forbidden_key in ("warehouse", "erp", "cad", "db_write", "supabase_write", "production"):
            req = _valid_request(**{forbidden_key: True})
            _, body = _run_endpoint(req)
            self.assertEqual(body["error"]["error_code"], "ERR_FORBIDDEN_FLAG", msg=forbidden_key)

    def test_response_contains_fastener_decisions_rows(self):
        _, body = _run_endpoint(_valid_request())
        rows = body["data"]["fastener_decisions"]
        self.assertTrue(any(r["connection_group"] == "BUSBAR_SIDE_CONNECTIONS" and r["candidate_bolt"] == "DEMO_BOLT_M12X45" and r["decision"] == "REJECTED" for r in rows))
        self.assertTrue(any(r["connection_group"] == "BUSBAR_SIDE_CONNECTIONS" and r["candidate_bolt"] == "DEMO_BOLT_M12X55" and r["decision"] == "SELECTED" for r in rows))
        self.assertTrue(any(r["connection_group"] == "EQUIPMENT_SIDE_CONNECTIONS" and r["candidate_bolt"] == "DEMO_BOLT_M12X45" and r["decision"] == "SELECTED" for r in rows))

    def test_fastener_decisions_match_runner_output_without_api_reconstruction(self):
        demo_data = main._run_module_01_demo_in_memory()
        with patch("main._run_module_01_demo_in_memory", return_value=demo_data):
            _, body = _run_endpoint(_valid_request())
        self.assertEqual(body["data"]["fastener_decisions"], demo_data["fastener_decisions"])
        self.assertFalse(hasattr(main, "_build_fastener_decision_rows"))

    def test_response_contains_expected_kit_issue_totals(self):
        _, body = _run_endpoint(_valid_request())
        lines = body["data"]["kit_issue_lines"]
        totals = {line["item_id"]: line["total_quantity"] for line in lines}
        self.assertEqual(totals["DEMO_BOLT_M12X55"], 6.0)
        self.assertEqual(totals["DEMO_BOLT_M12X45"], 6.0)
        self.assertEqual(totals["DEMO_NUT_M12"], 12.0)
        self.assertEqual(totals["DEMO_FLAT_WASHER_M12"], 24.0)
        self.assertEqual(totals["DEMO_DISC_SPRING_WASHER_M12"], 12.0)

    def test_response_contains_traceability_and_registry_versions(self):
        _, body = _run_endpoint(_valid_request())
        trace = body["data"]["traceability"]
        self.assertTrue(trace["source_node_ids"])
        self.assertTrue(trace["source_line_ids"])
        self.assertTrue(trace["traceability_refs"])
        self.assertIn("registry_versions", body["data"])

    def test_response_not_final_erp_or_procurement_or_pricing(self):
        _, body = _run_endpoint(_valid_request())
        blob = str(body).lower()
        self.assertNotIn("erp_posting", blob)
        self.assertNotIn("warehouse_reservation", blob)
        self.assertNotIn("purchase_request", blob)
        self.assertNotIn("stock_movement", blob)
        self.assertNotIn("supplier_selection", blob)

    def test_api_function_has_no_db_supabase_calls(self):
        source = inspect.getsource(main.run_module_01_demo_api)
        self.assertNotIn("insert_snapshot_row", source)
        self.assertNotIn("find_snapshot_by_request_id", source)
        self.assertNotIn("validate_kzo_mvp_snapshot_v1", source)

    def test_api_runner_import_is_not_from_tests_package(self):
        source = inspect.getsource(main._run_module_01_demo_in_memory)
        self.assertIn("src.runners.module_01_demo_runner", source)
        self.assertNotIn("tests.demo_runner_module_01", source)

    def test_deterministic_response_for_same_input(self):
        fixed_request_id = str(uuid4())
        req = _valid_request(request_id=fixed_request_id)
        _, first = _run_endpoint(deepcopy(req))
        _, second = _run_endpoint(deepcopy(req))
        self.assertEqual(first["status"], second["status"])
        self.assertEqual(first["data"], second["data"])
        self.assertEqual(first["metadata"]["request_id"], second["metadata"]["request_id"])
        self.assertEqual(first["metadata"]["demo_version"], second["metadata"]["demo_version"])

    def test_management_summary_missing_guard(self):
        demo_data = main._run_module_01_demo_in_memory()
        demo_data["management_summary"] = ""
        with patch("main._run_module_01_demo_in_memory", return_value=demo_data):
            _, body = _run_endpoint(_valid_request())
        self.assertEqual(body["status"], "error")
        self.assertEqual(body["error"]["error_code"], "ERR_LOGIC_CHAIN_FAILURE")

    def test_boundary_note_contains_all_required_markers(self):
        _, body = _run_endpoint(_valid_request())
        boundary = body["data"]["boundary_note"].lower()
        for marker in (
            "local demo only",
            "not production data",
            "not final erp bom",
            "not procurement",
            "not warehouse",
            "not erp/1c",
            "not pricing",
            "not cad",
        ):
            self.assertIn(marker, boundary)

    def test_boundary_note_missing_marker_rejects(self):
        demo_data = main._run_module_01_demo_in_memory()
        demo_data["boundary_note"] = "Local demo only. Not final ERP BOM."
        with patch("main._run_module_01_demo_in_memory", return_value=demo_data):
            _, body = _run_endpoint(_valid_request())
        self.assertEqual(body["status"], "error")
        self.assertEqual(body["error"]["error_code"], "ERR_BOUNDARY_VIOLATION")

    def test_demo_v1_present_in_metadata_and_registry_versions(self):
        _, body = _run_endpoint(_valid_request())
        self.assertEqual(body["metadata"]["demo_version"], "demo_v1")
        self.assertIn("demo_v1", str(body["data"]["registry_versions"]))


if __name__ == "__main__":
    unittest.main()
