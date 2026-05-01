import unittest
from unittest.mock import patch

from main import save_snapshot


def _normalized_row(request_id: str) -> dict:
    return {
        "product_type": "KZO",
        "snapshot_version": "KZO_MVP_SNAPSHOT_V1",
        "run_status": "SUCCESS",
        "timestamp_basis": "2026-05-01T00:00:00+00:00",
        "logic_version": "KZO_MVP_V1",
        "request_metadata": {
            "request_id": request_id,
            "api_version": "0.1.0",
            "logic_version": "KZO_MVP_V1",
            "execution_time_ms": 1,
        },
        "normalized_input": {"object_number": "7445-B"},
        "structural_composition_summary": {"ok": True},
        "physical_summary": {"ok": True},
        "physical_topology_summary": {"ok": True},
        "engineering_class_summary": {"ok": True},
        "engineering_burden_summary": {"ok": True},
        "failure": None,
    }


class SaveSnapshotDuplicateProtectionTests(unittest.TestCase):
    def test_first_request_stores(self):
        with (
            patch("main.validate_kzo_mvp_snapshot_v1", return_value=(_normalized_row("req-1"), None, {"l1_snapshot_version_ok": True})),
            patch("main.find_snapshot_by_request_id", return_value=(None, None, None)),
            patch("main.insert_snapshot_row", return_value=("snap-1", "2026-05-01T10:00:00+00:00", None)),
        ):
            payload = save_snapshot({}, x_eds_client_type="GAS")

        self.assertEqual(payload["status"], "SUCCESS")
        self.assertEqual(payload["persistence_status"], "STORED")
        self.assertEqual(payload["snapshot_id"], "snap-1")

    def test_duplicate_request_is_blocked(self):
        with (
            patch("main.validate_kzo_mvp_snapshot_v1", return_value=(_normalized_row("req-dup"), None, {"l1_snapshot_version_ok": True})),
            patch("main.find_snapshot_by_request_id", return_value=("snap-existing", "2026-05-01T10:01:00+00:00", None)),
            patch("main.insert_snapshot_row") as insert_mock,
        ):
            payload = save_snapshot({}, x_eds_client_type="GAS")

        self.assertEqual(payload["status"], "FAILED")
        self.assertEqual(payload["persistence_status"], "DUPLICATE_REJECTED")
        self.assertEqual(payload["error_code"], "SNAPSHOT_DUPLICATE_REJECTED")
        self.assertEqual(payload["snapshot_id"], "snap-existing")
        insert_mock.assert_not_called()

    def test_non_duplicate_request_still_stores(self):
        with (
            patch("main.validate_kzo_mvp_snapshot_v1", return_value=(_normalized_row("req-2"), None, {"l1_snapshot_version_ok": True})),
            patch("main.find_snapshot_by_request_id", return_value=(None, None, None)),
            patch("main.insert_snapshot_row", return_value=("snap-2", "2026-05-01T10:02:00+00:00", None)),
        ):
            payload = save_snapshot({}, x_eds_client_type="GAS")

        self.assertEqual(payload["status"], "SUCCESS")
        self.assertEqual(payload["persistence_status"], "STORED")
        self.assertEqual(payload["snapshot_id"], "snap-2")
