# MODULE 01 USER SESSION DATA MODEL EXTENSION PLAN

## Status
DOC ONLY / DATA MODEL PLANNING / NO SQL

## Purpose
Define planned data model extension for storing opaque user sessions in Module 01.

## Source Decisions
Reference:
- Corporate Email Authorization Doctrine
- API Auth Endpoint Plan
- API Auth Endpoint Data Contract Plan
- Multi-Role Authorization Addendum

Key decisions:
- opaque session token for MVP
- API stores only session_token_hash
- GAS stores only raw session_token in UserProperties
- terminal binding required
- refresh_menu on onOpen required
- logout revokes session
- no cookies as primary mechanism
- JWT deferred

## Why Session Table Is Required

The login/refresh/logout endpoints require persisted session state.

Without `module01_user_sessions`, API cannot:
- validate opaque session tokens
- revoke sessions
- bind sessions to terminals
- expire sessions
- update `last_seen_at`
- enforce logout
- detect terminal-token mismatch
- audit session lifecycle properly

Therefore API Auth Endpoint Implementation is blocked until session data model is planned and migrated.

## Recommended Table
Create future table:
`public.module01_user_sessions`

## Planned Fields

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
- ip_hash text
- user_agent_hash text
- metadata jsonb

Do not implement fields in this task.

## Field Doctrine

### session_token_hash
Stores only hash of raw opaque session token.
Raw token is returned to GAS only once during login.
Raw token is never stored in DB or logs.

### token_algorithm
Stores hash/derivation algorithm used for session token hash.
Example planned values:
- SHA256
- HMAC_SHA256

Exact choice deferred to API implementation/security plan.

### terminal_id
Session is bound to one terminal.
Every authenticated request must include `X-EDS-Terminal-ID` / `spreadsheet_id`.
If request terminal does not match session-bound terminal:
- revoke session
- return `AUTH_SESSION_INVALID`
- audit `SESSION_TERMINAL_MISMATCH`

### expires_at
Session expiration timestamp.
MVP should define a finite expiration period.
Exact TTL deferred to API Auth Endpoint Implementation Plan.

### revoked_at
If not null, session is invalid.

### last_seen_at
Updated by API on successful authenticated requests or `refresh_menu`.
Exact update policy deferred to API implementation.

### client_type
Expected initial value:
- GAS

### ip_hash / user_agent_hash
Optional future security telemetry.
Store hashes only if used.
No raw IP/user-agent required in MVP unless separately approved.

## Constraints

Planned constraints:
- session_token_hash not empty
- token_algorithm not empty
- client_type not empty
- expires_at > created_at
- revoked_at is null or revoked_at >= created_at
- last_seen_at is null or last_seen_at >= created_at

Recommended:
- partial unique index on session_token_hash where revoked_at is null
or
- unique session_token_hash globally

Decision needed for Gemini:
Should session_token_hash be globally unique or partial unique for active sessions only?

## Indexes

Planned indexes:
- user_id
- terminal_id
- expires_at
- revoked_at
- last_seen_at
- session_token_hash lookup index
- maybe composite index (user_id, terminal_id)
- maybe active sessions index where revoked_at is null and expires_at > now() is not directly index-stable, so avoid volatile now() in index predicate

## Session Lifecycle

### Login
1. User provides corporate email, password, spreadsheet_id.
2. API validates user/password/terminal/roles.
3. API generates high-entropy opaque token.
4. API hashes token.
5. API creates `module01_user_sessions` row.
6. API returns raw session_token to GAS once.
7. GAS stores token in UserProperties.

### Refresh Menu / onOpen
1. GAS sends `Authorization: Bearer session_token`.
2. GAS sends `X-EDS-Terminal-ID = spreadsheet_id`.
3. API validates session token hash.
4. API checks `expires_at`/`revoked_at`.
5. API checks terminal binding.
6. API checks current user status and roles.
7. API returns current `permissions[]` and `menu_schema`.

### Logout
1. GAS sends token and terminal header.
2. API sets `revoked_at = now()`.
3. API sets `revoked_reason = USER_LOGOUT`.
4. GAS deletes local token and menu cache.

### Terminal Mismatch
If valid token is presented from different terminal:
- set `revoked_at = now()`
- `revoked_reason = TERMINAL_MISMATCH`
- return `AUTH_SESSION_INVALID`
- audit event

## Audit Requirements

Use existing `module01_audit_events`.

Session-related events:
- SESSION_CREATED
- SESSION_REFRESHED
- SESSION_REVOKED
- SESSION_EXPIRED if explicitly processed
- SESSION_TERMINAL_MISMATCH
- LOGOUT

Audit metadata should include:
- user_id
- terminal_id
- session_id if safe
- request_id
- client_type
- error_code
- no raw session token
- no session_token_hash unless specifically approved

## Security Guardrails

Forbidden:
- store raw session token in DB
- log raw session token
- send token in URL
- use cookies as primary mechanism
- use JWT as MVP default
- allow token reuse across terminals
- keep session valid after terminal mismatch
- store service keys or secrets

Required:
- high-entropy token
- token hash only in DB
- terminal-bound session
- expiration
- revocation
- API-side validation on every authenticated request

## Relation To Existing Data Model

Depends on:
- module01_users
- module01_user_terminals

Supports:
- API Auth Endpoint Plan
- refresh_menu
- logout
- role-aware menu refresh
- future admin session management

Does not change:
- module01_user_auth
- module01_users
- module01_roles
- module01_user_roles

## Open Questions For Gemini

1. Should session_token_hash be globally unique or partial unique for active sessions only?
2. Should terminal_id use ON DELETE CASCADE or ON DELETE SET NULL?
3. Should user_id use ON DELETE CASCADE?
4. Should token_algorithm be strict CHECK values?
5. Should metadata jsonb be included in MVP or deferred?
6. Should ip_hash/user_agent_hash be included in MVP or deferred?
7. What initial session TTL is recommended: 8 hours, 12 hours, 24 hours?
8. Should only one active session per user+terminal be allowed, or multiple sessions?
9. Should login revoke old active sessions for same user+terminal?

## Recommended Next Step

Gemini audit of User Session Data Model Extension Plan.

If PASS:
Create User Session SQL/Migration Plan.

## Gemini Audit Status

- final verdict: PASS
- plan status: CLOSED / APPROVED
- `module01_user_sessions` data model accepted
- `session_token_hash` must be globally UNIQUE
- `terminal_id` FK: `ON DELETE CASCADE` for MVP
- `user_id` FK: `ON DELETE CASCADE`
- `token_algorithm` strict CHECK values accepted: `SHA256`, `HMAC_SHA256`
- `metadata jsonb` deferred
- `ip_hash` deferred
- `user_agent_hash` deferred
- initial session TTL recommended: 12 hours
- multiple active sessions per user+terminal allowed
- old sessions older than 24 hours should be revoked/cleaned by future API logic
- cleanup of expired/revoked sessions must be planned later
- no required blocking fixes
- next allowed step: User Session SQL/Migration Plan
