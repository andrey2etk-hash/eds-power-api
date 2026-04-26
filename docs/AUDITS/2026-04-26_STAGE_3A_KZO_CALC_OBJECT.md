# Stage 3A KZO Calculation Object

## Audit date

2026-04-26

## Trigger

Stage 3A creates the first real KZO MVP Calculation Object V1 contract before API skeleton work.

## First true product contract

KZO Calculation Object V1 defines:

- object_number
- product_type
- logic_version
- voltage_class
- configuration_type
- quantity_total
- cell_distribution
- status
- optional breaker_type
- optional notes

## Implementation-safe

The contract is documentation-only and aligns with:

- `docs/00-02_CALC_CONFIGURATOR/09_KZO/07_VALIDATION.md`
- `docs/00_SYSTEM/04_DATA_CONTRACTS.md`
- `docs/00_SYSTEM/06_OBJECT_STATUSES.md`

The first MVP scenario is documented as a JSON payload for object `7445-B`.

## No code

No implementation was created.

Not performed:

- API code
- FastAPI endpoint
- Render deployment
- Supabase migration
- DB schema changes
- AUTH expansion
- KTP logic
- Powerline logic
- architecture rewrite

## Stage 3B gate

Stage 3B gate = API skeleton.

Stage 3B may start only after final verification that:

- KZO Calculation Object V1 fields match validation docs
- MVP inputs match output expectations
- object statuses map to global business object lifecycle
- API skeleton remains contract-first and implementation-minimal

## Status

Stage 3A documentation created.
