# MODULE 01 MANUAL SQL EDITOR APPLY EXECUTION PLAN

## Status
PASS / CLOSED / APPROVED (DOC ONLY / EXECUTION PLANNING / NO SQL EXECUTION)

## Gemini Audit Closeout

- Final verdict: `PASS`
- Plan status: `CLOSED / APPROVED`
- Next allowed step: `Manual SQL Editor Apply Execution` as a separate operator task
- Naming correction accepted: `module01_calculations` is the correct Slice 01 table name (not `module01_kzo_calculations`)
- `schema_migrations` manual insert remains forbidden in apply step
- `migration repair` remains forbidden in apply step

## Purpose
Plan controlled manual application of Module 01 Schema Slice 01 through Supabase SQL Editor.

## Source Of Truth

Approved migration file:
`supabase/migrations/20260504190000_module01_schema_slice_01.sql`

Rules:
- SQL must be copied from this file only
- migration file must not be edited during apply
- no invented SQL
- no partial custom DDL

## Remote Target

- project: EDSPower Database
- ref: `mvcxtwoxhopumxcryxlc`
- schema: `public`

## Pre-Apply Checks

Before execution, operator must confirm:
- correct Supabase project selected
- SQL Editor opened on EDSPower Database
- migration file content copied fully
- no password/secret in SQL
- no `schema_migrations` insert included
- no migration repair
- no unrelated SQL

## Apply Scope

Allowed:
- execute only the SQL from:
  `supabase/migrations/20260504190000_module01_schema_slice_01.sql`

Expected Slice 01 tables:
- `module01_users`
- `module01_roles`
- `module01_user_roles`
- `module01_user_terminals`
- `module01_calculations`
- `module01_calculation_versions`
- `module01_calculation_status_history`
- `module01_audit_events`

Expected seed roles:
- `OWNER`
- `ADMIN`
- `DIRECTOR`
- `SALES_MANAGER`
- `CALCULATION_ENGINEER`
- `CONSTRUCTOR`
- `TECHNOLOGIST`
- `PRODUCTION`
- `KITTING`

Forbidden:
- no `schema_migrations` insert
- no migration repair
- no ERP/procurement/warehouse/pricing/CAD tables
- no product composition tables
- no `module_routes`
- no `object_conversion_links`
- no API/GAS/Python changes

## Execution Steps

1. Open Supabase Dashboard.
2. Select EDSPower Database.
3. Open SQL Editor.
4. Paste full SQL from approved migration file.
5. Review pasted SQL visually:
   - begins and ends as expected
   - contains only Slice 01 objects
   - contains no secrets
   - contains no `schema_migrations` insert
6. Execute once.
7. If execution fails:
   - stop immediately
   - do not rerun blindly
   - capture error text
   - do not manually patch
   - create FAIL/BLOCKED result
8. If execution succeeds:
   - run verification queries only.

## SQL Payload (Copy Without Edits)

