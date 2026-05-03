# KZO WELDED BUSBAR EVALUATION ENGINE V1

## Status
MVP / PROTOTYPE / DOC-FIRST / NO IMPLEMENTATION

## Purpose
Define how the system selects a valid busbar candidate using:
- global material catalog
- KZO product usage registry
- busbar node matrix
- equipment interface registry

MVP doctrine:
- registries are code-based/manual registry constants
- admin panel is explicitly out of scope
- algorithm must read registries and must not hide engineering truth inside decision logic

## Core Evaluation Flow
Input:
- cell_type
- busbar_node_id
- cell_rated_current
- global_busbar_current
- bridge_rated_current
- equipment_id

Flow:
1. Load active node from busbar_node_matrix_v1
2. Resolve current_source
3. Resolve required current value
4. Resolve usage_context
5. Load equipment interface constraints if equipment_id exists
6. Scan global busbar material catalog
7. Filter candidates by catalog availability / registry eligibility
8. Apply product usage check
9. Apply current capacity check
10. Apply equipment form-factor check
11. Apply conflict resolution / precedence rule
12. Return selected candidate, proposed candidate, or failure reason

Note:
Product Usage is a product permission layer.
It does not override equipment physical constraints.

## Evaluation Status Model

Allowed statuses:

- PASS
- FAIL
- INCOMPLETE
- ENGINEERING_REQUIRED
- AMBIGUOUS
- SELECTION_REQUIRED

Rules:

PASS:
Allowed only when all mandatory checks are fully passed.
PASS is forbidden if any mandatory check returns:
- NEEDS_ENGINEERING_VALUE
- UNKNOWN
- INCOMPLETE
- WARNING_ONLY

INCOMPLETE:
Used when required input data is missing.
Examples:
- current value missing
- current_source cannot be resolved
- equipment_id required but missing
- registry version missing

ENGINEERING_REQUIRED:
Used when candidate exists but cannot be automatically approved because engineering confirmation is required.
Examples:
- rated_current_a is null
- short-circuit / thermal / environment constraints are outside MVP
- boundary conditions require manual engineering decision

AMBIGUOUS:
Used when the engine cannot determine one clear candidate due to conflicting or incomplete constraints.

SELECTION_REQUIRED:
Used when multiple valid candidates remain and automatic choice is not allowed.

FAIL:
Used when no valid candidate can satisfy mandatory constraints.

## Evaluation Layers

### L1 — Node Activation Check
Node must exist and be active for cell_type.

### L2 — Current Source Resolution
Allowed:
- GLOBAL_BUSBAR_CURRENT
- CELL_RATED_CURRENT
- BRIDGE_RATED_CURRENT
- INTERFACE_RATED_CURRENT
- EXTERNAL_REFERENCE

### L3 — Product Usage Check
Candidate must be allowed in 09_KZO usage registry for the required usage_context.

### L4 — Current Capacity Check
Candidate rated_current_a must be >= required current.
If rated_current_a is null:
- candidate must NOT produce PASS
- candidate may only produce ENGINEERING_REQUIRED
- output must include `failure_code = CANDIDATE_CURRENT_UNKNOWN`
- `selected_material_catalog_id` must be null unless explicitly marked as `proposed_candidate_id`
- notes must state that automatic final selection is blocked

### L5 — Equipment Form-Factor Check
Candidate width/thickness/material must satisfy equipment_interface_registry constraints.
Example:
terminal_min_width_mm = 60
candidate width < 60 => FAIL_FORM_FACTOR

### L6 — Selection Rule
Automatic final selection is allowed only if:
- all mandatory checks pass
- exactly one valid candidate remains
- no mandatory engineering value is missing
- no unresolved conflict exists

If multiple valid candidates remain:
- status = SELECTION_REQUIRED
- failure_code = MULTIPLE_VALID_CANDIDATES
- the engine must return candidates list for human or later optimization decision

Do NOT automatically choose smallest candidate unless:
- explicit optimization policy exists
- mass/pricing/availability priority is defined
- engineering approval boundary is satisfied

For MVP:
No automatic smallest-candidate optimization.

