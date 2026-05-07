# EDS Power SQL Registry S01 Final Implementation Plan

**Mode:** DOC ONLY. This file is governance and documentation. It does **not** authorize SQL execution, `db push`, Supabase mutation, or creation of a real `*.sql` migration file.

## 1. Purpose

Prepare final **pre-migration** implementation plan for SQL Registry S01 (dynamic menu registry slice), after aligned DDL review, **without** rushing into execution.

## 2. Current Status

- DDL draft created (`docs/ARCHITECTURE/EDS_POWER_SQL_REGISTRY_S01_DDL_DRAFT.md`).
- Gemini DDL draft audit = **PASS WITH FIXES**.
- Final alignment completed in that draft.
- Gemini final alignment re-audit = **ALIGNMENT_PASS** (accepted for purposes of this plan).
- **Real SQL migration file:** **NOT** created.
- **SQL execution:** **BLOCKED** until separate user approval and audited migration authoring task.

## 3. Scope

**In scope:**

- `public.eds_power_modules`
- `public.eds_power_module_actions`
- `public.eds_power_role_module_access`
- `SYSTEM_SHELL` seed intent
- `MODULE_01` seed intent
- Registry grants strategy (design-only; no binding INSERTs with unconfirmed `role_id`)

**Out of scope:**

- Auth session tables (`public.module01_user_sessions`, etc.)
- `expires_at` / session hardening (`AUTH_SESSION_HARDENING_FOLLOWUP` — separate migration)
- Backend implementation
- GAS implementation
- DB-driven menu runtime implementation
- Calculation / product logic

**Canonical references:**

- Migration planning: `docs/DB_MIGRATIONS/EDS_POWER_SQL_MIGRATION_PLAN_REGISTRY_S01.md`
- Aligned DDL narrative: `docs/ARCHITECTURE/EDS_POWER_SQL_REGISTRY_S01_DDL_DRAFT.md`
- Registry contract: `docs/ARCHITECTURE/EDS_POWER_DB_DRIVEN_DYNAMIC_MENU_REGISTRY_CONTRACT.md`

## 4. Final Table Names

Confirmed for S01 implementation planning:

- `public.eds_power_modules`
- `public.eds_power_module_actions`
- `public.eds_power_role_module_access`

All DDL and indexes below use schema **`public`** explicitly.

## 5. updated_at Strategy Decision

**Decision field:**

`UPDATED_AT_STRATEGY = DB_TRIGGER_IF_CONFIRMED`

**Rules:**

- Do **not** invent a new trigger function.
- **Repo baseline confirmation:** `public.set_updated_at()` exists in `supabase/migrations/20260429110000_remote_legacy_baseline.sql` (used by legacy table triggers).
- **Recommended:** If that function is **confirmed present** on the target database (same definition) when the migration runs, attach `BEFORE UPDATE` triggers on the three registry tables executing `public.set_updated_at()`.
- If `public.set_updated_at()` is **not** confirmed on the target (e.g. divergent baseline), **do not** assume it — migration authoring **blocked** pending read-only schema confirmation or explicit decision to use **API-managed** `updated_at` for these tables only (requires documented override in a later governance amendment).

**Anti-rush:** Choosing API-managed instead of trigger is valid only if recorded explicitly; do not silently skip triggers on prod without audit.

## 6. RLS / Service Role Strategy

**Decision field:**

`REGISTRY_ACCESS_STRATEGY = BACKEND_SERVICE_ROLE_ONLY_MVP`

**MVP doctrine:**

- Registry tables are **backend-owned**; **GAS must not** query them directly.
- **Direct client / anon** access to these tables must **not** be granted for MVP.
- Backend reads/writes registry via **service role** (or equivalent server-side credentials) under application validation.

**Open point (not blocking documentation, blocking naive “open read”):**

- Final **RLS** policy SQL may be **deferred** only if **all** of the following remain true: no grants to `anon`/`authenticated` on these tables for MVP; only backend service path touches data; governance sign-off that service-role-only is sufficient for the threat model.

## 7. Role FK Strategy

- **Do not** hardcode role UUIDs in repo documentation or seeds.
- Before migration apply, **confirm** on target DB:
  - `public.module01_roles` exists
  - `public.module01_roles.id` is `uuid`
  - role binding rows can reference existing roles

**Preferred final FK (if confirmed):**

```sql
role_id uuid not null references public.module01_roles (id)
```

**If not confirmed:** migration remains **blocked** (do not ship `role_module_access` without a defined `role_id` target).

## 8. SYSTEM_SHELL Seed Order

Mandatory order for future migration authoring:

1. `SYSTEM_SHELL` module row in `public.eds_power_modules`
2. `MODULE_01` module row in `public.eds_power_modules`
3. `SYSTEM_SHELL` actions in `public.eds_power_module_actions`
4. `MODULE_01` actions in `public.eds_power_module_actions`
5. **Role bindings** in `public.eds_power_role_module_access` **only after** `role_id` (and FK) are confirmed

## 9. Final SQL Text Draft

**Documentation only.** Not a migration file. Not executed by this task.

Preconditions stated in comments inside the block. Includes: tables, constraints, FKs (where specified), unique grant constraint, indexes, **optional** `updated_at` triggers **if** `public.set_updated_at()` is confirmed (see section 5), seed for modules + actions only, **placeholder** for role bindings.

