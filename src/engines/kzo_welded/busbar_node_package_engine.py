from __future__ import annotations

from typing import Any

from src.engines.kzo_welded.busbar_evaluation_engine import (
    STATUS_ENGINEERING_REQUIRED,
    STATUS_FAIL,
    STATUS_INCOMPLETE,
    STATUS_PASS,
)

# DOC 37 Slice 01 implementation boundary:
# node geometry + joint stack readiness only.
# This module must not implement fastener selection, BOM, pricing, CAD, DB, GAS, or API logic.

FAILURE_DOC36_SELECTION_NOT_PASS = "DOC36_SELECTION_NOT_PASS"
FAILURE_PHASE_LENGTH_MISSING = "PHASE_LENGTH_MISSING"
FAILURE_CONNECTION_POINT_COUNT_MISSING = "CONNECTION_POINT_COUNT_MISSING"
FAILURE_PHASE_CONNECTION_MISMATCH = "PHASE_CONNECTION_MISMATCH"
FAILURE_JOINT_STACK_THICKNESS_MISSING = "JOINT_STACK_THICKNESS_MISSING"
FAILURE_MAIN_BUSBAR_THICKNESS_MISSING = "MAIN_BUSBAR_THICKNESS_MISSING"
FAILURE_EQUIPMENT_TERMINAL_THICKNESS_MISSING = "EQUIPMENT_TERMINAL_THICKNESS_MISSING"
FAILURE_NODE_PACKAGE_INCOMPLETE = "NODE_PACKAGE_INCOMPLETE"

GROUP_BUSBAR_SIDE = "BUSBAR_SIDE_CONNECTIONS"
GROUP_EQUIPMENT_SIDE = "EQUIPMENT_SIDE_CONNECTIONS"
REQUIRED_GROUP_IDS = (GROUP_BUSBAR_SIDE, GROUP_EQUIPMENT_SIDE)


def _is_missing(value: Any) -> bool:
    return value is None or (isinstance(value, str) and value.strip() == "")