## Constraint Precedence Rule

Precedence order:

1. Safety / mandatory engineering blockers
2. Equipment Interface Constraints
3. Current Capacity Constraints
4. Product Usage Registry
5. Selection preference rules

Rules:

Equipment Interface Constraints override Product Usage defaults.

If product usage allows a busbar but equipment interface rejects it:
result = FAIL
failure_code = INTERFACE_VIOLATION or FAIL_FORM_FACTOR

If equipment interface requires dimensions/material that product usage does not allow:
result = FAIL or ENGINEERING_REQUIRED depending on whether exception governance exists.

No silent override is allowed.

## Failure Codes
- NODE_NOT_ACTIVE
- CURRENT_SOURCE_MISSING
- USAGE_NOT_ALLOWED
- CURRENT_VALUE_MISSING
- CANDIDATE_CURRENT_UNKNOWN
- FAIL_CURRENT_CAPACITY
- FAIL_FORM_FACTOR
- NO_VALID_CANDIDATE
- INSUFFICIENT_DATA
- USAGE_CONTEXT_MISSING
- EQUIPMENT_CONSTRAINT_MISSING
- INTERFACE_VIOLATION
- DIMENSION_CONFLICT
- MATERIAL_RESTRICTION
- CATALOG_EMPTY
- PACKAGE_NOT_FOUND
- AMBIGUOUS_CANDIDATE
- MULTIPLE_VALID_CANDIDATES
- REGISTRY_VERSION_MISSING

## MVP Boundary
- No pricing
- No mass optimization if mass is null
- No thermal/dynamic final certification
- No short-circuit force calculation
- No final BOM
- No CAD
- No admin panel

Registry-source boundary for MVP:
- registry data is authoritative input
- algorithmic branches may interpret registry facts but must not replace them with hidden engineering constants
- any new engineering truth must enter via registry contract update, not hardcoded decision drift

## MVP Safety Boundary Note

DOC 36 does NOT certify final busbar engineering.

MVP engine may reject or block automatic selection, but must not claim final engineering safety for:
- thermal behavior
- short-circuit dynamic stability
- environment factor
- mechanical force
- final CAD fit
- final BOM release

Any candidate affected by these unresolved checks must be marked:
ENGINEERING_REQUIRED
not PASS.

## Output Contract
Required output fields:
- status
- selected_material_catalog_id
- proposed_candidate_id
- selected_usage_id
- package_id
- checks
- failure_code
- candidate_list
- registry_versions
- notes

Registry versions object:
{
  "global_material_catalog_version": "string",
  "kzo_usage_registry_version": "string",
  "busbar_node_matrix_version": "string",
  "equipment_interface_registry_version": "string"
}

Rule:
If registry versions cannot be resolved:
status = INCOMPLETE
failure_code = REGISTRY_VERSION_MISSING

Example output:
{
  "status": "ENGINEERING_REQUIRED",
  "selected_material_catalog_id": null,
  "proposed_candidate_id": "BUSBAR_CU_SHMT_60X10_1",
  "selected_usage_id": "KZO_MAIN_BUS_CU_60X10_1",
  "package_id": "KZO_BUSBAR_MAIN_PACKAGE_V1",
  "checks": {
    "node": "PASS",
    "usage": "PASS",
    "current": "NEEDS_ENGINEERING_VALUE",
    "form_factor": "PASS",
    "equipment_interface": "PASS"
  },
  "failure_code": "CANDIDATE_CURRENT_UNKNOWN",
  "notes": [
    "Candidate cannot be automatically approved because rated_current_a is missing.",
    "Engineering value is required before final selection."
  ]
}

## Implementation Readiness

Current status:
IMPLEMENTATION BLOCKED UNTIL DOC 36 FIXES ARE RE-AUDITED.

After fixes:
Implementation may only proceed as a separate narrow slice and only if:
- status model is unambiguous
- PASS cannot hide unknown engineering values
- precedence rule is documented
- multiple candidate behavior is documented
- registry traceability is documented

## Governance
This document defines decision logic only.
Implementation requires separate approved task.
