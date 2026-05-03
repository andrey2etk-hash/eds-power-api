import inspect
import unittest

from src.engines.kzo_welded.busbar_evaluation_engine import (
    STATUS_ENGINEERING_REQUIRED,
    STATUS_INCOMPLETE,
    STATUS_PASS,
    STATUS_SELECTION_REQUIRED,
)
from src.engines.kzo_welded.busbar_node_fastener_selection_engine import (
    FAILURE_BOLT_LENGTH_AMBIGUOUS,
    FAILURE_BOLT_LENGTH_NOT_FOUND,
    FAILURE_FASTENER_DEFAULT_NOT_APPROVED,
    FAILURE_HARDWARE_STACK_SUM_MISSING,
    FAILURE_INTERFACE_FASTENER_CONFLICT,
    FAILURE_NODE_PACKAGE_INCOMPLETE,
    FAILURE_NUT_DATA_MISSING,
    FAILURE_SAFETY_MARGIN_MISSING,
    FAILURE_SLICE01_GEOMETRY_NOT_PASS,
    FAILURE_THREAD_PITCH_MISSING,
    FAILURE_WASHER_DATA_MISSING,
    evaluate_busbar_node_fastener_selection,
)


def _base_input():
    return {
        "slice01_output": {
            "status": STATUS_PASS,
            "busbar_node_id": "KZO_NODE_MAIN_TO_BREAKER_A",
            "phase_count": 3,
            "connection_point_groups": [
                {
                    "group_id": "BUSBAR_SIDE_CONNECTIONS",
                    "connection_point_count": 3,
                    "joint_stack_thickness_mm": 20.0,
                    "stack_status": STATUS_PASS,
                    "failure_code": None,
                },
                {
                    "group_id": "EQUIPMENT_SIDE_CONNECTIONS",
                    "connection_point_count": 3,
                    "joint_stack_thickness_mm": 18.0,
                    "stack_status": STATUS_PASS,
                    "failure_code": None,
                },
            ],
            "node_fastener_lines": [],
            "node_material_lines": [],
        },
        "registry_versions": {
            "fastener_registry_version": "v1",
            "joint_stack_rule_registry_version": "v1",
            "washer_package_rule_registry_version": "v1",
        },
        "joint_stack_rules": [
            {
                "joint_stack_rule_id": "JSR_BUSBAR",
                "connection_group_type": "BUSBAR_SIDE_CONNECTIONS",
                "allowed_bolt_diameter_mm": 12,
                "washer_package_rule_id": "WPR_BUSBAR",
                "required_bolt_type": "HEX",
                "thread_pitch_mm": 1.75,
                "safety_margin_mm": 0.0,
                "selection_policy": "MIN_LENGTH",
                "is_active": True,
            },
            {
                "joint_stack_rule_id": "JSR_EQUIPMENT",
                "connection_group_type": "EQUIPMENT_SIDE_CONNECTIONS",
                "allowed_bolt_diameter_mm": 12,
                "washer_package_rule_id": "WPR_EQUIPMENT",
                "required_bolt_type": "HEX",
                "thread_pitch_mm": 1.75,
                "safety_margin_mm": 0.0,
                "selection_policy": "MIN_LENGTH",
                "is_active": True,
            },
        ],
        "washer_package_rules": [
            {
                "washer_package_rule_id": "WPR_BUSBAR",
                "flat_washer_count": 2,
                "flat_washer_fastener_id": "WASHER_M12",
                "disc_spring_washer_count": 1,
                "disc_spring_washer_fastener_id": "DISC_WASHER_M12",
                "nut_fastener_id": "NUT_M12",
                "hardware_stack_sum_mm": 8.5,
                "allowed_bolt_diameter_mm": 12,
                "usage_context": "BUSBAR",
                "is_active": True,
            },
            {
                "washer_package_rule_id": "WPR_EQUIPMENT",
                "flat_washer_count": 2,
                "flat_washer_fastener_id": "WASHER_M12",
                "disc_spring_washer_count": 1,
                "disc_spring_washer_fastener_id": "DISC_WASHER_M12",
                "nut_fastener_id": "NUT_M12",
                "hardware_stack_sum_mm": 8.5,
                "allowed_bolt_diameter_mm": 12,
                "usage_context": "EQUIPMENT",
                "is_active": True,
            },
        ],
        "fastener_registry_items": [
            {
                "fastener_id": "BOLT_M12X30",
                "item_type": "BOLT",
                "diameter_mm": 12,
                "thread_pitch_mm": 1.75,
                "length_mm": 30,
                "is_active": True,
            },
            {
                "fastener_id": "BOLT_M12X40",
                "item_type": "BOLT",
                "diameter_mm": 12,
                "thread_pitch_mm": 1.75,
                "length_mm": 40,
                "is_active": True,
            },
            {
                "fastener_id": "NUT_M12",
                "item_type": "NUT",
                "diameter_mm": 12,
                "item_height_mm": 10,
                "is_active": True,
            },
            {
                "fastener_id": "WASHER_M12",
                "item_type": "FLAT_WASHER",
                "diameter_mm": 12,
                "item_height_mm": 2,
                "is_active": True,
            },
            {
                "fastener_id": "DISC_WASHER_M12",
                "item_type": "DISC_SPRING_WASHER",
                "diameter_mm": 12,
                "item_height_mm": 2.5,
                "is_active": True,
            },
        ],
        "equipment_interface_constraints": {},
    }


