# MODULE 01 REMOTE APPLY METHOD DECISION

## Status
DOC ONLY / METHOD DECISION / NO EXECUTION

## Purpose
Choose the safe remote apply method for Module 01 Schema Slice 01 after CLI migration path remained blocked by SQLSTATE 28P01.

## Retrospective Finding From Stage 8A
Stage 8A live PASS proved:
- API route worked
- Render env `SUPABASE_URL` / `SUPABASE_SERVICE_ROLE_KEY` worked
- insert into `calculation_snapshots` succeeded
- row correlation by `snapshot_id` succeeded

Stage 8A did NOT prove:
- `supabase db push` worked
- `supabase migration list` worked

Stage 8A accepted:
- SQL Editor or `db push` as possible migration apply methods

## Current Blocker
CLI migration-management path is unstable:
- `migration list` fails with SQLSTATE 28P01
- `db push` fails with SQLSTATE 28P01
- pooler path diagnostics failed
- password/reset/relink attempts did not yet clear migration-history gate

## Baseline Governance Status
- Stage 8A.0.2 historical hold superseded
- operational migration-history guardrail remains
- ordering accepted:
  `20260429110000_remote_legacy_baseline.sql`
  -> `20260429120000_calculation_snapshots_v1.sql`
  -> `20260504190000_module01_schema_slice_01.sql`

## Decision
Proceed with Manual SQL Editor / Direct SQL Apply Path for Module 01 Schema Slice 01, under a separate execution plan and Gemini audit.

## Rationale
- avoids current CLI auth/pooler blocker
- matches Stage 8A acceptable apply options
- preserves velocity
- migration SQL remains version-controlled and approved
- apply can be verified by direct table/role checks

## Scope Of Manual Apply
Only approved migration file:
`supabase/migrations/20260504190000_module01_schema_slice_01.sql`

No edits to migration SQL during apply.

## Mandatory Verification After Apply
Verify:
- all 8 `module01_` tables exist
- 9 seed roles exist
- excluded tables absent:
  `commercial_products`
  `calculation_product_items`
  `product_composition_items`
  `module_routes`
  `object_conversion_links`
- no ERP/procurement/warehouse/pricing/CAD tables
- legacy tables remain present
- no API/GAS/Python code changed

## Migration History Alignment
Manual SQL apply does not automatically prove CLI migration history alignment.

Required rule:
Do NOT manually insert into `supabase_migrations.schema_migrations` in the apply step.

After successful SQL apply + verification:
Open separate audited decision:
- use `supabase migration repair` if possible
- or define emergency manual `schema_migrations` alignment plan
- or keep CLI history intentionally blocked with documented reason

## Forbidden In This Decision
- no SQL execution
- no `db push`
- no DDL
- no table creation
- no DB writes
- no `schema_migrations` manual insert
- no migration repair
- no API/GAS/Python code
- no migration edits
- no secrets

## Next Allowed Step
Gemini audit of this Remote Apply Method Decision.

If PASS:
Create Manual SQL Editor Apply Execution Plan for Module 01 Schema Slice 01.
