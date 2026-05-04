# MODULE 01 DEMO UI / API-GAS INTEGRATION PLAN

## Status

PLANNING ONLY / NO IMPLEMENTATION

## Purpose

Define a controlled demo UI path for running Module 01 verified local engineering logic from Google Sheets through GAS and API.

The purpose is to show how the verified local demo can become an operator-facing demo without compromising governance.

## Current Verified Foundation

- DOC 36 Slice 01 verified
- DOC 37 Slice 01 verified
- DOC 37 Slice 02 verified
- DOC 38 Slice 01 verified
- immutable demo fixtures verified
- local demo runner verified
- 72 tests OK
- executive summary PASS
- milestone committed and pushed

## Target Demo Flow

Google Sheets UI
-> GAS thin client
-> API endpoint
-> Module 01 engine chain
-> API response envelope
-> GAS writeback
-> Google Sheets output blocks

## GAS Boundary

Allowed in GAS:

- collect operator input
- build request envelope
- include demo mode flag
- call API
- receive JSON response
- write output blocks
- show status/failure_code/notes
- show `kit_issue_lines`
- show traceability fields

Forbidden in GAS:

- busbar calculation
- joint stack calculation
- fastener selection
- kit issue aggregation
- registry truth
- pricing
- BOM finalization
- procurement
- warehouse
- ERP/1C
- CAD validation

## API Boundary

API is allowed to:

- receive request envelope
- validate structure
- run Module 01 chain or demo runner
- return response envelope
- include `status_flow`
- include `node_results`
- include `fastener_decisions`
- include `kit_issue_lines`
- include traceability
- include boundary note

API is NOT allowed in this demo slice to:

- write DB
- create procurement
- create warehouse transaction
- create final ERP BOM
- perform pricing
- mutate registry data

## Demo Mode Boundary

Demo mode may use:

- verified immutable demo fixtures
- `demo_v1` registry metadata
- local engine chain
- deterministic output

Demo mode must clearly state:

- not production data
- not final ERP BOM
- not procurement
- not warehouse
- not ERP/1C
- not pricing
- not CAD

## Proposed Request Envelope

Fields:

- `request_id`
- `client_type = GAS_DEMO`
- `mode = MODULE_01_DEMO`
- `product_type = KZO`
- `demo_id = MODULE_01_KZO_DEMO_001`
- `requested_output_blocks`
- `operator_context`

No production object number required for MVP demo.

## Proposed API Response Envelope

Required:

- `status`
- `data`
- `error`
- `metadata`

Data should include:

- `demo_id`
- `status_flow`
- `node_results`
- `fastener_decisions`
- `kit_issue_lines`
- `traceability`
- `registry_versions`
- `management_summary`
- `boundary_note`

Metadata should include:

- `request_id`
- `logic_version`
- `demo_version`
- `generated_at`
- `client_type`

## Google Sheets Output Blocks

Planned blocks:

1. Demo status
2. Status flow
3. Node results
4. Fastener decisions
5. Kit issue lines
6. Traceability
7. Boundary note

Must show:

- PASS / `failure_code`
- `M12x55` vs `M12x45` decision
- `kit_issue_lines` totals
- `source_node_ids` / `traceability_refs`
- "not final ERP BOM"

## Google Sheets fastener_decisions Output Block

Purpose:
Show the engineering reasoning behind fastener selection.

This block must make clear why the system selected one bolt and rejected another.

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

Example rows:

| Node | Connection Group | Required Bolt Length, mm | Candidate Bolt | Candidate Length, mm | Decision | Selected Bolt | Reason | Registry Version |
|---|---|---:|---|---:|---|---|---|---|
| Node A | BUSBAR_SIDE | 48.5 | M12x45 | 45 | REJECTED | M12x55 | Candidate is shorter than required length | demo_v1 |
| Node A | BUSBAR_SIDE | 48.5 | M12x55 | 55 | SELECTED | M12x55 | Shortest active valid bolt | demo_v1 |
| Node A | EQUIPMENT_SIDE | 36.5 | M12x45 | 45 | SELECTED | M12x45 | Candidate length is sufficient | demo_v1 |
| Node B | BUSBAR_SIDE | 48.5 | M12x45 | 45 | REJECTED | M12x55 | Candidate is shorter than required length | demo_v1 |
| Node B | BUSBAR_SIDE | 48.5 | M12x55 | 55 | SELECTED | M12x55 | Shortest active valid bolt | demo_v1 |
| Node B | EQUIPMENT_SIDE | 36.5 | M12x45 | 45 | SELECTED | M12x45 | Candidate length is sufficient | demo_v1 |

Rules:

- GAS only displays this block.
- GAS must not calculate `required_bolt_length_mm`.
- GAS must not compare bolt lengths.
- GAS must not select bolts.
- All `fastener_decisions` must come from API response.
- If `fastener_decisions` are missing, GAS shows a display error, not a fallback calculation.

Director-facing explanation:
"Цей блок показує не тільки який болт вибрано, а й чому коротший болт не підходить."

## Failure Behavior

If API returns non-PASS:
GAS displays:

- `status`
- `failure_code`
- `message`
- `notes`

GAS does not attempt to fix or calculate.

If API unavailable:
GAS displays transport error only.
No local fallback calculation.

## Governance Boundary

This plan does NOT authorize:

- GAS code implementation
- API code implementation
- DB integration
- Supabase integration
- registry data creation
- production deployment
- procurement/warehouse/ERP behavior
- final BOM release

Implementation requires:

- Gemini audit of this plan
- separate slice planning if needed
- separate implementation task
- implementation audit

## Success Criteria

The demo UI/API-GAS integration is successful if:

- Google Sheets can trigger a demo request
- GAS remains thin client
- API returns deterministic Module 01 demo output
- Sheets displays engineering result clearly
- traceability is visible
- boundary note is visible
- no engineering logic appears in GAS
- no API/GAS/DB/procurement/warehouse/ERP drift occurs

## Next Allowed Steps After This Plan

- Gemini audit of Demo UI / API-GAS Integration Plan
- Demo API endpoint planning only
- Demo GAS thin client planning only
- Google Sheets output layout planning only

## Gemini Audit Status

- final verdict: `PASS`
- required fastener_decisions Sheets output block: added
- plan approved for next-stage technical component planning
- no implementation performed
- no GAS/API code created
- no DB/Supabase/procurement/warehouse/ERP/pricing/CAD actions
