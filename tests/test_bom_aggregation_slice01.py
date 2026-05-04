import inspect
import unittest

from src.engines.kzo_welded.bom_aggregation_engine import (
    FAILURE_DUPLICATE_SOURCE_LINE,
    FAILURE_DUPLICATE_TRACEABILITY_REF,
    FAILURE_ITEM_ID_MISSING,
    FAILURE_MIXED_REGISTRY_SOURCE_CONFLICT,
    FAILURE_MIXED_UNIT_CONFLICT,
    FAILURE_NODE_OUTPUT_NOT_PASS,
    FAILURE_NON_NUMERIC_QUANTITY,
    FAILURE_REGISTRY_VERSION_MISMATCH,
    FAILURE_SELECTED_MATERIAL_CATALOG_ID_MISSING,
    FAILURE_SOURCE_LINE_ID_MISSING,
    FAILURE_TRACEABILITY_REF_MISSING,
    FAILURE_UNSUPPORTED_AGGREGATION_SCOPE,
    FAILURE_ZERO_OR_NEGATIVE_QUANTITY,
    aggregate_kzo_node_package_lines,
)
from src.engines.kzo_welded.busbar_evaluation_engine import (
    STATUS_ENGINEERING_REQUIRED,
    STATUS_FAIL,
    STATUS_INCOMPLETE,
    STATUS_PASS,
)


def _base_input():
    return {
        "aggregation_scope": "DEMO_MVP",
        "product_type": "KZO",
        "product_id": "KZO_DEMO_CELL_001",
        "calculation_id": "CALC_DEMO_001",
        "source_node_outputs": [
            {
                "status": STATUS_PASS,
                "busbar_node_id": "KZO_NODE_MAIN_TO_BREAKER_A",
                "registry_versions": {
                    "fastener_registry_version": "v1",
                    "joint_stack_rule_registry_version": "v1",
                    "washer_package_rule_registry_version": "v1",
                },
                "node_material_lines": [],
                "node_fastener_lines": [
                    {
                        "source_line_id": "line_ref_001",
                        "traceability_ref": "trace_ref_001",
                        "item_id": "BOLT_FROM_FASTENER_REGISTRY_A",
                        "item_type": "BOLT",
                        "quantity": 3,
                        "unit": "pcs",
                        "source_node_id": "KZO_NODE_MAIN_TO_BREAKER_A",
                        "source_group": "BUSBAR_SIDE_CONNECTIONS",
                        "registry_source": "fastener_registry_v1",
                        "registry_version": "v1",
                        "issue_context": "NODE_FASTENER_ISSUE",
                        "fastener_registry_version": "v1",
                    }
                ],
            },
            {
                "status": STATUS_PASS,
                "busbar_node_id": "KZO_NODE_MAIN_TO_BREAKER_B",
                "registry_versions": {
                    "fastener_registry_version": "v1",
                    "joint_stack_rule_registry_version": "v1",
                    "washer_package_rule_registry_version": "v1",
                },
                "node_material_lines": [],
                "node_fastener_lines": [
                    {
                        "source_line_id": "line_ref_002",
                        "traceability_ref": "trace_ref_002",
                        "item_id": "BOLT_FROM_FASTENER_REGISTRY_A",
                        "item_type": "BOLT",
                        "quantity": 3,
                        "unit": "pcs",
                        "source_node_id": "KZO_NODE_MAIN_TO_BREAKER_B",
                        "source_group": "BUSBAR_SIDE_CONNECTIONS",
                        "registry_source": "fastener_registry_v1",
                        "registry_version": "v1",
                        "issue_context": "NODE_FASTENER_ISSUE",
                        "fastener_registry_version": "v1",
                    }
                ],
            },
        ],
    }


