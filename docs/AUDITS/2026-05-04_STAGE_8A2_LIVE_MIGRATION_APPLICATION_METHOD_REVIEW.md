# Stage 8A.2 Live Migration Application Method Review

## Status
DIAGNOSTIC REVIEW ONLY / NO DB ACTIONS

## Why This Review Was Needed

Current Module 01 remote lane has repeated `SQLSTATE 28P01` / `db push` authentication failures, while historical Stage 8A records indicate a prior live PASS around 2026-04-30. This review was required to recover exactly how hosted `calculation_snapshots_v1` was actually applied and whether prior success proved `db push` tooling or bypassed it.

## Documents Found

- `docs/AUDITS/2026-04-30_STAGE_8A_2_1_LIVE_DEPLOY_CALCULATION_SNAPSHOTS.md` (exists)
- `docs/AUDITS/2026-04-30_STAGE_8A_2_0_REMOTE_MIGRATION_HISTORY_PREFLIGHT.md` (exists; operator playbook)
- `docs/AUDITS/2026-04-29_STAGE_8A_SUPABASE_LIVE_VERIFICATION_GATE.md`
- `docs/AUDITS/2026-04-29_STAGE_8A_0_6_ACTUAL_REMOTE_BASELINE_CAPTURE.md`
- `docs/CHANGELOG.md` (Stage 8A closure entries)
- `docs/AUDITS/00_AUDIT_INDEX.md` (Stage 8A.2.0 / 8A.2.1 index entries)
- `supabase/README.md`
- `supabase/migrations/README.md`

## Actual Previous Application Method

- **Method identity:** **unknown / not explicitly recorded**
- **What is documented:**
  - `8A.2.1` states hosted migration was applied "**directly or via controlled `db push` after schema_migrations alignment**".
  - Stage 8A live gate precondition states migration applied in target Supabase by "**SQL editor or `supabase db push`**".
  - `8A.2.0` is a preflight/playbook and does not record final executed operator command transcript for the successful live mutation.
- **Evidence-based conclusion:** repo confirms live result (table exists + API insert PASS), but does not preserve a single explicit operator command path proving whether final apply was SQL Editor, `db push`, or another direct SQL path.
- **Confidence level:** **High** for "method not explicitly recoverable from repo docs"; **Low** for picking one concrete method.

## What Previous Success Proved

- **API insert success:** proven (`POST /api/kzo/save_snapshot` live PASS record).
- **Table existed on hosted Supabase:** proven (`public.calculation_snapshots` row correlation with returned `snapshot_id`).
- **Row confirmed:** proven (live verification gate references persisted row confirmation).
- **`supabase migration list` proven on successful path:** **not proven** by recorded evidence.
- **`supabase db push` proven on successful path:** **not proven** by recorded evidence.
- **Bypass possibility:** documented as possible (SQL Editor/manual path explicitly allowed in gate wording), but exact executed path remains unpinned.

## Implication For Module 01 Slice 01

- Do **not** assume prior Stage 8A live PASS validates current CLI auth path.
- Current Module 01 should not continue blind `db push` retries without method clarity and credential-path stability.
- Most defensible path is a **separate audited manual remote apply decision**:
  - either stabilize CLI auth + prove `migration list`/`db push` path end-to-end first, or
  - explicitly authorize controlled manual SQL Editor (or equivalent direct SQL) apply path with verification/rollback doctrine.
- If governance requires reproducibility and auditability, create a dedicated "Remote Apply Method Decision + Execution Plan" before any write action.

## Recommended Next Step

Open a narrow audited decision task: **Module 01 Remote Apply Method Decision (CLI `db push` path vs Manual SQL Editor path)** with explicit acceptance criteria for traceability, rollback, and post-apply verification. Until that decision is closed, keep remote mutation blocked.

## Safety Confirmation

- no `db push`
- no migration execution
- no DDL
- no table creation
- no DB writes
- no password reset
- no relink
- no API/GAS/Python changes
- no migration file edits
- no secrets stored
