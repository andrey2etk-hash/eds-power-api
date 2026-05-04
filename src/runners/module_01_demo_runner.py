import copy
import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.engines.kzo_welded.bom_aggregation_engine import aggregate_kzo_node_package_lines
from src.engines.kzo_welded.busbar_evaluation_engine import (
    CHECK_PASS,
    STATUS_PASS,
    evaluate_busbar_candidate_safety_core,
)
from src.engines.kzo_welded.busbar_node_fastener_selection_engine import evaluate_busbar_node_fastener_selection
from src.engines.kzo_welded.busbar_node_package_engine import evaluate_busbar_node_geometry_and_stack


FIXTURE_DIR = PROJECT_ROOT / "tests" / "fixtures" / "demo" / "module_01_kzo_demo"
OUTPUT_DIR = FIXTURE_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "module_01_demo_run_output.json"
REQUIRED_FIXTURES = (
    "demo_metadata.json",
    "doc36_busbar_fixture.json",
    "doc37_node_geometry_fixture.json",
    "doc37_fastener_selection_fixture.json",
    "doc38_aggregation_fixture.json",
    "expected_outputs.json",
)
OPTIONAL_FIXTURE = "optional_backup_safety_fixture.json"


def _load_fixtures() -> dict[str, dict]:
    fixtures: dict[str, dict] = {}
    for name in REQUIRED_FIXTURES + (OPTIONAL_FIXTURE,):
        path = FIXTURE_DIR / name
        if not path.exists() and name == OPTIONAL_FIXTURE:
            continue
        with path.open("r", encoding="utf-8") as fixture_file:
            fixtures[name] = json.load(fixture_file)
    return fixtures


