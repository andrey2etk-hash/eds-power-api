-- EDS Power Dynamic Menu Registry S01
-- Authored from: docs/DB_MIGRATIONS/EDS_POWER_SQL_REGISTRY_S01_FINAL_IMPLEMENTATION_PLAN.md
-- Governance: CODE ONLY — this file was added without executing SQL, db push, or Supabase mutation.
--
-- Preconditions (verified from repo migrations only):
--   - public.set_updated_at() in 20260429110000_remote_legacy_baseline.sql (apply order before Module 01 slice)
--   - public.module01_roles with id uuid in 20260504190000_module01_schema_slice_01.sql
--
-- MVP access posture (documentation; not enforced by RLS in this file):
--   - Registry tables are for backend service-role access only.
--   - GAS must not read these tables directly.
--   - Do not grant broad anon/authenticated policies without a separate audited task.

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

create index eds_power_modules_module_code_idx on public.eds_power_modules (module_code);
create index eds_power_modules_module_status_idx on public.eds_power_modules (module_status);
create index eds_power_module_actions_action_key_idx on public.eds_power_module_actions (action_key);
create index eds_power_module_actions_module_id_idx on public.eds_power_module_actions (module_id);
create index eds_power_role_module_access_role_id_idx on public.eds_power_role_module_access (role_id);
create index eds_power_role_module_access_action_id_idx on public.eds_power_role_module_access (action_id);
create index eds_power_role_module_access_module_id_idx on public.eds_power_role_module_access (module_id);
create index eds_power_role_module_access_environment_scope_idx on public.eds_power_role_module_access (environment_scope);

-- public.set_updated_at() confirmed in remote_legacy_baseline migration.
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

-- Seed order: SYSTEM_SHELL module, MODULE_01 module, actions, then role bindings (role_id via join — no UUID literals).
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
select
    m.id,
    v.action_key,
    v.action_type,
    v.menu_label,
    'VISIBLE',
    v.enabled,
    v.sort_order,
    v.requires_auth
from public.eds_power_modules m
cross join (
    values
        ('SYSTEM_SHELL', 'REFRESH_MENU', 'REFRESH_MENU', 'Оновити меню', true, 10, true),
        ('SYSTEM_SHELL', 'SESSION_STATUS', 'SESSION_STATUS', 'Статус сесії', true, 20, true),
        ('SYSTEM_SHELL', 'LOGOUT', 'LOGOUT', 'Вийти', true, 30, true),
        ('MODULE_01', 'MODULE_01_PLACEHOLDER', 'PLACEHOLDER_DISABLED', 'Module 01 — Розрахунки (planned)', false, 10, true)
) as v(module_code, action_key, action_type, menu_label, enabled, sort_order, requires_auth)
where m.module_code = v.module_code;

-- Role bindings: join public.module01_roles by id (no hardcoded UUIDs). Active roles only.
-- Bootstrap policy: PRODUCTION scope, USE, visible/enabled, for the four S01 menu actions.
-- Tighten per-role grants in a follow-up migration if governance requires least-privilege by role_code.
insert into public.eds_power_role_module_access (
    role_id,
    module_id,
    action_id,
    access_level,
    visible,
    enabled,
    environment_scope
)
select
    r.id,
    a.module_id,
    a.id,
    'USE',
    true,
    true,
    'PRODUCTION'
from public.module01_roles r
cross join public.eds_power_module_actions a
where r.is_active = true
  and a.action_key in (
    'REFRESH_MENU',
    'SESSION_STATUS',
    'LOGOUT',
    'MODULE_01_PLACEHOLDER'
  );

-- Verification (do not execute inside automated migration runner as a blocking step; for manual operator use only).
-- select to_regclass('public.eds_power_modules');
-- select count(*) from public.eds_power_modules where module_code in ('SYSTEM_SHELL', 'MODULE_01');
-- select count(*) from public.eds_power_module_actions;
-- select count(*) from public.eds_power_role_module_access;
