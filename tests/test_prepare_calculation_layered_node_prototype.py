import unittest

from main import prepare_calculation


def _request_payload(**extra):
    payload = {
        "object_number": "7445-B",
        "product_type": "KZO",
        "logic_version": "KZO_MVP_V1",
        "voltage_class": "VC_10",
        "busbar_current": 1250,
        "configuration_type": "CFG_SINGLE_BUS_SECTION",
        "quantity_total": 22,
        "cell_distribution": {
            "CELL_INCOMER": 2,
            "CELL_OUTGOING": 16,
            "CELL_PT": 2,
            "CELL_BUS_SECTION": 2,
        },
        "status": "DRAFT",
    }
    payload.update(extra)
    return {
        "meta": {"request_id": "test-layered-node"},
        "module": "CALC_CONFIGURATOR",
        "action": "prepare_calculation",
        "payload": payload,
    }


class PrepareCalculationLayeredNodePrototypeTests(unittest.TestCase):
    def test_selected_demo_case_returns_layered_node_summary(self):
        req = _request_payload(
            constructive_family="KZO_WELDED",
            cell_role="VACUUM_BREAKER",
            cell_position="LEFT_END",
            node="INSULATOR_SYSTEM",
        )
        response = prepare_calculation(req)
        self.assertEqual(response["status"], "success")
        data = response["data"]
        self.assertIn("layered_node_summary", data)
        summary = data["layered_node_summary"]
        self.assertEqual(summary["constructive_family"], "KZO_WELDED")
        self.assertEqual(summary["cell_role"], "VACUUM_BREAKER")
        self.assertEqual(summary["cell_position"], "LEFT_END")
        self.assertEqual(summary["node"], "INSULATOR_SYSTEM")
        for key in (
            "placement_points",
            "presence_rules_result",
            "primary_components",
            "dependent_hardware",
            "aggregate_bom",
        ):
            self.assertIn(key, summary)

    def test_non_selected_case_does_not_return_fake_summary(self):
        req = _request_payload(
            constructive_family="KZO_BOLTED",
            cell_role="VACUUM_BREAKER",
            cell_position="LEFT_END",
            node="INSULATOR_SYSTEM",
        )
        response = prepare_calculation(req)
        self.assertEqual(response["status"], "success")
        self.assertNotIn("layered_node_summary", response["data"])

    def test_existing_prepare_calculation_response_still_works(self):
        response = prepare_calculation(_request_payload())
        self.assertEqual(response["status"], "success")
        self.assertIn("basic_result_summary", response["data"])
        self.assertIn("engineering_burden_summary", response["data"])


if __name__ == "__main__":
    unittest.main()