class BomAggregationSlice01Tests(unittest.TestCase):
    def test_pass_aggregation_with_two_nodes_same_bolt_item(self):
        result = aggregate_kzo_node_package_lines(_base_input())
        self.assertEqual(result["status"], STATUS_PASS)
        self.assertEqual(len(result["kit_issue_lines"]), 1)
        self.assertEqual(result["kit_issue_lines"][0]["total_quantity"], 6.0)
        self.assertEqual(result["kit_issue_lines"][0]["source_line_ids"], ["line_ref_001", "line_ref_002"])
        self.assertEqual(result["kit_issue_lines"][0]["traceability_refs"], ["trace_ref_001", "trace_ref_002"])

    def test_node_output_not_pass(self):
        data = _base_input()
        data["source_node_outputs"][1]["status"] = STATUS_INCOMPLETE
        result = aggregate_kzo_node_package_lines(data)
        self.assertEqual(result["status"], STATUS_INCOMPLETE)
        self.assertEqual(result["failure_code"], FAILURE_NODE_OUTPUT_NOT_PASS)

    def test_missing_source_line_id(self):
        data = _base_input()
        del data["source_node_outputs"][0]["node_fastener_lines"][0]["source_line_id"]
        result = aggregate_kzo_node_package_lines(data)
        self.assertEqual(result["status"], STATUS_INCOMPLETE)
        self.assertEqual(result["failure_code"], FAILURE_SOURCE_LINE_ID_MISSING)

    def test_duplicate_source_line_id(self):
        data = _base_input()
        data["source_node_outputs"][1]["node_fastener_lines"][0]["source_line_id"] = "line_ref_001"
        result = aggregate_kzo_node_package_lines(data)
        self.assertEqual(result["status"], STATUS_FAIL)
        self.assertEqual(result["failure_code"], FAILURE_DUPLICATE_SOURCE_LINE)

    def test_missing_traceability_ref(self):
        data = _base_input()
        del data["source_node_outputs"][0]["node_fastener_lines"][0]["traceability_ref"]
        result = aggregate_kzo_node_package_lines(data)
        self.assertEqual(result["status"], STATUS_INCOMPLETE)
        self.assertEqual(result["failure_code"], FAILURE_TRACEABILITY_REF_MISSING)

    def test_duplicate_traceability_ref(self):
        data = _base_input()
        data["source_node_outputs"][1]["node_fastener_lines"][0]["traceability_ref"] = "trace_ref_001"
        result = aggregate_kzo_node_package_lines(data)
        self.assertEqual(result["status"], STATUS_FAIL)
        self.assertEqual(result["failure_code"], FAILURE_DUPLICATE_TRACEABILITY_REF)

    def test_non_numeric_quantity(self):
        data = _base_input()
        data["source_node_outputs"][0]["node_fastener_lines"][0]["quantity"] = "three"
        result = aggregate_kzo_node_package_lines(data)
        self.assertEqual(result["status"], STATUS_INCOMPLETE)
        self.assertEqual(result["failure_code"], FAILURE_NON_NUMERIC_QUANTITY)

    def test_zero_quantity(self):
        data = _base_input()
        data["source_node_outputs"][0]["node_fastener_lines"][0]["quantity"] = 0
        result = aggregate_kzo_node_package_lines(data)
        self.assertEqual(result["status"], STATUS_FAIL)
        self.assertEqual(result["failure_code"], FAILURE_ZERO_OR_NEGATIVE_QUANTITY)

    def test_negative_quantity(self):
        data = _base_input()
        data["source_node_outputs"][0]["node_fastener_lines"][0]["quantity"] = -1
        result = aggregate_kzo_node_package_lines(data)
        self.assertEqual(result["status"], STATUS_FAIL)
        self.assertEqual(result["failure_code"], FAILURE_ZERO_OR_NEGATIVE_QUANTITY)

    def test_mixed_unit_for_same_item_id(self):
        data = _base_input()
        data["source_node_outputs"][1]["node_fastener_lines"][0]["unit"] = "kg"
        result = aggregate_kzo_node_package_lines(data)
        self.assertEqual(result["status"], STATUS_INCOMPLETE)
        self.assertEqual(result["failure_code"], FAILURE_MIXED_UNIT_CONFLICT)

    def test_mixed_registry_source_for_same_item_id(self):
        data = _base_input()
        data["source_node_outputs"][1]["node_fastener_lines"][0]["registry_source"] = "alt_fastener_registry_v1"
        result = aggregate_kzo_node_package_lines(data)
        self.assertEqual(result["status"], STATUS_INCOMPLETE)
        self.assertEqual(result["failure_code"], FAILURE_MIXED_REGISTRY_SOURCE_CONFLICT)

    def test_registry_version_mismatch_for_same_item_id(self):
        data = _base_input()
        data["source_node_outputs"][1]["node_fastener_lines"][0]["registry_version"] = "v2"
        result = aggregate_kzo_node_package_lines(data)
        self.assertEqual(result["status"], STATUS_ENGINEERING_REQUIRED)
        self.assertEqual(result["failure_code"], FAILURE_REGISTRY_VERSION_MISMATCH)

    def test_material_line_missing_selected_material_catalog_id(self):
        data = _base_input()
        data["source_node_outputs"][0]["node_material_lines"] = [
            {
                "source_line_id": "mat_ref_001",
                "traceability_ref": "mat_trace_001",
                "item_id": "BUSBAR_CU_SHMT_60X10_1",
                "item_type": "MATERIAL",
                "quantity": 5.0,
                "unit": "kg",
                "source_node_id": "KZO_NODE_MAIN_TO_BREAKER_A",
                "source_group": "BUSBAR_SIDE_CONNECTIONS",
                "registry_source": "material_catalog_v1",
                "registry_version": "v1",
            }
        ]
        result = aggregate_kzo_node_package_lines(data)
        self.assertEqual(result["status"], STATUS_INCOMPLETE)
        self.assertEqual(result["failure_code"], FAILURE_SELECTED_MATERIAL_CATALOG_ID_MISSING)

    def test_material_identity_uses_selected_material_catalog_id(self):
        data = _base_input()
        data["source_node_outputs"][0]["node_material_lines"] = [
            {
                "source_line_id": "mat_ref_001",
                "traceability_ref": "mat_trace_001",
                "item_id": "BUSBAR_MATERIAL_GENERIC",
                "item_type": "MATERIAL",
                "quantity": 5.0,
                "unit": "kg",
                "source_node_id": "KZO_NODE_MAIN_TO_BREAKER_A",
                "source_group": "BUSBAR_SIDE_CONNECTIONS",
                "registry_source": "material_catalog_v1",
                "registry_version": "v1",
                "selected_material_catalog_id": "MAT_A",
            }
        ]
        data["source_node_outputs"][1]["node_material_lines"] = [
            {
                "source_line_id": "mat_ref_002",
                "traceability_ref": "mat_trace_002",
                "item_id": "BUSBAR_MATERIAL_GENERIC",
                "item_type": "MATERIAL",
                "quantity": 7.0,
                "unit": "kg",
                "source_node_id": "KZO_NODE_MAIN_TO_BREAKER_B",
                "source_group": "BUSBAR_SIDE_CONNECTIONS",
                "registry_source": "material_catalog_v1",
                "registry_version": "v1",
                "selected_material_catalog_id": "MAT_B",
            }
        ]
        result = aggregate_kzo_node_package_lines(data)
        self.assertEqual(result["status"], STATUS_PASS)
        material_lines = [x for x in result["kit_issue_lines"] if x["item_type"] == "MATERIAL"]
        self.assertEqual(len(material_lines), 2)

    def test_unsupported_aggregation_scope(self):
        data = _base_input()
        data["aggregation_scope"] = "LINEUP"
        result = aggregate_kzo_node_package_lines(data)
        self.assertEqual(result["status"], STATUS_INCOMPLETE)
        self.assertEqual(result["failure_code"], FAILURE_UNSUPPORTED_AGGREGATION_SCOPE)

    def test_output_not_final_erp_bom(self):
        result = aggregate_kzo_node_package_lines(_base_input())
        self.assertEqual(result["status"], STATUS_PASS)
        flat_result = str(result).lower()
        self.assertNotIn("erp_posting", flat_result)
        self.assertNotIn("warehouse_reservation", flat_result)
        self.assertNotIn("purchase_request", flat_result)
        self.assertNotIn("supplier", flat_result)
        self.assertNotIn("price", flat_result)
        self.assertNotIn("stock_movement", flat_result)

    def test_no_api_gas_db_access(self):
        import src.engines.kzo_welded.bom_aggregation_engine as engine_module

        source = inspect.getsource(engine_module)
        self.assertNotIn("requests.", source)
        self.assertNotIn("sqlalchemy", source)
        self.assertNotIn("supabase", source)
        self.assertNotIn("googleapiclient", source)


if __name__ == "__main__":
    unittest.main()
