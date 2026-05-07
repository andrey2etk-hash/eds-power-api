# EDS Power SQL Migration Plan Registry S01

## 1. Purpose

Plan the first Supabase registry slice for DB-driven dynamic menu.

Goal:
Replace hardcoded mock menu payload with controlled DB registry later.

## 2. Scope

S01 covers only:
- modules
- module_actions
- role_module_access

S01 does NOT cover:
- terminal_module_access
- admin provisioning
- calculation modules
- production routing
- NCR
- KZO logic
- BOM
- notifications

## 3. Existing Schema Check Required

Before writing final DDL, existing baseline docs/migrations must be checked.

Referenced artifacts for S01 planning:
- `supabase/migrations/README.md` (migration ordering and naming rules)
- `supabase/schema_registry/REGISTRY_INDEX.md` (baseline structure and ordering)
- `supabase/migrations/20260429110000_remote_legacy_baseline.sql` (legacy baseline)
- `supabase/migrations/20260429120000_calculation_snapshots_v1.sql` (post-baseline additive pattern)
- `supabase/migrations/20260504190000_module01_schema_slice_01.sql` (existing users/roles model)
- `supabase/migrations/20260505110000_module01_user_auth.sql` (existing auth model)
- `supabase/migrations/20260505120000_module01_user_sessions.sql` (existing sessions model)

Confirmed existing entities relevant to this plan:
- existing users table: `public.module01_users`
- existing roles table: `public.module01_roles`
- existing auth table: `public.module01_user_auth`
- existing sessions table: `public.module01_user_sessions`

Do not guess conflicts with existing tables.

Required check before SQL execution:
- confirm whether `public.module01_roles` is canonical role source for menu RBAC
- confirm `role_id` FK target from active auth/roles schema in target environment
- confirm migration naming slot against latest repo migration at execution time
- reconfirm baseline ordering (`remote_legacy_baseline` before additive slices)

If canonical role table changes by execution time, mark as OPEN QUESTION and block SQL apply.

## 4. Proposed Tables

### 4.1 modules

Purpose:
Registry of system modules.

Proposed fields:
- id uuid primary key
- module_code text unique not null
- module_name text not null
- module_status text not null
- module_version text
- description text
- sort_order integer not null default 100
- is_active boolean not null default true
- created_at timestamptz not null default now()
- updated_at timestamptz not null default now()

Allowed module_status:
- RELEASED
- ADMIN_TEST
- DEV
- DISABLED
- MAINTENANCE
- HIDDEN
- PLANNED

### 4.2 module_actions

Purpose:
Registry of menu/actions per module or system shell.

Proposed fields:
- id uuid primary key
- module_id uuid nullable references modules(id)
- action_key text unique not null
- action_type text not null
- menu_label text not null
- visibility text not null default 'VISIBLE'
- enabled boolean not null default true
- requires_auth boolean not null default true
- required_core_version text
- sort_order integer not null default 100
- metadata jsonb not null default '{}'::jsonb
- created_at timestamptz not null default now()
- updated_at timestamptz not null default now()

Allowed action_type:
- OPEN_DIALOG
- OPEN_SIDEBAR
- RUN_BATCH_ACTION
- REFRESH_MENU
- LOGOUT
- SESSION_STATUS
- PLACEHOLDER_DISABLED

Allowed visibility:
- VISIBLE
- HIDDEN

### 4.3 role_module_access

Purpose:
Maps roles to allowed modules/actions.

Proposed fields:
- id uuid primary key
- role_id uuid not null
- module_id uuid nullable references modules(id)
- action_id uuid not null references module_actions(id)
- access_level text not null default 'NONE'
- visible boolean not null default false
- enabled boolean not null default false
- environment_scope text not null default 'PRODUCTION'
- created_at timestamptz not null default now()
- updated_at timestamptz not null default now()

Allowed access_level:
- NONE
- VIEW
- USE
- ADMIN
- DEV_TEST

Allowed environment_scope:
- PRODUCTION
- ADMIN_TEST
- DEV
- TEMPLATE

Important:
`role_id` FK target must be confirmed from existing auth/roles schema before SQL execution.

## 5. Constraints

Plan constraints:
- `module_code` unique
- `action_key` unique
- role/action uniqueness should prevent duplicate grants
- check constraints for statuses/types should be considered
- `updated_at` trigger should follow existing repo convention if present

Planned uniqueness candidates for duplicate grant prevention:
- unique (`role_id`, `action_id`, `environment_scope`)
- optional unique (`role_id`, `module_id`, `environment_scope`) if module-level grants are used

## 6. Indexes

Proposed indexes:
- modules(module_code)
- modules(module_status)
- module_actions(action_key)
- module_actions(module_id)
- role_module_access(role_id)
- role_module_access(action_id)
- role_module_access(module_id)
- role_module_access(environment_scope)

## 7. Seed Data Plan

Initial seed should include:

Modules:
- SYSTEM_SHELL
- MODULE_01

Actions:
- REFRESH_MENU
- SESSION_STATUS
- LOGOUT
- MODULE_01_PLACEHOLDER

Initial statuses:
- SYSTEM_SHELL = RELEASED
- MODULE_01 = PLANNED or ADMIN_TEST depending audit decision

Initial menu labels:
- Оновити меню
- Статус сесії
- Вийти
- Module 01 — Розрахунки (planned)

Role bindings:
- Use existing role IDs only after schema confirmation.
- If canonical role IDs are not confirmed for target environment, keep seed role bindings blocked as OPEN QUESTION.

## 8. Migration File Naming Plan

Proposed migration filename pattern only:
- `supabase/migrations/YYYYMMDDHHMMSS_eds_power_dynamic_menu_registry_s01.sql`

Candidate naming handle:
- `eds_power_dynamic_menu_registry_s01`

No SQL file is created in this task.

## 9. Rollback Plan

Rollback must be planned carefully.

Options:
- drop only S01 tables if no dependent data exists
- avoid destructive rollback after production use
- prefer migration-forward correction after real data exists

Operational note:
- once role/action grants are used by production flows, destructive rollback should be avoided in favor of additive corrective migrations.

## 10. Security Notes

- no secrets in seed data
- no tokens
- no passwords
- no service role exposure
- no user-specific terminal data in this slice

## 11. Backend Integration Preview

Future backend should:
- validate session
- resolve roles
- resolve terminal context
- query registry
- return same menu payload contract

This task does not implement backend.

## 12. Open Questions

- exact canonical roles table name at execution time (`module01_roles` vs future shared roles table)
- canonical `role_id` source for seed bindings (UUID source of truth)
- whether role names or UUIDs are canonical for seed mapping governance
- `updated_at` trigger convention (DB trigger vs API-managed timestamps)
- RLS expectations for service-role backend access to registry tables
- whether SYSTEM_SHELL actions should use nullable `module_id` or mandatory dedicated module row
- whether MASTER_TEMPLATE must always map to `environment_scope = TEMPLATE`

## 13. What This Does NOT Do

This plan does not:
- execute SQL
- create migration file
- alter Supabase
- edit backend
- edit GAS
- implement DB-driven menu

## 14. Verdict

SQL implementation is blocked until this migration plan is audited.
