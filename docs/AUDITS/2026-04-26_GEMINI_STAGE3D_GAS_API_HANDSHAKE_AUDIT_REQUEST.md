# GEMINI STAGE 3D GAS API HANDSHAKE AUDIT REQUEST

## Audit Context

Stage 3D created the first minimal Google Apps Script to Render API handshake for KZO `prepare_calculation`.

## Files Under Review

1. gas/Stage3D_KZO_Handshake.gs
2. docs/CHANGELOG.md
3. docs/AUDITS/2026-04-26_STAGE_3D_GAS_API_HANDSHAKE.md
4. docs/00_SYSTEM/04_DATA_CONTRACTS.md
5. docs/00-02_CALC_CONFIGURATOR/09_KZO/06_DATA_MODEL.md
6. docs/00-02_CALC_CONFIGURATOR/09_KZO/07_VALIDATION.md
7. docs/00-02_CALC_CONFIGURATOR/09_KZO/04_OUTPUTS.md
8. main.py

## Scope Implemented

- GAS handshake only
- one valid KZO MVP request body
- `UrlFetchApp.fetch` POST request
- response JSON parsing
- HTTP code logging
- response status logging
- error logging
- `data.basic_result_summary` logging on success
- timeout / request failure structured logging without automatic retry

## Explicit Exclusions

- no full UI
- no Supabase
- no DB writes
- no AUTH expansion
- no roles
- no costing
- no BOM
- no weight / dimensions
- no production logic
- no architecture rewrite
- no API contract change

## Contract Question

Stage 3D task specified GAS target:

`https://YOUR_RENDER_URL/calc/kzo/prepare`

Current Stage 3B FastAPI endpoint is:

`/api/calc/prepare_calculation`

Cursor did not change the API route.

Gemini must judge whether the GAS placeholder should remain as requested or be aligned to the existing Stage 3B endpoint before commit.

## Gemini Questions

1. Does GAS remain a thin client only?
2. Does the request body match `04_DATA_CONTRACTS.md`?
3. Does the payload match KZO Calculation Object V1?
4. Does the script avoid business logic, calculations, DB, AUTH, and UI expansion?
5. Is timeout/error handling acceptable for MVP handshake?
6. Is the endpoint path mismatch acceptable, or must it be fixed before commit?
7. Is Stage 3D safe to commit/push?
8. Is Stage 3E allowed to proceed to manual Google Sheets / Apps Script run?

## Required Gemini Output

SAFE TO COMMIT / COMMIT WITH FIXES / DO NOT COMMIT

## POST-AUDIT FIX IMPLEMENTATION REPORT

### Gemini verdict

COMMIT WITH FIXES

### Accepted fixes applied

- GAS `API_URL` aligned to current committed API route:
  `https://YOUR_RENDER_URL/api/calc/prepare_calculation`
- `contentType: "application/json"` remains explicit in `UrlFetchApp.fetch` options
- hardcoded test payload includes `logic_version`
- large KZO MVP request body moved to `buildStage3DKzoPayload()`
- `testKzoPrepareCalculation()` now calls `buildStage3DKzoPayload()`
- `MVP_TIMEOUT_NOTE` constant added
- no retry logic added
- no async queue added
- no UI added

### Rejected / deferred items

- no automatic retry
- no async queue
- no Google Sheets UI
- no API route change
- no API contract change
- no Supabase
- no AUTH

### Final internal status

READY_FOR_COMMIT

## Strict Rules

- No implementation expansion
- No API rewrite
- No architecture rewrite
- Audit only
- Aggressive scope and contract check

Final rule:

Until Gemini verdict, Stage 3D remains UNCOMMITTED / PENDING_EXTERNAL_AUDIT.
