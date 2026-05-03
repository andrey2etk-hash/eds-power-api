from __future__ import annotations

from typing import Any

from src.engines.kzo_welded.busbar_evaluation_engine import (
    STATUS_ENGINEERING_REQUIRED,
    STATUS_FAIL,
    STATUS_INCOMPLETE,
    STATUS_PASS,
    STATUS_SELECTION_REQUIRED,
)
from src.engines.kzo_welded.busbar_node_package_engine import (
    GROUP_BUSBAR_SIDE,
    GROUP_EQUIPMENT_SIDE,
)

# DOC 37 Slice 02 implementation boundary:
# local node fastener selection only.
# No BOM aggregation, pricing, CAD, DB, GAS, or API logic is allowed here.

FAILURE_SLICE01_GEOMETRY_NOT_PASS = "SLICE01_GEOMETRY_NOT_PASS"
FAILURE_NODE_PACKAGE_INCOMPLETE = "NODE_PACKAGE_INCOMPLETE"
FAILURE_FASTENER_RULE_MISSING = "FASTENER_RULE_MISSING"
FAILURE_FASTENER_DATA_MISSING = "FASTENER_DATA_MISSING"
FAILURE_FASTENER_DEFAULT_NOT_APPROVED = "FASTENER_DEFAULT_NOT_APPROVED"
FAILURE_HARDWARE_STACK_SUM_MISSING = "HARDWARE_STACK_SUM_MISSING"
FAILURE_THREAD_PITCH_MISSING = "THREAD_PITCH_MISSING"
FAILURE_SAFETY_MARGIN_MISSING = "SAFETY_MARGIN_MISSING"
FAILURE_BOLT_LENGTH_NOT_FOUND = "BOLT_LENGTH_NOT_FOUND"
FAILURE_BOLT_LENGTH_AMBIGUOUS = "BOLT_LENGTH_AMBIGUOUS"
FAILURE_FASTENER_PACKAGE_AMBIGUOUS = "FASTENER_PACKAGE_AMBIGUOUS"
FAILURE_NUT_DATA_MISSING = "NUT_DATA_MISSING"
FAILURE_WASHER_DATA_MISSING = "WASHER_DATA_MISSING"
FAILURE_FASTENER_REGISTRY_VERSION_MISSING = "FASTENER_REGISTRY_VERSION_MISSING"
FAILURE_INTERFACE_FASTENER_CONFLICT = "INTERFACE_FASTENER_CONFLICT"

REQUIRED_GROUP_IDS = (GROUP_BUSBAR_SIDE, GROUP_EQUIPMENT_SIDE)
REQUIRED_FASTENER_REGISTRY_VERSION_KEYS = (
    "fastener_registry_version",
    "joint_stack_rule_registry_version",
    "washer_package_rule_registry_version",
)


def _is_missing(value: Any) -> bool:
    return value is None or (isinstance(value, str) and value.strip() == "")


def _is_positive_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def _base_result(evaluation_input: dict[str, Any]) -> dict[str, Any]:
    slice01 = evaluation_input.get("slice01_output") or {}
    return {
        "status": STATUS_INCOMPLETE,
        "busbar_node_id": slice01.get("busbar_node_id") or evaluation_input.get("busbar_node_id"),
        "connection_point_groups": [],
        "node_fastener_lines": [],
        "failure_code": None,
        "notes": list(evaluation_input.get("notes") or []),
        "registry_versions": dict(evaluation_input.get("registry_versions") or {}),
    }


def _choose_bolt_candidate(candidates: list[dict[str, Any]], selection_policy: Any) -> tuple[dict[str, Any] | None, str | None]:
    if not candidates:
        return None, FAILURE_BOLT_LENGTH_NOT_FOUND
    if len(candidates) == 1:
        return candidates[0], None
    if selection_policy == "MIN_LENGTH":
        return sorted(candidates, key=lambda x: float(x.get("length_mm")))[0], None
    return None, FAILURE_BOLT_LENGTH_AMBIGUOUS


