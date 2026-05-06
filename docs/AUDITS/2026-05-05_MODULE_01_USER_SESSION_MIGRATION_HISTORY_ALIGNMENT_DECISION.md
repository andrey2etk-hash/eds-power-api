# MODULE 01 USER SESSION MIGRATION HISTORY ALIGNMENT DECISION

## Status
DOC ONLY / ALIGNMENT DECISION / NO EXECUTION

## Purpose
Decide how to align Supabase migration history after `module01_user_sessions` was manually applied through SQL Editor.

## Current Applied State
Recorded state:
- remote session table applied manually (`public.module01_user_sessions`)
- 13 columns present
- indexes and constraints verified
- no session rows seeded (`session_row_count = 0`)
- dependent Module 01 tables present
- `schema_migrations` not touched yet

## Problem
Remote schema and migration history are asymmetric:
- `public.module01_user_sessions` exists
- migration version `20260505120000` may not be marked as applied in `supabase_migrations.schema_migrations`

## Why Alignment Is Needed
Without alignment:
- future migration tooling may try to re-apply `module01_user_sessions` migration
- migration history remains asymmetric
- `db push` remains unsafe
- operator cannot rely on migration history as canonical

## Candidate Alignment Paths

### Path A — Supabase CLI migration repair
Pros:
- official mechanism

Cons:
- current CLI migration-management path blocked by `SQLSTATE 28P01`

### Path B — Manual schema_migrations INSERT
Pros:
- practical after SQL Editor apply
- already used successfully for previous Module 01 alignments
- can restore history symmetry if done exactly

Cons:
- direct mutation of migration history
- requires exact `version` / `name` / `statements`
- must be separately planned, audited, and verified

### Path C — Intentional temporary drift
Pros:
- avoids touching migration history immediately

Cons:
- not acceptable long-term
- keeps tooling unsafe

## Recommended Path
Recommend **Path B** after:
- Gemini audit of this decision
- read-only check that version `20260505120000` is absent
- confirmation that `public.module01_user_sessions` still exists
- exact `statements[]` array generated from approved migration file
- final insert execution plan
- post-insert verification

## Critical Guardrails
- do not insert into `schema_migrations` in this decision step
- do not use guessed INSERT format
- use known `schema_migrations` structure:
  - `version` text NOT NULL
  - `statements` ARRAY nullable
  - `name` text nullable
- confirm no existing row for version `20260505120000`
- confirm session table apply verification remains PASS before alignment
- after alignment, verify row exists and duplicate count is 1
- `db push` remains forbidden until alignment result is audited

## Forbidden In This Decision
- no SQL execution
- no `schema_migrations` insert
- no migration repair
- no db push
- no DB writes
- no API/GAS/Python changes
- no migration edits
- no secrets

## Next Allowed Step
Gemini audit of User Session Migration History Alignment Decision.

If PASS:
Create User Session Migration History Alignment FINAL INSERT Execution Plan.

## Gemini Audit Status

- final verdict: PASS
- decision status: CLOSED / APPROVED
- Path B accepted under strict guardrails
- no INSERT authorized in this decision
- required: exact `statements[]` array from approved migration file
- next allowed step: User Session Migration History Alignment FINAL INSERT Execution Plan
