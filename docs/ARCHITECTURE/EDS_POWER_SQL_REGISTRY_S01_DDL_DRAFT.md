# EDS Power SQL Registry S01 DDL Draft

This revision applies Gemini **PASS WITH FIXES** (Critical Audit — SQL Registry S01 DDL Draft) to the DDL text. **DOC ONLY:** no migration file, no SQL execution, no Supabase changes.

## 1. Purpose

Prepare final DDL draft for DB-driven dynamic menu registry.

This document is planning-only: it does not create migration files, execute SQL, or change Supabase.

## 2. Source Plan

Canonical migration planning artifact:

- `docs/DB_MIGRATIONS/EDS_POWER_SQL_MIGRATION_PLAN_REGISTRY_S01.md` (`EDS_POWER_SQL_MIGRATION_PLAN_REGISTRY_S01`)

Normative behaviour and payload rules remain in:

- `docs/ARCHITECTURE/EDS_POWER_DB_DRIVEN_DYNAMIC_MENU_REGISTRY_CONTRACT.md`

## 3. Gemini Audit Findings Applied

**Initial DDL audit** — findings incorporated (baseline):

- Use existing `public.module01_roles`; do not introduce a parallel role system.
- Confirm `role_id` source and real row identifiers before any seed bindings that reference roles.
- Add uniqueness protection for `(role_id, action_id, environment_scope)` grant rows.
- Resolve `SYSTEM_SHELL` ownership with a dedicated module row (see section 5).
- Follow existing `updated_at` convention where possible; **final strategy is a migration blocker** (see section 11).
- `environment_scope` must be part of backend menu filtering (see section 12).

**PASS WITH FIXES** — additionally applied in this revision:

- Explicit `public.` schema qualification on all table names, indexes, foreign keys, and constraint definitions in draft SQL.
- Replace generic `public.modules` (and related names) with **`public.eds_power_modules`**, **`public.eds_power_module_actions`**, **`public.eds_power_role_module_access`** to avoid collision / ambiguity.
- Foreign keys: `public.eds_power_module_actions.module_id` → `public.eds_power_modules(id)`; `public.eds_power_role_module_access.module_id` → `public.eds_power_modules(id)`; `public.eds_power_role_module_access.action_id` → `public.eds_power_module_actions(id)`.
- Unique grant protection: named constraint `uq_eds_power_role_module_access_role_action_env` on `(role_id, action_id, environment_scope)`.
- **`SYSTEM_SHELL` seed order** documented (section 10): module row must be inserted before shell actions; role bindings last and only after confirmed `role_id` source.
- **Backend doctrine:** menu resolution must filter by role, module/action enabled flags, and `environment_scope`; production clients must not receive `DEV` / `ADMIN_TEST` / `TEMPLATE` scoped rows unless explicitly authorized by backend environment policy.
- **`updated_at`:** final SQL migration is **BLOCKED** until strategy is explicitly chosen (section 11).
- **RLS / service-role:** remains an open migration decision (section 14).

## 4. Existing Schema Confirmation

Documented from repository migrations only (read-only inspection). No live DB verification in this task.

| Item | Status | Detail |
| --- | --- | --- |
| Exact roles table name | **Confirmed (repo)** | `public.module01_roles` in `supabase/migrations/20260504190000_module01_schema_slice_01.sql` |
| Role primary key column | **Confirmed (repo)** | `id uuid primary key default gen_random_uuid()` |
| Role UUID vs role code canonicality | **Confirmed (repo)** | **`id` (UUID)** is the FK target for role links. **`role_code`** is unique business key (`constraint module01_roles_role_code_key unique (role_code)`). Seeds in that migration identify roles by `role_code`; UUIDs are not stable literals in repo. |
| Existing `updated_at` trigger function | **Confirmed (repo, legacy baseline)** | `public.set_updated_at()` in `supabase/migrations/20260429110000_remote_legacy_baseline.sql`, used by triggers on legacy tables (e.g. `public.bom_links`, `public.ncr`, `public.objects`). |
| `module01_users` / `module01_user_sessions` and `updated_at` triggers | **Confirmed (repo)** | No `CREATE TRIGGER` on `module01_*` tables appears in `20260504190000_module01_schema_slice_01.sql`. `public.module01_user_auth` documents **API-managed** `updated_at` with **no** trigger in that migration. `public.module01_user_sessions` has **no** `updated_at` column in `20260505120000_module01_user_sessions.sql`. |

**OPEN QUESTION (deployment):** Confirm on target Supabase that no out-of-repo trigger was added to `public.module01_roles` / `public.module01_users` before binding S01 registry tables to a trigger strategy.

## 5. SYSTEM_SHELL Decision

**Chosen approach (draft):** create a dedicated row in **`public.eds_power_modules`**:

- `module_code = 'SYSTEM_SHELL'`

**Reason:** shell-wide actions (`REFRESH_MENU`, `SESSION_STATUS`, `LOGOUT`) need a non-nullable `module_id` on `public.eds_power_module_actions` without ambiguity.

