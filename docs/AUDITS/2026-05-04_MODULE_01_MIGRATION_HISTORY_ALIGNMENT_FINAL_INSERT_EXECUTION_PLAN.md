# MODULE 01 MIGRATION HISTORY ALIGNMENT FINAL INSERT EXECUTION PLAN

## Status
DOC ONLY / FINAL INSERT PLANNING / NO SQL EXECUTION

## Gemini Audit Status
- final verdict: `PASS`
- plan status: `CLOSED / APPROVED`
- next allowed step: `Migration History Alignment FINAL INSERT Execution`
- `BEGIN` / `COMMIT` transaction wrapper is required for execution
- no `db push`
- no migration repair

## Purpose
Plan one controlled write to `supabase_migrations.schema_migrations` to align migration history after Module 01 manual SQL Editor apply.

## Source Of Truth
Approved migration file:
`supabase/migrations/20260504190000_module01_schema_slice_01.sql`

Target history row:
- version: `20260504190000`
- name: `module01_schema_slice_01`
- statements: array of SQL statements from approved migration file

## Confirmed Preconditions
- Module 01 remote schema physically applied
- 8 `module01_` tables present
- 9 role codes present and active
- excluded tables absent
- legacy tables present
- `schema_migrations` structure inspected
- version `20260504190000` absent
- `db push` not used
- migration repair not used

## Insert Strategy
Use Supabase SQL Editor.

The INSERT must:
- target only `supabase_migrations.schema_migrations`
- insert exactly one row
- use `version = '20260504190000'`
- use `name = 'module01_schema_slice_01'`
- use statements array derived from the approved migration file
- not modify any `public.module01_*` table
- not modify legacy tables
- not run migration repair
- not run db push
- run inside explicit `BEGIN` / `COMMIT` transaction wrapper

## Safe SQL Construction Requirement
Use PostgreSQL dollar-quoted strings for statements to avoid quote escaping errors.

Important:
- Do not include secrets.
- Do not include unrelated SQL.
- Do not include DDL execution for module01 tables in this insert step.
- The module01 DDL was already applied earlier.

## Pre-Insert Read-only Checks
Before INSERT, run:

1. Confirm target version absent:

```sql
select *
from supabase_migrations.schema_migrations
where version = '20260504190000';
```

Expected:
`0` rows.

2. Confirm Module 01 tables still present.
3. Confirm 9 roles still present.

If any check fails:
STOP. Do not insert.

## Final INSERT SQL
Prepared from:
`supabase/migrations/20260504190000_module01_schema_slice_01.sql`

Do not execute it in this planning task.
For future execution, wrap as:
`BEGIN;` -> single INSERT below -> `COMMIT;`

