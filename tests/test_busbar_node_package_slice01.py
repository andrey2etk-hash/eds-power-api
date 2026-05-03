import unittest

from src.engines.kzo_welded.busbar_evaluation_engine import (
    STATUS_ENGINEERING_REQUIRED,
    STATUS_INCOMPLETE,
    STATUS_PASS,
)
from src.engines.kzo_welded.busbar_node_package_engine import (
    FAILURE_DOC36_SELECTION_NOT_PASS,
    FAILURE_EQUIPMENT_TERMINAL_THICKNESS_MISSING,
    FAILURE_MAIN_BUSBAR_THICKNESS_MISSING,
    FAILURE_PHASE_CONNECTION_MISMATCH,
    FAILURE_PHASE_LENGTH_MISSING,
    evaluate_busbar_node_geometry_and_stack,
)


def _base_input():
    return {
        "doc36": {"status": STATUS_PASS},
        "busbar_node_id": "KZO_NODE_MAIN_TO_BREAKER_A",
        "phase_count": 3,
        "phase_length_l1_mm": 420,
        "phase_length_l2_mm": 420,
        "phase_length_l3_mm": 420,
        "node_busbar_thickness_mm": 10,
        "main_busbar_pack_thickness_mm": 8,
        "equipment_terminal_thickness_mm": 6,
        "connection_point_groups": [
            {
                "group_id": "BUSBAR_SIDE_CONNECTIONS",
                "connection_point_count": 3,
                "connected_part_a": "NODE_BUSBAR",
                "connected_part_b": "MAIN_BUSBAR",
                "stack_thickness_formula": "NODE_PLUS_MAIN",
            },
            {
                "group_id": "EQUIPMENT_SIDE_CONNECTIONS",
                "connection_point_count": 3,
                "connected_part_a": "NODE_BUSBAR",
                "connected_part_b": "EQUIPMENT_TERMINAL",
                "stack_thickness_formula": "NODE_PLUS_EQUIPMENT",
            },
        ],
    }


class BusbarNodePackageSlice01Tests(unittest.TestCase):
    def test_pass_happy_path(self):
        result = evaluate_busbar_node_geometry_and_stack(_base_input())
        self.assertEqual(result["status"], STATUS_PASS)
        self.assertEqual(result["total_busbar_length_mm"], 1260)
        self.assertEqual(result["connection_point_groups"][0]["joint_stack_thickness_mm"], 18)
        self.assertEqual(result["connection_point_groups"][1]["joint_stack_thickness_mm"], 16)
        self.assertEqual(result["node_fastener_lines"], [])

    def test_doc36_not_pass_blocks_result(self):
        data = _base_input()
        data["doc36"]["status"] = STATUS_ENGINEERING_REQUIRED
        result = evaluate_busbar_node_geometry_and_stack(data)
        self.assertNotEqual(result["status"], STATUS_PASS)
        self.assertEqual(result["failure_code"], FAILURE_DOC36_SELECTION_NOT_PASS)
        self.assertEqual(result["node_fastener_lines"], [])

    def test_missing_phase_length_returns_phase_length_missing(self):
        data = _base_input()
        data["phase_length_l2_mm"] = None
        result = evaluate_busbar_node_geometry_and_stack(data)
        self.assertEqual(result["status"], STATUS_INCOMPLETE)
        self.assertEqual(result["failure_code"], FAILURE_PHASE_LENGTH_MISSING)

    def test_invalid_mm_value_zero_returns_phase_length_missing(self):
        data = _base_input()
        data["phase_length_l1_mm"] = 0
        result = evaluate_busbar_node_geometry_and_stack(data)
        self.assertEqual(result["status"], STATUS_INCOMPLETE)
        self.assertEqual(result["failure_code"], FAILURE_PHASE_LENGTH_MISSING)

    def test_connection_mismatch_returns_phase_connection_mismatch(self):
        data = _base_input()
        data["connection_point_groups"][0]["connection_point_count"] = 1
        result = evaluate_busbar_node_geometry_and_stack(data)
        self.assertNotEqual(result["status"], STATUS_PASS)
        self.assertEqual(result["failure_code"], FAILURE_PHASE_CONNECTION_MISMATCH)

    def test_missing_main_busbar_thickness_returns_specific_failure(self):
        data = _base_input()
        data["main_busbar_pack_thickness_mm"] = None
        result = evaluate_busbar_node_geometry_and_stack(data)
        self.assertEqual(result["status"], STATUS_INCOMPLETE)
        self.assertEqual(result["failure_code"], FAILURE_MAIN_BUSBAR_THICKNESS_MISSING)

    def test_missing_equipment_terminal_thickness_returns_specific_failure(self):
        data = _base_input()
        data["equipment_terminal_thickness_mm"] = None
        result = evaluate_busbar_node_geometry_and_stack(data)
        self.assertEqual(result["status"], STATUS_INCOMPLETE)
        self.assertEqual(result["failure_code"], FAILURE_EQUIPMENT_TERMINAL_THICKNESS_MISSING)

    def test_no_fastener_output_even_for_pass(self):
        result = evaluate_busbar_node_geometry_and_stack(_base_input())
        self.assertEqual(result["status"], STATUS_PASS)
        self.assertEqual(result["node_fastener_lines"], [])
        self.assertNotIn("BOLT", str(result))
        self.assertNotIn("WASHER", str(result))
        self.assertNotIn("NUT", str(result))


if __name__ == "__main__":
    unittest.main()