**Seed ordering rule:** **`SYSTEM_SHELL` must be inserted first** among modules so that shell `action` rows can reference a stable `module_id`. Full order: section 10.

**Scope:** decision is documented only; no table creation or seed execution in this task.

## 6. DDL Draft — public.eds_power_modules

Draft only (not executed). All objects below are in schema **`public`**.

```sql
-- DRAFT — do not execute until audited migration file is approved.

create table public.eds_power_modules (
    id uuid primary key default gen_random_uuid(),
    module_code text not null,
    module_name text not null,
    module_status text not null,
    module_version text,
    description text,
    sort_order integer not null default 100,
    is_active boolean not null default true,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    constraint eds_power_modules_module_code_key unique (module_code),
    constraint eds_power_modules_module_status_check check (
        module_status in (
            'RELEASED',
            'ADMIN_TEST',
            'DEV',
            'DISABLED',
            'MAINTENANCE',
            'HIDDEN',
            'PLANNED'
        )
    )
);
```

## 7. DDL Draft — public.eds_power_module_actions

Draft only (not executed).

```sql
-- DRAFT — do not execute until audited migration file is approved.

create table public.eds_power_module_actions (
    id uuid primary key default gen_random_uuid(),
    module_id uuid not null references public.eds_power_modules (id),
    action_key text not null,
    action_type text not null,
    menu_label text not null,
    visibility text not null default 'VISIBLE',
    enabled boolean not null default false,
    sort_order integer not null default 100,
    requires_auth boolean not null default true,
    required_core_version text,
    metadata jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    constraint eds_power_module_actions_action_key_key unique (action_key),
    constraint eds_power_module_actions_action_type_check check (
        action_type in (
            'OPEN_DIALOG',
            'OPEN_SIDEBAR',
            'RUN_BATCH_ACTION',
            'REFRESH_MENU',
            'LOGOUT',
            'SESSION_STATUS',
            'PLACEHOLDER_DISABLED'
        )
    ),
    constraint eds_power_module_actions_visibility_check check (visibility in ('VISIBLE', 'HIDDEN'))
);
```

## 8. DDL Draft — public.eds_power_role_module_access

Draft only (not executed).

**`role_id`:** keep as `role_id uuid not null` **without** a hardcoded `references` clause in this draft. The final migration must confirm whether the FK should be:

```text
REFERENCES public.module01_roles (id)
```

(or another audited roles table). **No hardcoded role UUIDs in seed text** until read-only inspection confirms real `role_id` values in the target environment.

```sql
-- DRAFT — do not execute until audited migration file is approved.

create table public.eds_power_role_module_access (
    id uuid primary key default gen_random_uuid(),
    role_id uuid not null,
    -- Final migration: confirm FK, e.g. references public.module01_roles (id)
    module_id uuid not null references public.eds_power_modules (id),
    action_id uuid not null references public.eds_power_module_actions (id),
    access_level text not null default 'NONE',
    visible boolean not null default false,
    enabled boolean not null default false,
    environment_scope text not null default 'PRODUCTION',
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    constraint eds_power_role_module_access_access_level_check check (
        access_level in ('NONE', 'VIEW', 'USE', 'ADMIN', 'DEV_TEST')
    ),
    constraint eds_power_role_module_access_environment_scope_check check (
        environment_scope in ('PRODUCTION', 'ADMIN_TEST', 'DEV', 'TEMPLATE')
    ),
    constraint uq_eds_power_role_module_access_role_action_env
        unique (role_id, action_id, environment_scope)
);
```

## 9. Index Draft

Proposed indexes (all on **`public`** — final set to be trimmed at migration authoring):

- `public.eds_power_modules (module_code)`
- `public.eds_power_modules (module_status)`
- `public.eds_power_module_actions (action_key)`
- `public.eds_power_module_actions (module_id)`
- `public.eds_power_role_module_access (role_id)`
- `public.eds_power_role_module_access (action_id)`
- `public.eds_power_role_module_access (module_id)`
- `public.eds_power_role_module_access (environment_scope)`

Example draft names (not executed):

```sql
-- DRAFT
create index eds_power_modules_module_code_idx on public.eds_power_modules (module_code);
create index eds_power_modules_module_status_idx on public.eds_power_modules (module_status);
create index eds_power_module_actions_action_key_idx on public.eds_power_module_actions (action_key);
create index eds_power_module_actions_module_id_idx on public.eds_power_module_actions (module_id);
create index eds_power_role_module_access_role_id_idx on public.eds_power_role_module_access (role_id);
create index eds_power_role_module_access_action_id_idx on public.eds_power_role_module_access (action_id);
create index eds_power_role_module_access_module_id_idx on public.eds_power_role_module_access (module_id);
create index eds_power_role_module_access_environment_scope_idx on public.eds_power_role_module_access (environment_scope);
```

## 10. Seed Draft

Intent only. **No seed SQL execution.**

**Mandatory seed order (normative for future migration authoring):**

