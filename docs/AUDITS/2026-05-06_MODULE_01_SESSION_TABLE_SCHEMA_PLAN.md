# MODULE 01 SESSION TABLE SCHEMA PLAN

## Objective
Define planned database schema for Module 01 DB-backed auth sessions.

## Context
DB Session was selected as MVP session strategy because it supports:
- session revocation
- active session visibility
- user_id binding
- terminal_id binding
- auditability
- governance-first auth control

## Proposed Table Name
module01_user_sessions

## Purpose
Store active and historical auth sessions for Module 01 / Sakura.

## Proposed Columns

Required:

- id uuid primary key
- user_id uuid not null
- terminal_id uuid not null
- session_token_hash text not null
- issued_at timestamptz not null default now()
- expires_at timestamptz not null
- revoked_at timestamptz null
- last_seen_at timestamptz null
- created_at timestamptz not null default now()
- updated_at timestamptz not null default now()

Recommended optional:

- client_type text null
- user_agent_hash text null
- ip_hash text null
- revoke_reason text null

## Foreign Keys

- user_id -> module01_users.id
- terminal_id -> module01_user_terminals.id

## Indexes

Required:
- index on user_id
- index on terminal_id
- index on session_token_hash
- index on expires_at
- index on revoked_at

Recommended:
- composite index on user_id, revoked_at, expires_at
- composite index on terminal_id, revoked_at, expires_at

## Session Token Storage Rule

Raw session token must never be stored in DB.

Only store:
session_token_hash

Raw token may be returned once to client after login.
It must not be logged.

## Session Validity Rule

A session is valid only if:

- session_token_hash matches
- expires_at > now()
- revoked_at is null
- linked user is ACTIVE
- linked terminal is ACTIVE
- linked role assignment is active where required

## Session Revocation Rule

Revocation sets:

- revoked_at = now()
- revoke_reason = reason if column exists

Do not delete active/history sessions for normal logout.
Deletion only allowed for cleanup policy later.

## TTL Rule

Session TTL is controlled by:
AUTH_SESSION_TTL_HOURS

Default MVP:
12 hours

## RLS / Access Rule

Session table must not be exposed to GAS/client.

Only backend/API may:
- create session
- validate session
- revoke session

## Audit Considerations

Session events that should be auditable:
- login success
- login failure
- session issued
- session validated
- session expired
- session revoked

Audit table is not created in this task.
Record as future/adjacent requirement.

## Open Questions

- Should client_type be included now or deferred?
- Should ip_hash / user_agent_hash be included now or deferred?
- Should revoke_reason be included now?
- Should session cleanup policy be defined now?
- Should failed login events be stored in separate audit table?
- Should session_token_hash be unique?

## Recommended MVP Decision

Include:
- id
- user_id
- terminal_id
- session_token_hash
- issued_at
- expires_at
- revoked_at
- last_seen_at
- created_at
- updated_at

Defer:
- client_type
- user_agent_hash
- ip_hash
- revoke_reason

But record them as future migration candidates.

## Implementation Gate

Before auth implementation:
- Gemini audit of this schema plan
- SQL creation plan
- Manual DB Bridge execution
- verification SELECT
- update auth implementation plan with actual session table name/columns

## Boundary Confirmation

Confirm:
- no SQL executed
- no DB writes
- no table created
- no API implementation
- no GAS changes
- no Render changes
- no secrets used

## Verdict
SESSION_TABLE_SCHEMA_PLAN_PREPARED / PENDING_GEMINI_AUDIT
