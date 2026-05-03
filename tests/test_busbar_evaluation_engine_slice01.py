import unittest

from src.engines.kzo_welded.busbar_evaluation_engine import (
    CHECK_NEEDS_ENGINEERING_VALUE,
    CHECK_PASS,
    FAILURE_CANDIDATE_CURRENT_UNKNOWN,
    FAILURE_MULTIPLE_VALID_CANDIDATES,
    FAILURE_REGISTRY_VERSION_MISSING,
    STATUS_ENGINEERING_REQUIRED,
    STATUS_INCOMPLETE,
    STATUS_PASS,
    STATUS_SELECTION_REQUIRED,
    evaluate_busbar_candidate_safety_core,
)


def _registry_versions(**overrides):
    base = {
        "global_material_catalog_version": "v1",
        "kzo_usage_registry_version": "v1",
        "busbar_node_matrix_version": "v1",
        "equipment_interface_registry_version": "v1",
    }
    base.update(overrides)
    return base


def _base_input():
    return {
        "registry_versions": _registry_versions(),
        "candidate": {
            "id": "BUSBAR_CU_SHMT_60X10_1",
            "rated_current_a": 1000,
        },
        "selected_material_catalog_id": "BUSBAR_CU_SHMT_60X10_1",
        "selected_usage_id": "KZO_MAIN_BUS_CU_60X10_1",
        "package_id": "KZO_BUSBAR_MAIN_PACKAGE_V1",
        "checks": {
            "node": CHECK_PASS,
            "usage": CHECK_PASS,
            "current": CHECK_PASS,
            "form_factor": CHECK_PASS,
        },
        "mandatory_check_keys": ["node", "usage", "current", "form_factor"],
        "valid_candidate_count": 1,
        "auto_selection_allowed": True,
    }


class BusbarEvaluationEngineSlice01Tests(unittest.TestCase):
    def test_pass_allowed_when_all_mandatory_checks_pass(self):
        result = evaluate_busbar_candidate_safety_core(_base_input())
        self.assertEqual(result["status"], STATUS_PASS)
        self.assertIsNone(result["failure_code"])

    def test_pass_paradox_blocked_when_current_needs_engineering_value(self):
        data = _base_input()
        data["checks"]["current"] = CHECK_NEEDS_ENGINEERING_VALUE
        result = evaluate_busbar_candidate_safety_core(data)
        self.assertNotEqual(result["status"], STATUS_PASS)
        self.assertIn(result["status"], (STATUS_ENGINEERING_REQUIRED, STATUS_INCOMPLETE))
        self.assertIsNotNone(result["failure_code"])

    def test_missing_registry_version_returns_incomplete(self):
        data = _base_input()
        data["registry_versions"] = _registry_versions(kzo_usage_registry_version=None)
        result = evaluate_busbar_candidate_safety_core(data)
        self.assertEqual(result["status"], STATUS_INCOMPLETE)
        self.assertEqual(result["failure_code"], FAILURE_REGISTRY_VERSION_MISSING)
        self.assertIsNone(result["selected_material_catalog_id"])

    def test_empty_string_registry_version_returns_incomplete(self):
        data = _base_input()
        data["registry_versions"] = _registry_versions(kzo_usage_registry_version="")
        result = evaluate_busbar_candidate_safety_core(data)
        self.assertEqual(result["status"], STATUS_INCOMPLETE)
        self.assertEqual(result["failure_code"], FAILURE_REGISTRY_VERSION_MISSING)
        self.assertIsNone(result["selected_material_catalog_id"])

    def test_candidate_current_unknown_returns_engineering_required(self):
        data = _base_input()
        data["candidate"]["rated_current_a"] = None
        result = evaluate_busbar_candidate_safety_core(data)
        self.assertEqual(result["status"], STATUS_ENGINEERING_REQUIRED)
        self.assertIsNone(result["selected_material_catalog_id"])
        self.assertEqual(result["proposed_candidate_id"], "BUSBAR_CU_SHMT_60X10_1")
        self.assertEqual(result["failure_code"], FAILURE_CANDIDATE_CURRENT_UNKNOWN)

    def test_engineering_required_returns_selected_material_none(self):
        data = _base_input()
        data["checks"]["current"] = CHECK_NEEDS_ENGINEERING_VALUE
        result = evaluate_busbar_candidate_safety_core(data)
        self.assertEqual(result["status"], STATUS_ENGINEERING_REQUIRED)
        self.assertIsNone(result["selected_material_catalog_id"])

    def test_multiple_valid_candidates_without_policy_returns_selection_required(self):
        data = _base_input()
        data["valid_candidate_count"] = 2
        data["auto_selection_allowed"] = False
        result = evaluate_busbar_candidate_safety_core(data)
        self.assertEqual(result["status"], STATUS_SELECTION_REQUIRED)
        self.assertEqual(result["failure_code"], FAILURE_MULTIPLE_VALID_CANDIDATES)
        self.assertIsNone(result["selected_material_catalog_id"])


if __name__ == "__main__":
    unittest.main()
