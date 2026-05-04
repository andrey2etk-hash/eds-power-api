# MODULE 01 DEMO API ENDPOINT PLAN

## Status

PLANNING ONLY / NO API IMPLEMENTATION

## Purpose

Define a demo-only API endpoint for exposing verified Module 01 local demo output to a future GAS thin client.

The endpoint must make the verified local demo available through a controlled response envelope without:

- DB writes
- Supabase integration
- procurement
- warehouse
- ERP / 1C
- pricing
- CAD
- final BOM release

## Current Verified Foundation

- DOC 36 Slice 01 verified
- DOC 37 Slice 01 verified
- DOC 37 Slice 02 verified
- DOC 38 Slice 01 verified
- immutable demo fixtures verified
- fixture validation verified
- local demo runner verified
- 72 tests OK
- Demo UI / API-GAS Integration Plan PASS

## Proposed Endpoint

Endpoint path:
`POST /api/demo/module-01/kzo/run`

Endpoint type:
demo-only

Allowed client:
`GAS_DEMO`

Allowed mode:
`MODULE_01_DEMO`

## Request Envelope

Required fields:

- `request_id`
- `client_type`
- `mode`
- `product_type`
- `demo_id`
- `requested_output_blocks`
- `operator_context`

Validation rules:

- `client_type` must be `GAS_DEMO`
- `mode` must be `MODULE_01_DEMO`
- `product_type` must be `KZO`
- `demo_id` must be `MODULE_01_KZO_DEMO_001`
- no production object number required
- no pricing flag allowed
- no procurement flag allowed
- no warehouse flag allowed
- no ERP flag allowed

## request_id Rule

- `request_id` is required.
- `request_id` must be valid UUID v4.
- API must reject missing or invalid `request_id`.
- Failure code: `ERR_INVALID_REQUEST_ID`.

Rationale:
Guarantees request traceability and prevents ambiguous demo logs.

## requested_output_blocks Allowlist

Allowed output blocks:

- `demo_status`
- `status_flow`
- `node_results`
- `fastener_decisions`
- `kit_issue_lines`
- `traceability`
- `boundary_note`
- `management_summary`
- `registry_versions`

Rules:

- `requested_output_blocks` is required.
- It must be a non-empty array.
- Every requested block must be in the allowlist.
- Unknown blocks must be rejected.
- Failure code: `ERR_UNSUPPORTED_OUTPUT_BLOCK`.

## Response Envelope

Required top-level fields:

- `status`
- `data`
- `error`
- `metadata`

On PASS:
`status = success`

`data` includes:

- `demo_id`
- `status_flow`
- `node_results`
- `fastener_decisions`
- `kit_issue_lines`
- `traceability`
- `registry_versions`
- `management_summary`
- `boundary_note`

`management_summary` is mandatory.
If missing:
- `status = error`
- `error_code = ERR_LOGIC_CHAIN_FAILURE`

`metadata` includes:

- `request_id`
- `logic_version`
- `demo_version`
- `generated_at`
- `client_type`
- `response_source = MODULE_01_LOCAL_DEMO_RUNNER`

`error = null`

On failure:
`status = error`

`error` includes:

- `error_code`
- `message`
- `source_field`
- `notes`

`metadata` still includes:

- `request_id`
- `client_type`
- `generated_at`

## API Execution Boundary

API may:

- validate request envelope
- call verified local demo runner or equivalent verified local chain
- return deterministic demo output
- include boundary note
- include traceability
- include registry versions

API must NOT:

- calculate new engineering logic outside verified Module 01 chain
- mutate fixtures
- write DB
- call Supabase
- create production registry data
- create procurement request
- create warehouse transaction
- create ERP/1C posting
- create final BOM
- calculate pricing
- perform CAD validation
- accept forbidden production flags

If request includes any of these flags:

- `pricing`
- `procurement`
- `warehouse`
- `erp`
- `cad`
- `production`
- `db_write`
- `supabase_write`

API must reject request.
Failure code:
`ERR_FORBIDDEN_FLAG`

## Demo Runner Use

Preferred:
API calls a pure local function or wrapper around the verified demo runner logic.

Requirement:
runner/output must remain deterministic.

If demo runner currently writes output file:
API planning must decide whether endpoint:

- reads generated output
or
- calls runner function and returns in-memory output

Preferred for future implementation:
call a pure function and return in-memory output.
Do not depend on file write for API response unless separately justified.

## Pure Function Demo Runner Rule

Future API implementation must call a pure function or in-memory wrapper around the verified Module 01 demo chain.

Preferred:

- call local verified demo chain in memory
- return in-memory response object

Forbidden as source of truth:

- reading previously generated `module_01_demo_run_output.json` as the primary response source
- relying on stale output file
- mutating fixture files

Allowed only for comparison/debug:

- reading expected output fixtures if explicitly treated as validation reference, not runtime truth

