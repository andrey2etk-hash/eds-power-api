# DOC 37 SLICE 01 NODE GEOMETRY AND JOINT STACK PLAN

## Status
PLANNING ONLY / NO IMPLEMENTATION

## Scope
Included:
- DOC 36 status dependency validation
- phase_count validation
- phase lengths validation
- total busbar length calculation
- connection point group validation
- phase/connection count mismatch detection
- joint stack thickness calculation

Excluded:
- fastener package selection
- bolt length selection
- washer/nut rules
- fastener registry scan
- final BOM
- pricing
- CAD
- API/GAS/DB integration

## Required Inputs

From DOC 36:
- status
- selected_material_catalog_id
- package_id
- registry_versions

From Node Matrix / prepared node input:
- busbar_node_id
- phase_count
- phase_length_l1_mm
- phase_length_l2_mm
- phase_length_l3_mm
- node_busbar_thickness_mm
- main_busbar_pack_thickness_mm
- equipment_terminal_thickness_mm
- connection_point_groups

Connection point group fields:
- group_id
- connection_point_count
- connected_part_a
- connected_part_b
- stack_thickness_formula

## Planned Function Boundary

Proposed function name:
evaluate_busbar_node_geometry_and_stack(evaluation_input)

Function type:
- pure deterministic function
- no side effects
- no registry loading
- no DB/API/GAS access

## Planned Output

Required fields:
- status
- busbar_node_id
- phase_count
- phase_lengths
- total_busbar_length_mm
- connection_point_groups
- failure_code
- notes

For each connection group:
- group_id
- connection_point_count
- joint_stack_thickness_mm
- stack_status
- failure_code

## Status Rules

PASS allowed only if:
- DOC 36 status is PASS
- L1/L2/L3 exist
- total_busbar_length_mm is resolved
- required connection point groups exist
- connection_point_count matches phase_count unless registry-backed override exists
- joint_stack_thickness_mm is resolved for all required groups

If DOC 36 status is not PASS:
status = INCOMPLETE or ENGINEERING_REQUIRED
failure_code = DOC36_SELECTION_NOT_PASS

If any phase length is missing:
status = INCOMPLETE
failure_code = PHASE_LENGTH_MISSING

If connection_point_count != phase_count:
status = INCOMPLETE or ENGINEERING_REQUIRED
failure_code = PHASE_CONNECTION_MISMATCH

If joint stack thickness cannot be resolved:
status = INCOMPLETE
failure_code = JOINT_STACK_THICKNESS_MISSING

## Failure Codes

Required:
- DOC36_SELECTION_NOT_PASS
- PHASE_LENGTH_MISSING
- CONNECTION_POINT_COUNT_MISSING
- PHASE_CONNECTION_MISMATCH
- JOINT_STACK_THICKNESS_MISSING
- MAIN_BUSBAR_THICKNESS_MISSING
- EQUIPMENT_TERMINAL_THICKNESS_MISSING
- NODE_PACKAGE_INCOMPLETE

## Test Plan

Required future tests:
1. PASS when DOC36 PASS, all phase lengths present, connection counts match, stack thickness resolved.
2. DOC36 not PASS blocks DOC37 PASS.
3. Missing L2 returns PHASE_LENGTH_MISSING.
4. connection_point_count != phase_count returns PHASE_CONNECTION_MISMATCH.
5. Missing main_busbar_pack_thickness_mm returns MAIN_BUSBAR_THICKNESS_MISSING.
6. Missing equipment_terminal_thickness_mm returns EQUIPMENT_TERMINAL_THICKNESS_MISSING.
7. Missing required connection group returns CONNECTION_POINT_COUNT_MISSING or NODE_PACKAGE_INCOMPLETE.
8. No fastener lines are produced in Slice 01.

## Governance Boundary

Slice 01 is not a complete DOC 37 implementation.
It is only node geometry and joint stack readiness.

Fastener selection belongs to future slice.
BOM aggregation belongs to DOC 38.
Any attempt to generate final fastener package in Slice 01 is governance breach.
