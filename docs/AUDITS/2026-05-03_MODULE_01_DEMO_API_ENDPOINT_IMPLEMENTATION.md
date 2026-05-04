# MODULE 01 DEMO API ENDPOINT IMPLEMENTATION

## Status

IMPLEMENTED / CLOSED / VERIFIED

## Scope

NARROW API IMPLEMENTATION ONLY for demo endpoint:

- endpoint `POST /api/demo/module-01/kzo/run`
- request/response envelope and validation
- demo-only error code mapping
- in-memory verified local runner usage
- no GAS
- no DB/Supabase
- no procurement/warehouse/ERP
- no pricing/CAD
- no production deployment

## Files Changed

- `main.py`
- `src/runners/module_01_demo_runner.py`
- `tests/demo_runner_module_01.py`
- `tests/test_module_01_demo_api_endpoint.py`
- `tests/test_module_01_local_demo_runner.py`
- `docs/AUDITS/2026-05-03_MODULE_01_DEMO_API_ENDPOINT_IMPLEMENTATION.md`
- `docs/CHANGELOG.md`
- `docs/NOW.md`

## Endpoint Implemented

Added:

- `POST /api/demo/module-01/kzo/run`

Behavior:

- validates required request fields
- enforces UUID v4 `request_id`
- enforces exact `client_type` / `mode` / `product_type` / `demo_id`
- validates non-empty `requested_output_blocks` by strict allowlist
- rejects forbidden flags (`pricing`, `procurement`, `warehouse`, `erp`, `cad`, `production`, `db_write`, `supabase_write`)
- returns demo-only envelope with `status`, `data`, `error`, `metadata`

## Validation and Error Codes Implemented

Implemented API error code registry:

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

Error responses return:

- `status = error`
- `data = null`
- `error.error_code`
- `error.message`
- `error.source_field`
- `error.notes`
- `metadata.request_id`
- `metadata.client_type`
- `metadata.generated_at`

## Response Header Implemented

Both success and error responses now include:

- `X-EDS-Power-Mode: DEMO`

## Pure Function / In-Memory Rule

Endpoint uses in-memory runner call:

- helper `_run_module_01_demo_in_memory()`
- invokes `run_module_01_local_demo(write_output=False)`
- runner import source is runtime-safe: `src/runners/module_01_demo_runner.py`

Boundary compliance:

- endpoint does not read generated output JSON as source of truth
- endpoint does not write output files
- endpoint does not mutate fixtures (runner deep-copy guard preserved)
- fixture mutation assertion is mapped to `ERR_FIXTURE_MUTATION_DETECTED`

## Response Data Notes

- `management_summary` is mandatory (empty/missing -> `ERR_LOGIC_CHAIN_FAILURE`)
- `boundary_note` is mandatory and validated for demo boundary markers (`ERR_BOUNDARY_VIOLATION`)
- `fastener_decisions` returned as row contract:
  - `node`
  - `connection_group`
  - `required_bolt_length_mm`
  - `candidate_bolt`
  - `candidate_length_mm`
  - `decision`
  - `selected_bolt`
  - `reason`
  - `registry_version`
- output block filtering is enabled by `requested_output_blocks`
- `boundary_note` and `management_summary` are force-included on PASS for demo safety

## Gemini PASS WITH FIXES Corrections

Applied corrections from Gemini `PASS WITH FIXES` audit:

- Removed API-side `fastener_decisions` reconstruction.
- API now relays `fastener_decisions` directly from verified in-memory runner output.
- Boundary note aligned to include all required markers:
  - local demo only
  - not production data
  - not final ERP BOM
  - not procurement
  - not warehouse
  - not ERP/1C
  - not pricing
  - not CAD
- Moved pure runner into runtime module: `src/runners/module_01_demo_runner.py`.
- `tests/demo_runner_module_01.py` converted to thin CLI wrapper importing runtime runner module.
- API no longer imports demo runner from `tests` package.
- Missing request identity fields now map to specific error codes:
  - `request_id` -> `ERR_INVALID_REQUEST_ID`
  - `client_type` -> `ERR_INVALID_CLIENT_TYPE`
  - `mode` -> `ERR_INVALID_MODE`
  - `product_type` -> `ERR_INVALID_PRODUCT_TYPE`
  - `demo_id` -> `ERR_INVALID_DEMO_ID`
- Added tests for error-header presence on validation/forbidden failures.
- Added tests proving `fastener_decisions` source truth is runner output.
- Forbidden scope remains clean.

## Tests Added

Created:

- `tests/test_module_01_demo_api_endpoint.py`

Coverage includes:

- valid request success path
- all required request validation failures
- unsupported output block handling
- forbidden flag rejection
- fastener decisions presence and expected selections/rejections
- kit issue totals
- traceability and registry versions
- no final ERP/procurement/warehouse/pricing fields in response
- no DB/Supabase calls in endpoint function
- API runtime runner import is not from `tests` package
- boundary note full marker validation
- specific error-code mapping for missing identity fields
- error response header `X-EDS-Power-Mode: DEMO` on validation/forbidden paths
- `fastener_decisions` equals runner output source truth
- deterministic stable data for same input
- management summary guard
- `demo_v1` presence checks

## Test Results

Executed:

- `python -m unittest tests.test_module_01_demo_api_endpoint`
  - result: `Ran 28 tests ... OK`
- `python -m unittest tests.test_busbar_evaluation_engine_slice01 tests.test_busbar_node_package_slice01 tests.test_busbar_node_fastener_selection_slice02 tests.test_bom_aggregation_slice01 tests.test_module_01_demo_fixtures_validation tests.test_module_01_local_demo_runner tests.test_module_01_demo_api_endpoint`
  - result: `Ran 100 tests ... OK`

## Forbidden Scope Confirmation

Confirmed in this implementation:

- no GAS code changes
- no DB/Supabase integration changes
- no procurement/warehouse/ERP behavior added
- no pricing/CAD behavior added
- no production deployment actions
- no final ERP BOM behavior

## Gemini Re-Audit Status

- final verdict: `PASS`
- Module 01 Demo API Endpoint status: `CLOSED / VERIFIED`
- no required fixes remain
- fastener source-truth: `SAFE`
- boundary note: `COMPLETE`
- runtime runner isolation: `SAFE`
- error normalization: `ACCEPTED`
- boundary check: `CLEAN`
- test evidence: `Ran 100 tests ... OK`
- next allowed step: `Demo GAS Thin Client Planning Only`
