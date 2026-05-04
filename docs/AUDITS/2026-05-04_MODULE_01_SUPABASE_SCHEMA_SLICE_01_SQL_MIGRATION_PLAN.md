# MODULE 01 SUPABASE SCHEMA SLICE 01 SQL / MIGRATION PLAN

## Status
DOC ONLY / SQL MIGRATION PLANNING / NO SQL FILE

## Purpose

Plan the future SQL migration for Module 01 Supabase Schema Slice 01.

This plan prepares SQL/DDL implementation but does not create or execute SQL.

## Source of Truth Reminder

Supabase is the single source of truth.
Google Sheets is only a personal terminal.
GAS is only a thin client.
API is the only gateway.

## Migration Scope

Included tables:
1. `module01_users`
2. `module01_roles`
3. `module01_user_roles`
4. `module01_user_terminals`
5. `module01_calculations`
6. `module01_calculation_versions`
7. `module01_calculation_status_history`
8. `module01_audit_events`

Use `module01_` prefix to avoid collision with existing legacy/public tables unless project convention strongly prefers another schema/prefix.

Excluded:
- product composition
- object conversion links
- lock table implementation
- RLS policies
- triggers
- database functions
- production ERP integration
- pricing
- procurement
- warehouse
- CAD

## Proposed Migration Filename

Proposed filename:
`YYYYMMDDHHMMSS_module01_schema_slice_01.sql`

Example:
`20260504190000_module01_schema_slice_01.sql`

Rule:
Actual timestamp must be selected at implementation time.

## Table Creation Order

1. module01_users
2. module01_roles
3. module01_user_roles
4. module01_user_terminals
5. module01_calculations
6. module01_calculation_versions
7. module01_calculation_status_history
8. module01_audit_events

Reason:
Respect foreign key dependencies.

## Common Column Rules

Use:
- `id uuid primary key default gen_random_uuid()`
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

Note:
Do not implement triggers for `updated_at` in Slice 01 unless separately approved.
Manual/API update of `updated_at` can be planned later.

## Table: module01_users

Columns:
- id uuid primary key default gen_random_uuid()
- email text not null
- display_name text
- status text not null default 'ACTIVE'
- created_at timestamptz not null default now()
- updated_at timestamptz not null default now()

Constraints:
- unique(email)
- check status in ('ACTIVE', 'DISABLED', 'ARCHIVED')

Indexes:
- unique index on email
- index on status

Notes:
- Do not bind to auth.users yet.
- Auth integration is separate future slice.

## Table: module01_roles

Columns:
- id uuid primary key default gen_random_uuid()
- role_code text not null
- role_name text not null
- description text
- is_active boolean not null default true
- created_at timestamptz not null default now()
- updated_at timestamptz not null default now()

Constraints:
- unique(role_code)

Indexes:
- unique index on role_code
- index on is_active

Seed roles:
- OWNER
- ADMIN
- DIRECTOR
- SALES_MANAGER
- CALCULATION_ENGINEER
- CONSTRUCTOR
- TECHNOLOGIST
- PRODUCTION
- KITTING

Seed rule:
Use idempotent insert/upsert pattern in future SQL.

## Table: module01_user_roles

Columns:
- id uuid primary key default gen_random_uuid()
- user_id uuid not null references module01_users(id)
- role_id uuid not null references module01_roles(id)
- assigned_by_user_id uuid references module01_users(id)
- assigned_at timestamptz not null default now()
- is_active boolean not null default true

Constraints:
- prevent exact duplicate user_id + role_id + is_active=true if feasible
- foreign keys to users and roles

Recommended constraint:
Partial unique index:
unique(user_id, role_id) where is_active = true

Indexes:
- index on user_id
- index on role_id
- index on is_active

## Table: module01_user_terminals

Columns:
- id uuid primary key default gen_random_uuid()
- user_id uuid not null references module01_users(id)
- spreadsheet_id text not null
- spreadsheet_url text
- status text not null default 'ACTIVE'
- assigned_by_user_id uuid references module01_users(id)
- assigned_at timestamptz not null default now()
- last_seen_at timestamptz
- created_at timestamptz not null default now()
- updated_at timestamptz not null default now()

Constraints:
- unique(spreadsheet_id)
- unique(user_id) for MVP one user = one terminal
- check status in ('ACTIVE', 'DISABLED', 'REPLACED', 'ARCHIVED')

Indexes:
- index on user_id
- unique index on spreadsheet_id
- index on status

Notes:
Personal terminal is not source of truth.
It only points to user's Google Sheet.

## Table: module01_calculations

Columns:
- id uuid primary key default gen_random_uuid()
- calculation_base_number text not null
- title text
- potential_customer text
- sales_manager_user_id uuid references module01_users(id)
- created_by_user_id uuid not null references module01_users(id)
- current_status text not null default 'DRAFT'
- is_archived boolean not null default false
- created_at timestamptz not null default now()
- updated_at timestamptz not null default now()

Constraints:
- unique(calculation_base_number)
- check calculation_base_number matches YYYYMMDDHHMM pattern
- check current_status in allowed statuses

Allowed statuses:
- DRAFT
- CALCULATED
- SENT_TO_CLIENT
- REVISED
- APPROVED
- CONVERTED_TO_OBJECT
- CANCELLED
- ARCHIVED

Indexes:
- unique index on calculation_base_number
- index on created_by_user_id
- index on sales_manager_user_id
- index on current_status
- index on created_at

Rules:
- calculation_base_number is not object_number
- object_number excluded from Slice 01

## Table: module01_calculation_versions

