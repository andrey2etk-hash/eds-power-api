# SQL migrations — rules

## Stage **8A.0.6** baseline (root file — factual DDL)

| File | Role |
| --- | --- |
| **`20260429110000_remote_legacy_baseline.sql`** | **Legacy baseline migration** — **merged** from **`remote_schema.sql`** (**8A.0.6**). **Schema-only**. **Replay:** **8A.0.7** (`supabase db reset` local/disposable); **2026-04-29** agent session **`BLOCKED_BY_DOCKER`** — **`BASELINE_REPLAY_VERIFIED`** **not** yet (audit **8A.0.7**). **`calculation_snapshots`** still **`_pending_after_remote_baseline/`** only. |

**Freeze:** no Dashboard DDL edits to listed legacy **`public`** objects during capture window — **`LEGACY_REMOTE_BASELINE.md`**.

## Held — `calculation_snapshots` (**until `BASELINE_REPLAY_VERIFIED`**)

Canonical DDL **`_pending_after_remote_baseline/20260429120000_calculation_snapshots_v1.sql`** — **still not** promoted to **`migrations/`** root until **8A.0.7** achieves **`BASELINE_REPLAY_VERIFIED`** (currently **`BLOCKED_BY_DOCKER`** at 2026-04-29 — audit **8A.0.7**).

| Location | Purpose |
| --- | --- |
| **`_pending_after_remote_baseline/`** | Held **`calculation_snapshots`** + checklist |
| **`LEGACY_REMOTE_BASELINE.md`** | Legacy tables / **`v_*`** + freeze rules |

---

## Conventions

- **Timestamp lexicographic order** dictates apply order (**`YYYYMMDDHHMMSS_*.sql`**).
- Baseline (**`110000`**) strictly **before** snapshot (**`120000`**).

## Archive

**`_archive_pre_8a0_1_kzo_tables/`** — superseded **`kzo_mvp_snapshots_v1`** draft only.
