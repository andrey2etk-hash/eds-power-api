# MODULE 01 AUDIT EVENT DATA CONTRACT PLAN

## Status
DOC ONLY / DATA CONTRACT PLANNING / NO IMPLEMENTATION

## Purpose
Define how Module 01 authorization endpoints will write audit events into `public.module01_audit_events`.

## Existing Audit Table

Known columns:
- id
- entity_type
- entity_id
- event_type
- actor_user_id
- event_at
- request_id uuid
- source_client
- metadata jsonb

No schema change in this plan.

## Source Principles

Audit events must support:
- login
- refresh_menu
- logout
- terminal mismatch
- session revocation
- failed credentials
- locked/disabled users
- no-active-role state

Audit events must not contain:
- password
- password_hash
- raw session_token
- session_token_hash
- reset_token
- reset_token_hash
- Supabase service keys
- secrets
- full connection strings

## request_id Policy

Because `module01_audit_events.request_id` is uuid:
- API must accept `request_id` only if it is valid UUID.
- If client provides no `request_id`, API generates UUID server-side.
- If client provides invalid `request_id`:
  - do not write invalid value into `request_id`
  - generate new server UUID
  - store original invalid request id only in `metadata.client_request_id_raw` if safe and non-secret
  - or drop it entirely if unsafe
- API responses should return the effective UUID `request_id` in `metadata.request_id`.

GAS should generate UUID if possible later, but API remains final authority.

## source_client Policy

Expected initial value:
- GAS

Mapping:
- `X-EDS-Client-Type` header maps to `source_client`.

If missing:
- `source_client = UNKNOWN` or request rejected depending endpoint policy.

Recommended MVP:
- require `X-EDS-Client-Type = GAS` for auth endpoints.

## entity_type / entity_id Policy

Recommended entity mapping:

### LOGIN_SUCCESS
- entity_type = USER
- entity_id = user_id
- actor_user_id = user_id

### LOGIN_FAILED
If user known:
- entity_type = USER
- entity_id = user_id
- actor_user_id = user_id or null

If user unknown:
- entity_type = AUTH
- entity_id = null
- actor_user_id = null

### SESSION_CREATED
- entity_type = SESSION
- entity_id = session_id
- actor_user_id = user_id

### SESSION_REFRESHED
- entity_type = SESSION
- entity_id = session_id
- actor_user_id = user_id

### SESSION_REVOKED
- entity_type = SESSION
- entity_id = session_id
- actor_user_id = user_id

### SESSION_TERMINAL_MISMATCH
- entity_type = SESSION
- entity_id = session_id
- actor_user_id = user_id

### LOGOUT
- entity_type = SESSION
- entity_id = session_id
- actor_user_id = user_id

### AUTH_NO_ACTIVE_ROLES
- entity_type = USER
- entity_id = user_id
- actor_user_id = user_id

### AUTH_USER_DISABLED
- entity_type = USER
- entity_id = user_id
- actor_user_id = user_id

### AUTH_USER_LOCKED
- entity_type = USER
- entity_id = user_id
- actor_user_id = user_id

## Event Types

Allowed auth event types for MVP:
- LOGIN_SUCCESS
- LOGIN_FAILED
- SESSION_CREATED
- SESSION_REFRESHED
- SESSION_REVOKED
- SESSION_TERMINAL_MISMATCH
- LOGOUT
- AUTH_NO_ACTIVE_ROLES
- AUTH_USER_DISABLED
- AUTH_USER_LOCKED

Deferred:
- PASSWORD_CHANGED
- PASSWORD_RESET_REQUESTED
- PASSWORD_RESET_COMPLETED
- ADMIN_PASSWORD_RESET
- USER_UNLOCKED

## Metadata Contract

Common metadata fields:
- endpoint
- auth_status
- error_code
- terminal_id
- spreadsheet_id
- roles_count
- permissions_count
- menu_schema_version
- session_expires_at
- revoked_reason
- client_type
- client_request_id_raw only if safe
- failure_stage
- note

Forbidden metadata fields:
- password
- current_password
- new_password
- confirm_password
- password_hash
- session_token
- session_token_hash
- reset_token
- reset_token_hash
- service_role_key
- authorization_header
- full headers dump

## Event-Specific Metadata

