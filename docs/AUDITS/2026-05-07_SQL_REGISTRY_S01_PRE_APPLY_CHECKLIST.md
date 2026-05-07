# SQL Registry S01 Pre-Apply Checklist

**Mode:** operational governance — **DOC ONLY** in the repo task that created this file. Completing this checklist does **not** run SQL by itself.

## 1. Migration File

Confirm target file (must match audited artifact):

- `supabase/migrations/20260507100000_eds_power_dynamic_menu_registry_s01.sql`

## 2. Current Verdict

**Gemini (final migration file audit):** `MIGRATION_READY_FOR_APPLY`

## 3. Execution Boundary

- This checklist **does not** authorize execution.
- Physical SQL apply requires **explicit user / operator approval** and a **separate** tracked apply task.
- Do **not** treat audit PASS as automatic permission to mutate production.

## 4. Pre-Apply Confirmations

Operator / user must positively confirm:

- **Target environment** is identified (e.g. staging vs production).
- **Remote Supabase project** (or target DB) is the intended one (no wrong-project apply).
- **Local vs remote** execution path is chosen and understood (Dashboard SQL Editor vs CLI `db push` vs other approved path).
- **Backup / recovery** awareness: operator accepts rollback limitations for DDL + seeds.
- **Migration file** has been reviewed; byte-for-byte same as audit snapshot (no post-audit edits).
- **No secrets** embedded in migration text (passwords, tokens, keys).
- **No bundled** backend / GAS / Render changes in the same “apply moment” unless separately approved (this migration is DB-only).

## 5. Required Stop Conditions

**Stop immediately** if apply reports any of:

- `foreign_key_violation`
- `undefined_function` (e.g. missing `public.set_updated_at()`)
- `duplicate key` / unique violation (including unique grant constraint)
- Missing dependency: **`public.module01_roles`** not present or empty when FK + seed grants run
- **`public.set_updated_at()`** missing on target
- **Relation already exists** / unexpected name collision on `eds_power_*` tables
- **Seed count mismatch** after apply (see section 7 — expected counts)

Document the error, **do not** “patch live” without a governed correction path.

## 6. Apply Method Options

Documented **options only** — no auto-recommendation:

- **Supabase Dashboard — SQL Editor:** paste/run migration as a single controlled transaction per operator playbook (if used).
- **Supabase CLI —** `supabase db push` **or** `supabase migration up` (exact command per team playbook; must match linked project and permissions).

**User / operator must choose** method and account for project governance (e.g. migration history alignment, `schema_migrations` policy).

## 7. Post-Apply Verification Queries

Run **after** successful apply (intent only — adjust to your SQL client):

**Existence**

- `to_regclass('public.eds_power_modules')` is non-null.
- `to_regclass('public.eds_power_module_actions')` is non-null.
- `to_regclass('public.eds_power_role_module_access')` is non-null.

**Modules**

- Rows exist for `module_code` **`SYSTEM_SHELL`** and **`MODULE_01`** (expect **2** module rows for this migration’s seed).

**Actions**

- Expect **4** rows in `public.eds_power_module_actions` for keys: `REFRESH_MENU`, `SESSION_STATUS`, `LOGOUT`, `MODULE_01_PLACEHOLDER`.

**Role bindings**

- Count in `public.eds_power_role_module_access` should equal:  
  **`(SELECT count(*) FROM public.module01_roles WHERE is_active = true) * 4`**  
  (bootstrap: every active role × four actions, `environment_scope = 'PRODUCTION'`).
- If `module01_roles` has zero active rows, expect **0** grants — **FAIL** relative to intended menu registry bootstrap unless that state is explicitly accepted.

**Triggers (`updated_at`)**

- Expect triggers on registry tables, e.g. names matching migration:  
  `trg_eds_power_modules_updated_at`, `trg_eds_power_module_actions_updated_at`, `trg_eds_power_role_module_access_updated_at`  
  (verify via `information_schema.triggers` or `pg_trigger` / project-specific query).

## 8. PASS Criteria

PASS **only if**:

- All **three** tables exist and are usable.
- Expected **two** seed modules (`SYSTEM_SHELL`, `MODULE_01`) exist with expected status fields.
- Expected **four** actions exist with correct `action_key` values.
- Role bindings count matches **active roles × 4** (or documented intentional exception).
- No SQL errors during apply; no ad-hoc manual edits were required to “make it fit”.

## 9. FAIL Criteria

FAIL if:

- Migration required **live editing** to succeed.
- Any **FK / function / duplicate / exists** error occurred (see section 5).
- Seed data **incomplete** vs section 7 expectations.
- Verification queries **do not** match expected results.

## 10. Next Step After Approval

If user **explicitly** approves physical apply:

- Open a **separate** governed task: **EDS POWER SQL REGISTRY S01 — SUPABASE APPLY** (or equivalent name), with environment, method, and rollback note captured.

## 11. Verdict

**PRE_APPLY_CHECKLIST_READY_FOR_USER_APPROVAL**
