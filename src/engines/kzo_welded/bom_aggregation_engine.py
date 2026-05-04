from __future__ import annotations

from typing import Any

from src.engines.kzo_welded.busbar_evaluation_engine import (
    STATUS_ENGINEERING_REQUIRED,
    STATUS_FAIL,
    STATUS_INCOMPLETE,
    STATUS_PASS,
)

# DOC 38 Slice 01 boundary:
# Basic aggregation for verified DOC 37 local node outputs only.
# No ERP/procurement/warehouse/API/GAS/DB behavior is allowed.

FAILURE_NODE_OUTPUT_NOT_PASS = "NODE_OUTPUT_NOT_PASS"
FAILURE_TRACEABILITY_MISSING = "TRACEABILITY_MISSING"
FAILURE_ITEM_ID_MISSING = "ITEM_ID_MISSING"
FAILURE_ITEM_TYPE_MISSING = "ITEM_TYPE_MISSING"
FAILURE_QUANTITY_MISSING = "QUANTITY_MISSING"
FAILURE_UNIT_MISSING = "UNIT_MISSING"
FAILURE_REGISTRY_SOURCE_MISSING = "REGISTRY_SOURCE_MISSING"
FAILURE_REGISTRY_VERSION_MISSING = "REGISTRY_VERSION_MISSING"
FAILURE_AGGREGATION_SCOPE_MISSING = "AGGREGATION_SCOPE_MISSING"
FAILURE_UNSUPPORTED_AGGREGATION_SCOPE = "UNSUPPORTED_AGGREGATION_SCOPE"
FAILURE_SOURCE_NODE_ID_MISSING = "SOURCE_NODE_ID_MISSING"
FAILURE_SOURCE_LINE_ID_MISSING = "SOURCE_LINE_ID_MISSING"
FAILURE_TRACEABILITY_REF_MISSING = "TRACEABILITY_REF_MISSING"
FAILURE_DUPLICATE_SOURCE_LINE = "DUPLICATE_SOURCE_LINE"
FAILURE_DUPLICATE_TRACEABILITY_REF = "DUPLICATE_TRACEABILITY_REF"
FAILURE_NON_NUMERIC_QUANTITY = "NON_NUMERIC_QUANTITY"
FAILURE_ZERO_OR_NEGATIVE_QUANTITY = "ZERO_OR_NEGATIVE_QUANTITY"
FAILURE_MIXED_UNIT_CONFLICT = "MIXED_UNIT_CONFLICT"
FAILURE_MIXED_REGISTRY_SOURCE_CONFLICT = "MIXED_REGISTRY_SOURCE_CONFLICT"
FAILURE_REGISTRY_VERSION_MISMATCH = "REGISTRY_VERSION_MISMATCH"
FAILURE_SELECTED_MATERIAL_CATALOG_ID_MISSING = "SELECTED_MATERIAL_CATALOG_ID_MISSING"
FAILURE_KIT_ISSUE_AGGREGATION_INCOMPLETE = "KIT_ISSUE_AGGREGATION_INCOMPLETE"

ALLOWED_SCOPES = {"DEMO_MVP", "SINGLE_CELL", "CELL_GROUP"}


def _is_missing(value: Any) -> bool:
    return value is None or (isinstance(value, str) and value.strip() == "")


