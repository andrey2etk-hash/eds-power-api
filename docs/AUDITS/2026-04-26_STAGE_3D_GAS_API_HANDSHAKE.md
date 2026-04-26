# Stage 3D GAS API Handshake

## Audit date

2026-04-26

## Trigger

Stage 3D creates the first minimal Google Apps Script to Render API handshake for KZO `prepare_calculation`.

## What was created

- `gas/Stage3D_KZO_Handshake.gs`
- `testKzoPrepareCalculation()`
- `API_URL` placeholder
- one valid KZO MVP request body
- `UrlFetchApp.fetch` POST call
- response JSON parsing
- HTTP code logging
- response status logging
- error logging
- `data.basic_result_summary` logging on success
- structured timeout / request failure logging without automatic retry

## No UI added

No Google Sheets UI, menu, sidebar, modal, or form was created.

## No DB added

No Supabase connection, DB table, DB write, or migration was added.

## No business logic added

GAS remains a thin client only.

Not added:

- costing
- BOM
- weight
- dimensions
- production logic
- AUTH expansion
- roles
- architecture rewrite

## Contract note

The GAS request body follows `docs/00_SYSTEM/04_DATA_CONTRACTS.md`.

The GAS request payload follows KZO Calculation Object V1.

Gemini fixes applied:

- endpoint aligned
- contentType explicit
- logic_version verified
- payload moved to helper
- timeout note added

Endpoint aligned to current Stage 3B FastAPI route:

`https://YOUR_RENDER_URL/api/calc/prepare_calculation`

No API route was changed in Stage 3D.

## Tests

- script syntax review
- valid request shape matches `04_DATA_CONTRACTS.md`
- no business logic in GAS

## Stage 3E gate

Stage 3E gate = manual run from Google Sheets / Apps Script.

## Status

Stage 3D handshake draft created pending Gemini audit.
