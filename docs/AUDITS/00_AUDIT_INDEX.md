# Audit Index

## Purpose

Single current index for audits in EDS Power.

Rule:

- `docs/AUDITS/` = history
- `00_AUDIT_INDEX.md` = active entry point
- audit archive is history, index is active navigation

## Latest audit

- **Stage 8A.1 — `calculation_snapshots` migration promotion test (local)** — `2026-04-30_STAGE_8A_1_CALCULATION_SNAPSHOTS_PROMOTION_TEST.md` (**`FIRST_PERSISTENCE_READY_NON_PROD`** — promoted DDL to **`supabase/migrations/`** + **`supabase db reset`** PASS; legacy tables/views + **`calculation_snapshots`** present; **no** prod `db push`)
- **Stage 8A.0.8 — Cursor local Supabase connectivity** — `2026-04-30_STAGE_8A_0_8_CURSOR_LOCAL_CONNECTIVITY.md` (**`CURSOR_LOCAL_STACK_VERIFIED`**)
- **Stage 8A.0.6 — Actual remote baseline DDL import** — `2026-04-29_STAGE_8A_0_6_ACTUAL_REMOTE_BASELINE_CAPTURE.md` (**`REAL_BASELINE_CAPTURED_PENDING_REPLAY`**; merged **`remote_schema.sql`** · **no** `db push`; **`calculation_snapshots`** promoted locally in **8A.1**)
- **Stage 8A.0.5 — Local tooling precheck** — `2026-04-29_STAGE_8A_0_5_LOCAL_TOOLING_PRECHECK.md` (**`READY_FOR_OPERATOR_TOOLING_INSTALL`**)
- **Stage 8A.0.4 — Baseline DDL + local replay test** — `2026-04-29_STAGE_8A_0_4_BASELINE_REPLAY_TEST.md` (**`BLOCKED_BY_LOCAL_TOOLING`**; **no** DDL captured; **no** `db push`; **no** **`calculation_snapshots`** promotion)
- **Stage 8A.0.3 — Remote baseline capture (ordering slot + scaffold / operator DDL)** — `2026-04-29_STAGE_8A_0_3_REMOTE_BASELINE_CAPTURE.md` (**`BASELINE_CAPTURED_PENDING_REPLAY_TEST`**; **no** `db push`; **`IDEA-0022` `IMPLEMENTED`** after **8A.1** local promotion test)
- **Stage 8A.0.2 — Supabase remote baseline alignment (governance + DDL hold)** — `2026-04-29_STAGE_8A_0_2_SUPABASE_REMOTE_BASELINE_ALIGNMENT.md` (**`LEGACY_REMOTE_SCHEMA_DETECTED`**; additive only; **`IDEA-0020` `IMPLEMENTED`**; **no** `db push` in TASK)
- **Stage 8A.0.1 — Root migration governance correction** — `2026-04-29_STAGE_8A_0_1_ROOT_MIGRATION_GOVERNANCE_CORRECTION.md` (**`calculation_snapshots`** + **`product_type`** — **`TABLE=SYSTEM`, `ROW=PRODUCT`**; **`IDEA-0019` `IMPLEMENTED`**)
- **Stage 8A — Supabase live verification gate** — `2026-04-29_STAGE_8A_SUPABASE_LIVE_VERIFICATION_GATE.md` (**LIVE PASS PENDING**; **`IDEA-0017` `ACTIVE` / `PENDING_SUPABASE_VERIFICATION`**; automated probe **`404`** on `eds-power-api.onrender.com` **`/api/kzo/save_snapshot`** at 2026-04-29 — redeploy + env + migration required)
- **Stage 8A — Supabase first persistence MVP (implementation audit)** — `2026-04-29_STAGE_8A_SUPABASE_FIRST_PERSISTENCE_MVP.md` (insert-only **`calculation_snapshots`**; **`IDEA-0017` `IMPLEMENTED`** only after live PASS in live gate audit)
- **Stage 7B — final closure (Gemini `SAFE TO PROCEED TO STAGE 8A` + governance doc-pass)** — `2026-04-29_STAGE_7B_KZO_MVP_SNAPSHOT_CONTRACT_FREEZE.md` (**`KZO_MVP_SNAPSHOT_V1` frozen**; **IDEA-0016 `IMPLEMENTED`**)
- **Gemini external audit request — Stage 7B** — `2026-04-29_STAGE_7B_GEMINI_EXTERNAL_AUDIT_REQUEST.md`
- **Gemini external audit request — Stage 7A final closure** — `2026-04-29_STAGE_7A_GEMINI_EXTERNAL_AUDIT_REQUEST.md`
- **Stage 7A — operator verification PASS + MVP cohesion dossier** — `2026-04-29_STAGE_7A_KZO_END_TO_END_MVP_STABILIZATION.md` (**manual `runKzoMvpFlow()`**, **`mvp_run_outcome` `MVP_RUN_SUCCESS`**, Sheet **`E4:F19`/`E20:F20`**, **`E21:F26`**, **`E27:F40`**; **IDEA-0015 `IMPLEMENTED`**)
- **Gemini external audit request (Stage 6C full closure)** — `2026-04-29_STAGE_6C_GEMINI_EXTERNAL_AUDIT_REQUEST.md`
- Stage 6C — **operator-visible Sheet PASS** + Render gate dossier **`2026-04-29_STAGE_6C_ENGINEERING_BURDEN_RENDER_GATE.md`**
- Stage 6C engineering burden foundation MVP — `2026-04-29_STAGE_6C_ENGINEERING_BURDEN_FOUNDATION.md`
- **Stage 6B — formal closure** (operator PASS + Gemini **`SAFE TO PROCEED TO STAGE 6C`**) — `2026-04-29_STAGE_6B_ENGINEERING_CLASSIFICATION.md`
- Stage 6A reserved operator block — operator verification PASS 29.04.2026 — `2026-04-29_STAGE_6A_RESERVED_BLOCK_ACTIVATION.md`
- Stage 5D governance verification — **PASS WITH DOC FIXES**, doc-pass closed — `2026-04-29_STAGE_5D_GOVERNANCE_VERIFICATION_GATE.md` (upstream MVP audit: `2026-04-29_STAGE_5D_OPERATOR_LAYOUT_GOVERNANCE.md`)
- Stage 5C operator Sheet visibility (topology — thin GAS, **VERIFIED**) — `2026-04-29_STAGE_5C_SHEET_OUTPUT_INTEGRATION.md`
- **Gemini external audit request** — `2026-04-29_STAGE_5C_SHEET_GEMINI_AUDIT_REQUEST.md`
- Operational gate — `2026-04-29_STAGE_5C_PHYSICAL_TOPOLOGY_RENDER_GATE.md`
- Prior gate — `2026-04-29_STAGE_5B_PHYSICAL_FOOTPRINT_RENDER_GATE.md`
- Gemini technical review PASS — `2026-04-29_STAGE_5B_GEMINI_TECHNICAL_AUDIT.md`

