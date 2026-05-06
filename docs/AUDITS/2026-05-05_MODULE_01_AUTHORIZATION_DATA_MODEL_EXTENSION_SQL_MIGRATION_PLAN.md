# MODULE 01 AUTHORIZATION DATA MODEL EXTENSION SQL/MIGRATION PLAN

## Status
DOC ONLY / SQL-MIGRATION PLANNING / NO EXECUTION

## Purpose
Plan a future Supabase migration to add authentication storage for corporate email + password authorization.

## Source Doctrine And Plan
Reference:
- `docs/AUDITS/2026-05-05_MODULE_01_CORPORATE_EMAIL_AUTHORIZATION_DOCTRINE.md`
- `docs/AUDITS/2026-05-05_MODULE_01_AUTHORIZATION_DATA_MODEL_EXTENSION_PLAN.md`

## Scope
Create one new table:
- `public.module01_user_auth`

No API/GAS implementation in this plan.
No password hashing implementation in this plan.
No user seed passwords.
No real secrets.

## Proposed Migration File Name
Propose:
`supabase/migrations/20260505110000_module01_user_auth.sql`

Note:
Exact timestamp may be adjusted by operator before migration file creation.

## Table: module01_user_auth

Planned fields:
- id uuid primary key default gen_random_uuid()
- user_id uuid not null references public.module01_users(id) on delete cascade
- password_hash text not null
- password_algorithm text not null
- password_updated_at timestamptz
- must_change_password boolean not null default true
- reset_token_hash text
- reset_token_expires_at timestamptz
- reset_requested_at timestamptz
- failed_login_attempts integer not null default 0
- locked_until timestamptz
- last_login_at timestamptz
- last_login_terminal_id uuid references public.module01_user_terminals(id)
- created_at timestamptz not null default now()
- updated_at timestamptz not null default now()

## Constraints

Required constraints:
- unique(user_id)
- failed_login_attempts >= 0
- password_algorithm not empty
- password_hash not empty
- if reset_token_hash is null then reset_token_expires_at may be null
- if reset_token_hash is not null then reset_token_expires_at should not be null

Consider check constraint for password_algorithm:
Allowed values initially:
- ARGON2ID
- BCRYPT

Decision needed:
Keep broad text check or strict enum-like check.

Recommended for MVP:
check password_algorithm in ('ARGON2ID', 'BCRYPT')

## Indexes

Required indexes:
- module01_user_auth_user_id_idx
- module01_user_auth_locked_until_idx
- module01_user_auth_reset_token_expires_at_idx

Consider partial index:
- reset_token_hash where reset_token_hash is not null

Important:
Do not create a globally unique plain reset_token_hash unless justified.
If uniqueness is needed, use partial unique index:
unique(reset_token_hash) where reset_token_hash is not null

## updated_at Handling

Gemini recommended updated_at triggers.

But current Module 01 Slice 01 intentionally deferred updated_at triggers.

Decision required:
Option A — keep updated_at manual/API-managed for consistency with Slice 01
Option B — introduce trigger function and trigger for module01_user_auth

Recommended:
Option A for this slice, unless a separate updated_at trigger doctrine is approved.

Reason:
Avoid introducing trigger behavior only for auth table while Slice 01 tables still use manual updated_at.

## Existing Users / Backfill

This migration must not create real passwords.

If existing users exist:
- migration should create table only
- no default auth rows with fake passwords
- admin provisioning flow will create auth rows later

No seed passwords.
No real user credentials.
No secrets.

## Terminal Reference

last_login_terminal_id references module01_user_terminals(id).

Login API must still receive spreadsheet_id/terminal_id and resolve current terminal through module01_user_terminals.

This migration only stores last successful terminal reference.
It does not itself enforce login rules.

## Audit Integration

No new audit table required.
Use existing:
- module01_audit_events

Future API actions should write events:
- LOGIN_SUCCESS
- LOGIN_FAILED
- PASSWORD_CHANGED
- PASSWORD_RESET_REQUESTED
- PASSWORD_RESET_COMPLETED
- ADMIN_PASSWORD_RESET
- USER_LOCKED
- USER_UNLOCKED

No implementation in this plan.

## Security Guardrails

Forbidden:
- storing plain passwords
- seed passwords
- real reset tokens
- service keys
- credentials in migration file
- exposing password_hash in API response
- logging password_hash or reset_token_hash

## Verification Plan

After future migration execution, verify:

1. Table exists:
`public.module01_user_auth`

2. Columns exist:
all planned fields.

3. Constraints exist:
- unique user_id
- failed_login_attempts check
- password_algorithm check
- reset token consistency check if implemented.

4. Indexes exist:
planned indexes.

5. Existing Slice 01 tables remain present:
- module01_users
- module01_roles
- module01_user_roles
- module01_user_terminals

6. No auth rows seeded automatically unless explicitly planned later.

7. No secrets present.

## Boundary

This plan does not authorize:
- migration file creation
- SQL execution
- DB writes
- API implementation
- GAS implementation
- password hashing implementation
- email sending implementation
- production deployment

## Open Questions For Gemini

1. Should password_algorithm use strict check constraint or free text?
2. Should reset_token_hash have partial unique index?
3. Should updated_at trigger be introduced now or deferred?
4. Should password_updated_at be NOT NULL after provisioning or nullable until first auth record?
5. Should module01_user_auth.user_id use ON DELETE CASCADE or RESTRICT?
6. Should last_login_terminal_id use ON DELETE SET NULL if terminal is replaced/deleted?

## Recommended Next Step

Migration File Creation.

Create migration file as separate task:
`supabase/migrations/20260505110000_module01_user_auth.sql`

## Gemini Audit Status

- final verdict: PASS
- plan status: CLOSED / APPROVED
- module01_user_auth SQL/migration plan accepted
- password_algorithm strict CHECK approved: `ARGON2ID`, `BCRYPT`
- partial unique index approved: `unique(reset_token_hash) where reset_token_hash is not null`
- updated_at triggers deferred for Slice 01 consistency
- password_updated_at remains nullable
- user_id FK uses `ON DELETE CASCADE`
- last_login_terminal_id FK uses `ON DELETE SET NULL`
- no seed passwords
- no real secrets
- no required blocking fixes
- next allowed step: Migration File Creation

## Migration File Audit Status

- final verdict: PASS
- migration file approved
- file path: `supabase/migrations/20260505110000_module01_user_auth.sql`
- no required fixes
- next allowed step: Module 01 User Auth Remote Apply Execution Plan