def evaluate_busbar_node_fastener_selection(evaluation_input: dict[str, Any]) -> dict[str, Any]:
    """DOC 37 Slice 02 — fastener selection for one local node package.

    Deterministic pure function consuming prepared registry truth.
    """
    result = _base_result(evaluation_input)
    slice01_output = evaluation_input.get("slice01_output") or {}
    if slice01_output.get("status") != STATUS_PASS:
        result["status"] = STATUS_INCOMPLETE
        result["failure_code"] = FAILURE_SLICE01_GEOMETRY_NOT_PASS
        result["notes"].append("Slice 01 status is not PASS.")
        return result

    registry_versions = result["registry_versions"]
    missing_registry_versions = [
        k for k in REQUIRED_FASTENER_REGISTRY_VERSION_KEYS if _is_missing(registry_versions.get(k))
    ]
    if missing_registry_versions:
        result["status"] = STATUS_INCOMPLETE
        result["failure_code"] = FAILURE_FASTENER_REGISTRY_VERSION_MISSING
        result["notes"].append("Required fastener registry versions are missing.")
        return result

    input_groups = slice01_output.get("connection_point_groups")
    if not isinstance(input_groups, list):
        result["status"] = STATUS_INCOMPLETE
        result["failure_code"] = FAILURE_NODE_PACKAGE_INCOMPLETE
        result["notes"].append("Slice 01 connection_point_groups are missing.")
        return result

    groups_by_id: dict[str, dict[str, Any]] = {}
    for group in input_groups:
        if isinstance(group, dict) and isinstance(group.get("group_id"), str):
            groups_by_id[group["group_id"]] = group

    for required_group in REQUIRED_GROUP_IDS:
        if required_group not in groups_by_id:
            result["status"] = STATUS_INCOMPLETE
            result["failure_code"] = FAILURE_NODE_PACKAGE_INCOMPLETE
            result["notes"].append(f"Missing required group: {required_group}.")
            return result

    joint_stack_rules = evaluation_input.get("joint_stack_rules") or []
    washer_package_rules = evaluation_input.get("washer_package_rules") or []
    fastener_registry_items = evaluation_input.get("fastener_registry_items") or []
    equipment_interface_constraints = evaluation_input.get("equipment_interface_constraints") or {}

    if not isinstance(joint_stack_rules, list) or not isinstance(washer_package_rules, list) or not isinstance(
        fastener_registry_items, list
    ):
        result["status"] = STATUS_INCOMPLETE
        result["failure_code"] = FAILURE_FASTENER_RULE_MISSING
        result["notes"].append("Prepared registry collections must be lists.")
        return result

    washer_rule_by_id = {
        item.get("washer_package_rule_id"): item
        for item in washer_package_rules
        if isinstance(item, dict) and item.get("is_active") is True
    }

    fastener_item_by_id = {
        item.get("fastener_id"): item
        for item in fastener_registry_items
        if isinstance(item, dict) and item.get("is_active") is True and isinstance(item.get("fastener_id"), str)
    }

    active_bolts = [
        item
        for item in fastener_registry_items
        if isinstance(item, dict)
        and item.get("item_type") == "BOLT"
        and item.get("is_active") is True
        and _is_positive_number(item.get("diameter_mm"))
        and _is_positive_number(item.get("length_mm"))
    ]

    group_outputs: list[dict[str, Any]] = []
    node_fastener_lines: list[dict[str, Any]] = []
    for group_id in REQUIRED_GROUP_IDS:
        group = groups_by_id[group_id]
        connection_point_count = group.get("connection_point_count")
        joint_stack_thickness_mm = group.get("joint_stack_thickness_mm")
        if not isinstance(connection_point_count, int) or connection_point_count <= 0:
            result["status"] = STATUS_INCOMPLETE
            result["failure_code"] = FAILURE_NODE_PACKAGE_INCOMPLETE
            result["notes"].append(f"Invalid connection_point_count for {group_id}.")
            return result
        if not _is_positive_number(joint_stack_thickness_mm):
            result["status"] = STATUS_INCOMPLETE
            result["failure_code"] = FAILURE_FASTENER_DATA_MISSING
            result["notes"].append(f"joint_stack_thickness_mm missing/invalid for {group_id}.")
            return result

        candidate_rules = [
            r
            for r in joint_stack_rules
            if isinstance(r, dict) and r.get("is_active") is True and r.get("connection_group_type") == group_id
        ]
        if not candidate_rules:
            result["status"] = STATUS_INCOMPLETE
            result["failure_code"] = FAILURE_FASTENER_RULE_MISSING
            result["notes"].append(f"No active joint stack rule for {group_id}.")
            return result
        if len(candidate_rules) > 1:
            with_policy = [r for r in candidate_rules if r.get("selection_policy")]
            if len(with_policy) != 1:
                result["status"] = STATUS_SELECTION_REQUIRED
                result["failure_code"] = FAILURE_FASTENER_PACKAGE_AMBIGUOUS
                result["notes"].append(f"Ambiguous joint stack rules for {group_id}.")
                return result
            joint_rule = with_policy[0]
        else:
            joint_rule = candidate_rules[0]

        allowed_bolt_diameter_mm = joint_rule.get("allowed_bolt_diameter_mm")
        if not _is_positive_number(allowed_bolt_diameter_mm):
            result["status"] = STATUS_INCOMPLETE
            result["failure_code"] = FAILURE_FASTENER_RULE_MISSING
            result["notes"].append(f"allowed_bolt_diameter_mm missing in joint rule for {group_id}.")
            return result

        interface_constraints = equipment_interface_constraints.get(group_id) or equipment_interface_constraints
        if interface_constraints:
            interface_diameter = interface_constraints.get("allowed_bolt_diameter_mm")
            interface_bolt_type = interface_constraints.get("required_bolt_type")
            if _is_positive_number(interface_diameter) and float(interface_diameter) != float(allowed_bolt_diameter_mm):
                result["status"] = STATUS_FAIL
                result["failure_code"] = FAILURE_INTERFACE_FASTENER_CONFLICT
                result["notes"].append(f"Interface diameter conflicts with joint rule for {group_id}.")
                return result
            required_bolt_type = joint_rule.get("required_bolt_type")
            if interface_bolt_type and required_bolt_type and interface_bolt_type != required_bolt_type:
                result["status"] = STATUS_FAIL
                result["failure_code"] = FAILURE_INTERFACE_FASTENER_CONFLICT
                result["notes"].append(f"Interface bolt type conflicts with joint rule for {group_id}.")
                return result

        washer_package_rule_id = joint_rule.get("washer_package_rule_id")
        if _is_missing(washer_package_rule_id):
            result["status"] = STATUS_INCOMPLETE
            result["failure_code"] = FAILURE_FASTENER_DEFAULT_NOT_APPROVED
            result["notes"].append(f"washer_package_rule_id missing for {group_id}.")
            return result

        washer_rule = washer_rule_by_id.get(washer_package_rule_id)
        if not washer_rule:
            result["status"] = STATUS_INCOMPLETE
            result["failure_code"] = FAILURE_FASTENER_DEFAULT_NOT_APPROVED
            result["notes"].append(f"No active washer package rule for {group_id}.")
            return result

        hardware_stack_sum_mm = washer_rule.get("hardware_stack_sum_mm")
        if not _is_positive_number(hardware_stack_sum_mm):
            result["status"] = STATUS_INCOMPLETE
            result["failure_code"] = FAILURE_HARDWARE_STACK_SUM_MISSING
            result["notes"].append(f"hardware_stack_sum_mm missing for {group_id}.")
            return result

        nut_fastener_id = washer_rule.get("nut_fastener_id")
        if _is_missing(nut_fastener_id) or nut_fastener_id not in fastener_item_by_id:
            result["status"] = STATUS_INCOMPLETE
            result["failure_code"] = FAILURE_NUT_DATA_MISSING
            result["notes"].append(f"Nut data missing for {group_id}.")
            return result

        flat_washer_fastener_id = washer_rule.get("flat_washer_fastener_id")
        disc_spring_washer_fastener_id = washer_rule.get("disc_spring_washer_fastener_id")
        if _is_missing(flat_washer_fastener_id) or _is_missing(disc_spring_washer_fastener_id):
            result["status"] = STATUS_INCOMPLETE
            result["failure_code"] = FAILURE_WASHER_DATA_MISSING
            result["notes"].append(f"Washer references missing for {group_id}.")
            return result
        if flat_washer_fastener_id not in fastener_item_by_id or disc_spring_washer_fastener_id not in fastener_item_by_id:
            result["status"] = STATUS_INCOMPLETE
            result["failure_code"] = FAILURE_WASHER_DATA_MISSING
            result["notes"].append(f"Washer data missing for {group_id}.")
            return result

        thread_pitch_mm = joint_rule.get("thread_pitch_mm")
        if not _is_positive_number(thread_pitch_mm):
            candidate_thread_pitches = sorted(
                {
                    float(b["thread_pitch_mm"])
                    for b in active_bolts
                    if float(b["diameter_mm"]) == float(allowed_bolt_diameter_mm)
                    and _is_positive_number(b.get("thread_pitch_mm"))
                }
            )
            if len(candidate_thread_pitches) == 1:
                thread_pitch_mm = candidate_thread_pitches[0]
            else:
                result["status"] = STATUS_INCOMPLETE
                result["failure_code"] = FAILURE_THREAD_PITCH_MISSING
                result["notes"].append(f"thread_pitch_mm missing/ambiguous for {group_id}.")
                return result

        safety_margin_mm = joint_rule.get("safety_margin_mm")
        if not isinstance(safety_margin_mm, (int, float)) or isinstance(safety_margin_mm, bool):
            result["status"] = STATUS_INCOMPLETE
            result["failure_code"] = FAILURE_SAFETY_MARGIN_MISSING
            result["notes"].append(f"safety_margin_mm missing for {group_id}.")
            return result
        if safety_margin_mm < 0:
            result["status"] = STATUS_INCOMPLETE
            result["failure_code"] = FAILURE_SAFETY_MARGIN_MISSING
            result["notes"].append(f"safety_margin_mm cannot be negative for {group_id}.")
            return result

        thread_allowance_rule = joint_rule.get("thread_allowance_rule")
        thread_allowance_mm: float | None = None
        if isinstance(thread_allowance_rule, dict):
            explicit_allowance = thread_allowance_rule.get("value_mm")
            if _is_positive_number(explicit_allowance):
                thread_allowance_mm = float(explicit_allowance)
        if thread_allowance_mm is None:
            thread_allowance_mm = 2 * float(thread_pitch_mm)

        required_bolt_length_mm = (
            float(joint_stack_thickness_mm)
            + float(hardware_stack_sum_mm)
            + float(thread_allowance_mm)
            + float(safety_margin_mm)
        )

        matching_bolts = [
            b
            for b in active_bolts
            if float(b.get("diameter_mm")) == float(allowed_bolt_diameter_mm)
            and float(b.get("length_mm")) >= float(required_bolt_length_mm)
        ]
        selected_bolt, bolt_failure = _choose_bolt_candidate(matching_bolts, joint_rule.get("selection_policy"))
        if bolt_failure == FAILURE_BOLT_LENGTH_NOT_FOUND:
            result["status"] = STATUS_INCOMPLETE
            result["failure_code"] = FAILURE_BOLT_LENGTH_NOT_FOUND
            result["notes"].append(f"No active bolt candidates for {group_id}.")
            return result
        if bolt_failure == FAILURE_BOLT_LENGTH_AMBIGUOUS:
            result["status"] = STATUS_SELECTION_REQUIRED
            result["failure_code"] = FAILURE_BOLT_LENGTH_AMBIGUOUS
            result["notes"].append(f"Multiple bolt candidates for {group_id} without selection_policy.")
            return result

        assert selected_bolt is not None
        selected_bolt_id = selected_bolt.get("fastener_id")
        if _is_missing(selected_bolt_id):
            result["status"] = STATUS_INCOMPLETE
            result["failure_code"] = FAILURE_FASTENER_DATA_MISSING
            result["notes"].append(f"Selected bolt has no fastener_id for {group_id}.")
            return result

        group_outputs.append(
            {
                "group_id": group_id,
                "connection_point_count": connection_point_count,
                "joint_stack_thickness_mm": joint_stack_thickness_mm,
                "required_bolt_length_mm": required_bolt_length_mm,
                "selected_bolt_fastener_id": selected_bolt_id,
                "washer_package_rule_id": washer_package_rule_id,
                "fastener_selection_status": STATUS_PASS,
                "failure_code": None,
            }
        )

        node_fastener_lines.append(
            {
                "item_id": selected_bolt_id,
                "item_type": "BOLT",
                "quantity": connection_point_count,
                "source_group": group_id,
                "source_connection_count": connection_point_count,
                "registry_source": "FASTENER_REGISTRY",
            }
        )

    result["status"] = STATUS_PASS
    result["failure_code"] = None
    result["connection_point_groups"] = group_outputs
    result["node_fastener_lines"] = node_fastener_lines
    return result
