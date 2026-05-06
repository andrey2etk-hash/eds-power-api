# REMOTE BASELINE GOVERNANCE REVIEW BEFORE DB PUSH

## Status
DIAGNOSTIC REVIEW ONLY / NO DB PUSH

## Background
Stage 8A.0.2 introduced a governance hold: remote `public` was non-empty (`legacy_baseline`), and `db push` to remote was forbidden until baseline alignment/migration slotting was established.

Hold mechanics at that time:
- detect remote legacy objects (`objects`, `bom_links`, `ncr`, `production_status`, `v_*`)
- keep `calculation_snapshots_v1` out of root migrations
- require baseline-first ordering before any safe push planning

## Findings

### Current migration root files (`supabase/migrations/`)
- `20260429110000_remote_legacy_baseline.sql`
- `20260429120000_calculation_snapshots_v1.sql`
- `20260504190000_module01_schema_slice_01.sql`
- (archive) `_archive_pre_8a0_1_kzo_tables/20260429120000_kzo_mvp_snapshots_v1_SUPERSEDED.sql`

### Pending folder state (`supabase/migrations/_pending_after_remote_baseline/`)
- no `.sql` files found

### Baseline registry/governance state
- `supabase/schema_registry/LEGACY_REMOTE_BASELINE.md` confirms baseline capture lineage through 8A.0.6 and historical replay blockers.
- `supabase/migrations/README.md` states Stage 8A.1 active chain and explicitly records:
  - baseline `110000` first
  - `calculation_snapshots_v1` promoted to root as `120000` second
- `supabase/README.md` Stage table reflects:
  - 8A.0.2 hold (historical)
  - 8A.0.3 capture
  - 8A.1 local promotion PASS
  - 8A.2.x remote/live alignment with Stage 8A complete

### Later closeouts found
- 8A.0.3: baseline slot created in root
- 8A.0.6: factual remote baseline DDL imported into `110000`
- 8A.1: `120000` promoted from pending to root and local reset PASS
- 8A.2.1: `STAGE_8A_COMPLETE` recorded with hosted `calculation_snapshots` live-pass evidence

### Is 8A.0.2 hold still active?
- As a strict repo-level hold, **no** — it appears superseded by 8A.1 promotion and 8A.2.1 closeout.
- As an operational caution, **yes conditionally** — remote migration history must still be verified before any future push attempt.

## Migration Ordering Assessment
Relevant order in root migrations:
1. `20260429110000_remote_legacy_baseline.sql`
2. `20260429120000_calculation_snapshots_v1.sql`
3. `20260504190000_module01_schema_slice_01.sql`

This ordering is governance-correct for baseline-first progression.

## Push Safety Assessment
Verdict: **SAFE_TO_PLAN_PUSH_AFTER_AUTH**

Interpretation:
- Governance structure for baseline ordering appears in place.
- `calculation_snapshots_v1` is already promoted (not pending).
- Current practical blocker remains remote auth failures (`SQLSTATE 28P01`) plus inability to reliably complete migration-history read in recent sessions.

Important risk note:
- `supabase db push` could still attempt older migrations if remote migration history is not aligned/visible in `schema_migrations`.
- Therefore, after auth is fixed, read-only migration history verification remains mandatory before any push planning.

## Recommended Next Step
Continue auth-fix track first (password reset + relink preflight), then run read-only migration history gate (`migration list --linked`) and confirm expected baseline versions are visible before any push planning.

Then request Gemini audit of this governance review.

## Gemini Audit Status

- final verdict: PASS
- review status: CLOSED / APPROVED
- historical Stage 8A.0.2 strict hold superseded by later 8A.1/8A.2.x stages
- operational migration-history guardrail remains active
- migration ordering accepted:
  - `20260429110000_remote_legacy_baseline.sql`
  - `20260429120000_calculation_snapshots_v1.sql`
  - `20260504190000_module01_schema_slice_01.sql`
- `SAFE_TO_PLAN_PUSH_AFTER_AUTH` accepted
- required gate before any `db push`:
  - `supabase migration list --linked` must pass and confirm baseline alignment
- local recovery note:
  - `docs/AUDITS/00_AUDIT_INDEX.md` recovered from `HEAD`
  - disk space improved to approximately 4.96 GB on `C:`
- `db push` remains forbidden until auth + migration-history gate passes