Columns:
- id uuid primary key default gen_random_uuid()
- calculation_id uuid not null references module01_calculations(id)
- version_suffix text not null default '-00'
- calculation_version_number text not null
- status text not null default 'DRAFT'
- created_by_user_id uuid not null references module01_users(id)
- source_version_id uuid references module01_calculation_versions(id)
- locked_at timestamptz
- locked_by_user_id uuid references module01_users(id)
- lock_reason text
- notes text
- created_at timestamptz not null default now()
- updated_at timestamptz not null default now()

Constraints:
- unique(calculation_version_number)
- unique(calculation_id, version_suffix)
- check version_suffix matches pattern '-00' or '-NN'
- check calculation_version_number format = calculation_base_number + version_suffix
  NOTE: exact cross-table validation may require trigger/function and should not be implemented in Slice 01 unless approved.
- check status in allowed statuses
- if locked_at is not null, lock_reason should be present if feasible

Recommended initial version:
-00

Examples:
- base: 202605041530
- initial: 202605041530-00
- next: 202605041530-01

Indexes:
- index on calculation_id
- unique index on calculation_version_number
- index on status
- index on created_by_user_id
- index on locked_at

Rules:
- locked version cannot be edited
- actual enforcement may be API-side in Slice 01
- DB trigger/RLS enforcement planned later

## Table: module01_calculation_status_history

Columns:
- id uuid primary key default gen_random_uuid()
- calculation_version_id uuid not null references module01_calculation_versions(id)
- old_status text
- new_status text not null
- changed_by_user_id uuid not null references module01_users(id)
- changed_at timestamptz not null default now()
- reason text
- notes text
- request_id uuid
- source_client text

Constraints:
- check new_status in allowed statuses
- check old_status in allowed statuses or null
- source_client optional but recommended

Indexes:
- index on calculation_version_id
- index on changed_by_user_id
- index on changed_at
- index on request_id

Rules:
- every status change should create history row
- no trigger in Slice 01 unless separately approved
- API will be responsible initially

## Table: module01_audit_events

Columns:
- id uuid primary key default gen_random_uuid()
- entity_type text not null
- entity_id uuid not null
- event_type text not null
- actor_user_id uuid references module01_users(id)
- event_at timestamptz not null default now()
- request_id uuid
- source_client text
- metadata jsonb

Constraints:
- entity_type required
- event_type required

Indexes:
- index on entity_type, entity_id
- index on actor_user_id
- index on event_at
- index on request_id
- optional GIN index on metadata if justified later

Initial event types:
- user_terminal_assigned
- calculation_created
- calculation_version_created
- calculation_status_changed
- calculation_locked
- calculation_viewed
- calculation_search_executed

Notes:
audit_events does not replace status history.

## Data Type Rules

Use:
- uuid for primary keys
- text for flexible codes/statuses in Slice 01
- timestamptz for timestamps
- boolean for active flags
- jsonb only for audit metadata

Avoid:
- numeric/product quantities in Slice 01
- pricing columns
- object_number fields
- ERP identifiers
- procurement identifiers
- warehouse fields

## Check Constraint Planning

Plan check constraints for:
- user status
- terminal status
- calculation status
- version status
- calculation_base_number pattern
- version_suffix pattern

Do not overuse database functions in Slice 01.

## Index Planning

Required indexes:
- all FK columns
- status fields used for filtering
- calculation_base_number
- calculation_version_number
- request_id in audit/history tables
- created_at / changed_at / event_at for timeline queries

## Seed Data Planning

Seed only roles in Slice 01.

Do not seed users unless separately approved.

Roles:
- OWNER
- ADMIN
- DIRECTOR
- SALES_MANAGER
- CALCULATION_ENGINEER
- CONSTRUCTOR
- TECHNOLOGIST
- PRODUCTION
- KITTING

## RLS / Security Boundary

RLS policies are NOT implemented in Slice 01 migration unless separately approved.

This plan must mention:
- RLS is required for production readiness
- RLS planning should be separate Slice 04
- until then, API must enforce access in demo/prototype mode

## updated_at Boundary

Do not add updated_at triggers in Slice 01 unless separately approved.

Options:
- API manually updates `updated_at`
- later shared trigger/function for updated_at

Recommendation:
Keep triggers out of Slice 01.

## Verification Query Planning

Future migration verification should check:
- all 8 tables exist
- role seed rows exist
- unique constraints exist
- check constraints exist
- FK relationships exist
- no excluded tables were created
- no ERP/procurement/pricing/warehouse/CAD columns exist

## Rollback Planning

Future rollback must be cautious.

Recommended:
- no destructive rollback in production
- for local/dev: drop tables in reverse dependency order
- for production: require separate rollback plan

## Open Decisions For Gemini Audit

List open decisions:
1. Is `module01_` prefix acceptable, or should tables live in a dedicated schema?
2. Is initial version suffix `-00` accepted?
3. Should `updated_at` triggers be deferred?
4. Should RLS be deferred to separate slice?
5. Should `calculation_base_number` be generated by API only, or later DB function?
6. Should users table later map to auth.users?

## Governance Boundary

This plan does not authorize:
- SQL file creation
- migration creation
- DDL execution
- DB writes
- API implementation
- GAS implementation
- RLS implementation
- triggers/functions
- production deployment

## Next Allowed Step

After this plan:
- Gemini audit of SQL/Migration Plan
- if PASS: create migration file as separate narrow task
- migration execution only after separate approval

## Gemini Audit Status

- final verdict: PASS
- plan status: CLOSED / APPROVED
- required fixes: none
- module01_ prefix accepted for MVP
- initial version suffix -00 accepted
- updated_at triggers deferred
- RLS deferred
- next allowed step: Create migration file
- no SQL file / migration / DDL execution / table creation performed
