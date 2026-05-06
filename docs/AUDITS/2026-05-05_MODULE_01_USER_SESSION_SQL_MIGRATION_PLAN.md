# MODULE 01 USER SESSION SQL/MIGRATION PLAN

## Status
DOC ONLY / SQL-MIGRATION PLANNING / NO EXECUTION

## Purpose
Plan a future Supabase migration to add `public.module01_user_sessions` for stateful opaque session token authorization.

## Source Decisions
Reference:
- User Session Data Model Extension Plan
- API Auth Endpoint Data Contract Plan
- Corporate Email Authorization Doctrine

Gemini-approved decisions:
- session_token_hash globally UNIQUE
- terminal_id FK ON DELETE CASCADE for MVP
- user_id FK ON DELETE CASCADE
- token_algorithm strict CHECK in ('SHA256', 'HMAC_SHA256')
- metadata/ip_hash/user_agent_hash deferred
- initial session TTL = 12 hours as API policy, not DB default unless separately approved
- multiple active sessions per user+terminal allowed
- cleanup/revoke of sessions older than 24 hours handled by future API logic

## Scope
Create one new table:
- public.module01_user_sessions

No API/GAS implementation.
No session token generation implementation.
No seed sessions.
No real secrets.

## Proposed Migration File Name
Propose:
`supabase/migrations/20260505120000_module01_user_sessions.sql`

Note:
Exact timestamp may be adjusted by operator before migration file creation.

## Table: module01_user_sessions

Planned fields:
- id uuid primary key default gen_random_uuid()
- user_id uuid not null references public.module01_users(id) on delete cascade
- terminal_id uuid not null references public.module01_user_terminals(id) on delete cascade
- session_token_hash text not null
- token_algorithm text not null
- created_at timestamptz not null default now()
- expires_at timestamptz not null
- revoked_at timestamptz
- last_seen_at timestamptz
- client_type text not null
- created_request_id text
- revoked_request_id text
- revoked_reason text

Deferred fields:
- ip_hash
- user_agent_hash
- metadata jsonb

## Constraints

Required constraints:
- unique(session_token_hash)
- session_token_hash not empty
- token_algorithm in ('SHA256', 'HMAC_SHA256')
- token_algorithm not empty
- client_type not empty
- expires_at > created_at
- revoked_at is null or revoked_at >= created_at
- last_seen_at is null or last_seen_at >= created_at

Optional but recommended:
- check client_type in ('GAS')

Decision:
For MVP, use strict client_type check:
client_type in ('GAS')

## Indexes

Required indexes:
- module01_user_sessions_user_id_idx
- module01_user_sessions_terminal_id_idx
- module01_user_sessions_expires_at_idx
- module01_user_sessions_revoked_at_idx
- module01_user_sessions_last_seen_at_idx
- module01_user_sessions_user_terminal_idx on (user_id, terminal_id)

session_token_hash already has unique index/constraint.

Avoid volatile partial index using now().

## No Seed Sessions

Migration must not insert:
- session rows
- raw tokens
- token hashes
- real users
- secrets

## updated_at Decision

No updated_at field is planned for sessions.

Reason:
Session lifecycle is represented by created_at, expires_at, revoked_at, last_seen_at.
Avoid introducing updated_at trigger behavior.

## Expiration / Cleanup

DB does not enforce TTL by default.
API creates expires_at based on 12-hour policy.
Future API cleanup/revoke logic handles sessions older than 24 hours.

No scheduled cleanup implementation in this migration.

## Terminal Binding Enforcement

DB stores terminal_id.
API must enforce:
- request X-EDS-Terminal-ID matches session terminal.
- mismatch revokes session and returns AUTH_SESSION_INVALID.

DB migration only supports this; it does not implement API behavior.

## Audit Integration

No new audit table.
Use existing:
- public.module01_audit_events

Future events:
- SESSION_CREATED
- SESSION_REFRESHED
- SESSION_REVOKED
- SESSION_TERMINAL_MISMATCH
- LOGOUT

No audit implementation in this migration.

## Verification Plan

After future migration execution, verify:

1. Table exists:
`public.module01_user_sessions`

2. Columns exist:
all planned fields.

3. Constraints exist:
- PK
- FK user_id
- FK terminal_id
- unique session_token_hash
- token_algorithm check
- client_type check
- time checks

4. Indexes exist:
planned indexes.

5. No rows seeded:
`select count(*) = 0`

6. Existing Module 01 tables remain present:
- module01_users
- module01_user_auth
- module01_user_terminals

7. No secrets present.

## Boundary

This plan does not authorize:
- migration file creation
- SQL execution
- DB writes
- API implementation
- GAS implementation
- session token generation
- production deployment

## Open Questions For Gemini

1. Should client_type be strict check ('GAS') or broad text for future clients?
2. Should expires_at > created_at be enforced by DB, or only by API?
3. Should last_seen_at be nullable initially?
4. Should multiple active sessions per user+terminal remain allowed with no uniqueness constraint?
5. Should revoked_reason be constrained to known values?
6. Should created_request_id / revoked_request_id have indexes?
7. Is deferring ip_hash/user_agent_hash/metadata acceptable for MVP?

## Recommended Next Step

Gemini audit of this SQL/Migration Plan.

If PASS:
Create migration file:
`supabase/migrations/20260505120000_module01_user_sessions.sql`

## Gemini Audit Status

- final verdict: PASS
- plan status: CLOSED / APPROVED
- `module01_user_sessions` SQL/migration plan accepted
- `session_token_hash` globally UNIQUE
- `user_id` FK `ON DELETE CASCADE`
- `terminal_id` FK `ON DELETE CASCADE`
- `token_algorithm` strict CHECK accepted: `SHA256`, `HMAC_SHA256`
- `client_type` strict CHECK accepted: `GAS`
- `expires_at > created_at` enforced at DB level
- `last_seen_at` nullable
- multiple active sessions per user+terminal allowed
- `revoked_reason` remains broad text for MVP
- no `request_id` indexes for MVP
- `ip_hash` / `user_agent_hash` / `metadata` deferred
- no required blocking fixes
- next allowed step: Migration File Creation

## Migration File Audit Status

- final verdict: PASS
- migration file approved
- file path: `supabase/migrations/20260505120000_module01_user_sessions.sql`
- no required fixes
- next allowed step: Module 01 User Session Remote Apply Execution Plan