## Required Output Blocks

API response must support `requested_output_blocks`.

Allowed:

- `demo_status`
- `status_flow`
- `node_results`
- `fastener_decisions`
- `kit_issue_lines`
- `traceability`
- `boundary_note`
- `management_summary`

If requested block is unsupported:
return error:
`error_code = UNSUPPORTED_OUTPUT_BLOCK`

## fastener_decisions Contract

API must provide rows compatible with Google Sheets output block.

Fields:

- `node`
- `connection_group`
- `required_bolt_length_mm`
- `candidate_bolt`
- `candidate_length_mm`
- `decision`
- `selected_bolt`
- `reason`
- `registry_version`

Rules:

- `decision` must be `SELECTED` or `REJECTED`
- `required_bolt_length_mm` must come from engine/demo output
- API must not calculate or modify the decision
- GAS will only display these rows

## API-Level Fixture Immutability Rule

Before passing fixture/demo data into engine functions:

- API implementation must deep-copy input objects
- API must not mutate fixture objects
- API must detect fixture mutation if feasible

If mutation detected:

- `status = error`
- `error_code = ERR_FIXTURE_MUTATION_DETECTED`

## Boundary Note Requirement

Response must include `boundary_note` stating:

- local demo only
- not production data
- not final ERP BOM
- not procurement
- not warehouse
- not ERP/1C
- not pricing
- not CAD

## Demo Boundary Response Header

API response must include header:

`X-EDS-Power-Mode: DEMO`

Rules:

- GAS must verify this header in future GAS implementation.
- If missing or not `DEMO`, GAS must treat response as invalid.
- Header does not replace body `boundary_note`; both are required.

## Failure Behavior

If request invalid:

- return `status = error`
- do not run demo chain

If demo runner fails:

- return `status = error`
- include `error_code`
- include `notes`
- do not fallback to partial calculation

If API unavailable:
handled by GAS, not by this endpoint plan.

## Demo API Error Codes

Required error codes:

- `ERR_INVALID_REQUEST_ID`
- `ERR_INVALID_CLIENT_TYPE`
- `ERR_INVALID_MODE`
- `ERR_INVALID_PRODUCT_TYPE`
- `ERR_INVALID_DEMO_ID`
- `ERR_UNSUPPORTED_OUTPUT_BLOCK`
- `ERR_FORBIDDEN_FLAG`
- `ERR_DEMO_RUNNER_FAILURE`
- `ERR_LOGIC_CHAIN_FAILURE`
- `ERR_FIXTURE_MUTATION_DETECTED`
- `ERR_DEMO_VERSION_MISMATCH`
- `ERR_BOUNDARY_VIOLATION`

Rules:

- API must return specific `error_code`.
- API must not return generic error only.
- GAS must display `error_code` and message.
- API must not fallback to partial calculation.

## Security / Exposure Boundary

For MVP demo:

- endpoint is demo-only
- do not expose production data
- do not accept arbitrary registry data
- do not accept production object IDs
- do not allow unauthenticated broad production use

Authentication/authorization may be planned later, but this plan does not implement it.

## Test Plan For Future Implementation

Required future tests:

1. valid request returns success.
2. invalid `client_type` returns error.
3. invalid `mode` returns error.
4. invalid `product_type` returns error.
5. invalid `demo_id` returns error.
6. unsupported output block returns `UNSUPPORTED_OUTPUT_BLOCK`.
7. pricing/procurement/warehouse/ERP flags are rejected.
8. response contains `fastener_decisions`.
9. response contains `boundary_note`.
10. response contains traceability and registry_versions.
11. response does not write DB/Supabase.
12. response does not contain final ERP BOM fields.
13. response is deterministic for same input.
14. demo runner failure maps to error envelope.

## Governance Boundary

This plan does NOT authorize:

- API code implementation
- GAS implementation
- DB/Supabase integration
- production deployment
- registry data creation
- procurement/warehouse/ERP behavior
- pricing/CAD behavior

Future API implementation requires:

- Gemini audit of this plan
- separate implementation task
- implementation audit

## Success Criteria

The demo API endpoint is successful if:

- valid `GAS_DEMO` request receives deterministic Module 01 demo output
- response envelope is compatible with GAS thin client
- `fastener_decisions` block is present
- `kit_issue_lines` and traceability are present
- `boundary_note` is present
- no DB/Supabase/procurement/warehouse/ERP/pricing/CAD drift occurs

## Gemini Audit Status

- audit verdict: `SAFE WITH FIXES`
- fixes applied:
  - UUID v4 `request_id`
  - output block allowlist
  - error code registry
  - pure function / in-memory rule
  - API-level immutability rule
  - demo boundary header
  - mandatory `management_summary`
  - strict forbidden flags
- implementation remains blocked until re-audit/pass
- no API/GAS code created
- no DB/Supabase/procurement/warehouse/ERP/pricing/CAD actions
