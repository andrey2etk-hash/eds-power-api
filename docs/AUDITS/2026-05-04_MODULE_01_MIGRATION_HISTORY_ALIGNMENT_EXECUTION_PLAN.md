# MODULE 01 MIGRATION HISTORY ALIGNMENT EXECUTION PLAN

## Status
DOC ONLY / EXECUTION PLANNING / NO SQL EXECUTION

## Gemini Audit Status
- final verdict: `PASS`
- plan status: `CLOSED / APPROVED`
- Phase 1 read-only inspection approved
- final INSERT remains forbidden in this closeout step
- next allowed step: `Migration History Alignment Read-only Inspection Execution`

## Purpose
Plan controlled alignment of Supabase migration history for migration version `20260504190000` after manual SQL Editor apply.

## Source Facts
- remote schema applied
- 8 Module 01 tables present
- 9 roles present
- `schema_migrations` not modified yet
- `db push` not used
- migration repair not used

## Alignment Target
- schema: `supabase_migrations`
- table: `schema_migrations`
- version: `20260504190000`
- migration file: `20260504190000_module01_schema_slice_01.sql`

## Critical Rule
Do not guess INSERT format.
First inspect actual `schema_migrations` table structure.

## Phase 1 — Read-only Inspection Queries

### 1. Inspect table columns
Use:

```sql
select column_name, data_type, is_nullable, column_default
from information_schema.columns
where table_schema = 'supabase_migrations'
  and table_name = 'schema_migrations'
order by ordinal_position;
```

### 2. Check existing version row
Use:

```sql
select *
from supabase_migrations.schema_migrations
where version = '20260504190000';
```

Expected:
`0` rows.

### 3. Inspect recent migration history shape
Use:

```sql
select *
from supabase_migrations.schema_migrations
order by version desc
limit 5;
```

Purpose:
Confirm actual row shape and whether fields like `name`, `statements`, `inserted_at`, `checksum`, or `execution_time` exist.

### 4. Re-confirm Module 01 apply still valid
Verify 8 tables and 9 roles are still present.

## Phase 2 — Insert Format Determination

Based on Phase 1 output:
- determine exact required columns
- determine whether version-only insert is sufficient
- determine whether `name` or `statements`/`checksum` fields are required
- do not proceed if structure is unclear

## Phase 3 — Controlled Alignment Write

Only after Phase 1 confirms structure and Gemini/execution plan is approved:
prepare exact INSERT.

Example placeholder only, not final:

```sql
insert into supabase_migrations.schema_migrations (...)
values (...);
```

IMPORTANT:
Do not include final guessed INSERT in this plan unless the structure is already known from verified inspection.
If structure is not known yet, the execution result must first capture read-only inspection and then request a second micro-plan for the actual INSERT.

## Phase 4 — Post-insert Verification

After alignment write:
- verify row for version `20260504190000` exists
- verify no duplicate version row
- verify 8 `module01_` tables still present
- verify 9 roles still present
- verify `db push` remains not executed

## Failure Handling

If `schema_migrations` table does not exist:
- stop
- do not create it
- return to planning

If version already exists:
- stop
- do not insert duplicate
- record `PASS/ALREADY_ALIGNED` or investigate

If required columns are unclear:
- stop
- do not insert
- request audit

If INSERT fails:
- stop
- do not retry blindly
- do not patch manually
- document exact error

## Forbidden
- no SQL execution in this planning task
- no `schema_migrations` INSERT in this planning task
- no migration repair
- no `db push`
- no DDL/table creation
- no API/GAS/Python changes
- no migration file edits
- no secrets

## Next Allowed Step
Gemini audit of Migration History Alignment Execution Plan.

If PASS:
Migration History Alignment Read-only Inspection Execution.

Important:
Actual INSERT may require another micro-plan after inspection if table structure is not already known.
