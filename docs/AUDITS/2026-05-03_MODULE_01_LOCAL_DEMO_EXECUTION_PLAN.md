# MODULE 01 LOCAL DEMO EXECUTION PLAN

## Status

PLANNING ONLY / NO RUNNER / NO IMPLEMENTATION

## Purpose

Define how the Module 01 local demo will execute verified immutable fixtures through verified local engine functions.

The demo must show:

DOC 36 fixture
-> DOC 36 safety/status engine
-> DOC 37 Slice 01 node geometry engine
-> DOC 37 Slice 02 fastener selection engine
-> DOC 38 Slice 01 aggregation engine
-> final local demo output

## Demo Execution Boundary

Allowed:

- local fixture loading
- local engine function calls
- local JSON-style output
- local validation of expected results

Forbidden:

- API
- GAS
- DB
- Supabase
- admin panel
- live registry loading
- fixture mutation
- procurement
- warehouse
- ERP / 1C
- pricing
- CAD
- final BOM release

## Input Fixtures

Use verified immutable fixtures from:

`tests/fixtures/demo/module_01_kzo_demo/`

Required files:

- `demo_metadata.json`
- `doc36_busbar_fixture.json`
- `doc37_node_geometry_fixture.json`
- `doc37_fastener_selection_fixture.json`
- `doc38_aggregation_fixture.json`
- `expected_outputs.json`

Optional backup fixture:

- `optional_backup_safety_fixture.json`

Backup fixture must NOT be included in main PASS execution.

## Planned Execution Flow

### Step 1 - Fixture Load

Load verified immutable fixtures.
Do not modify fixtures.
Do not write back to fixture files.

### Step 2 - DOC 36 Safety Status

Use:
`src/engines/kzo_welded/busbar_evaluation_engine.py`

Function:
`evaluate_busbar_candidate_safety_core(...)`

Expected:
`status = PASS`

### Step 3 - DOC 37 Slice 01 Node Geometry

Use:
`src/engines/kzo_welded/busbar_node_package_engine.py`

Function:
`evaluate_busbar_node_geometry_and_stack(...)`

Run for:

- `KZO_DEMO_NODE_A`
- `KZO_DEMO_NODE_B`

Expected:

Node A:

- `total_busbar_length_mm = 1290`
- `BUSBAR_SIDE joint_stack = 30`
- `EQUIPMENT_SIDE joint_stack = 18`

Node B:

- `total_busbar_length_mm = 1200`
- `BUSBAR_SIDE joint_stack = 30`
- `EQUIPMENT_SIDE joint_stack = 18`

### Step 4 - DOC 37 Slice 02 Fastener Selection

Use:
`src/engines/kzo_welded/busbar_node_fastener_selection_engine.py`

Function:
`evaluate_busbar_node_fastener_selection(...)`

Run for:

- `KZO_DEMO_NODE_A`
- `KZO_DEMO_NODE_B`

Expected per node:

- `BUSBAR_SIDE selected bolt = DEMO_BOLT_M12X55`
- `EQUIPMENT_SIDE selected bolt = DEMO_BOLT_M12X45`
- local `node_fastener_lines` generated
- no final BOM

### Step 5 - DOC 38 Slice 01 Basic Aggregation

Use:
`src/engines/kzo_welded/bom_aggregation_engine.py`

Function:
`aggregate_kzo_node_package_lines(...)`

Expected aggregation totals:

- `DEMO_BOLT_M12X55 = 6 pcs`
- `DEMO_BOLT_M12X45 = 6 pcs`
- `DEMO_NUT_M12 = 12 pcs`
- `DEMO_FLAT_WASHER_M12 = 24 pcs`
- `DEMO_DISC_SPRING_WASHER_M12 = 12 pcs`

Expected:

- `status = PASS`
- `kit_issue_lines` generated
- traceability preserved

## Planned Demo Output

Future runner may produce a local JSON-style output file or console output.

Output must include:

- `demo_id`
- status flow
- node results
- `kit_issue_lines`
- `source_node_ids`
- `source_line_ids`
- `traceability_refs`
- `registry_versions`
- `management_summary`
- note: not final ERP BOM

Output must NOT include:

- price
- stock status
- purchase request
- warehouse movement
- ERP posting

## Audit Trail Requirement

At least one audit trail sample for Node A:

1. DOC 36 accepted busbar candidate.
2. DOC 37 Slice 01 calculated geometry and joint stack.
3. DOC 37 Slice 02 selected fasteners from registry truth.
4. DOC 38 included Node A lines into `kit_issue_lines`.

Each step must include:

- input summary
- decision
- status
- `registry_version`
- traceability reference

## Optional Backup Safety Execution

Backup fixture may be planned as a separate optional execution.

Rules:

- not part of main demo
- not run unless explicitly requested
- expected `status = INCOMPLETE`
- expected `failure_code = PHASE_LENGTH_MISSING`

## Success Criteria

Local demo execution is successful if:

- all main fixtures load
- DOC 36 returns PASS
- both nodes return PASS through DOC 37 Slice 01 and Slice 02
- DOC 38 aggregation returns PASS
- expected `kit_issue_lines` match expected outputs
- traceability is visible
- `registry_versions` are visible
- output is clearly not final ERP BOM
- no API/GAS/DB/procurement/warehouse/ERP drift occurs

## Future Runner Requirements

A future runner/test may be created only after this plan is audited.

Runner must:

- be local-only
- read fixtures without modifying them
- call verified engine functions only
- compare actual outputs to `expected_outputs.json`
- produce deterministic output
- avoid any external integration

## Governance Boundary

This plan does not authorize runner creation.

Runner creation requires:

- Gemini audit of this execution plan
- separate implementation task
- implementation audit