```sql
-- Module 01 Supabase Schema Slice 01 migration
-- Scope: foundational identity/access/terminal/calculation/version/status/audit tables only.

create table public.module01_users (
    id uuid primary key default gen_random_uuid(),
    email text not null,
    display_name text,
    status text not null default 'ACTIVE',
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    constraint module01_users_email_key unique (email),
    constraint module01_users_status_check
        check (status in ('ACTIVE', 'DISABLED', 'ARCHIVED'))
);

create index module01_users_status_idx
    on public.module01_users (status);

create table public.module01_roles (
    id uuid primary key default gen_random_uuid(),
    role_code text not null,
    role_name text not null,
    description text,
    is_active boolean not null default true,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    constraint module01_roles_role_code_key unique (role_code)
);

create index module01_roles_is_active_idx
    on public.module01_roles (is_active);

create table public.module01_user_roles (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references public.module01_users(id),
    role_id uuid not null references public.module01_roles(id),
    assigned_by_user_id uuid references public.module01_users(id),
    assigned_at timestamptz not null default now(),
    is_active boolean not null default true
);

create index module01_user_roles_user_id_idx
    on public.module01_user_roles (user_id);

create index module01_user_roles_role_id_idx
    on public.module01_user_roles (role_id);

create index module01_user_roles_is_active_idx
    on public.module01_user_roles (is_active);

create unique index module01_user_roles_unique_active_user_role_idx
    on public.module01_user_roles (user_id, role_id)
    where is_active = true;

create table public.module01_user_terminals (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references public.module01_users(id),
    spreadsheet_id text not null,
    spreadsheet_url text,
    status text not null default 'ACTIVE',
    assigned_by_user_id uuid references public.module01_users(id),
    assigned_at timestamptz not null default now(),
    last_seen_at timestamptz,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    constraint module01_user_terminals_spreadsheet_id_key unique (spreadsheet_id),
    constraint module01_user_terminals_user_id_key unique (user_id),
    constraint module01_user_terminals_status_check
        check (status in ('ACTIVE', 'DISABLED', 'REPLACED', 'ARCHIVED'))
);

create index module01_user_terminals_user_id_idx
    on public.module01_user_terminals (user_id);

create index module01_user_terminals_status_idx
    on public.module01_user_terminals (status);

create table public.module01_calculations (
    id uuid primary key default gen_random_uuid(),
    calculation_base_number text not null,
    title text,
    potential_customer text,
    sales_manager_user_id uuid references public.module01_users(id),
    created_by_user_id uuid not null references public.module01_users(id),
    current_status text not null default 'DRAFT',
    is_archived boolean not null default false,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    constraint module01_calculations_calculation_base_number_key unique (calculation_base_number),
    constraint module01_calculations_base_number_format_check
        check (calculation_base_number ~ '^[0-9]{12}$'),
    constraint module01_calculations_current_status_check
        check (
            current_status in (
                'DRAFT',
                'CALCULATED',
                'SENT_TO_CLIENT',
                'REVISED',
                'APPROVED',
                'CONVERTED_TO_OBJECT',
                'CANCELLED',
                'ARCHIVED'
            )
        )
);

create index module01_calculations_created_by_user_id_idx
    on public.module01_calculations (created_by_user_id);

create index module01_calculations_sales_manager_user_id_idx
    on public.module01_calculations (sales_manager_user_id);

create index module01_calculations_current_status_idx
    on public.module01_calculations (current_status);

create index module01_calculations_created_at_idx
    on public.module01_calculations (created_at);

create table public.module01_calculation_versions (
    id uuid primary key default gen_random_uuid(),
    calculation_id uuid not null references public.module01_calculations(id),
    version_suffix text not null default '-00',
    calculation_version_number text not null,
    status text not null default 'DRAFT',
    created_by_user_id uuid not null references public.module01_users(id),
    source_version_id uuid references public.module01_calculation_versions(id),
    locked_at timestamptz,
    locked_by_user_id uuid references public.module01_users(id),
    lock_reason text,
    notes text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    constraint module01_calculation_versions_number_key unique (calculation_version_number),
    constraint module01_calculation_versions_unique_suffix_per_calculation
        unique (calculation_id, version_suffix),
    constraint module01_calculation_versions_suffix_format_check
        check (version_suffix ~ '^-[0-9]{2}$'),
    constraint module01_calculation_versions_status_check
        check (
            status in (
                'DRAFT',
                'CALCULATED',
                'SENT_TO_CLIENT',
                'REVISED',
                'APPROVED',
                'CONVERTED_TO_OBJECT',
                'CANCELLED',
                'ARCHIVED'
            )
        ),
    constraint module01_calculation_versions_lock_reason_check
        check (locked_at is null or lock_reason is not null)
);

create index module01_calculation_versions_calculation_id_idx
    on public.module01_calculation_versions (calculation_id);

create index module01_calculation_versions_status_idx
    on public.module01_calculation_versions (status);

create index module01_calculation_versions_created_by_user_id_idx
    on public.module01_calculation_versions (created_by_user_id);

create index module01_calculation_versions_locked_at_idx
    on public.module01_calculation_versions (locked_at);

create table public.module01_calculation_status_history (
    id uuid primary key default gen_random_uuid(),
    calculation_version_id uuid not null references public.module01_calculation_versions(id),
    old_status text,
    new_status text not null,
    changed_by_user_id uuid not null references public.module01_users(id),
    changed_at timestamptz not null default now(),
    reason text,
    notes text,
    request_id uuid,
    source_client text,
    constraint module01_calculation_status_history_new_status_check
        check (
            new_status in (
                'DRAFT',
                'CALCULATED',
                'SENT_TO_CLIENT',
                'REVISED',
                'APPROVED',
                'CONVERTED_TO_OBJECT',
                'CANCELLED',
                'ARCHIVED'
            )
        ),
    constraint module01_calculation_status_history_old_status_check
        check (
            old_status is null
            or old_status in (
                'DRAFT',
                'CALCULATED',
                'SENT_TO_CLIENT',
                'REVISED',
                'APPROVED',
                'CONVERTED_TO_OBJECT',
                'CANCELLED',
                'ARCHIVED'
            )
        )
);

create index module01_calculation_status_history_version_id_idx
    on public.module01_calculation_status_history (calculation_version_id);

create index module01_calculation_status_history_changed_by_user_id_idx
    on public.module01_calculation_status_history (changed_by_user_id);

create index module01_calculation_status_history_changed_at_idx
    on public.module01_calculation_status_history (changed_at);

create index module01_calculation_status_history_request_id_idx
    on public.module01_calculation_status_history (request_id);

create table public.module01_audit_events (
    id uuid primary key default gen_random_uuid(),
    entity_type text not null,
    entity_id uuid not null,
    event_type text not null,
    actor_user_id uuid references public.module01_users(id),
    event_at timestamptz not null default now(),
    request_id uuid,
    source_client text,
    metadata jsonb
);

create index module01_audit_events_entity_idx
    on public.module01_audit_events (entity_type, entity_id);

create index module01_audit_events_actor_user_id_idx
    on public.module01_audit_events (actor_user_id);

create index module01_audit_events_event_at_idx
    on public.module01_audit_events (event_at);

create index module01_audit_events_request_id_idx
    on public.module01_audit_events (request_id);

-- Seed roles idempotently.
insert into public.module01_roles (role_code, role_name, description, is_active)
values
    ('OWNER', 'Owner', 'System owner role', true),
    ('ADMIN', 'Administrator', 'Administrative role', true),
    ('DIRECTOR', 'Director', 'Director role', true),
    ('SALES_MANAGER', 'Sales Manager', 'Sales manager role', true),
    ('CALCULATION_ENGINEER', 'Calculation Engineer', 'Calculation engineer role', true),
    ('CONSTRUCTOR', 'Constructor', 'Constructor role', true),
    ('TECHNOLOGIST', 'Technologist', 'Technologist role', true),
    ('PRODUCTION', 'Production', 'Production role', true),
    ('KITTING', 'Kitting', 'Kitting role', true)
on conflict (role_code) do update
set
    role_name = excluded.role_name,
    description = excluded.description,
    is_active = excluded.is_active,
    updated_at = now();
```

