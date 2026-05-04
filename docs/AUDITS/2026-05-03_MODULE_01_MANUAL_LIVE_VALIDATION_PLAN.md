# MODULE 01 MANUAL LIVE VALIDATION PLAN

## Status

PLANNING ONLY / NO LIVE EXECUTION

## Purpose

Define a manual validation checklist for the full Module 01 demo chain.

This validation proves:

- Google Sheets UI works
- GAS request envelope works
- API endpoint responds
- DEMO header is validated
- Module 01 output is written back into Sheets
- no engineering logic is performed in Sheets/GAS

## Pre-Validation Requirements

Before live validation:

- API service is deployed and reachable
- endpoint URL known: `/api/demo/module-01/kzo/run`
- Google Sheet contains or can create sheet: `MODULE_01_DEMO`
- GAS file: `Module01DemoClient.gs`
- API URL entered in cell `B2`
- no production data used
- no DB/Supabase/ERP/procurement/warehouse/pricing/CAD involved

## Validation Checklist

### 1. Sheet Initialization

Expected:

- Sheet `MODULE_01_DEMO` exists or is created automatically.
- Control block exists in `A1:H9`.
- Cell `B2` contains API base URL or full endpoint URL.

PASS if:

- sheet exists
- control labels visible
- API URL is set

FAIL if:

- sheet cannot be created
- B2 is empty before run

### 2. Menu Check

Expected menu:
`EDS Power Demo`

Items:

- `Run Module 01 Demo`
- `Clear Module 01 Demo Output`

PASS if:

- menu appears after spreadsheet open/reload

FAIL if:

- menu missing

### 3. Run Command

Action:
Click:
`EDS Power Demo -> Run Module 01 Demo`

Expected:

- previous output blocks clear
- Run Status changes to `RUNNING...`
- Last Request ID is generated
- Last Run Time is updated

PASS if:

- visible RUNNING state appears
- old results are cleared

FAIL if:

- old results remain mixed with new run
- request_id not generated

### 4. API Response Header Validation

Expected:

- API response includes: `X-EDS-Power-Mode = DEMO`

PASS if:

- GAS accepts response and proceeds

FAIL if:

- GAS displays invalid demo mode response error

### 5. Demo Status Output

Expected:

- status = success
- demo_id = MODULE_01_KZO_DEMO_001
- demo_version = demo_v1

PASS if:

- status block shows success/PASS-like result

FAIL if:

- status missing
- demo_version not demo_v1

### 6. Status Flow Output

Expected:

- DOC36 = PASS
- DOC37 Slice 01 = PASS
- DOC37 Slice 02 = PASS
- DOC38 Slice 01 = PASS

PASS if:

- all stages visible and PASS

FAIL if:

- any stage missing or non-PASS

### 7. Node Results Output

Expected:

Node A:

- total length = 1290 mm

Node B:

- total length = 1200 mm

Expected joint stacks:

- BUSBAR_SIDE = 30 mm
- EQUIPMENT_SIDE = 18 mm

PASS if:

- Node A and Node B values match expected outputs

FAIL if:

- values missing or changed

### 8. Fastener Decisions Output

Expected:

BUSBAR_SIDE:

- required bolt length = 48.5 mm
- M12x45 = REJECTED
- M12x55 = SELECTED

EQUIPMENT_SIDE:

- required bolt length = 36.5 mm
- M12x45 = SELECTED

PASS if:

- fastener decision rows clearly show selected/rejected logic

FAIL if:

- GAS calculates or edits values
- selected/rejected rows missing
- M12x45 incorrectly selected for BUSBAR_SIDE

### 9. Kit Issue Lines Output

Expected totals:

- M12x55 bolt = 6 pcs
- M12x45 bolt = 6 pcs
- M12 nut = 12 pcs
- M12 flat washer = 24 pcs
- M12 disc spring washer = 12 pcs

PASS if:

- all totals match

FAIL if:

- any quantity is missing or wrong

### 10. Traceability Output

Expected visible fields:

- source_node_ids
- source_line_ids
- traceability_refs
- registry_version

PASS if:

- traceability data is visible for kit issue lines

FAIL if:

- traceability missing

### 11. Boundary Note / Management Summary

Expected boundary note includes:

- local demo only
- not production data
- not final ERP BOM
- not procurement
- not warehouse
- not ERP/1C
- not pricing
- not CAD

PASS if:

- boundary note is visible

FAIL if:

- boundary note missing or incomplete

### 12. Error Scenario — Empty API URL

Action:
Clear `B2`.
Run demo.

Expected:

- transport/configuration error displayed
- engineering result blocks remain empty
- no fallback calculation

PASS if:

- error block appears
- old results are not visible

FAIL if:

- old PASS result remains
- local calculation happens

### 13. Error Scenario — Invalid API URL

Action:
Set invalid API URL.
Run demo.

Expected:

- transport error displayed
- engineering result blocks remain empty

PASS if:

- transport error shown
- old results cleared

FAIL if:

- old result remains visible

### 14. Clear Output Command

Action:
Click:
`EDS Power Demo -> Clear Module 01 Demo Output`

Expected:

- all output blocks clear
- control block remains

PASS if:

- output blocks empty

FAIL if:

- control block deleted
- output blocks remain

## Evidence To Capture

During manual validation, capture:

- screenshot of successful run
- screenshot of fastener_decisions block
- screenshot of kit_issue_lines block
- screenshot of boundary_note block
- screenshot of error scenario if possible
- API URL used
- timestamp
- operator name
- result: PASS / FAIL

## Manual Validation Result Template

Create result fields:

- validation_date
- operator
- API URL
- commit hash
- overall_result
- checklist_results
- notes
- screenshots_reference

## Governance Boundary

This plan does NOT authorize:

- changing GAS code
- changing API code
- changing engine code
- changing fixtures
- DB/Supabase integration
- production deployment
- procurement/warehouse/ERP behavior
- pricing/CAD behavior
- final ERP BOM release

If manual validation fails:

- record failure
- do not hotfix without separate task
- return to targeted fix planning

## Gemini Audit Status

- final verdict: `PASS`
- no required fixes
- plan `CLOSED / APPROVED FOR MANUAL EXECUTION`
- next allowed step: `Manual Live Validation Execution`
- no live execution performed in this closeout
