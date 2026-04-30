# Stage **8A.0.6** — Actual remote baseline DDL import (**PASS**)

## Objective

Import operator **`remote_schema.sql`** (schema-only **`public`** DDL from **`pg_dump`** via Supabase pooler) into **`supabase/migrations/20260429110000_remote_legacy_baseline.sql`**, replacing the noop **`DO`** block — **without** `db push`, **without** guessed DDL, **without** activating **`calculation_snapshots`**.

## Final stage status

**`REAL_BASELINE_CAPTURED_PENDING_REPLAY`**

(Next: **Stage 8A.0.4** — local **`supabase db reset`** / disposable migrate to confirm replay.)

---

## Input

| Item | Value |
| --- | --- |
| **Source** | **`C:\Users\Kubantsev\eds-power-api\remote_schema.sql`** (repo root) |
| **Sanitization** | Removed pg_dump **`\restrict`** / **`\unrestrict`** lines (invalid in migration SQL); **`CREATE SCHEMA public`** → **`CREATE SCHEMA IF NOT EXISTS public`**. |

---

## Schema-only verification

| Check | Result |
| --- | :---: |
| **`INSERT` / `COPY` data** | **absent** (grep on merged migration) |
| **`public.objects`**, **`bom_links`**, **`ncr`**, **`production_status`** | **present** |
| **`public.v_*` views** | **23 views** (e.g. **`v_bom_tree`**, **`v_production_status_live`**, …) |
| Functions | **yes** — **`get_bom_tree`**, **`get_leaf_summary`**, **`set_updated_at`** |
| Constraints, indexes, triggers, FKs | **yes** |

---

## Strict boundary

| Constraint | Result |
| --- | :---: |
| Prod **`db push`** | **not performed** |
| Remote DB mutation | **none** |
| **`calculation_snapshots_v1.sql`** in **`migrations/`** root | **no** — stays **`_pending_after_remote_baseline/`** |

---

## Artifact

- **`supabase/migrations/20260429110000_remote_legacy_baseline.sql`** — factual sanitized DDL (no fabrication).

---

## References

- **`docs/AUDITS/2026-04-29_STAGE_8A_0_5_LOCAL_TOOLING_PRECHECK.md`**
- **`docs/AUDITS/2026-04-29_STAGE_8A_0_4_BASELINE_REPLAY_TEST.md`** (prior tooling block)
- **`supabase/schema_registry/LEGACY_REMOTE_BASELINE.md`**
