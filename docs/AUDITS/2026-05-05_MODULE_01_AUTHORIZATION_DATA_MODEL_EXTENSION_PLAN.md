# MODULE 01 AUTHORIZATION DATA MODEL EXTENSION PLAN

## Status
DOC ONLY / DATA MODEL PLANNING / NO SQL

## Purpose
Define planned data model extensions required for corporate email + password authentication in Module 01.

## Source Doctrine
Reference:
`docs/AUDITS/2026-05-05_MODULE_01_CORPORATE_EMAIL_AUTHORIZATION_DOCTRINE.md`

Key doctrine decisions:
- corporate email is primary identity
- password required
- self-registration forbidden
- admin provisions users
- API validates credentials and roles
- GAS is thin client
- terminal_id / spreadsheet_id must be included in future login flow

## Current Data Model Baseline
Existing tables:
- `module01_users`
- `module01_roles`
- `module01_user_roles`
- `module01_user_terminals`

Current `module01_users` already contains:
- id
- email
- display_name
- status
- created_at
- updated_at

Current missing auth fields:
- password_hash
- password_updated_at
- must_change_password
- reset_token_hash
- reset_token_expires_at
- failed_login_attempts
- locked_until
- last_login_at
- last_login_terminal_id

## Design Question
Should auth fields be added directly to `module01_users` or separated into `module01_user_auth`?

Analyze both options.

### Option A — Extend `module01_users`
Pros:
- simpler first MVP
- fewer joins
- easier login endpoint
- directly attached to corporate identity

Cons:
- mixes identity profile and auth security data
- harder to isolate sensitive auth fields
- future audit/security logic may become less clean

### Option B — Create `module01_user_auth`
Pros:
- separates user profile from password/security state
- cleaner security boundary
- easier to restrict exposure of auth fields
- supports future SSO/MFA extensions

Cons:
- requires additional table and FK
- slightly more complex login query
- requires careful one-to-one constraint

## Recommended Model
Recommend Option B:
create a separate future table `module01_user_auth` linked one-to-one to `module01_users`.

Reason:
- better security separation
- cleaner future extension
- avoids exposing auth fields through user profile queries
- aligns with enterprise/corporate system discipline

No SQL in this document.

## Planned module01_user_auth Fields

Planned fields:
- id uuid primary key
- user_id uuid not null unique references module01_users(id)
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
- last_login_terminal_id uuid references module01_user_terminals(id)
- created_at timestamptz not null default now()
- updated_at timestamptz not null default now()

Do not implement these fields in this task.

## Password Hashing Doctrine

Password must never be stored as plain text.

Planned principles:
- password_hash only
- password_algorithm must be stored
- prefer modern slow hashing algorithm such as Argon2id or bcrypt
- never log passwords
- never return password_hash to GAS
- never expose reset_token_hash
- password reset tokens must be stored hashed

Exact algorithm selection is deferred to API Auth Endpoint Plan or Security Implementation Plan.

## Admin Provisioning Data Flow

Admin creates user:
1. create module01_users row
2. assign role in module01_user_roles
3. assign personal terminal in module01_user_terminals if needed
4. create auth record with temporary password hash
5. set must_change_password = true

No implementation in this task.

## Login Data Flow Requirements

Future API login must check:
- corporate email exists
- module01_users.status = ACTIVE
- module01_user_auth exists
- password is valid
- user is not locked
- terminal_id / spreadsheet_id is provided
- terminal exists and is active/assigned if terminal enforcement enabled
- user has at least one active role
- API returns permission/menu schema

## Password Change Requirements

User-initiated password change must require:
- current password
- new password
- confirmation
- API validation
- update password_hash
- update password_updated_at
- set must_change_password = false
- reset failed_login_attempts

No implementation in this task.

## Forgot Password / Reset Requirements

Forgot password flow:
- user enters corporate email
- API checks active user
- generate reset token
- store reset_token_hash
- store reset_token_expires_at
- send reset link/code to corporate email
- user sets new password
- clear reset_token_hash and reset_token_expires_at
- update password_updated_at
- set must_change_password = false

No email implementation in this task.

## Admin Reset Requirements

Admin reset must:
- generate temporary password or reset link
- update password_hash or reset token fields
- set must_change_password = true
- clear lockout if needed
- audit admin action in module01_audit_events

No admin UI implementation in this task.

## Lockout / Brute Force Protection

Planned fields:
- failed_login_attempts
- locked_until

Future behavior:
- increment failed_login_attempts on failed login
- reset counter on successful login
- temporary lock after threshold
- exact threshold deferred to API Auth Endpoint Plan

No implementation in this task.

## Terminal Enforcement

Login must include terminal identifier:
- terminal_id or spreadsheet_id

Recommended for GAS:
- send spreadsheet_id from SpreadsheetApp.getActiveSpreadsheet().getId()
- API resolves it through module01_user_terminals
- user must be assigned to that terminal or terminal must be allowed by policy
- Google Session email must not be used as primary identity

Terminal enforcement must be included in API Auth Endpoint Plan.

## Audit Requirements

Future auth actions should be audited in module01_audit_events:
- LOGIN_SUCCESS
- LOGIN_FAILED
- PASSWORD_CHANGED
- PASSWORD_RESET_REQUESTED
- PASSWORD_RESET_COMPLETED
- ADMIN_PASSWORD_RESET
- USER_LOCKED
- USER_UNLOCKED
- LOGOUT if needed

Audit should include:
- actor_user_id if available
- target user if applicable
- terminal_id if available
- source_client
- request_id
- metadata without secrets

## Required Future Migration Scope

Future migration should add:
- module01_user_auth table
- indexes for user_id, reset_token_expires_at, locked_until if needed
- constraints for failed_login_attempts >= 0
- optional password_algorithm check constraint
- no seed passwords
- no real user passwords
- no secrets

Do not create migration in this task.

## Boundary

This document does not authorize:
- SQL migration
- schema changes
- password hashing implementation
- API endpoints
- GAS login modal
- email service
- DB writes
- production deployment

## Next Allowed Step

Authorization Data Model Extension SQL/Migration Plan.

Follow-up planning options:
1. Authorization Data Model Extension SQL/Migration Plan
2. API Auth Endpoint Plan
3. Login Modal UI Plan
4. Role-Aware Menu Plan

Recommended next:
Authorization Data Model Extension SQL/Migration Plan

## Gemini Audit Status

- final verdict: PASS
- plan status: CLOSED / APPROVED
- Option B accepted
- data model fields accepted
- terminal enforcement accepted
- auth audit requirements accepted
- carry-forward notes recorded:
  - `user_id` must keep strict one-to-one uniqueness
  - `last_login_terminal_id` references `module01_user_terminals`
  - API plan must handle login attempt from unregistered/new terminal
  - `reset_token_hash` handling requires care in future SQL plan
  - `password_hash` must never be exposed or logged
- next allowed step: Authorization Data Model Extension SQL/Migration Plan
