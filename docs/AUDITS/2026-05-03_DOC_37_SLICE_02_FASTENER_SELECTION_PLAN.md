# DOC 37 SLICE 02 FASTENER SELECTION PLAN

## Status
PLANNING ONLY / NO IMPLEMENTATION

## Scope

Included:
- Slice 01 PASS dependency check
- connection group input validation
- washer package rule resolution plan
- hardware_stack_sum_mm resolution plan
- thread_pitch_mm resolution plan
- safety_margin_mm resolution plan
- required_bolt_length_mm calculation plan
- active bolt length matching plan
- node_fastener_lines generation plan as local node output only
- status / failure_code behavior

Excluded:
- final BOM aggregation
- cross-node aggregation
- procurement
- pricing
- CAD validation
- thermal / short-circuit certification
- API/GAS/DB integration
- admin panel
- registry data creation
- DOC 36 Slice 02

## Required Inputs

From DOC 37 Slice 01:
- status
- busbar_node_id
- phase_count
- connection_point_groups
- node_fastener_lines must be []
- node_material_lines must be []
- registry_versions if already present

For each connection_point_group:
- group_id
- connection_point_count
- joint_stack_thickness_mm
- stack_status
- failure_code

From DOC 33 Fastener Registry:
- active bolt records
- fastener_id
- item_type
- diameter_mm
- thread_pitch_mm
- length_mm
- is_active
- registry_version

From DOC 33 Washer Package Rule Registry:
- washer_package_rule_id
- flat_washer_count
- flat_washer_fastener_id
- disc_spring_washer_count
- disc_spring_washer_fastener_id
- nut_fastener_id
- hardware_stack_sum_mm
- allowed_bolt_diameter_mm
- usage_context
- is_active
- registry_version

From DOC 33 Joint Stack Rule Registry:
- joint_stack_rule_id
- connection_group_type
- allowed_bolt_diameter_mm
- washer_package_rule_id
- required_nut_type
- required_bolt_type
- thread_allowance_rule
- safety_margin_mm
- selection_policy
- is_active
- registry_version

## Planned Function Boundary

Proposed function name:
evaluate_busbar_node_fastener_selection(evaluation_input)

Function type:
- pure deterministic function
- no side effects
- no DB/API/GAS access
- no admin panel access
- no registry loading from DB

Important:
For MVP, registries may be provided as prepared input objects.
The function consumes prepared registry truth.
It must not fetch or create registry data.

## Planned Flow

1. Validate Slice 01 output status.
   If Slice 01 status is not PASS:
   status = INCOMPLETE
   failure_code = SLICE01_GEOMETRY_NOT_PASS

2. Validate connection groups.
   Required groups:
   - BUSBAR_SIDE_CONNECTIONS
   - EQUIPMENT_SIDE_CONNECTIONS

3. For each connection group:
   - resolve applicable Joint Stack Rule
   - resolve washer_package_rule_id
   - resolve Washer Package Rule
   - resolve hardware_stack_sum_mm
   - resolve thread_pitch_mm from selected bolt/thread rule
   - resolve safety_margin_mm
   - calculate required_bolt_length_mm:
     joint_stack_thickness_mm
     + hardware_stack_sum_mm
     + thread_allowance_mm
     + safety_margin_mm

4. Match active bolt candidates:
   - item_type = BOLT
   - is_active = true
   - diameter matches allowed_bolt_diameter_mm
   - length_mm >= required_bolt_length_mm

5. Selection behavior:
   - if no bolt matches:
     status = INCOMPLETE
     failure_code = BOLT_LENGTH_NOT_FOUND
   - if multiple bolt candidates match and no selection_policy exists:
     status = SELECTION_REQUIRED
     failure_code = BOLT_LENGTH_AMBIGUOUS
   - if one valid bolt is selected:
     create local node_fastener_lines for that connection group

6. Aggregate local node_fastener_lines across connection groups.
   This is local node package output only.
   It is NOT final BOM.

## Required Output

