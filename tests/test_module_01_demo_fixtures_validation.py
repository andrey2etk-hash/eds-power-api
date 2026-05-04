import json
import unittest
from pathlib import Path


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "demo" / "module_01_kzo_demo"
FIXTURE_FILES = [
    "demo_metadata.json",
    "doc36_busbar_fixture.json",
    "doc37_node_geometry_fixture.json",
    "doc37_fastener_selection_fixture.json",
    "doc38_aggregation_fixture.json",
    "expected_outputs.json",
    "optional_backup_safety_fixture.json",
]


def _is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


class Module01DemoFixturesValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures = {}
        for name in FIXTURE_FILES:
            path = FIXTURE_DIR / name
            with path.open("r", encoding="utf-8") as fixture_file:
                cls.fixtures[name] = json.load(fixture_file)

    def test_01_fixture_files_exist_and_load_as_json(self):
        for name in FIXTURE_FILES:
            path = FIXTURE_DIR / name
            self.assertTrue(path.exists(), msg=f"Missing fixture file: {name}")
            self.assertIsInstance(self.fixtures[name], dict, msg=f"Fixture {name} must load as object")

    def test_02_required_metadata_exists_in_each_fixture(self):
        for name, payload in self.fixtures.items():
            self.assertIn("fixture_id", payload, msg=f"{name}: fixture_id missing")
            self.assertIn("fixture_version", payload, msg=f"{name}: fixture_version missing")
            self.assertIn("display_name", payload, msg=f"{name}: display_name missing")
            self.assertIn("short_description", payload, msg=f"{name}: short_description missing")
            self.assertTrue(payload.get("immutable"), msg=f"{name}: immutable must be true")
            self.assertTrue(payload.get("demo_only"), msg=f"{name}: demo_only must be true")
            self.assertTrue(payload.get("not_production_data"), msg=f"{name}: not_production_data must be true")

    def test_03_demo_boundary_validation(self):
        meta = self.fixtures["demo_metadata.json"]
        backup = self.fixtures["optional_backup_safety_fixture.json"]

        self.assertEqual(meta.get("main_flow"), "PASS_ONLY")
        boundaries = meta.get("boundaries", {})
        self.assertEqual(boundaries.get("api"), False)
        self.assertEqual(boundaries.get("gas"), False)
        self.assertEqual(boundaries.get("db"), False)
        self.assertEqual(boundaries.get("erp"), False)
        self.assertEqual(boundaries.get("procurement"), False)
        self.assertEqual(boundaries.get("warehouse"), False)
        self.assertEqual(boundaries.get("pricing"), False)
        self.assertEqual(boundaries.get("cad"), False)

        self.assertEqual(backup.get("fixture_role"), "OPTIONAL_BACKUP_ONLY")
        self.assertTrue(backup.get("not_main_demo_flow"))

    def test_04_numeric_type_guards_for_mm_and_quantity_values(self):
        geometry = self.fixtures["doc37_node_geometry_fixture.json"]
        fastener = self.fixtures["doc37_fastener_selection_fixture.json"]
        aggregation = self.fixtures["doc38_aggregation_fixture.json"]
        backup = self.fixtures["optional_backup_safety_fixture.json"]

        for node in geometry["nodes"]:
            self.assertTrue(_is_number(node["phase_length_l1_mm"]))
            self.assertTrue(_is_number(node["phase_length_l2_mm"]))
            self.assertTrue(_is_number(node["phase_length_l3_mm"]))
            self.assertTrue(_is_number(node["node_busbar_thickness_mm"]))
            self.assertTrue(_is_number(node["main_busbar_pack_thickness_mm"]))
            self.assertTrue(_is_number(node["equipment_terminal_thickness_mm"]))
            for group in node["expected_output"]["joint_stacks"]:
                self.assertTrue(_is_number(group["joint_stack_thickness_mm"]))

        for item in fastener["fastener_registry"]["items"]:
            if item["item_type"] == "BOLT":
                self.assertTrue(_is_number(item["thread_pitch_mm"]))
                self.assertTrue(_is_number(item["length_mm"]))
                self.assertTrue(_is_number(item["diameter_mm"]))
            if "item_height_mm" in item:
                self.assertTrue(_is_number(item["item_height_mm"]))

        self.assertTrue(
            _is_number(fastener["washer_package_rules"]["items"][0]["hardware_stack_sum_mm"])
        )
        for rule in fastener["joint_stack_rules"]["items"]:
            self.assertTrue(_is_number(rule["safety_margin_mm"]))

        for source_line in aggregation["source_node_outputs"]:
            self.assertTrue(_is_number(source_line["quantity"]))
            self.assertGreater(source_line["quantity"], 0)

        # Backup fixture is expected to have a missing L2 phase value by design.
        self.assertIsNone(backup["input"]["phase_length_l2_mm"])

    def test_05_unit_validation_for_fastener_quantities(self):
        aggregation = self.fixtures["doc38_aggregation_fixture.json"]
        expected = self.fixtures["expected_outputs.json"]

        for source_line in aggregation["source_node_outputs"]:
            self.assertEqual(source_line.get("unit"), "pcs")

        for issue_line in aggregation["expected_aggregation"]["kit_issue_lines"]:
            self.assertEqual(issue_line.get("unit"), "pcs")

        for issue_line in expected["expected_doc38_aggregation"]["kit_issue_lines"]:
            self.assertEqual(issue_line.get("unit"), "pcs")

    def test_06_cross_file_consistency_core(self):
        doc36 = self.fixtures["doc36_busbar_fixture.json"]
        geometry = self.fixtures["doc37_node_geometry_fixture.json"]
        aggregation = self.fixtures["doc38_aggregation_fixture.json"]
        expected = self.fixtures["expected_outputs.json"]

        geometry_node_ids = {node["busbar_node_id"] for node in geometry["nodes"]}
        aggregation_node_ids = {line["source_node_id"] for line in aggregation["source_node_outputs"]}
        expected_node_ids = {
            expected["expected_node_a_geometry"]["busbar_node_id"],
            expected["expected_node_b_geometry"]["busbar_node_id"],
        }

        self.assertSetEqual(geometry_node_ids, {"KZO_DEMO_NODE_A", "KZO_DEMO_NODE_B"})
        self.assertTrue(geometry_node_ids.issubset(aggregation_node_ids))
        self.assertSetEqual(geometry_node_ids, expected_node_ids)

        self.assertEqual(doc36["selected_material_catalog_id"], "DEMO_BUSBAR_CU_60X10")
        self.assertEqual(aggregation["product_id"], "KZO_DEMO_PRODUCT_001")
        self.assertEqual(aggregation["calculation_id"], "DEMO_CALC_001")

        # expected_outputs fixture is stage-focused and does not duplicate product/calculation ids.
        self.assertNotIn("product_id", expected)
        self.assertNotIn("calculation_id", expected)

    def test_07_geometry_expected_output_validation(self):
        geometry = self.fixtures["doc37_node_geometry_fixture.json"]
        by_id = {node["busbar_node_id"]: node for node in geometry["nodes"]}

        node_a = by_id["KZO_DEMO_NODE_A"]
        self.assertEqual(
            node_a["phase_length_l1_mm"] + node_a["phase_length_l2_mm"] + node_a["phase_length_l3_mm"],
            1290,
        )
        joint_map_a = {x["group_type"]: x["joint_stack_thickness_mm"] for x in node_a["expected_output"]["joint_stacks"]}
        self.assertEqual(joint_map_a["BUSBAR_SIDE_CONNECTIONS"], 30)
        self.assertEqual(joint_map_a["EQUIPMENT_SIDE_CONNECTIONS"], 18)

        node_b = by_id["KZO_DEMO_NODE_B"]
        self.assertEqual(
            node_b["phase_length_l1_mm"] + node_b["phase_length_l2_mm"] + node_b["phase_length_l3_mm"],
            1200,
        )
        joint_map_b = {x["group_type"]: x["joint_stack_thickness_mm"] for x in node_b["expected_output"]["joint_stacks"]}
        self.assertEqual(joint_map_b["BUSBAR_SIDE_CONNECTIONS"], 30)
        self.assertEqual(joint_map_b["EQUIPMENT_SIDE_CONNECTIONS"], 18)

        # Equal stack values are valid: stack depends on thickness pairing, not phase lengths.
        self.assertEqual(joint_map_a, joint_map_b)

    def test_08_fastener_math_validation(self):
        fastener = self.fixtures["doc37_fastener_selection_fixture.json"]
        fastener_by_id = {item["fastener_id"]: item for item in fastener["fastener_registry"]["items"]}
        calc = fastener["expected_bolt_length_calculation"]

        busbar_required = calc["busbar_side"]["joint_stack_thickness_mm"]
        busbar_required += calc["busbar_side"]["hardware_stack_sum_mm"]
        busbar_required += calc["busbar_side"]["thread_allowance_mm"]
        busbar_required += calc["busbar_side"]["safety_margin_mm"]
        self.assertEqual(busbar_required, 48.5)
        self.assertEqual(calc["busbar_side"]["required_bolt_length_mm"], 48.5)
        self.assertLess(fastener_by_id["DEMO_BOLT_M12X45"]["length_mm"], 48.5)
        self.assertGreaterEqual(fastener_by_id["DEMO_BOLT_M12X55"]["length_mm"], 48.5)

        equip_required = calc["equipment_side"]["joint_stack_thickness_mm"]
        equip_required += calc["equipment_side"]["hardware_stack_sum_mm"]
        equip_required += calc["equipment_side"]["thread_allowance_mm"]
        equip_required += calc["equipment_side"]["safety_margin_mm"]
        self.assertEqual(equip_required, 36.5)
        self.assertEqual(calc["equipment_side"]["required_bolt_length_mm"], 36.5)
        self.assertGreaterEqual(fastener_by_id["DEMO_BOLT_M12X45"]["length_mm"], 36.5)

    def test_09_registry_id_cross_checks(self):
        doc36 = self.fixtures["doc36_busbar_fixture.json"]
        fastener = self.fixtures["doc37_fastener_selection_fixture.json"]
        aggregation = self.fixtures["doc38_aggregation_fixture.json"]

        registry_fastener_ids = {
            item["fastener_id"] for item in fastener["fastener_registry"]["items"]
        }

        expected_local = fastener["expected_local_fasteners_per_node"]
        self.assertIn(expected_local["BUSBAR_SIDE_CONNECTIONS"]["selected_bolt_fastener_id"], registry_fastener_ids)
        self.assertIn(expected_local["EQUIPMENT_SIDE_CONNECTIONS"]["selected_bolt_fastener_id"], registry_fastener_ids)
        for shared_line in expected_local["shared_hardware"]:
            self.assertIn(shared_line["fastener_id"], registry_fastener_ids)

        for source_line in aggregation["source_node_outputs"]:
            self.assertIn(source_line["item_id"], registry_fastener_ids)

        self.assertEqual(doc36["selected_material_catalog_id"], "DEMO_BUSBAR_CU_60X10")

    def test_10_aggregation_expected_totals_validation(self):
        aggregation = self.fixtures["doc38_aggregation_fixture.json"]
        expected = self.fixtures["expected_outputs.json"]

        computed = {}
        for source_line in aggregation["source_node_outputs"]:
            item_id = source_line["item_id"]
            qty = source_line["quantity"]
            self.assertTrue(_is_number(qty))
            self.assertGreater(qty, 0)
            computed[item_id] = computed.get(item_id, 0) + qty

        self.assertDictEqual(
            computed,
            {
                "DEMO_BOLT_M12X55": 6,
                "DEMO_BOLT_M12X45": 6,
                "DEMO_NUT_M12": 12,
                "DEMO_FLAT_WASHER_M12": 24,
                "DEMO_DISC_SPRING_WASHER_M12": 12,
            },
        )

        expected_totals = {
            line["item_id"]: line["quantity"]
            for line in expected["expected_doc38_aggregation"]["kit_issue_lines"]
        }
        self.assertDictEqual(expected_totals, computed)

        scope_note = aggregation["expected_aggregation"]["scope_note"].lower()
        self.assertIn("production-preparation", scope_note)
        self.assertIn("not a final erp bom", scope_note)

    def test_11_traceability_validation(self):
        aggregation = self.fixtures["doc38_aggregation_fixture.json"]
        expected = self.fixtures["expected_outputs.json"]

        source_line_ids = [line["source_line_id"] for line in aggregation["source_node_outputs"]]
        traceability_refs = [line["traceability_ref"] for line in aggregation["source_node_outputs"]]
        source_node_ids = {line["source_node_id"] for line in aggregation["source_node_outputs"]}

        self.assertEqual(len(source_line_ids), len(set(source_line_ids)))
        self.assertEqual(len(traceability_refs), len(set(traceability_refs)))

        mapping = {}
        for line in aggregation["source_node_outputs"]:
            source_line_id = line["source_line_id"]
            traceability_ref = line["traceability_ref"]
            if source_line_id in mapping:
                self.assertEqual(mapping[source_line_id], traceability_ref)
            mapping[source_line_id] = traceability_ref

        self.assertSetEqual(source_node_ids, {"KZO_DEMO_NODE_A", "KZO_DEMO_NODE_B"})

        expected_source_line_ids = expected["expected_doc38_aggregation"]["source_line_ids"]
        expected_traceability_refs = expected["expected_doc38_aggregation"]["traceability_refs"]
        self.assertSetEqual(set(source_line_ids), set(expected_source_line_ids))
        self.assertSetEqual(set(traceability_refs), set(expected_traceability_refs))

    def test_12_registry_metadata_validation_and_demo_v1_boundary(self):
        doc36 = self.fixtures["doc36_busbar_fixture.json"]
        fastener = self.fixtures["doc37_fastener_selection_fixture.json"]
        aggregation = self.fixtures["doc38_aggregation_fixture.json"]
        expected = self.fixtures["expected_outputs.json"]

        for source in doc36["registry_sources"]:
            self.assertEqual(source["registry_version"], "demo_v1")
            self.assertIn("last_updated", source)
            self.assertIn("display_name", source)

        self.assertEqual(fastener["fastener_registry"]["registry_version"], "demo_v1")
        self.assertEqual(fastener["joint_stack_rules"]["registry_version"], "demo_v1")
        self.assertEqual(fastener["washer_package_rules"]["registry_version"], "demo_v1")
        for section in (
            fastener["fastener_registry"],
            fastener["joint_stack_rules"],
            fastener["washer_package_rules"],
        ):
            self.assertIn("last_updated", section)
            self.assertIn("display_name", section)

        self.assertEqual(aggregation["registry_version"], "demo_v1")
        self.assertIn("last_updated", aggregation)
        self.assertEqual(expected["registry_version"], "demo_v1")

        registry_version_keys = []

        def collect_registry_versions(node):
            if isinstance(node, dict):
                for key, value in node.items():
                    if key == "registry_version" or key.endswith("_registry_version"):
                        registry_version_keys.append(value)
                    collect_registry_versions(value)
            elif isinstance(node, list):
                for item in node:
                    collect_registry_versions(item)

        for payload in self.fixtures.values():
            collect_registry_versions(payload)

        self.assertTrue(all(version == "demo_v1" for version in registry_version_keys))

    def test_13_optional_backup_fixture_validation(self):
        backup = self.fixtures["optional_backup_safety_fixture.json"]

        self.assertEqual(backup["fixture_role"], "OPTIONAL_BACKUP_ONLY")
        self.assertTrue(backup["not_main_demo_flow"])
        self.assertEqual(backup["expected_status"], "INCOMPLETE")
        self.assertEqual(backup["expected_failure_code"], "PHASE_LENGTH_MISSING")
        self.assertIsInstance(backup["expected_failure_reason"], str)
        self.assertTrue(backup["expected_failure_reason"].strip())
        self.assertIsNone(backup["input"]["phase_length_l2_mm"])


if __name__ == "__main__":
    unittest.main()
