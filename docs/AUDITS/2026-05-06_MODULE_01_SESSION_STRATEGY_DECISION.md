# MODULE 01 SESSION STRATEGY DECISION

## Objective
Choose MVP session strategy for Module 01 Auth before implementation.

## Decision
MVP strategy:
DB Session

## Alternatives Considered

### Option A — HMAC Signed Token
Pros:
- fast
- no DB lookup per request
- simple MVP

Cons:
- harder revocation
- weaker active session visibility
- harder terminal/session audit

Status:
DEFERRED

### Option B — DB Session
Pros:
- revocation possible
- active session visibility
- session can bind to user_id and terminal_id
- audit-friendly
- aligns with Sakura governance-first model

Cons:
- requires session table
- requires DB lookup per authenticated action
- requires schema planning

Status:
SELECTED FOR MVP

### Option C — JWT
Status:
DEFERRED
Reason:
Not approved yet; could create premature token complexity.

## Account Enumeration Rule

External API response for login failures should use generic:
AUTH_FAILED

Internal audit may record detailed reason:
- EMAIL_NOT_FOUND
- PASSWORD_INVALID
- USER_INACTIVE
- ACCOUNT_LOCKED
- TERMINAL_NOT_BOUND

Rule:
Do not expose detailed credential failure reason to client.

## Terminal Binding Risk

Current MVP terminal validation relies on:
- spreadsheet_id

Known gap:
- no terminal_type
- no terminal_secret
- no terminal fingerprint

Decision:
Accept spreadsheet_id-only binding for MVP.
Record terminal_secret / fingerprint as future enhancement.

## Required Session Table Plan

Before implementation, create DOC-only plan for session table.

Minimum expected fields:
- id
- user_id
- terminal_id
- session_token_hash or session_handle_hash
- issued_at
- expires_at
- revoked_at
- last_seen_at
- created_at
- updated_at

Do NOT create table in this task.

## Implementation Blockers

Auth implementation remains blocked until:
- session table schema plan is created
- session table SQL migration/provisioning plan is audited
- login response contract updated for DB session
- failed login / lockout policy is defined
- audit logging boundary is defined

## Verdict
DB_SESSION_SELECTED / IMPLEMENTATION_STILL_BLOCKED