Required fields:
- status
- busbar_node_id
- connection_point_groups
- node_fastener_lines
- failure_code
- notes
- registry_versions

For each connection group output:
- group_id
- connection_point_count
- joint_stack_thickness_mm
- required_bolt_length_mm
- selected_bolt_fastener_id
- washer_package_rule_id
- fastener_selection_status
- failure_code

node_fastener_lines:
- item_id
- item_type
- quantity
- source_group
- source_connection_count
- registry_source

Important:
node_fastener_lines are local node output only.
They must not be treated as final BOM.
DOC 38 owns aggregation.

## Status Rules

PASS allowed only if:
- Slice 01 status is PASS
- all required connection groups are present
- applicable joint stack rules are resolved
- washer package rules are resolved
- hardware_stack_sum_mm is resolved
- thread_pitch_mm or approved thread allowance rule is resolved
- safety_margin_mm is resolved
- exactly one valid bolt is selected for each required group
- node_fastener_lines are generated from registry-backed rules only
- registry versions are present

If Slice 01 status is not PASS:
status = INCOMPLETE
failure_code = SLICE01_GEOMETRY_NOT_PASS

If washer package is missing:
status = INCOMPLETE
failure_code = FASTENER_DEFAULT_NOT_APPROVED

If hardware_stack_sum_mm is missing:
status = INCOMPLETE
failure_code = HARDWARE_STACK_SUM_MISSING

If thread_pitch_mm is missing:
status = INCOMPLETE
failure_code = THREAD_PITCH_MISSING

If safety_margin_mm is missing:
status = INCOMPLETE
failure_code = SAFETY_MARGIN_MISSING

If no bolt length matches:
status = INCOMPLETE
failure_code = BOLT_LENGTH_NOT_FOUND

If multiple bolt lengths match and no selection policy exists:
status = SELECTION_REQUIRED
failure_code = BOLT_LENGTH_AMBIGUOUS

## Failure Codes

Required:
- SLICE01_GEOMETRY_NOT_PASS
- FASTENER_RULE_MISSING
- FASTENER_DATA_MISSING
- FASTENER_DEFAULT_NOT_APPROVED
- HARDWARE_STACK_SUM_MISSING
- THREAD_PITCH_MISSING
- SAFETY_MARGIN_MISSING
- BOLT_LENGTH_NOT_FOUND
- BOLT_LENGTH_AMBIGUOUS
- FASTENER_PACKAGE_AMBIGUOUS
- NUT_DATA_MISSING
- WASHER_DATA_MISSING
- FASTENER_REGISTRY_VERSION_MISSING
- NODE_PACKAGE_INCOMPLETE

## Test Plan

Required future tests:
1. Slice 01 not PASS blocks Slice 02.
2. Missing BUSBAR_SIDE_CONNECTIONS returns NODE_PACKAGE_INCOMPLETE.
3. Missing washer package returns FASTENER_DEFAULT_NOT_APPROVED.
4. Missing hardware_stack_sum_mm returns HARDWARE_STACK_SUM_MISSING.
5. Missing thread_pitch_mm returns THREAD_PITCH_MISSING.
6. Missing safety_margin_mm returns SAFETY_MARGIN_MISSING.
7. No active bolt length satisfies required_bolt_length_mm returns BOLT_LENGTH_NOT_FOUND.
8. Multiple valid bolt candidates with no selection_policy returns BOLT_LENGTH_AMBIGUOUS.
9. One valid bolt candidate generates local node_fastener_lines.
10. node_fastener_lines are local output only and do not contain final BOM markers.
11. No API/GAS/DB access occurs.
12. No pricing/CAD/BOM aggregation occurs.

## Governance Boundary

Slice 02 is not final DOC 37 completion.
Slice 02 only plans fastener selection for one local node package.

DOC 38 owns:
- final BOM aggregation
- cross-node aggregation
- kit issue
- procurement interface

Any attempt to treat Slice 02 node_fastener_lines as final BOM is governance breach.

Any attempt to invent fastener data instead of consuming prepared registry truth is governance breach.
