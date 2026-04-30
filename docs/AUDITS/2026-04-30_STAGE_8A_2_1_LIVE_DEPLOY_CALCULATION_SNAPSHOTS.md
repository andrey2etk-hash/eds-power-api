# Stage 8A.2.1 — Live deploy `calculation_snapshots` documentation closeout

## Audit date

2026-04-30

## Objective

Close the Stage **8A** live verification gate after **successful production-class deployment**: hosted Supabase exposes **`public.calculation_snapshots`**, API host exposes **`POST /api/kzo/save_snapshot`** with **`SUPABASE_*`** env set, end-to-end **INSERT** (**`SUCCESS`**) correlated to a persisted row (**`product_type`** = **`KZO`**).

This dossier completes **IDEA-0017** and marks **`STAGE_8A_COMPLETE`** for documentation and master-table purposes.

Upstream gates: **`FIRST_PERSISTENCE_READY_NON_PROD`** (**8A.1**), remote history preflight playbook (**8A.2.0**), canonical criteria **`docs/AUDITS/2026-04-29_STAGE_8A_SUPABASE_LIVE_VERIFICATION_GATE.md`** ( **`Live PASS record`** synced to **PASS** in the same closure wave).

## Live PASS correlation (minimal public record)

| Check | Requirement |
| --- | --- |
| Migration | Hosted project includes **`20260429120000_calculation_snapshots_v1`** DDL applied (directly or via controlled `db push` after **`schema_migrations`** alignment per **8A.2.0**). |
| API | **`POST /api/kzo/save_snapshot`** returns **`status`** **`SUCCESS`**, **`persistence_status`** **`STORED`**, UUID **`snapshot_id`**. |
| Database | Row exists with **`id`** = **`snapshot_id`**, **`product_type`** **`KZO`**, **`snapshot_version`** **`KZO_MVP_SNAPSHOT_V1`**. |

Details and redacted **`snapshot_id`**: **`docs/AUDITS/2026-04-29_STAGE_8A_SUPABASE_LIVE_VERIFICATION_GATE.md`** — **Live PASS record** table.

## Governance

- Calculation truth remains **`prepare_calculation`**; **`save_snapshot`** is **insert-only** frozen JSON (**`14_CALC_TRUTH_VS_PERSISTENCE_STAGE_8A`**).
- No BOM / pricing / auth expansion in **`IDEA-0017`** scope.

## Next recommended stage (not started until new **IDEA → TASK`)

**Operational first-write path:** make the **first repeatable operator-driven** **`POST /api/kzo/save_snapshot`** production path the default thin GAS flow after **`runKzoMvpFlow()`** (or a single orchestrated runner that sequences **`prepare_calculation`** → **`KZO_MVP_SNAPSHOT_V1`** envelope assembly → **`saveKzoSnapshotV1()`**), with execution logging and **`logic_version`** echo — so snapshot rows are attributable to governed Sheet workflow, not ad-hoc HTTP probes.

Separate **IDEAs** remain for retrieval / history UI / analytics (explicitly **out** of Stage 8A).

## Final status

**`STAGE_8A_COMPLETE`**
