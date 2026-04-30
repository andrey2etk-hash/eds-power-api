# Schema registry — index

_Keep governance rows aligned with Postgres; **`calculation_snapshots`** DDL remains **held**._

## Migration ordering (Stage 8A.0.x)

| Order | Artifact | Purpose |
| --- | --- | --- |
| 1 | **`supabase/migrations/20260429110000_remote_legacy_baseline.sql`** | **8A.0.6** factual DDL · **8A.0.7** replay **`BLOCKED_BY_DOCKER`** → **`BASELINE_REPLAY_VERIFIED`** pending (audit **8A.0.7**) |
| 2 *(held)* | **`supabase/migrations/_pending_after_remote_baseline/20260429120000_calculation_snapshots_v1.sql`** | **`calculation_snapshots`** — **not** in root until **`BASELINE_REPLAY_VERIFIED`** (**8A.0.7** gate) |

---

## Remote legacy baseline (declared + capture)

Tables / views below are **`legacy_baseline`** — mirrored in baseline migration **`20260429110000`** when operator DDL is pasted.

| Resource | Classification |
| --- | --- |
| **`public.objects`** | `legacy_baseline` |
| **`public.bom_links`** | `legacy_baseline` |
| **`public.ncr`** | `legacy_baseline` |
| **`public.production_status`** | `legacy_baseline` |
| **`public.v_*`** (pattern) | `legacy_baseline` |

**Governance docs:** **`LEGACY_REMOTE_BASELINE.md`**, audits **`docs/AUDITS/2026-04-29_STAGE_8A_0_3_REMOTE_BASELINE_CAPTURE.md`**, **`docs/AUDITS/2026-04-29_STAGE_8A_0_4_BASELINE_REPLAY_TEST.md`**, **`docs/AUDITS/2026-04-29_STAGE_8A_0_6_ACTUAL_REMOTE_BASELINE_CAPTURE.md`**, **`docs/AUDITS/2026-04-29_STAGE_8A_0_7_BASELINE_REPLAY_VERIFICATION.md`**.

---

## Intentional EDS Power snapshots (additive MVP — **held**)

| table (schema.table) | domain | IDEA | snapshot / version | notes |
| --- | --- | --- | --- | --- |
| **`public.calculation_snapshots`** | `snapshots` | IDEA-0017 (+ **8A.0.1**) | **`product_type` KZO**, **`snapshot_version` KZO_MVP_SNAPSHOT_V1** | DDL **`_pending_after_remote_baseline/`** — promoted after staging replay |

---

**Superseded (do not extend):** **`public.kzo_mvp_snapshots_v1`** draft DDL — **`migrations/_archive_pre_8a0_1_kzo_tables/`**.