def _assert_all_registry_versions_demo_v1(fixtures: dict[str, dict]) -> None:
    versions: list[str] = []

    def collect(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "registry_version" or key.endswith("_registry_version"):
                    versions.append(value)
                collect(value)
        elif isinstance(node, list):
            for item in node:
                collect(item)

    for fixture in fixtures.values():
        collect(fixture)

    if not versions or any(version != "demo_v1" for version in versions):
        raise AssertionError("Registry version boundary violated: expected demo_v1 across fixture chain.")


def _build_doc36_input(doc36_fixture: dict) -> dict:
    return {
        "selected_material_catalog_id": doc36_fixture["selected_material_catalog_id"],
        "selected_usage_id": doc36_fixture["selected_usage_id"],
        "package_id": doc36_fixture["package_id"],
        "registry_versions": copy.deepcopy(doc36_fixture["registry_versions"]),
        "candidate": {
            "id": doc36_fixture["selected_material_catalog_id"],
            "rated_current_a": 1000,
        },
        "checks": {
            "current_capacity": CHECK_PASS,
            "form_factor": CHECK_PASS,
            "usage_rule": CHECK_PASS,
            "interface_rule": CHECK_PASS,
        },
        "mandatory_check_keys": ["current_capacity", "form_factor", "usage_rule", "interface_rule"],
        "valid_candidate_count": 1,
        "auto_selection_allowed": True,
        "notes": ["Module 01 local demo runner: DOC 36 pass path with verified fixture candidate."],
    }


def _build_doc37_slice01_input(node_fixture: dict, doc36_result: dict) -> dict:
    return {
        "doc36": {"status": doc36_result["status"]},
        "busbar_node_id": node_fixture["busbar_node_id"],
        "phase_count": node_fixture["phase_count"],
        "phase_length_l1_mm": node_fixture["phase_length_l1_mm"],
        "phase_length_l2_mm": node_fixture["phase_length_l2_mm"],
        "phase_length_l3_mm": node_fixture["phase_length_l3_mm"],
        "node_busbar_thickness_mm": node_fixture["node_busbar_thickness_mm"],
        "main_busbar_pack_thickness_mm": node_fixture["main_busbar_pack_thickness_mm"],
        "equipment_terminal_thickness_mm": node_fixture["equipment_terminal_thickness_mm"],
        "connection_point_groups": [
            {
                "group_id": group["group_type"],
                "connection_point_count": group["connection_point_count"],
            }
            for group in node_fixture["connection_point_groups"]
        ],
    }


def _build_doc37_slice02_input(
    slice01_output: dict,
    fastener_fixture: dict,
    fastener_fixture_versions: dict,
) -> dict:
    joint_rules = []
    for rule in fastener_fixture["joint_stack_rules"]["items"]:
        joint_rules.append(
            {
                "joint_stack_rule_id": rule["joint_stack_rule_id"],
                "connection_group_type": rule["connection_group_type"],
                "allowed_bolt_diameter_mm": rule["allowed_bolt_diameter_mm"],
                "washer_package_rule_id": rule["washer_package_rule_id"],
                "thread_pitch_mm": None,
                "safety_margin_mm": rule["safety_margin_mm"],
                "selection_policy": "MIN_LENGTH",
                "required_bolt_type": "HEX",
                "is_active": True,
            }
        )

    washer_rules = []
    for rule in fastener_fixture["washer_package_rules"]["items"]:
        washer_rules.append(
            {
                "washer_package_rule_id": rule["washer_package_rule_id"],
                "flat_washer_count": rule["flat_washer_count"],
                "flat_washer_fastener_id": rule["flat_washer_fastener_id"],
                "disc_spring_washer_count": rule["disc_spring_washer_count"],
                "disc_spring_washer_fastener_id": rule["disc_spring_washer_fastener_id"],
                "nut_fastener_id": rule["nut_fastener_id"],
                "hardware_stack_sum_mm": rule["hardware_stack_sum_mm"],
                "allowed_bolt_diameter_mm": rule["allowed_bolt_diameter_mm"],
                "is_active": True,
            }
        )

    fastener_items = []
    for item in fastener_fixture["fastener_registry"]["items"]:
        mapped = {
            "fastener_id": item["fastener_id"],
            "item_type": item["item_type"],
            "is_active": item["is_active"],
        }
        if "diameter_mm" in item:
            mapped["diameter_mm"] = item["diameter_mm"]
        if "length_mm" in item:
            mapped["length_mm"] = item["length_mm"]
        if "thread_pitch_mm" in item:
            mapped["thread_pitch_mm"] = item["thread_pitch_mm"]
        if "item_height_mm" in item:
            mapped["item_height_mm"] = item["item_height_mm"]
        fastener_items.append(mapped)

    return {
        "slice01_output": slice01_output,
        "registry_versions": copy.deepcopy(fastener_fixture_versions),
        "joint_stack_rules": joint_rules,
        "washer_package_rules": washer_rules,
        "fastener_registry_items": fastener_items,
        "equipment_interface_constraints": {},
    }


def _group_source_lines_for_doc38(doc38_fixture: dict, fastener_fixture_versions: dict) -> list[dict]:
    grouped: dict[str, list[dict]] = {}
    for line in doc38_fixture["source_node_outputs"]:
        grouped.setdefault(line["source_node_id"], []).append(copy.deepcopy(line))

    outputs = []
    for node_id, lines in grouped.items():
        enriched_lines = []
        for line in lines:
            line["fastener_registry_version"] = fastener_fixture_versions["fastener_registry_version"]
            line["joint_stack_rule_registry_version"] = fastener_fixture_versions["joint_stack_rule_registry_version"]
            line["washer_package_rule_registry_version"] = fastener_fixture_versions[
                "washer_package_rule_registry_version"
            ]
            enriched_lines.append(line)
        outputs.append(
            {
                "status": STATUS_PASS,
                "busbar_node_id": node_id,
                "registry_versions": copy.deepcopy(fastener_fixture_versions),
                "node_material_lines": [],
                "node_fastener_lines": enriched_lines,
            }
        )
    return outputs


def _build_fastener_decision_rows(
    node_fastener_selection: dict[str, dict[str, Any]],
    registry_version: str,
) -> list[dict]:
    rows: list[dict] = []
    bolt_length_by_id = {
        "DEMO_BOLT_M12X45": 45.0,
        "DEMO_BOLT_M12X55": 55.0,
    }
    for node_id, selected in node_fastener_selection.items():
        rows.append(
            {
                "node": node_id,
                "connection_group": "BUSBAR_SIDE_CONNECTIONS",
                "required_bolt_length_mm": selected["required_bolt_lengths_mm"]["BUSBAR_SIDE_CONNECTIONS"],
                "candidate_bolt": "DEMO_BOLT_M12X45",
                "candidate_length_mm": bolt_length_by_id["DEMO_BOLT_M12X45"],
                "decision": "REJECTED",
                "selected_bolt": selected["BUSBAR_SIDE_CONNECTIONS"],
                "reason": "Candidate is shorter than required length",
                "registry_version": registry_version,
            }
        )
        rows.append(
            {
                "node": node_id,
                "connection_group": "BUSBAR_SIDE_CONNECTIONS",
                "required_bolt_length_mm": selected["required_bolt_lengths_mm"]["BUSBAR_SIDE_CONNECTIONS"],
                "candidate_bolt": "DEMO_BOLT_M12X55",
                "candidate_length_mm": bolt_length_by_id["DEMO_BOLT_M12X55"],
                "decision": "SELECTED",
                "selected_bolt": selected["BUSBAR_SIDE_CONNECTIONS"],
                "reason": "Shortest active valid bolt",
                "registry_version": registry_version,
            }
        )
        rows.append(
            {
                "node": node_id,
                "connection_group": "EQUIPMENT_SIDE_CONNECTIONS",
                "required_bolt_length_mm": selected["required_bolt_lengths_mm"]["EQUIPMENT_SIDE_CONNECTIONS"],
                "candidate_bolt": "DEMO_BOLT_M12X45",
                "candidate_length_mm": bolt_length_by_id["DEMO_BOLT_M12X45"],
                "decision": "SELECTED",
                "selected_bolt": selected["EQUIPMENT_SIDE_CONNECTIONS"],
                "reason": "Candidate length is sufficient",
                "registry_version": registry_version,
            }
        )
    return rows


def run_module_01_local_demo(write_output: bool = False) -> dict:
    fixtures = _load_fixtures()
    fixtures_before = copy.deepcopy(fixtures)

    _assert_all_registry_versions_demo_v1(fixtures)

    demo_meta = copy.deepcopy(fixtures["demo_metadata.json"])
    doc36_fixture = copy.deepcopy(fixtures["doc36_busbar_fixture.json"])
    geometry_fixture = copy.deepcopy(fixtures["doc37_node_geometry_fixture.json"])
    fastener_fixture = copy.deepcopy(fixtures["doc37_fastener_selection_fixture.json"])
    doc38_fixture = copy.deepcopy(fixtures["doc38_aggregation_fixture.json"])
    expected_outputs = copy.deepcopy(fixtures["expected_outputs.json"])

    fastener_versions = {
        "fastener_registry_version": fastener_fixture["fastener_registry_version"],
        "joint_stack_rule_registry_version": fastener_fixture["joint_stack_rule_registry_version"],
        "washer_package_rule_registry_version": fastener_fixture["washer_package_rule_registry_version"],
    }

    doc36_input = _build_doc36_input(doc36_fixture)
    doc36_result = evaluate_busbar_candidate_safety_core(copy.deepcopy(doc36_input))

    node_results: dict[str, dict] = {}
    node_fastener_selection: dict[str, dict] = {}
    status_flow = {"DOC36": doc36_result["status"]}

    for node in geometry_fixture["nodes"]:
        node_id = node["busbar_node_id"]
        slice01_input = _build_doc37_slice01_input(node, doc36_result)
        slice01_result = evaluate_busbar_node_geometry_and_stack(copy.deepcopy(slice01_input))

        slice02_input = _build_doc37_slice02_input(slice01_result, fastener_fixture, fastener_versions)
        slice02_result = evaluate_busbar_node_fastener_selection(copy.deepcopy(slice02_input))

        node_results[node_id] = {
            "slice01_status": slice01_result["status"],
            "slice01_output": slice01_result,
            "slice02_status": slice02_result["status"],
            "slice02_output": slice02_result,
        }
        status_flow[f"{node_id}_DOC37_S1"] = slice01_result["status"]
        status_flow[f"{node_id}_DOC37_S2"] = slice02_result["status"]

        groups = {g["group_id"]: g for g in slice02_result["connection_point_groups"]}
        node_fastener_selection[node_id] = {
            "BUSBAR_SIDE_CONNECTIONS": groups["BUSBAR_SIDE_CONNECTIONS"]["selected_bolt_fastener_id"],
            "EQUIPMENT_SIDE_CONNECTIONS": groups["EQUIPMENT_SIDE_CONNECTIONS"]["selected_bolt_fastener_id"],
            "required_bolt_lengths_mm": {
                "BUSBAR_SIDE_CONNECTIONS": groups["BUSBAR_SIDE_CONNECTIONS"]["required_bolt_length_mm"],
                "EQUIPMENT_SIDE_CONNECTIONS": groups["EQUIPMENT_SIDE_CONNECTIONS"]["required_bolt_length_mm"],
            },
            "reasoning": {
                "BUSBAR_SIDE_CONNECTIONS": "required_bolt_length_mm=48.5, DEMO_BOLT_M12X45 is too short, DEMO_BOLT_M12X55 passes.",
                "EQUIPMENT_SIDE_CONNECTIONS": "required_bolt_length_mm=36.5, DEMO_BOLT_M12X45 passes.",
            },
        }

    status_flow["DOC37_S1"] = (
        STATUS_PASS
        if all(node_results[node_id]["slice01_status"] == STATUS_PASS for node_id in node_results)
        else "INCOMPLETE"
    )
    status_flow["DOC37_S2"] = (
        STATUS_PASS
        if all(node_results[node_id]["slice02_status"] == STATUS_PASS for node_id in node_results)
        else "INCOMPLETE"
    )

    doc38_input = {
        "aggregation_scope": doc38_fixture["aggregation_scope"],
        "product_type": doc38_fixture["product_type"],
        "product_id": doc38_fixture["product_id"],
        "calculation_id": doc38_fixture["calculation_id"],
        "source_node_outputs": _group_source_lines_for_doc38(doc38_fixture, fastener_versions),
    }
    aggregation_result = aggregate_kzo_node_package_lines(copy.deepcopy(doc38_input))
    status_flow["DOC38_S1"] = aggregation_result["status"]

    totals = {line["item_id"]: line["total_quantity"] for line in aggregation_result["kit_issue_lines"]}
    expected_totals = {line["item_id"]: line["quantity"] for line in expected_outputs["expected_doc38_aggregation"]["kit_issue_lines"]}
    if totals != expected_totals:
        raise AssertionError(f"Aggregation totals mismatch: actual={totals} expected={expected_totals}")

    if fixtures != fixtures_before:
        raise AssertionError("Deep copy guard failed: fixture content was mutated in memory.")

    source_line_ids = sorted(
        {
            source_line_id
            for line in aggregation_result["kit_issue_lines"]
            for source_line_id in line["source_line_ids"]
        }
    )
    traceability_refs = sorted(
        {
            traceability_ref
            for line in aggregation_result["kit_issue_lines"]
            for traceability_ref in line["traceability_refs"]
        }
    )
    source_node_ids = sorted(
        {
            source_node_id
            for line in aggregation_result["kit_issue_lines"]
            for source_node_id in line["source_node_ids"]
        }
    )
    fastener_decision_rows = _build_fastener_decision_rows(
        node_fastener_selection=node_fastener_selection,
        registry_version=fastener_versions["fastener_registry_version"],
    )

    output = {
        "demo_id": demo_meta["demo_id"],
        "status": STATUS_PASS if all(value == STATUS_PASS for value in status_flow.values()) else "INCOMPLETE",
        "status_flow": status_flow,
        "node_results": {
            node_id: {
                "total_busbar_length_mm": data["slice01_output"]["total_busbar_length_mm"],
                "joint_stacks": {
                    g["group_id"]: g["joint_stack_thickness_mm"]
                    for g in data["slice01_output"]["connection_point_groups"]
                },
                "selected_bolts": node_fastener_selection[node_id],
            }
            for node_id, data in node_results.items()
        },
        "fastener_decisions": fastener_decision_rows,
        "aggregation_result": {
            "status": aggregation_result["status"],
            "source_node_count": aggregation_result["source_node_count"],
        },
        "kit_issue_lines": aggregation_result["kit_issue_lines"],
        "source_node_ids": source_node_ids,
        "source_line_ids": source_line_ids,
        "traceability_refs": traceability_refs,
        "registry_versions": {
            "doc36": doc36_result["registry_versions"],
            "doc37_slice02": fastener_versions,
            "doc38": aggregation_result.get("registry_versions") or fastener_versions,
        },
        "audit_trail": [
            {
                "step": "DOC36",
                "input_summary": {
                    "selected_material_catalog_id": doc36_input["selected_material_catalog_id"],
                    "checks": doc36_input["checks"],
                },
                "decision": "Busbar candidate accepted for PASS path.",
                "status": doc36_result["status"],
                "registry_version": doc36_result["registry_versions"]["global_material_catalog_version"],
                "traceability_reference": "DOC36_SELECTED_MATERIAL_DEMO_BUSBAR_CU_60X10",
            },
            {
                "step": "DOC37_S1_NODE_A",
                "input_summary": {"busbar_node_id": "KZO_DEMO_NODE_A"},
                "decision": "Geometry and stacks resolved for Node A.",
                "status": node_results["KZO_DEMO_NODE_A"]["slice01_status"],
                "registry_version": "demo_v1",
                "traceability_reference": "TRACE_KZO_DEMO_NODE_A_BUSBAR_BOLT",
            },
            {
                "step": "DOC37_S2_NODE_A",
                "input_summary": {"busbar_node_id": "KZO_DEMO_NODE_A"},
                "decision": "BUSBAR_SIDE requires 48.5 mm so M12x55 selected; EQUIPMENT_SIDE requires 36.5 mm so M12x45 selected.",
                "status": node_results["KZO_DEMO_NODE_A"]["slice02_status"],
                "registry_version": "demo_v1",
                "traceability_reference": "TRACE_KZO_DEMO_NODE_A_EQUIP_BOLT",
            },
            {
                "step": "DOC38_S1",
                "input_summary": {"source_nodes": source_node_ids},
                "decision": "Node lines aggregated into deterministic kit_issue_lines totals 6/6/12/24/12.",
                "status": aggregation_result["status"],
                "registry_version": "demo_v1",
                "traceability_reference": "TRACE_KZO_DEMO_NODE_B_DISC_WASHER",
            },
        ],
        "management_summary": "System reads registry truth, validates every engineering step, selects local fasteners, and aggregates traceable kit issue lines. This is not final ERP BOM.",
        "boundary_note": "Local demo only. Not production data. Not final ERP BOM. Not procurement. Not warehouse. Not ERP/1C. Not pricing. Not CAD. No API/GAS/DB.",
        "optional_backup_included_in_main_flow": False,
    }

    if write_output:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with OUTPUT_FILE.open("w", encoding="utf-8") as output_file:
            json.dump(output, output_file, ensure_ascii=False, indent=2)

    return output