```sql
insert into supabase_migrations.schema_migrations (version, statements, name)
values (
  '20260504190000',
  array[
    $stmt$create table public.module01_users (
    id uuid primary key default gen_random_uuid(),
    email text not null,
    display_name text,
    status text not null default 'ACTIVE',
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    constraint module01_users_email_key unique (email),
    constraint module01_users_status_check
        check (status in ('ACTIVE', 'DISABLED', 'ARCHIVED'))
);$stmt$,
    $stmt$create index module01_users_status_idx
    on public.module01_users (status);$stmt$,
    $stmt$create table public.module01_roles (
    id uuid primary key default gen_random_uuid(),
    role_code text not null,
    role_name text not null,
    description text,
    is_active boolean not null default true,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    constraint module01_roles_role_code_key unique (role_code)
);$stmt$,
    $stmt$create index module01_roles_is_active_idx
    on public.module01_roles (is_active);$stmt$,
    $stmt$create table public.module01_user_roles (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references public.module01_users(id),
    role_id uuid not null references public.module01_roles(id),
    assigned_by_user_id uuid references public.module01_users(id),
    assigned_at timestamptz not null default now(),
    is_active boolean not null default true
);$stmt$,
    $stmt$create index module01_user_roles_user_id_idx
    on public.module01_user_roles (user_id);$stmt$,
    $stmt$create index module01_user_roles_role_id_idx
    on public.module01_user_roles (role_id);$stmt$,
    $stmt$create index module01_user_roles_is_active_idx
    on public.module01_user_roles (is_active);$stmt$,
    $stmt$create unique index module01_user_roles_unique_active_user_role_idx
    on public.module01_user_roles (user_id, role_id)
    where is_active = true;$stmt$,
    $stmt$create table public.module01_user_terminals (
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
);$stmt$,
    $stmt$create index module01_user_terminals_user_id_idx
    on public.module01_user_terminals (user_id);$stmt$,
    $stmt$create index module01_user_terminals_status_idx
    on public.module01_user_terminals (status);$stmt$,
    $stmt$create table public.module01_calculations (
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
);$stmt$,
    $stmt$create index module01_calculations_created_by_user_id_idx
    on public.module01_calculations (created_by_user_id);$stmt$,
    $stmt$create index module01_calculations_sales_manager_user_id_idx
    on public.module01_calculations (sales_manager_user_id);$stmt$,
    $stmt$create index module01_calculations_current_status_idx
    on public.module01_calculations (current_status);$stmt$,
    $stmt$create index module01_calculations_created_at_idx
    on public.module01_calculations (created_at);$stmt$,
    $stmt$create table public.module01_calculation_versions (
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
);$stmt$,
    $stmt$create index module01_calculation_versions_calculation_id_idx
    on public.module01_calculation_versions (calculation_id);$stmt$,
    $stmt$create index module01_calculation_versions_status_idx
    on public.module01_calculation_versions (status);$stmt$,
    $stmt$create index module01_calculation_versions_created_by_user_id_idx
    on public.module01_calculation_versions (created_by_user_id);$stmt$,
    $stmt$create index module01_calculation_versions_locked_at_idx
    on public.module01_calculation_versions (locked_at);$stmt$,
    $stmt$create table public.module01_calculation_status_history (
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
);$stmt$,
    $stmt$create index module01_calculation_status_history_version_id_idx
    on public.module01_calculation_status_history (calculation_version_id);$stmt$,
    $stmt$create index module01_calculation_status_history_changed_by_user_id_idx
    on public.module01_calculation_status_history (changed_by_user_id);$stmt$,
    $stmt$create index module01_calculation_status_history_changed_at_idx
    on public.module01_calculation_status_history (changed_at);$stmt$,
    $stmt$create index module01_calculation_status_history_request_id_idx
    on public.module01_calculation_status_history (request_id);$stmt$,
    $stmt$create table public.module01_audit_events (
    id uuid primary key default gen_random_uuid(),
    entity_type text not null,
    entity_id uuid not null,
    event_type text not null,
    actor_user_id uuid references public.module01_users(id),
    event_at timestamptz not null default now(),
    request_id uuid,
    source_client text,
    metadata jsonb
);$stmt$,
    $stmt$create index module01_audit_events_entity_idx
    on public.module01_audit_events (entity_type, entity_id);$stmt$,
    $stmt$create index module01_audit_events_actor_user_id_idx
    on public.module01_audit_events (actor_user_id);$stmt$,
    $stmt$create index module01_audit_events_event_at_idx
    on public.module01_audit_events (event_at);$stmt$,
    $stmt$create index module01_audit_events_request_id_idx
    on public.module01_audit_events (request_id);$stmt$,
    $stmt$insert into public.module01_roles (role_code, role_name, description, is_active)
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
    updated_at = now();$stmt$
  ],
  'module01_schema_slice_01'
);
```

## Post-Insert Verification
After future execution, run:

1. Confirm target row exists:

```sql
select version, name, cardinality(statements) as statements_count
from supabase_migrations.schema_migrations
where version = '20260504190000';
```

Expected:
`1` row.

2. Confirm no duplicate:

```sql
select version, count(*) as row_count
from supabase_migrations.schema_migrations
where version = '20260504190000'
group by version;
```

Expected:
`row_count = 1`.

3. Confirm 8 Module 01 tables still present.
4. Confirm 9 roles still present.
5. Confirm `db push` was not used.

## Failure Handling
If INSERT fails:
- stop immediately
- do not retry blindly
- capture exact error
- do not manually patch
- return to planning

If duplicate exists:
- stop
- do not insert
- record already-aligned / investigate

If post-insert verification fails:
- stop
- document mismatch
- do not patch blindly
- return to planning

## Forbidden
- no SQL execution in this planning task
- no `schema_migrations` insert in this planning task
- no migration repair
- no `db push`
- no DDL/table creation
- no API/GAS/Python changes
- no migration file edits
- no secrets

## Next Allowed Step
Gemini audit of this FINAL INSERT Execution Plan.

If PASS:
Migration History Alignment FINAL INSERT Execution as separate operator task.