## Stage audits

- `2026-04-26_STAGE_1_GEMINI_AUDIT_FIX_PACK_V2.md`
- `2026-04-26_STAGE_2_CALC_SKELETON_AUDIT.md`
- `2026-04-26_STAGE_2B_KZO_MVP_SCOPE_AUDIT.md`
- `2026-04-26_GEMINI_STAGE2_KZO_AUDIT.md`
- `2026-04-26_STAGE_2C_GOVERNANCE_PATCH_REPORT.md`
- `2026-04-26_STAGE_2D_GOVERNANCE_STABILIZATION.md`
- `2026-04-26_STAGE_2E_KZO_VALIDATION_FOUNDATION.md`
- `2026-04-26_STAGE_2E_FIX_PACK.md`
- `2026-04-26_STAGE_3A_KZO_CALC_OBJECT.md`
- `2026-04-26_STAGE_3B_API_SKELETON.md`
- `2026-04-26_STAGE_3C_NORMALIZED_SUMMARY.md`
- `2026-04-26_STAGE_3D_GAS_API_HANDSHAKE.md`
- `2026-04-29_STAGE_3E_MANUAL_GAS_EXECUTION.md`
- `2026-04-29_STAGE_3F_SHEET_WRITEBACK_MVP.md`
- `2026-04-29_STAGE_4A_TEMPLATE_PROTECTION.md`
- `2026-04-29_STAGE_4B_INPUT_NORMALIZATION.md`
- `2026-04-29_STAGE_4C_OPERATOR_SHELL.md`
- `2026-04-29_STAGE_5A_STRUCTURAL_COMPOSITION_TASK.md`
- `2026-04-29_STAGE_5A_OUTPUT_INTEGRATION.md`
- `2026-04-29_STAGE_5B_PHYSICAL_FOOTPRINT_RENDER_GATE.md`
- `2026-04-29_STAGE_5B_GEMINI_TECHNICAL_AUDIT.md`
- `2026-04-29_STAGE_5C_PHYSICAL_TOPOLOGY_RENDER_GATE.md`
- `2026-04-29_STAGE_5C_SHEET_OUTPUT_INTEGRATION.md`
- `2026-04-29_STAGE_5C_SHEET_GEMINI_AUDIT_REQUEST.md`
- `2026-04-29_STAGE_5D_OPERATOR_LAYOUT_GOVERNANCE.md`
- `2026-04-29_STAGE_5D_GOVERNANCE_VERIFICATION_GATE.md`
- `2026-04-29_STAGE_6A_RESERVED_BLOCK_ACTIVATION.md`
- `2026-04-29_STAGE_6B_ENGINEERING_CLASSIFICATION.md`
- `2026-04-29_STAGE_7A_KZO_END_TO_END_MVP_STABILIZATION.md`
- `2026-04-29_STAGE_7A_GEMINI_EXTERNAL_AUDIT_REQUEST.md`
- `2026-04-29_STAGE_7B_KZO_MVP_SNAPSHOT_CONTRACT_FREEZE.md`
- `2026-04-29_STAGE_8A_0_2_SUPABASE_REMOTE_BASELINE_ALIGNMENT.md`
- `2026-04-29_STAGE_8A_0_1_ROOT_MIGRATION_GOVERNANCE_CORRECTION.md`
- `2026-04-29_STAGE_8A_SUPABASE_LIVE_VERIFICATION_GATE.md`
- `2026-04-29_STAGE_8A_SUPABASE_FIRST_PERSISTENCE_MVP.md`
- `2026-04-29_STAGE_7B_GEMINI_EXTERNAL_AUDIT_REQUEST.md`
- `2026-04-29_STAGE_6C_ENGINEERING_BURDEN_RENDER_GATE.md`
- `2026-04-29_STAGE_6C_ENGINEERING_BURDEN_FOUNDATION.md`
- `2026-04-30_STAGE_8A_0_8_CURSOR_LOCAL_CONNECTIVITY.md`
- `2026-04-30_STAGE_8A_1_CALCULATION_SNAPSHOTS_PROMOTION_TEST.md`

## Deprecated audits

- none

## Active blockers

- no sidebar / buttons / menus before a separate normalized task
- no BOM / costing / production transfer expansion without separate TASK

## Post–Stage 8A (explicit non-goals until tasked)

- retrieval API / snapshot history UI / analytics — **out of Stage 8A scope**