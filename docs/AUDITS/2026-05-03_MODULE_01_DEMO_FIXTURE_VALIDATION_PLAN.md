# MODULE 01 DEMO FIXTURE VALIDATION PLAN

## Status

PLANNING ONLY / NO VALIDATION RUNNER / NO TESTS

## Purpose

Define how immutable demo fixtures must be validated before running the Module 01 local demo.

The validation must prove:

- JSON fixture consistency
- cross-file consistency
- expected output consistency
- traceability integrity
- registry version visibility
- no production/API/GAS/DB/ERP drift

## Fixture Scope

Fixtures under validation:

- `demo_metadata.json`
- `doc36_busbar_fixture.json`
- `doc37_node_geometry_fixture.json`
- `doc37_fastener_selection_fixture.json`
- `doc38_aggregation_fixture.json`
- `expected_outputs.json`
- `optional_backup_safety_fixture.json`

## Validation Categories

### 1. JSON Structure Validation

Check:

- each fixture is valid JSON
- required metadata exists:
  - `fixture_id`
  - `fixture_version`
  - `immutable = true`
  - `demo_only = true`
  - `not_production_data = true`
  - `display_name`
  - `short_description`

### 2. Demo Boundary Validation

Check:

- no fixture claims production data
- no API/GAS/DB fields are active
- no ERP/1C/procurement/warehouse/pricing/CAD fields are active
- main flow remains PASS-only
- optional backup fixture is not part of main flow

Expected:

- `boundaries.api = false`
- `boundaries.gas = false`
- `boundaries.db = false`
- `boundaries.erp = false`
- `boundaries.procurement = false`
- `boundaries.warehouse = false`
- `boundaries.pricing = false`
- `boundaries.cad = false`

### 3. Cross-File Consistency Validation

Validate that:

- Node A exists consistently across geometry, fastener, aggregation, and expected outputs
- Node B exists consistently across geometry, fastener, aggregation, and expected outputs
- `selected_material_catalog_id` from DOC 36 appears consistently where required
- `registry_versions` are consistent across fixture files
- `product_id` and `calculation_id` match between aggregation fixture and expected outputs

### 4. Geometry Expected Output Validation

For Node A:

- `L1 + L2 + L3 = 1290`
- `BUSBAR_SIDE joint_stack = 30`
- `EQUIPMENT_SIDE joint_stack = 18`

For Node B:

- `L1 + L2 + L3 = 1200`
- `BUSBAR_SIDE joint_stack = 30`
- `EQUIPMENT_SIDE joint_stack = 18`

Important presentation note:
Same joint stack values for Node A and Node B are acceptable because stack depends on busbar/equipment thickness, not on phase length.

### 5. Fastener Calculation Consistency Validation

Validate expected bolt length logic:

BUSBAR_SIDE:

- `joint_stack = 30`
- `hardware_stack_sum = 14`
- `thread_allowance = 2 * 1.75 = 3.5`
- `safety_margin = 1`
- `required_bolt_length_mm = 48.5`
- `M12x45` must NOT pass
- `M12x55` must pass

EQUIPMENT_SIDE:

- `joint_stack = 18`
- `hardware_stack_sum = 14`
- `thread_allowance = 3.5`
- `safety_margin = 1`
- `required_bolt_length_mm = 36.5`
- `M12x45` must pass

### 6. Aggregation Expected Totals Validation

Expected DOC 38 totals:

- `DEMO_BOLT_M12X55 = 6 pcs`
- `DEMO_BOLT_M12X45 = 6 pcs`
- `DEMO_NUT_M12 = 12 pcs`
- `DEMO_FLAT_WASHER_M12 = 24 pcs`
- `DEMO_DISC_SPRING_WASHER_M12 = 12 pcs`

Validate:

- quantities are numeric
- quantities are `> 0`
- units are present
- `item_id` values match fixture-defined fastener IDs
- aggregation is production-preparation only, not final ERP BOM

### 7. Traceability Integrity Validation

Rule:
One `source_line_id` = one `traceability_ref`.

Validate:

- every `source_line_id` is unique
- every `traceability_ref` is unique
- every `source_line_id` has exactly one `traceability_ref`
- `kit_issue_lines` preserve `source_line_ids`
- `kit_issue_lines` preserve `traceability_refs`
- `source_node_ids` include both Node A and Node B where expected

### 8. Registry Metadata Validation

Check all required registry metadata:

- `registry_version`
- `last_updated`
- `display_name`

Required registry groups:

- global material catalog
- KZO usage registry
- busbar node matrix
- equipment interface registry
- fastener registry
- joint stack rule registry
- washer package rule registry

Expected version:

- `demo_v1`

Boundary assertion:
If fixture tries to use registry version outside `demo_v1`, validation must fail or flag boundary violation.

### 9. Optional Backup Fixture Validation

Validate:

- `fixture_role = OPTIONAL_BACKUP_ONLY`
- `not_main_demo_flow = true`
- `expected_status = INCOMPLETE`
- `expected_failure_code = PHASE_LENGTH_MISSING`
- `expected_failure_reason` exists and is human-readable
- `phase_length_l2_mm` is missing

Backup fixture must not be included in main PASS validation flow.

## Planned Validation Output

Future validator should produce:

- `status`
- `validation_summary`
- `checked_files`
- `pass_checks`
- `failed_checks`
- `warnings`
- `boundary_status`
- `fixture_ready_for_demo`

Expected successful validation:

- `status = PASS`
- `fixture_ready_for_demo = true`

## Required Future Tests / Runner Checks

When implementation is approved, the validation runner/test must check:

1. all fixture JSON files load
2. required metadata exists
3. Node A geometry expected outputs match
4. Node B geometry expected outputs match
5. fastener required length logic matches expected bolt choices
6. DOC 38 expected aggregation totals match
7. `source_line_id` uniqueness
8. `traceability_ref` uniqueness
9. one `source_line_id` maps to one `traceability_ref`
10. `registry_versions` are `demo_v1`
11. optional backup fixture is excluded from main flow
12. no production/API/GAS/DB/ERP/procurement/warehouse/pricing/CAD drift

## Governance Boundary

This plan does not authorize:

- demo runner creation
- test creation
- fixture modification
- engine code changes
- API/GAS/DB integration
- ERP/procurement/warehouse integration
- final BOM release

Future validation runner requires separate approved task.