### LOGIN_SUCCESS
metadata:
- endpoint = /api/v1/auth/login
- auth_status = AUTHENTICATED or PASSWORD_CHANGE_REQUIRED
- terminal_id
- spreadsheet_id
- roles_count
- permissions_count
- menu_schema_version
- session_expires_at

### LOGIN_FAILED
metadata:
- endpoint = /api/v1/auth/login
- error_code
- failure_stage
- terminal_id if known
- spreadsheet_id if provided
- email_domain optional
- email_hash optional only if separately approved

Do not store full email for unknown users unless separately approved.

### SESSION_CREATED
metadata:
- endpoint = /api/v1/auth/login
- terminal_id
- spreadsheet_id
- session_expires_at
- token_algorithm only if non-sensitive

### SESSION_REFRESHED
metadata:
- endpoint = /api/v1/auth/refresh_menu
- terminal_id
- spreadsheet_id
- roles_count
- permissions_count
- menu_schema_version

### SESSION_TERMINAL_MISMATCH
metadata:
- endpoint
- expected_terminal_id
- provided_spreadsheet_id
- error_code = AUTH_SESSION_INVALID

Do not store raw token.

### SESSION_REVOKED / LOGOUT
metadata:
- endpoint = /api/v1/auth/logout
- revoked_reason
- terminal_id
- spreadsheet_id

## Audit Write Timing

Recommended:
- LOGIN_FAILED: write after enough context is known, but without leaking enumeration.
- LOGIN_SUCCESS: write after session creation succeeds.
- SESSION_CREATED: optional separate event; if emitted, avoid duplicate noise by deciding whether LOGIN_SUCCESS already covers session creation.
- SESSION_REFRESHED: may be emitted on refresh_menu, but consider rate/noise.
- SESSION_TERMINAL_MISMATCH: write after session revocation.
- LOGOUT: write after session revocation.

Open question:
Should LOGIN_SUCCESS and SESSION_CREATED be two events, or one combined event?

## Minimal MVP Event Set

Recommended for first implementation:
- LOGIN_SUCCESS
- LOGIN_FAILED
- SESSION_TERMINAL_MISMATCH
- LOGOUT

Optional later:
- SESSION_REFRESHED
- SESSION_CREATED
- SESSION_REVOKED

Reason:
Avoid excessive audit noise while still capturing critical security events.

## Error Handling For Audit Writes

Audit write failure must not expose internal details to GAS.

Decision needed:
Should audit write failure block auth success?

Recommended:
- LOGIN_SUCCESS: if audit write fails, return success but log server-side warning if available.
- LOGIN_FAILED: best effort.
- SESSION_TERMINAL_MISMATCH: audit should be attempted after revoke; auth response still invalidates session.
- LOGOUT: logout should proceed even if audit write fails.

No implementation in this task.

## Boundary

This plan does not authorize:
- API code
- Python code
- GAS code
- SQL
- DB writes
- schema changes
- dependency installation
- secrets

## Open Questions For Gemini

1. Should LOGIN_SUCCESS and SESSION_CREATED be separate events or combined for MVP?
2. Should SESSION_REFRESHED be emitted on every refresh_menu or only when role/menu changes?
3. Should LOGIN_FAILED store email hash/domain, or avoid email-derived metadata entirely for MVP?
4. Should audit failure block successful auth response?
5. Is source_client = GAS strict enough for MVP?
6. Should client invalid request_id be stored in metadata or dropped?
7. Are event_type names acceptable as listed?

## Recommended Next Step

Gemini audit of this Audit Event Data Contract Plan.

If PASS:
Create one of:
- Auth Dependency/Environment Plan
- Test User Provisioning Plan
- API Auth Slice 1B Implementation Prompt

Recommended:
Auth Dependency/Environment Plan before code.

## Gemini Audit Status

- final verdict: PASS
- plan status: CLOSED / APPROVED
- request_id UUID policy accepted
- if request_id is missing or invalid, API generates server-side UUID
- invalid client request_id should be dropped, not stored in metadata
- LOGIN_SUCCESS and SESSION_CREATED should be combined for MVP
- SESSION_REFRESHED should be optional/throttled (emit on role-permission change or at most once per hour)
- LOGIN_FAILED may store email_domain, not full unknown email
- audit write failure should not block auth response for MVP, but should be logged server-side
- source_client = GAS is acceptable for MVP
- event names accepted as listed
- no required blocking fixes
- next allowed step: Auth Dependency & Environment Plan