class BusbarNodeFastenerSelectionSlice02Tests(unittest.TestCase):
    def test_slice01_not_pass_blocks_slice02(self):
        data = _base_input()
        data["slice01_output"]["status"] = STATUS_ENGINEERING_REQUIRED
        result = evaluate_busbar_node_fastener_selection(data)
        self.assertEqual(result["status"], STATUS_INCOMPLETE)
        self.assertEqual(result["failure_code"], FAILURE_SLICE01_GEOMETRY_NOT_PASS)

    def test_missing_required_connection_group(self):
        data = _base_input()
        data["slice01_output"]["connection_point_groups"] = data["slice01_output"]["connection_point_groups"][:1]
        result = evaluate_busbar_node_fastener_selection(data)
        self.assertEqual(result["status"], STATUS_INCOMPLETE)
        self.assertEqual(result["failure_code"], FAILURE_NODE_PACKAGE_INCOMPLETE)

    def test_missing_washer_package_rule(self):
        data = _base_input()
        data["washer_package_rules"] = []
        result = evaluate_busbar_node_fastener_selection(data)
        self.assertEqual(result["status"], STATUS_INCOMPLETE)
        self.assertEqual(result["failure_code"], FAILURE_FASTENER_DEFAULT_NOT_APPROVED)

    def test_missing_hardware_stack_sum(self):
        data = _base_input()
        data["washer_package_rules"][0]["hardware_stack_sum_mm"] = None
        result = evaluate_busbar_node_fastener_selection(data)
        self.assertEqual(result["status"], STATUS_INCOMPLETE)
        self.assertEqual(result["failure_code"], FAILURE_HARDWARE_STACK_SUM_MISSING)

    def test_missing_thread_pitch(self):
        data = _base_input()
        data["joint_stack_rules"][0]["thread_pitch_mm"] = None
        data["fastener_registry_items"][0]["thread_pitch_mm"] = None
        data["fastener_registry_items"][1]["thread_pitch_mm"] = None
        result = evaluate_busbar_node_fastener_selection(data)
        self.assertEqual(result["status"], STATUS_INCOMPLETE)
        self.assertEqual(result["failure_code"], FAILURE_THREAD_PITCH_MISSING)

    def test_missing_safety_margin(self):
        data = _base_input()
        data["joint_stack_rules"][0]["safety_margin_mm"] = None
        result = evaluate_busbar_node_fastener_selection(data)
        self.assertEqual(result["status"], STATUS_INCOMPLETE)
        self.assertEqual(result["failure_code"], FAILURE_SAFETY_MARGIN_MISSING)

    def test_no_active_bolts(self):
        data = _base_input()
        for item in data["fastener_registry_items"]:
            if item["item_type"] == "BOLT":
                item["is_active"] = False
        result = evaluate_busbar_node_fastener_selection(data)
        self.assertEqual(result["status"], STATUS_INCOMPLETE)
        self.assertEqual(result["failure_code"], FAILURE_BOLT_LENGTH_NOT_FOUND)

    def test_tight_fit_bolt_accepted(self):
        data = _base_input()
        # For BUSBAR group required length: 20 + 8.5 + 3.5 + 0 = 32.0
        data["fastener_registry_items"][0]["length_mm"] = 32.0
        data["fastener_registry_items"][1]["is_active"] = False
        result = evaluate_busbar_node_fastener_selection(data)
        self.assertEqual(result["status"], STATUS_PASS)
        self.assertEqual(result["connection_point_groups"][0]["selected_bolt_fastener_id"], "BOLT_M12X30")

    def test_no_downward_rounding(self):
        data = _base_input()
        data["washer_package_rules"][0]["hardware_stack_sum_mm"] = 16.6  # required = 40.1
        data["fastener_registry_items"][0]["length_mm"] = 40
        data["fastener_registry_items"][1]["is_active"] = False
        result = evaluate_busbar_node_fastener_selection(data)
        self.assertEqual(result["status"], STATUS_INCOMPLETE)
        self.assertEqual(result["failure_code"], FAILURE_BOLT_LENGTH_NOT_FOUND)

    def test_multiple_valid_bolts_without_selection_policy(self):
        data = _base_input()
        data["joint_stack_rules"][0]["selection_policy"] = None
        data["joint_stack_rules"][1]["selection_policy"] = None
        result = evaluate_busbar_node_fastener_selection(data)
        self.assertEqual(result["status"], STATUS_SELECTION_REQUIRED)
        self.assertEqual(result["failure_code"], FAILURE_BOLT_LENGTH_AMBIGUOUS)

    def test_one_valid_bolt_generates_local_node_fastener_lines(self):
        data = _base_input()
        data["joint_stack_rules"][0]["selection_policy"] = "MIN_LENGTH"
        data["joint_stack_rules"][1]["selection_policy"] = "MIN_LENGTH"
        data["fastener_registry_items"][0]["length_mm"] = 40
        data["fastener_registry_items"][1]["is_active"] = False
        result = evaluate_busbar_node_fastener_selection(data)
        self.assertEqual(result["status"], STATUS_PASS)
        self.assertTrue(len(result["node_fastener_lines"]) > 0)
        self.assertNotIn("final_bom", result["node_fastener_lines"][0])

    def test_missing_nut_data(self):
        data = _base_input()
        data["washer_package_rules"][0]["nut_fastener_id"] = "NUT_UNKNOWN"
        result = evaluate_busbar_node_fastener_selection(data)
        self.assertEqual(result["status"], STATUS_INCOMPLETE)
        self.assertEqual(result["failure_code"], FAILURE_NUT_DATA_MISSING)

    def test_missing_washer_data(self):
        data = _base_input()
        data["washer_package_rules"][0]["flat_washer_fastener_id"] = None
        result = evaluate_busbar_node_fastener_selection(data)
        self.assertEqual(result["status"], STATUS_INCOMPLETE)
        self.assertEqual(result["failure_code"], FAILURE_WASHER_DATA_MISSING)

    def test_equipment_interface_conflict(self):
        data = _base_input()
        data["equipment_interface_constraints"] = {
            "BUSBAR_SIDE_CONNECTIONS": {
                "allowed_bolt_diameter_mm": 10,
                "required_bolt_type": "HEX",
            }
        }
        result = evaluate_busbar_node_fastener_selection(data)
        self.assertNotEqual(result["status"], STATUS_PASS)
        self.assertEqual(result["failure_code"], FAILURE_INTERFACE_FASTENER_CONFLICT)

    def test_no_api_gas_db_access(self):
        import src.engines.kzo_welded.busbar_node_fastener_selection_engine as engine_module

        source = inspect.getsource(engine_module)
        self.assertNotIn("requests.", source)
        self.assertNotIn("sqlalchemy", source)
        self.assertNotIn("supabase", source)
        self.assertNotIn("googleapiclient", source)


if __name__ == "__main__":
    unittest.main()
