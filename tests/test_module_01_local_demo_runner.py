import inspect
import sys
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TESTS_DIR.parent
for path_value in (str(PROJECT_ROOT), str(TESTS_DIR)):
    if path_value not in sys.path:
        sys.path.insert(0, path_value)

import demo_runner_module_01 as demo_runner


class Module01LocalDemoRunnerTests(unittest.TestCase):
    def test_runner_completes_with_pass(self):
        result = demo_runner.run_module_01_local_demo(write_output=False)
        self.assertEqual(result["status"], "PASS")

    def test_status_flow_contains_all_required_pass_steps(self):
        result = demo_runner.run_module_01_local_demo(write_output=False)
        for step_key in ("DOC36", "DOC37_S1", "DOC37_S2", "DOC38_S1"):
            self.assertIn(step_key, result["status_flow"])
            self.assertEqual(result["status_flow"][step_key], "PASS")

    def test_node_lengths_match_expected(self):
        result = demo_runner.run_module_01_local_demo(write_output=False)
        self.assertEqual(result["node_results"]["KZO_DEMO_NODE_A"]["total_busbar_length_mm"], 1290)
        self.assertEqual(result["node_results"]["KZO_DEMO_NODE_B"]["total_busbar_length_mm"], 1200)

    def test_selected_bolts_match_expected(self):
        result = demo_runner.run_module_01_local_demo(write_output=False)
        rows = result["fastener_decisions"]
        for node_id in ("KZO_DEMO_NODE_A", "KZO_DEMO_NODE_B"):
            self.assertTrue(
                any(
                    row["node"] == node_id
                    and row["connection_group"] == "BUSBAR_SIDE_CONNECTIONS"
                    and row["candidate_bolt"] == "DEMO_BOLT_M12X55"
                    and row["decision"] == "SELECTED"
                    for row in rows
                )
            )
            self.assertTrue(
                any(
                    row["node"] == node_id
                    and row["connection_group"] == "EQUIPMENT_SIDE_CONNECTIONS"
                    and row["candidate_bolt"] == "DEMO_BOLT_M12X45"
                    and row["decision"] == "SELECTED"
                    for row in rows
                )
            )

    def test_doc38_totals_match_expected(self):
        result = demo_runner.run_module_01_local_demo(write_output=False)
        totals = {line["item_id"]: line["total_quantity"] for line in result["kit_issue_lines"]}
        self.assertDictEqual(
            totals,
            {
                "DEMO_BOLT_M12X55": 6.0,
                "DEMO_BOLT_M12X45": 6.0,
                "DEMO_NUT_M12": 12.0,
                "DEMO_FLAT_WASHER_M12": 24.0,
                "DEMO_DISC_SPRING_WASHER_M12": 12.0,
            },
        )

    def test_registry_versions_are_demo_v1(self):
        result = demo_runner.run_module_01_local_demo(write_output=False)

        versions = []

        def collect(node):
            if isinstance(node, dict):
                for key, value in node.items():
                    if key == "registry_version" or key.endswith("_registry_version"):
                        versions.append(value)
                    collect(value)
            elif isinstance(node, list):
                for item in node:
                    collect(item)

        collect(result["registry_versions"])
        collect(result["kit_issue_lines"])
        self.assertTrue(versions)
        self.assertTrue(all(version == "demo_v1" for version in versions))

    def test_source_line_ids_and_traceability_refs_preserved(self):
        result = demo_runner.run_module_01_local_demo(write_output=False)
        self.assertEqual(len(result["source_line_ids"]), 10)
        self.assertEqual(len(result["traceability_refs"]), 10)
        self.assertEqual(len(set(result["source_line_ids"])), 10)
        self.assertEqual(len(set(result["traceability_refs"])), 10)

    def test_optional_backup_fixture_excluded_from_main_flow(self):
        result = demo_runner.run_module_01_local_demo(write_output=False)
        self.assertFalse(result["optional_backup_included_in_main_flow"])
        self.assertNotIn("KZO_DEMO_NODE_BACKUP_INCOMPLETE", result["source_node_ids"])

    def test_output_not_final_erp_bom(self):
        result = demo_runner.run_module_01_local_demo(write_output=False)
        lower_blob = str(result).lower()
        self.assertIn("not final erp bom", result["management_summary"].lower())
        self.assertIn("not final erp bom", result["boundary_note"].lower())
        self.assertIn("not production data", result["boundary_note"].lower())
        self.assertIn("not pricing", result["boundary_note"].lower())
        self.assertIn("not cad", result["boundary_note"].lower())
        self.assertNotIn("warehouse_movement", lower_blob)
        self.assertNotIn("purchase_request", lower_blob)
        self.assertNotIn("erp_posting", lower_blob)
        self.assertNotIn("price", lower_blob)

    def test_no_api_gas_db_access(self):
        source = inspect.getsource(demo_runner)
        self.assertNotIn("requests.", source)
        self.assertNotIn("sqlalchemy", source)
        self.assertNotIn("supabase", source)
        self.assertNotIn("googleapiclient", source)

    def test_audit_trail_captured(self):
        result = demo_runner.run_module_01_local_demo(write_output=False)
        self.assertTrue(len(result["audit_trail"]) >= 4)
        self.assertTrue(any(step["step"] == "DOC36" for step in result["audit_trail"]))
        self.assertTrue(any(step["step"] == "DOC38_S1" for step in result["audit_trail"]))

    def test_deep_copy_guard_effective(self):
        first = demo_runner.run_module_01_local_demo(write_output=False)
        second = demo_runner.run_module_01_local_demo(write_output=False)
        self.assertEqual(first["status"], second["status"])
        self.assertEqual(first["kit_issue_lines"], second["kit_issue_lines"])


if __name__ == "__main__":
    unittest.main()