## Verification Queries

### 1. Verify 8 tables exist

```sql
select table_name
from information_schema.tables
where table_schema = 'public'
  and table_name in (
    'module01_users',
    'module01_roles',
    'module01_user_roles',
    'module01_user_terminals',
    'module01_calculations',
    'module01_calculation_versions',
    'module01_calculation_status_history',
    'module01_audit_events'
  )
order by table_name;
```

### 2. Verify 9 seed roles exist

```sql
select count(*) as role_count
from public.module01_roles;

select role_code
from public.module01_roles
order by role_code;
```

Expected `role_code` set:
`OWNER`, `ADMIN`, `DIRECTOR`, `SALES_MANAGER`, `CALCULATION_ENGINEER`, `CONSTRUCTOR`, `TECHNOLOGIST`, `PRODUCTION`, `KITTING`

### 3. Verify excluded tables absent

```sql
select table_name
from information_schema.tables
where table_schema = 'public'
  and table_name in (
    'commercial_products',
    'calculation_product_items',
    'product_composition_items',
    'module_routes',
    'object_conversion_links'
  )
order by table_name;
```

### 4. Verify legacy tables remain present

```sql
select table_name
from information_schema.tables
where table_schema = 'public'
  and table_name in ('objects', 'bom_links', 'ncr', 'production_status')
order by table_name;
```

### 5. Verify no schema_migrations alignment performed

Operator attestation is mandatory: no manual insertion into `supabase_migrations.schema_migrations` was performed in this apply step.

Optional read-only check:

```sql
select version, name
from supabase_migrations.schema_migrations
where version = '20260504190000'
order by version;
```

## Evidence To Capture

Operator result must record:
- execution timestamp
- project ref
- source migration file path
- git commit/hash if available
- SQL execution result PASS/FAIL
- table verification result
- role verification result
- excluded scope verification
- legacy safety confirmation
- schema_migrations not touched confirmation

Do not capture:
- passwords
- service_role keys
- full connection strings with secrets

## Failure Handling

If SQL apply fails:
- stop
- do not rerun blindly
- do not patch manually
- document exact error
- return to planning

If verification fails:
- stop
- document mismatch
- do not patch manually
- return to planning

## Migration History Alignment

Not part of this execution.
After successful apply + verification, open separate audited step:
`Module 01 Migration History Alignment Decision`.

Possible future paths:
- `supabase migration repair` if CLI path becomes usable
- manual `schema_migrations` alignment only as emergency fallback with separate plan
- documented intentional drift if alignment remains blocked

## Next Allowed Step

Manual SQL Editor Apply Execution as separate operator task.
