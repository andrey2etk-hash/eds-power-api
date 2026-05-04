# Module 01 Immutable Demo Fixtures Creation

## Scope

Creation of static immutable JSON fixture data for Module 01 local KZO engineering demo only.

No engine implementation, no test creation, and no integration work are included in this step.

## Files Created

- `tests/fixtures/demo/module_01_kzo_demo/demo_metadata.json`
- `tests/fixtures/demo/module_01_kzo_demo/doc36_busbar_fixture.json`
- `tests/fixtures/demo/module_01_kzo_demo/doc37_node_geometry_fixture.json`
- `tests/fixtures/demo/module_01_kzo_demo/doc37_fastener_selection_fixture.json`
- `tests/fixtures/demo/module_01_kzo_demo/doc38_aggregation_fixture.json`
- `tests/fixtures/demo/module_01_kzo_demo/expected_outputs.json`
- `tests/fixtures/demo/module_01_kzo_demo/optional_backup_safety_fixture.json`

## Fixture Purpose

These fixture files provide immutable demo-only input and expected output data for the verified local chain:

- `DOC36_BUSBAR_EVALUATION` (PASS fixture)
- `DOC37_SLICE01_NODE_GEOMETRY` (PASS fixtures for Node A and Node B)
- `DOC37_SLICE02_FASTENER_SELECTION` (prepared fastener rules and expected local selection)
- `DOC38_SLICE01_BASIC_AGGREGATION` (prepared source lines for visible aggregation)

The files are explicitly marked as demo-only and not production registry data.

## Node A / Node B Summary

### Node A

- `busbar_node_id`: `KZO_DEMO_NODE_A`
- Total busbar length: `1290 mm`
- Joint stack thickness:
  - `BUSBAR_SIDE_CONNECTIONS`: `30 mm`
  - `EQUIPMENT_SIDE_CONNECTIONS`: `18 mm`
- Fastener expectation:
  - Busbar side bolt: `DEMO_BOLT_M12X55` x `3`
  - Equipment side bolt: `DEMO_BOLT_M12X45` x `3`

### Node B

- `busbar_node_id`: `KZO_DEMO_NODE_B`
- Total busbar length: `1200 mm`
- Joint stack thickness:
  - `BUSBAR_SIDE_CONNECTIONS`: `30 mm`
  - `EQUIPMENT_SIDE_CONNECTIONS`: `18 mm`
- Fastener expectation:
  - Busbar side bolt: `DEMO_BOLT_M12X55` x `3`
  - Equipment side bolt: `DEMO_BOLT_M12X45` x `3`

Node geometry is intentionally different between Node A and Node B to avoid any hidden "multiply-by-two" assumption.

## Expected Outputs Summary

Expected aggregated `kit_issue_lines` totals (two PASS nodes combined):

- `DEMO_BOLT_M12X55` = `6 pcs`
- `DEMO_BOLT_M12X45` = `6 pcs`
- `DEMO_NUT_M12` = `12 pcs`
- `DEMO_FLAT_WASHER_M12` = `24 pcs`
- `DEMO_DISC_SPRING_WASHER_M12` = `12 pcs`

Aggregation remains local production-preparation output only and is not a final ERP BOM.

## Optional Backup Fixture Summary

- Backup file: `tests/fixtures/demo/module_01_kzo_demo/optional_backup_safety_fixture.json`
- Role: `OPTIONAL_BACKUP_ONLY`
- Node: `KZO_DEMO_NODE_BACKUP_INCOMPLETE`
- Expected status: `INCOMPLETE`
- Expected failure code: `PHASE_LENGTH_MISSING`
- Missing field: `phase_length_l2_mm`

The backup fixture is not included in the main PASS-only demo flow.

## Boundary Confirmation

- No engine code changes.
- No tests created.
- No runner created.
- No API/GAS/DB work.
- No production registry data creation.
- No procurement/warehouse/ERP behavior.
- No pricing/CAD behavior.
- No final BOM behavior.
