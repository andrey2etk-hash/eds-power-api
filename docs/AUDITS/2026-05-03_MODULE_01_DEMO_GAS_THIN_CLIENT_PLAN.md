# MODULE 01 DEMO GAS THIN CLIENT PLAN

## Status

PLANNING ONLY / NO GAS IMPLEMENTATION

## Purpose

Define how Google Sheets + GAS will act as a thin client for the verified Module 01 Demo API endpoint.

## Current Verified Foundation

- Module 01 engineering core verified
- Demo API endpoint verified
- 100 tests OK
- no DB/Supabase/procurement/warehouse/ERP/pricing/CAD active

## Target Flow

Google Sheets UI
-> GAS request envelope
-> POST /api/demo/module-01/kzo/run
-> API response
-> GAS validates DEMO header
-> GAS writes output blocks to Sheets

## Request Envelope

GAS sends:

- request_id = UUID v4
- client_type = GAS_DEMO
- mode = MODULE_01_DEMO
- product_type = KZO
- demo_id = MODULE_01_KZO_DEMO_001
- requested_output_blocks
- operator_context

Default requested_output_blocks:

- demo_status
- status_flow
- node_results
- fastener_decisions
- kit_issue_lines
- traceability
- boundary_note
- management_summary
- registry_versions

Forbidden request flags:

- pricing
- procurement
- warehouse
- erp
- cad
- production
- db_write
- supabase_write

## GAS Thin Client Boundary

Allowed in GAS:

- create UUID v4 request_id
- build request envelope
- call API with UrlFetchApp
- parse JSON response
- validate X-EDS-Power-Mode = DEMO
- display status/data/error blocks
- clear output ranges before writeback
- write result tables

Forbidden in GAS:

- busbar calculation
- joint stack calculation
- bolt length calculation
- fastener selection
- kit_issue aggregation
- registry truth storage
- price calculation
- final BOM generation
- procurement/warehouse/ERP actions
- CAD checks
- DB/Supabase writes

## Response Validation In GAS

GAS must validate:

- HTTP status
- response JSON parse
- X-EDS-Power-Mode = DEMO
- envelope.status
- envelope.error if status = error
- envelope.data if status = success
- metadata.request_id matches sent request_id
- metadata.client_type = GAS_DEMO
- metadata.demo_version = demo_v1

If header missing or not DEMO:

- display invalid response error
- do not write engineering result blocks

If envelope.status = error:

- display error_code, message, source_field, notes
- do not calculate fallback result

If transport timeout/unavailable:

- display transport error only
- do not calculate fallback result

## Planned Sheet Layout

Create one demo sheet:
MODULE_01_DEMO

Suggested zones:

1. Input / Control Block
- B2: API URL
- B3: Demo ID
- B4: Client Type
- B5: Mode
- B6: Product Type
- B7: Run Status
- B8: Last Request ID
- B9: Last Run Time

2. Demo Status Block
- A12:D16

3. Status Flow Block
- A19:E25

4. Node Results Block
- A28:H40

5. Fastener Decisions Block
- A43:I55

6. Kit Issue Lines Block
- A58:H70

7. Traceability Block
- A73:H85

8. Boundary Note / Management Summary Block
- A88:H96

## fastener_decisions Output Block

Required columns:

- Node
- Connection Group
- Required Bolt Length, mm
- Candidate Bolt
- Candidate Length, mm
- Decision
- Selected Bolt
- Reason
- Registry Version

Rules:

- GAS only writes rows returned by API.
- GAS does not calculate required_bolt_length_mm.
- GAS does not compare bolt lengths.
- GAS does not select bolts.
- If fastener_decisions missing, show display error.

## Kit Issue Lines Output Block

Display:

- item_id
- display_name if present
- item_type
- total_quantity
- unit
- registry_version
- source_node_ids
- traceability_refs

Add visible note:
"Production-preparation kit issue only - not final ERP BOM."

## Error Display Plan

If API returns error:
Display:

- status = error
- error_code
- message
- source_field
- notes
- request_id

If transport error:
Display:

- status = transport_error
- message
- timestamp

GAS must not retry infinitely.
Any retry policy must be explicit and bounded.

## Output Clearance Policy

Before every new Module 01 demo request, GAS must clear all previous output blocks.

Blocks to clear:

- Demo status
- Status flow
- Node results
- Fastener decisions
- Kit issue lines
- Traceability
- Boundary note
- Management summary
- Previous error display

Rules:

- Clear output blocks before sending the new API request.
- Set run status to `RUNNING...` before calling API.
- If API succeeds, write new result blocks.
- If API returns error, write only error block and keep engineering result blocks empty.
- If transport error occurs, write only transport error block and keep engineering result blocks empty.
- GAS must not mix previous successful results with a new failed request.
- GAS must not perform fallback calculations.

Director-facing reason:
"Кожен запуск показує тільки результат поточної сесії. Старі дані очищуються, щоб не змішати різні розрахунки."

## Timeout Plan

Use planned timeout expectation:

- API/GAS response target: 10-15 seconds
- if timeout occurs, display transport error
- no fallback calculation

## Menu / Trigger Plan

Future GAS may add custom menu:
EDS Power Demo
- Run Module 01 Demo
- Clear Demo Output

No installable triggers required for MVP demo.

## Success Criteria

GAS thin client plan is successful if:

- request envelope matches API contract
- API response header is validated
- output blocks show Module 01 demo result
- fastener_decisions are visible
- kit_issue_lines are visible
- traceability is visible
- boundary note is visible
- no engineering logic appears in GAS
- no DB/Supabase/procurement/warehouse/ERP/pricing/CAD drift occurs

## Governance Boundary

This plan does not authorize GAS implementation.

Future GAS implementation requires:

- Gemini audit of this plan
- separate implementation task
- implementation audit

## Gemini Audit Status

- final verdict: `PASS`
- Clearance Policy added
- plan approved for Demo GAS thin client implementation
- no GAS implementation performed
- no API code changed
- no DB/Supabase/procurement/warehouse/ERP/pricing/CAD actions
