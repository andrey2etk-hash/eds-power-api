from __future__ import annotations

from typing import Any

# This module implements DOC 36: KZO_WELDED_BUSBAR_EVALUATION_ENGINE_V1
# Slice 01 — status safety core only.
# It must not implement full busbar selection, BOM, pricing, CAD, DB, GAS, or API logic.

# Evaluation statuses (DOC 36 Slice 01 safety core)
STATUS_PASS = "PASS"
STATUS_FAIL = "FAIL"
STATUS_INCOMPLETE = "INCOMPLETE"
STATUS_ENGINEERING_REQUIRED = "ENGINEERING_REQUIRED"
STATUS_AMBIGUOUS = "AMBIGUOUS"
STATUS_SELECTION_REQUIRED = "SELECTION_REQUIRED"

# Check result statuses
CHECK_PASS = "PASS"
CHECK_FAIL = "FAIL"
CHECK_NEEDS_ENGINEERING_VALUE = "NEEDS_ENGINEERING_VALUE"
CHECK_UNKNOWN = "UNKNOWN"
CHECK_INCOMPLETE = "INCOMPLETE"
CHECK_WARNING_ONLY = "WARNING_ONLY"

# Failure codes (Slice 01 minimum set)
FAILURE_REGISTRY_VERSION_MISSING = "REGISTRY_VERSION_MISSING"
FAILURE_CURRENT_SOURCE_MISSING = "CURRENT_SOURCE_MISSING"
FAILURE_CURRENT_VALUE_MISSING = "CURRENT_VALUE_MISSING"
FAILURE_CANDIDATE_CURRENT_UNKNOWN = "CANDIDATE_CURRENT_UNKNOWN"
FAILURE_FAIL_CURRENT_CAPACITY = "FAIL_CURRENT_CAPACITY"
FAILURE_FAIL_FORM_FACTOR = "FAIL_FORM_FACTOR"
FAILURE_USAGE_NOT_ALLOWED = "USAGE_NOT_ALLOWED"
FAILURE_INTERFACE_VIOLATION = "INTERFACE_VIOLATION"
FAILURE_MULTIPLE_VALID_CANDIDATES = "MULTIPLE_VALID_CANDIDATES"
FAILURE_NO_VALID_CANDIDATE = "NO_VALID_CANDIDATE"

REQUIRED_REGISTRY_VERSION_KEYS = (
    "global_material_catalog_version",
    "kzo_usage_registry_version",
    "busbar_node_matrix_version",
    "equipment_interface_registry_version",
)


def _is_missing(value: Any) -> bool:
    return value is None or (isinstance(value, str) and value.strip() == "")


def _base_result(evaluation_input: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": STATUS_INCOMPLETE,
        "selected_material_catalog_id": evaluation_input.get("selected_material_catalog_id"),
        "proposed_candidate_id": evaluation_input.get("proposed_candidate_id"),
        "selected_usage_id": evaluation_input.get("selected_usage_id"),
        "package_id": evaluation_input.get("package_id"),
        "checks": dict(evaluation_input.get("checks") or {}),
        "failure_code": None,
        "candidate_list": list(evaluation_input.get("candidate_list") or []),
        "registry_versions": dict(evaluation_input.get("registry_versions") or {}),
        "notes": list(evaluation_input.get("notes") or []),
    }


def evaluate_busbar_candidate_safety_core(evaluation_input: dict[str, Any]) -> dict[str, Any]:
    """DOC 36 Slice 01 safety core.

    Deterministic and side-effect free status evaluator.
    """
    result = _base_result(evaluation_input)
    registry_versions = result["registry_versions"]

    # 1) Registry version guard (mandatory)
    missing_registry = [k for k in REQUIRED_REGISTRY_VERSION_KEYS if _is_missing(registry_versions.get(k))]
    if missing_registry:
        result["status"] = STATUS_INCOMPLETE
        result["failure_code"] = FAILURE_REGISTRY_VERSION_MISSING
        result["selected_material_catalog_id"] = None
        result["notes"].append("Registry versions are incomplete for mandatory dependencies.")
        return result

    candidate = evaluation_input.get("candidate") or {}
    candidate_id = candidate.get("id") or candidate.get("material_catalog_id")

    # 2) Candidate current unknown guard
    if _is_missing(candidate.get("rated_current_a")):
        result["status"] = STATUS_ENGINEERING_REQUIRED
        result["selected_material_catalog_id"] = None
        result["proposed_candidate_id"] = candidate_id
        result["failure_code"] = FAILURE_CANDIDATE_CURRENT_UNKNOWN
        result["notes"].append(
            "Candidate cannot be automatically approved because rated_current_a is missing."
        )
        return result

    checks: dict[str, str] = result["checks"]
    mandatory_check_keys = evaluation_input.get("mandatory_check_keys")
    if not mandatory_check_keys:
        mandatory_check_keys = list(checks.keys())

    mandatory_values = [checks.get(k) for k in mandatory_check_keys]

    # 3) Multiple valid candidates guard
    valid_candidate_count = int(evaluation_input.get("valid_candidate_count") or 0)
    auto_selection_allowed = bool(evaluation_input.get("auto_selection_allowed"))
    if valid_candidate_count > 1 and not auto_selection_allowed:
        result["status"] = STATUS_SELECTION_REQUIRED
        result["failure_code"] = FAILURE_MULTIPLE_VALID_CANDIDATES
        result["selected_material_catalog_id"] = None
        result["notes"].append("Multiple valid candidates exist; automatic selection is not allowed.")
        return result

    # 4) Strict PASS safety rule
    if all(v == CHECK_PASS for v in mandatory_values):
        result["status"] = STATUS_PASS
        result["failure_code"] = None
        return result

    if any(v == CHECK_FAIL for v in mandatory_values):
        result["status"] = STATUS_FAIL
        result["failure_code"] = result["failure_code"] or FAILURE_NO_VALID_CANDIDATE
        result["selected_material_catalog_id"] = None
        return result

    if any(v in (CHECK_INCOMPLETE, CHECK_UNKNOWN) for v in mandatory_values):
        result["status"] = STATUS_INCOMPLETE
        result["failure_code"] = result["failure_code"] or FAILURE_CURRENT_VALUE_MISSING
        result["selected_material_catalog_id"] = None
        return result

    if any(v in (CHECK_NEEDS_ENGINEERING_VALUE, CHECK_WARNING_ONLY) for v in mandatory_values):
        result["status"] = STATUS_ENGINEERING_REQUIRED
        result["failure_code"] = result["failure_code"] or FAILURE_CANDIDATE_CURRENT_UNKNOWN
        result["selected_material_catalog_id"] = None
        if candidate_id and not result["proposed_candidate_id"]:
            result["proposed_candidate_id"] = candidate_id
        return result

    result["status"] = STATUS_AMBIGUOUS
    result["failure_code"] = result["failure_code"] or FAILURE_NO_VALID_CANDIDATE
    result["selected_material_catalog_id"] = None
    result["notes"].append("Checks do not resolve to deterministic status.")
    return result
