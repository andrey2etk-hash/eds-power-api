# MODULE 01 MIGRATION HISTORY ALIGNMENT DECISION

## Status
DOC ONLY / ALIGNMENT DECISION / NO EXECUTION

## Gemini Audit Status

- final verdict: `PASS`
- decision status: `CLOSED / APPROVED`
- Path B (`schema_migrations` manual INSERT) is acceptable only after separate audited execution plan
- no INSERT is authorized in this decision step
- required before any future INSERT: inspect `supabase_migrations.schema_migrations` structure
- next allowed step: `Migration History Alignment Execution Plan`

## Purpose
Decide how to align Supabase migration history after Module 01 Schema Slice 01 was manually applied through SQL Editor.

## Current Applied State
Recorded state:
- remote schema applied manually via Supabase SQL Editor
- 8 `module01_` tables present
- 9 role codes present and active
- excluded tables absent
- legacy tables present
- `schema_migrations` not touched yet

## Problem
Remote schema and migration history are now asymmetric:
- schema objects exist
- migration version `20260504190000` may not be marked as applied in `supabase_migrations.schema_migrations`

## Why Alignment Is Needed
Without alignment:
- future CLI migration operations may try to re-apply Module 01 migration
- future migration history may drift
- `db push` remains unsafe
- operator cannot rely on migration list as canonical history

## Candidate Alignment Paths

### Path A — Supabase CLI migration repair
Use:
`supabase migration repair`

Pros:
- official Supabase mechanism for migration history repair
- avoids manual table mutation

Cons:
- current CLI migration-management path has failed with SQLSTATE `28P01`
- may be unavailable until auth/pooler issue is fixed

### Path B — Manual schema_migrations INSERT
Manually insert the applied migration version into:
`supabase_migrations.schema_migrations`

Pros:
- practical after SQL Editor apply
- bypasses currently blocked CLI repair path
- can restore history symmetry if done exactly

Cons:
- direct mutation of migration history
- requires exact version/name format
- must be separately planned, audited, and verified
- dangerous if SQL apply had not fully succeeded

### Path C — Intentional temporary drift
Do not align immediately, but document drift and forbid `db push`.

Pros:
- avoids touching migration history

Cons:
- leaves future migration tooling blocked/unsafe
- not acceptable long-term

## Recommended Path
Recommend Path B only after:
- Gemini audit of this decision
- separate execution plan
- exact target table structure is verified
- exact INSERT format is confirmed
- post-insert verification query is defined

If Path A becomes available safely, prefer official repair. But current `28P01` makes Path B the likely practical path.

## Critical Guardrails
- do not insert into `schema_migrations` in this decision step
- do not use guessed INSERT format
- first inspect `schema_migrations` columns before any write
- confirm no existing row for version `20260504190000`
- confirm Module 01 apply verification PASS before alignment
- after alignment, verify migration history contains version `20260504190000`
- `db push` remains forbidden until alignment result is audited

## Required Pre-Execution Checks For Future Plan
Future execution plan must include read-only checks:
1. Inspect columns of `supabase_migrations.schema_migrations`.
2. Check whether version `20260504190000` already exists.
3. Confirm `module01_` tables still exist.
4. Confirm 9 roles still exist.
5. Confirm excluded tables absent.

## Forbidden In This Decision
- no SQL execution
- no `schema_migrations` insert
- no migration repair
- no `db push`
- no DDL
- no table creation
- no DB writes
- no API/GAS/Python changes
- no migration edits
- no secrets

## Next Allowed Step
Gemini audit of Migration History Alignment Decision.

If PASS:
Create Migration History Alignment Execution Plan.