def _is_numeric(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _base_result(evaluation_input: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": STATUS_INCOMPLETE,
        "aggregation_scope": evaluation_input.get("aggregation_scope"),
        "product_type": evaluation_input.get("product_type"),
        "product_id": evaluation_input.get("product_id"),
        "calculation_id": evaluation_input.get("calculation_id"),
        "kit_issue_lines": [],
        "source_node_count": 0,
        "source_nodes": [],
        "registry_versions": dict(evaluation_input.get("registry_versions") or {}),
        "failure_code": None,
        "notes": list(evaluation_input.get("notes") or []),
    }


def _identity_tuple(line: dict[str, Any]) -> tuple[Any, ...]:
    # Base identity keys
    identity: list[Any] = [
        line.get("item_id"),
        line.get("item_type"),
        line.get("unit"),
        line.get("registry_source"),
        line.get("registry_version"),
        line.get("issue_context"),
    ]

    item_type = line.get("item_type")
    if item_type == "MATERIAL":
        identity.append(line.get("selected_material_catalog_id"))

    if item_type in {"BOLT", "NUT", "FLAT_WASHER", "DISC_SPRING_WASHER", "FASTENER"}:
        for key in (
            "fastener_registry_version",
            "washer_package_rule_registry_version",
            "joint_stack_rule_registry_version",
        ):
            if key in line:
                identity.append((key, line.get(key)))
    return tuple(identity)


def aggregate_kzo_node_package_lines(evaluation_input: dict[str, Any]) -> dict[str, Any]:
    """DOC 38 Slice 01 — basic aggregation for verified local node outputs."""
    result = _base_result(evaluation_input)

    aggregation_scope = evaluation_input.get("aggregation_scope")
    if _is_missing(aggregation_scope):
        result["status"] = STATUS_INCOMPLETE
        result["failure_code"] = FAILURE_AGGREGATION_SCOPE_MISSING
        return result
    if aggregation_scope not in ALLOWED_SCOPES:
        result["status"] = STATUS_INCOMPLETE
        result["failure_code"] = FAILURE_UNSUPPORTED_AGGREGATION_SCOPE
        return result
    result["aggregation_scope"] = aggregation_scope

    for ctx_key in ("product_type", "product_id", "calculation_id"):
        if _is_missing(evaluation_input.get(ctx_key)):
            result["status"] = STATUS_INCOMPLETE
            result["failure_code"] = FAILURE_KIT_ISSUE_AGGREGATION_INCOMPLETE
            result["notes"].append(f"Missing aggregation context field: {ctx_key}.")
            return result

    node_outputs = evaluation_input.get("source_node_outputs")
    if not isinstance(node_outputs, list) or len(node_outputs) == 0:
        result["status"] = STATUS_INCOMPLETE
        result["failure_code"] = FAILURE_KIT_ISSUE_AGGREGATION_INCOMPLETE
        result["notes"].append("No source_node_outputs were provided.")
        return result

    source_lines: list[dict[str, Any]] = []
    source_nodes: list[str] = []
    for node_output in node_outputs:
        if not isinstance(node_output, dict):
            result["status"] = STATUS_INCOMPLETE
            result["failure_code"] = FAILURE_KIT_ISSUE_AGGREGATION_INCOMPLETE
            result["notes"].append("Each source node output must be an object.")
            return result
        if node_output.get("status") != STATUS_PASS:
            result["status"] = STATUS_INCOMPLETE
            result["failure_code"] = FAILURE_NODE_OUTPUT_NOT_PASS
            return result

        node_id = node_output.get("busbar_node_id")
        if not _is_missing(node_id):
            source_nodes.append(node_id)

        for lines_key in ("node_material_lines", "node_fastener_lines"):
            lines = node_output.get(lines_key) or []
            if not isinstance(lines, list):
                result["status"] = STATUS_INCOMPLETE
                result["failure_code"] = FAILURE_KIT_ISSUE_AGGREGATION_INCOMPLETE
                result["notes"].append(f"{lines_key} must be an array.")
                return result
            for line in lines:
                if isinstance(line, dict):
                    source_lines.append(line)

    if len(source_lines) == 0:
        result["status"] = STATUS_INCOMPLETE
        result["failure_code"] = FAILURE_KIT_ISSUE_AGGREGATION_INCOMPLETE
        result["notes"].append("No source lines available for aggregation.")
        result["source_nodes"] = list(dict.fromkeys(source_nodes))
        result["source_node_count"] = len(result["source_nodes"])
        return result

    seen_source_line_ids: set[str] = set()
    seen_traceability_refs: set[str] = set()
    # Conflict checks by item_id, before grouping
    item_units: dict[str, Any] = {}
    item_sources: dict[str, Any] = {}
    item_versions: dict[str, Any] = {}

    for line in source_lines:
        required_field_checks = (
            ("source_line_id", FAILURE_SOURCE_LINE_ID_MISSING),
            ("traceability_ref", FAILURE_TRACEABILITY_REF_MISSING),
            ("item_id", FAILURE_ITEM_ID_MISSING),
            ("item_type", FAILURE_ITEM_TYPE_MISSING),
            ("quantity", FAILURE_QUANTITY_MISSING),
            ("unit", FAILURE_UNIT_MISSING),
            ("source_node_id", FAILURE_SOURCE_NODE_ID_MISSING),
            ("registry_source", FAILURE_REGISTRY_SOURCE_MISSING),
            ("registry_version", FAILURE_REGISTRY_VERSION_MISSING),
        )
        for field_name, failure_code in required_field_checks:
            if _is_missing(line.get(field_name)):
                result["status"] = STATUS_INCOMPLETE
                result["failure_code"] = failure_code
                return result

        source_line_id = str(line["source_line_id"])
        traceability_ref = str(line["traceability_ref"])
        if source_line_id in seen_source_line_ids:
            result["status"] = STATUS_FAIL
            result["failure_code"] = FAILURE_DUPLICATE_SOURCE_LINE
            return result
        seen_source_line_ids.add(source_line_id)

        if traceability_ref in seen_traceability_refs:
            result["status"] = STATUS_FAIL
            result["failure_code"] = FAILURE_DUPLICATE_TRACEABILITY_REF
            return result
        seen_traceability_refs.add(traceability_ref)

        quantity = line.get("quantity")
        if not _is_numeric(quantity):
            result["status"] = STATUS_INCOMPLETE
            result["failure_code"] = FAILURE_NON_NUMERIC_QUANTITY
            return result
        if float(quantity) <= 0:
            result["status"] = STATUS_FAIL
            result["failure_code"] = FAILURE_ZERO_OR_NEGATIVE_QUANTITY
            return result

        item_id = str(line["item_id"])
        unit = line.get("unit")
        registry_source = line.get("registry_source")
        registry_version = line.get("registry_version")
        if item_id in item_units and item_units[item_id] != unit:
            result["status"] = STATUS_INCOMPLETE
            result["failure_code"] = FAILURE_MIXED_UNIT_CONFLICT
            return result
        item_units[item_id] = unit

        if item_id in item_sources and item_sources[item_id] != registry_source:
            result["status"] = STATUS_INCOMPLETE
            result["failure_code"] = FAILURE_MIXED_REGISTRY_SOURCE_CONFLICT
            return result
        item_sources[item_id] = registry_source

        if item_id in item_versions and item_versions[item_id] != registry_version:
            result["status"] = STATUS_ENGINEERING_REQUIRED
            result["failure_code"] = FAILURE_REGISTRY_VERSION_MISMATCH
            result["notes"].append(
                f"item_id={item_id} registry_source={registry_source} versions: "
                f"{item_versions[item_id]} vs {registry_version}."
            )
            return result
        item_versions[item_id] = registry_version

        if line.get("item_type") == "MATERIAL" and _is_missing(line.get("selected_material_catalog_id")):
            result["status"] = STATUS_INCOMPLETE
            result["failure_code"] = FAILURE_SELECTED_MATERIAL_CATALOG_ID_MISSING
            return result

    grouped: dict[tuple[Any, ...], list[dict[str, Any]]] = {}
    for line in source_lines:
        identity = _identity_tuple(line)
        grouped.setdefault(identity, []).append(line)

    kit_issue_lines: list[dict[str, Any]] = []
    for group_lines in grouped.values():
        first = group_lines[0]
        total_quantity = sum(float(x["quantity"]) for x in group_lines)
        source_line_ids = list(dict.fromkeys(str(x["source_line_id"]) for x in group_lines))
        source_node_ids = list(dict.fromkeys(str(x["source_node_id"]) for x in group_lines))
        source_groups = list(dict.fromkeys(str(x.get("source_group")) for x in group_lines if not _is_missing(x.get("source_group"))))
        traceability_refs = list(dict.fromkeys(str(x["traceability_ref"]) for x in group_lines))

        line_output = {
            "item_id": first.get("item_id"),
            "item_type": first.get("item_type"),
            "total_quantity": total_quantity,
            "unit": first.get("unit"),
            "registry_source": first.get("registry_source"),
            "registry_version": first.get("registry_version"),
            "issue_context": first.get("issue_context"),
            "source_node_ids": source_node_ids,
            "source_groups": source_groups,
            "source_line_ids": source_line_ids,
            "traceability_refs": traceability_refs,
            "source_line_count": len(source_line_ids),
            "traceability_ref_count": len(traceability_refs),
        }
        if first.get("item_type") == "MATERIAL":
            line_output["selected_material_catalog_id"] = first.get("selected_material_catalog_id")
        for optional_key in (
            "fastener_registry_version",
            "washer_package_rule_registry_version",
            "joint_stack_rule_registry_version",
        ):
            if optional_key in first:
                line_output[optional_key] = first.get(optional_key)
        kit_issue_lines.append(line_output)

    # Node-level registry_versions are preserved if consistent.
    node_registry_versions = [n.get("registry_versions") for n in node_outputs if isinstance(n.get("registry_versions"), dict)]
    if node_registry_versions:
        first_versions = node_registry_versions[0]
        if all(v == first_versions for v in node_registry_versions):
            result["registry_versions"] = dict(first_versions)

    result["source_nodes"] = list(dict.fromkeys(source_nodes))
    result["source_node_count"] = len(result["source_nodes"])
    result["kit_issue_lines"] = kit_issue_lines
    result["status"] = STATUS_PASS
    result["failure_code"] = None
    return result