```sql
-- =============================================================================
-- EDS Power SQL Registry S01 — FINAL TEXT DRAFT (DOCUMENTATION ONLY)
-- DO NOT EXECUTE. DO NOT SAVE AS ACTIVE MIGRATION WITHOUT SEPARATE AUDIT + TASK.
-- Preconditions:
--   - public.set_updated_at() exists (see baseline) OR use API-managed updated_at instead.
--   - public.module01_roles(id) uuid confirmed before enabling role_id FK below.
-- =============================================================================

-- ---------------------------------------------------------------------------
-- Tables
-- ---------------------------------------------------------------------------

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

-- role_id FK: enable only after confirming public.module01_roles (see section 7).
create table public.eds_power_role_module_access (
    id uuid primary key default gen_random_uuid(),
    role_id uuid not null references public.module01_roles (id),
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

-- ---------------------------------------------------------------------------
-- Indexes
-- ---------------------------------------------------------------------------

create index eds_power_modules_module_code_idx on public.eds_power_modules (module_code);
create index eds_power_modules_module_status_idx on public.eds_power_modules (module_status);
create index eds_power_module_actions_action_key_idx on public.eds_power_module_actions (action_key);
create index eds_power_module_actions_module_id_idx on public.eds_power_module_actions (module_id);
create index eds_power_role_module_access_role_id_idx on public.eds_power_role_module_access (role_id);
create index eds_power_role_module_access_action_id_idx on public.eds_power_role_module_access (action_id);
create index eds_power_role_module_access_module_id_idx on public.eds_power_role_module_access (module_id);
create index eds_power_role_module_access_environment_scope_idx on public.eds_power_role_module_access (environment_scope);

-- ---------------------------------------------------------------------------
-- updated_at triggers (ONLY if public.set_updated_at() confirmed on target DB)
-- Baseline reference: supabase/migrations/20260429110000_remote_legacy_baseline.sql
-- ---------------------------------------------------------------------------

create trigger trg_eds_power_modules_updated_at
    before update on public.eds_power_modules
    for each row
    execute function public.set_updated_at();

create trigger trg_eds_power_module_actions_updated_at
    before update on public.eds_power_module_actions
    for each row
    execute function public.set_updated_at();

create trigger trg_eds_power_role_module_access_updated_at
    before update on public.eds_power_role_module_access
    for each row
    execute function public.set_updated_at();

-- ---------------------------------------------------------------------------
-- Seed: modules + actions ONLY (order: SYSTEM_SHELL, MODULE_01, shell actions, module actions)
-- No role UUID literals. Role bindings: see placeholder below.
-- ---------------------------------------------------------------------------

insert into public.eds_power_modules (module_code, module_name, module_status, sort_order, is_active)
values
    ('SYSTEM_SHELL', 'System shell', 'RELEASED', 10, true),
    ('MODULE_01', 'Module 01', 'PLANNED', 20, true);

insert into public.eds_power_module_actions (
    module_id,
    action_key,
    action_type,
    menu_label,
    visibility,
    enabled,
    sort_order,
    requires_auth
)
select m.id, v.action_key, v.action_type, v.menu_label, 'VISIBLE', v.enabled, v.sort_order, v.requires_auth
from public.eds_power_modules m
cross join (
    values
        ('SYSTEM_SHELL', 'REFRESH_MENU', 'REFRESH_MENU', 'Оновити меню', true, 10, true),
        ('SYSTEM_SHELL', 'SESSION_STATUS', 'SESSION_STATUS', 'Статус сесії', true, 20, true),
        ('SYSTEM_SHELL', 'LOGOUT', 'LOGOUT', 'Вийти', true, 30, true),
        ('MODULE_01', 'MODULE_01_PLACEHOLDER', 'PLACEHOLDER_DISABLED', 'Module 01 — Розрахунки (planned)', false, 10, true)
) as v(module_code, action_key, action_type, menu_label, enabled, sort_order, requires_auth)
where m.module_code = v.module_code;

-- ---------------------------------------------------------------------------
-- PENDING: public.eds_power_role_module_access (role bindings)
-- Do NOT insert until read-only confirmation, e.g.:
--   select id, role_code from public.module01_roles order by role_code;
-- Then author INSERTs or idempotent seed under a separate audited step.
-- No hardcoded role UUIDs in repo.
-- ---------------------------------------------------------------------------

-- (intentionally no INSERT into eds_power_role_module_access in this draft)
```

## 10. Pre-Migration Blockers

Before creating or applying a real migration:

| Blocker | Action |
| --- | --- |
| Confirm `public.set_updated_at()` on target | Read-only inspection, or switch to documented API-managed `updated_at` (governance amendment) |
| Confirm `public.module01_roles(id)` uuid and FK viability | Read-only inspection |
| Decide RLS vs service-role-only MVP | Sign off `REGISTRY_ACCESS_STRATEGY` with security posture |
| Confirm no table name collision | Check `information_schema.tables` / registry for `eds_power_*` |
| Seed role bindings strategy | Confirm role ids or use `role_code` join in controlled migration sub-step under audit |

## 11. Explicit No-Execution Rule

This document **does not** authorize:

- SQL execution  
- `db push`  
- Supabase Dashboard DDL  
- Creation of `supabase/migrations/*.sql` for S01  

## 12. Next Allowed Step

**Gemini final pre-migration audit** of this implementation plan (`EDS_POWER_SQL_REGISTRY_S01_FINAL_IMPLEMENTATION_PLAN.md`).

**Only after PASS:** user may approve a **separate, explicit task** to create the actual `.sql` migration file.  
**Still:** no SQL execution on production (or any environment) unless separately approved per project gates.

## 13. Verdict

**FINAL_IMPLEMENTATION_PLAN_READY_FOR_AUDIT**
