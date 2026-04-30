# Schema registry — index

_Keep governance rows aligned with Postgres; **`calculation_snapshots`** DDL lives in **`supabase/migrations/`** after **Stage 8A.1** (audit **`FIRST_PERSISTENCE_READY_NON_PROD`**)._

## Migration ordering (Stage 8A)

| Order | Artifact | Purpose |
| --- | --- | --- |
| 1 | **`supabase/migrations/20260429110000_remote_legacy_baseline.sql`** | **8A.0.6** factual legacy **`public`** DDL — applies **first** |
| 2 | **`supabase/migrations/20260429120000_calculation_snapshots_v1.sql`** | **`public.calculation_snapshots`** — applies **after** baseline (**8A.1** local **`db reset`** verified) |

**Future holds:** empty **`supabase/migrations/_pending_after_remote_baseline/`** reserved for DDL that must trail the next authoritative baseline revision.

---

## Remote legacy baseline (declared + capture)

Tables / views below are **`legacy_baseline`** — mirrored in baseline migration **`20260429110000`**.

| Resource | Classification |
| --- | --- |
| **`public.objects`** | `legacy_baseline` |
| **`public.bom_links`** | `legacy_baseline` |
| **`public.ncr`** | `legacy_baseline` |
| **`public.production_status`** | `legacy_baseline` |
| **`public.v_*`** (pattern) | `legacy_baseline` |

**Governance docs:** **`LEGACY_REMOTE_BASELINE.md`**, audits **`docs/AUDITS/2026-04-29_STAGE_8A_0_3_REMOTE_BASELINE_CAPTURE.md`**, **`docs/AUDITS/2026-04-29_STAGE_8A_0_4_BASELINE_REPLAY_TEST.md`**, **`docs/AUDITS/2026-04-29_STAGE_8A_0_6_ACTUAL_REMOTE_BASELINE_CAPTURE.md`**, **`docs/AUDITS/2026-04-29_STAGE_8A_0_7_BASELINE_REPLAY_VERIFICATION.md`**, **`docs/AUDITS/2026-04-30_STAGE_8A_0_8_CURSOR_LOCAL_CONNECTIVITY.md`**, **`docs/AUDITS/2026-04-30_STAGE_8A_1_CALCULATION_SNAPSHOTS_PROMOTION_TEST.md`**.

---

## Intentional EDS Power snapshots (additive MVP)

| table (schema.table) | domain | IDEA | snapshot / version | notes |
| --- | --- | --- | --- | --- |
| **`public.calculation_snapshots`** | `snapshots` | IDEA-0017 (+ **8A.0.1**) | **`product_type` KZO**, **`snapshot_version` KZO_MVP_SNAPSHOT_V1** | DDL **`supabase/migrations/20260429120000_calculation_snapshots_v1.sql`** — **live/hosted apply** gated by **`SUPABASE_LIVE_VERIFICATION_GATE`**, не **8A.1** |

---

**Superseded (do not extend):** **`public.kzo_mvp_snapshots_v1`** draft DDL — **`migrations/_archive_pre_8a0_1_kzo_tables/`**.
