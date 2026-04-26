# Stage 3B API Skeleton

## Audit date

2026-04-26

## Trigger

Stage 3B creates the first safe API skeleton endpoint for KZO Calculation Object V1.

## Endpoint created

`POST /api/calc/prepare_calculation`

## Scope

API skeleton only.

Implemented:

- JSON request acceptance
- envelope validation
- module/action validation
- KZO MVP required field validation
- enum validation
- quantity sum validation
- success response envelope
- validation error response envelope

## No implementation expansion

Not implemented:

- real calculation logic
- Supabase writes
- DB tables
- costing
- BOM
- production transfer
- AUTH expansion
- KTP
- Powerline
- architecture rewrite

## Contract references

- `docs/00-02_CALC_CONFIGURATOR/09_KZO/06_DATA_MODEL.md`
- `docs/00-02_CALC_CONFIGURATOR/09_KZO/07_VALIDATION.md`
- `docs/00_SYSTEM/04_DATA_CONTRACTS.md`

## Stage 3B tests

Gemini pre-commit fixes applied.

Smoke cases executed:

- valid KZO payload — passed
- missing required field — passed
- invalid enum — passed
- invalid configuration_type — passed
- invalid cell_distribution key — passed
- quantity mismatch — passed
- error envelope shape — passed

Test method:

- direct endpoint function call

Note:

- FastAPI `TestClient` was not used because local environment lacked `httpx`
- no new dependency was added for Stage 3B

## Status

Stage 3B API skeleton created.