def _is_positive_mm(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def _base_result(evaluation_input: dict[str, Any]) -> dict[str, Any]:
    phase_lengths = {
        "L1_mm": evaluation_input.get("phase_length_l1_mm"),
        "L2_mm": evaluation_input.get("phase_length_l2_mm"),
        "L3_mm": evaluation_input.get("phase_length_l3_mm"),
    }
    return {
        "status": STATUS_INCOMPLETE,
        "busbar_node_id": evaluation_input.get("busbar_node_id"),
        "phase_count": evaluation_input.get("phase_count"),
        "phase_lengths": phase_lengths,
        "total_busbar_length_mm": None,
        "connection_point_groups": [],
        "node_fastener_lines": [],
        "node_material_lines": [],
        "failure_code": None,
        "notes": list(evaluation_input.get("notes") or []),
    }


def evaluate_busbar_node_geometry_and_stack(evaluation_input: dict[str, Any]) -> dict[str, Any]:
    """DOC 37 Slice 01 — node geometry and joint stack only.

    Deterministic pure function with no side effects.
    """
    result = _base_result(evaluation_input)

    doc36 = evaluation_input.get("doc36") or {}
    doc36_status = doc36.get("status") or evaluation_input.get("doc36_status")
    if doc36_status != STATUS_PASS:
        result["status"] = (
            STATUS_ENGINEERING_REQUIRED if doc36_status == STATUS_ENGINEERING_REQUIRED else STATUS_INCOMPLETE
        )
        result["failure_code"] = FAILURE_DOC36_SELECTION_NOT_PASS
        result["notes"].append("DOC 36 status is not PASS, so DOC 37 Slice 01 cannot return PASS.")
        return result

    phase_count = evaluation_input.get("phase_count")
    if phase_count != 3:
        result["status"] = STATUS_INCOMPLETE
        result["failure_code"] = FAILURE_NODE_PACKAGE_INCOMPLETE
        result["notes"].append("MVP Slice 01 requires phase_count = 3.")
        return result
    result["phase_count"] = phase_count

    l1 = evaluation_input.get("phase_length_l1_mm")
    l2 = evaluation_input.get("phase_length_l2_mm")
    l3 = evaluation_input.get("phase_length_l3_mm")
    if not all(_is_positive_mm(v) for v in (l1, l2, l3)):
        result["status"] = STATUS_INCOMPLETE
        result["failure_code"] = FAILURE_PHASE_LENGTH_MISSING
        result["notes"].append("Phase lengths must be positive numeric values in millimeters.")
        return result

    result["phase_lengths"] = {"L1_mm": l1, "L2_mm": l2, "L3_mm": l3}
    result["total_busbar_length_mm"] = l1 + l2 + l3

    groups = evaluation_input.get("connection_point_groups")
    if not isinstance(groups, list):
        result["status"] = STATUS_INCOMPLETE
        result["failure_code"] = FAILURE_CONNECTION_POINT_COUNT_MISSING
        result["notes"].append("connection_point_groups must be provided as a list.")
        return result

    group_by_id: dict[str, dict[str, Any]] = {}
    for group in groups:
        if isinstance(group, dict):
            group_id = group.get("group_id")
            if isinstance(group_id, str):
                group_by_id[group_id] = group

    for required_group_id in REQUIRED_GROUP_IDS:
        group = group_by_id.get(required_group_id)
        if not group:
            result["status"] = STATUS_INCOMPLETE
            result["failure_code"] = FAILURE_CONNECTION_POINT_COUNT_MISSING
            result["notes"].append(f"Missing required connection group: {required_group_id}.")
            return result

        connection_point_count = group.get("connection_point_count")
        if not isinstance(connection_point_count, int) or connection_point_count <= 0:
            result["status"] = STATUS_INCOMPLETE
            result["failure_code"] = FAILURE_CONNECTION_POINT_COUNT_MISSING
            result["notes"].append(f"Invalid connection_point_count for {required_group_id}.")
            return result

        if connection_point_count != phase_count:
            result["status"] = STATUS_ENGINEERING_REQUIRED
            result["failure_code"] = FAILURE_PHASE_CONNECTION_MISMATCH
            result["notes"].append(
                f"connection_point_count for {required_group_id} must match phase_count ({phase_count})."
            )
            return result

    node_busbar_thickness_mm = evaluation_input.get("node_busbar_thickness_mm")
    if not _is_positive_mm(node_busbar_thickness_mm):
        result["status"] = STATUS_INCOMPLETE
        result["failure_code"] = FAILURE_JOINT_STACK_THICKNESS_MISSING
        result["notes"].append("node_busbar_thickness_mm must be a positive numeric value in millimeters.")
        return result

    main_busbar_pack_thickness_mm = evaluation_input.get("main_busbar_pack_thickness_mm")
    if not _is_positive_mm(main_busbar_pack_thickness_mm):
        result["status"] = STATUS_INCOMPLETE
        result["failure_code"] = FAILURE_MAIN_BUSBAR_THICKNESS_MISSING
        result["notes"].append("main_busbar_pack_thickness_mm must be a positive numeric value in millimeters.")
        return result

    equipment_terminal_thickness_mm = evaluation_input.get("equipment_terminal_thickness_mm")
    if not _is_positive_mm(equipment_terminal_thickness_mm):
        result["status"] = STATUS_INCOMPLETE
        result["failure_code"] = FAILURE_EQUIPMENT_TERMINAL_THICKNESS_MISSING
        result["notes"].append("equipment_terminal_thickness_mm must be a positive numeric value in millimeters.")
        return result

    busbar_stack = node_busbar_thickness_mm + main_busbar_pack_thickness_mm
    equipment_stack = node_busbar_thickness_mm + equipment_terminal_thickness_mm
    if not (_is_positive_mm(busbar_stack) and _is_positive_mm(equipment_stack)):
        result["status"] = STATUS_INCOMPLETE
        result["failure_code"] = FAILURE_JOINT_STACK_THICKNESS_MISSING
        result["notes"].append("joint_stack_thickness_mm could not be resolved for all required groups.")
        return result

    result["connection_point_groups"] = [
        {
            "group_id": GROUP_BUSBAR_SIDE,
            "connection_point_count": group_by_id[GROUP_BUSBAR_SIDE]["connection_point_count"],
            "joint_stack_thickness_mm": busbar_stack,
            "stack_status": STATUS_PASS,
            "failure_code": None,
        },
        {
            "group_id": GROUP_EQUIPMENT_SIDE,
            "connection_point_count": group_by_id[GROUP_EQUIPMENT_SIDE]["connection_point_count"],
            "joint_stack_thickness_mm": equipment_stack,
            "stack_status": STATUS_PASS,
            "failure_code": None,
        },
    ]
    result["status"] = STATUS_PASS
    result["failure_code"] = None
    # Gemini guardrail: Slice 01 must not produce fastener output.
    result["node_fastener_lines"] = []
    result["node_material_lines"] = []
    return result