1. Insert **`SYSTEM_SHELL`** module row into `public.eds_power_modules` **first**.
2. Insert **`MODULE_01`** module row into `public.eds_power_modules`.
3. Insert **SYSTEM_SHELL** actions into `public.eds_power_module_actions` (parent `module_id` = SYSTEM_SHELL row):
   - `REFRESH_MENU` — label: Оновити меню; `action_type`: `REFRESH_MENU`
   - `SESSION_STATUS` — label: Статус сесії; `action_type`: `SESSION_STATUS`
   - `LOGOUT` — label: Вийти; `action_type`: `LOGOUT`
4. Insert **MODULE_01** actions (e.g. `MODULE_01_PLACEHOLDER` — label: Module 01 — Розрахунки (planned); `action_type`: `PLACEHOLDER_DISABLED`; `module_id` = MODULE_01 row).
5. **Role bindings** (`public.eds_power_role_module_access`) **only after** real `role_id` source is confirmed (read-only inspection or audited idempotent pattern). **No hardcoded role UUIDs** in this draft.

## 11. updated_at Trigger Plan

- **Confirmed (repo):** `public.set_updated_at()` exists in legacy baseline and is used by triggers on selected legacy tables.
- **Confirmed (repo):** Module 01 auth slice documents API-managed `updated_at` for `public.module01_user_auth` without a DB trigger in that migration.

**Migration blocker (explicit):**

Final SQL migration authoring and execution are **BLOCKED** until an **`updated_at` strategy** is **selected and recorded**:

- **Option A — reuse trigger convention:** `BEFORE UPDATE` on `public.eds_power_modules`, `public.eds_power_module_actions`, and `public.eds_power_role_module_access` executing `public.set_updated_at()`; **or**
- **Option B — API-managed:** no trigger; backend must maintain `updated_at` on these registry tables (explicitly accepted in writing for this slice).

Until one option is chosen, the DDL draft is incomplete for production migration.

## 12. Environment Scope Backend Rule

Future backend menu resolution **must** filter registry-driven menu data by:

- **role** (resolved session roles vs `role_id` on grants),
- **module and action enabled state** (e.g. `public.eds_power_modules.is_active`, `public.eds_power_module_actions.enabled`, and grant-level `visible` / `enabled` on `public.eds_power_role_module_access`),
- **`environment_scope`** aligned to terminal/session/backend environment policy.

**Production clients** must **not** receive menu items whose effective grant row is scoped only to **`DEV`**, **`ADMIN_TEST`**, or **`TEMPLATE`**, unless **explicitly authorized** by audited backend environment policy (default: **deny**).

No backend or SQL implementation in this task.

## 13. Rollback Draft

- **Before production data:** dropping S01 registry tables only may be acceptable if no downstream FKs or external references exist; verify no other tables reference `public.eds_power_modules` / `public.eds_power_module_actions` / `public.eds_power_role_module_access`.
- **After real use:** prefer **forward** migrations (additive fixes, new constraints) over destructive rollback.
- **After production adoption:** avoid drop-based rollback; use corrective migrations and data repair plans under audit.

## 14. Open Questions

- Exact **FK** for `public.eds_power_role_module_access.role_id` → confirm `references public.module01_roles (id)` (or other audited table) at execution time.
- **`role_id` source** for seeds: operator read vs deterministic idempotency — not fixed in this draft.
- **Role UUID vs `role_code` canonicality** for operational seeds: UUID is FK truth; code is human/ops key — binding strategy still to be audited.
- **`updated_at` strategy** — **blocking** until Option A or Option B is selected (section 11).
- **RLS / service-role (final migration must decide):**
  - whether registry tables use RLS;
  - whether backend service-role bypass is sufficient for intended threat model;
  - whether read access is restricted to backend only for these tables.
- **Final `SYSTEM_SHELL` ownership** confirmation (draft uses dedicated module row; statuses still audit-gated).
- **`MASTER_TEMPLATE` behaviour:** map to `environment_scope = 'TEMPLATE'` for grants vs separate backend branch — confirm in menu contract + migration audit.

### Follow-up / out of S01 scope (deferred)

**`AUTH_SESSION_HARDENING_FOLLOWUP`**

Gemini **Fix 03** suggested a check such as `CHECK (expires_at > issued_at)` for session tables. **Not applied** in this S01 registry DDL — session tables are outside this registry migration.

**Follow-up:** Consider `CHECK (expires_at > issued_at)` (or equivalent, using existing column names on `public.module01_user_sessions`) in a **separate** auth/session hardening migration under audit. **Do not** modify session DDL inside this S01 registry draft.

## 15. Verdict

DDL draft updated per **PASS WITH FIXES** (explicit `public.*` naming, `eds_power_*` table names, FK wiring between registry tables, named unique constraint, seed order, strengthened environment doctrine, `updated_at` blocker, RLS decision deferred).

**SQL execution remains blocked.** No migration `.sql` file was created and no database changes were performed.
