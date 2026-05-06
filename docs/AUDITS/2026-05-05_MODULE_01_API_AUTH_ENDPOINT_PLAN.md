# MODULE 01 API AUTH ENDPOINT PLAN

## Status
DOC ONLY / API PLANNING / NO IMPLEMENTATION

## Purpose
Plan API endpoints required for corporate email + password authorization for Sakura / Module 01 personal Google Sheet terminals.

## Source Doctrines
Reference:
- Corporate Email Authorization Doctrine
- Authorization Data Model Extension Plan
- Multi-Role Authorization Addendum

## API Authority Doctrine
API is the sole authority for:
- identity validation
- password validation
- user status validation
- terminal validation
- role loading
- permission resolution
- menu_schema generation

GAS must not:
- decide authorization locally
- use Google Session email as login proof
- hardcode role hierarchy
- hardcode role-to-menu authority
- store passwords

## Planned Endpoints

### POST /api/v1/auth/login

Purpose:
Authenticate corporate user and return session/menu authorization result.

Request body:
- email
- password
- terminal_id or spreadsheet_id
- client_type = GAS
- request_id optional

Required:
- terminal_id/spreadsheet_id must be provided
- email must be manually entered by user in login modal
- password must be sent only over HTTPS
- password must not be logged

Validation flow:
1. Normalize email.
2. Find user in `module01_users` by corporate email.
3. Check `user.status = ACTIVE`.
4. Load `module01_user_auth` by `user_id`.
5. Check `locked_until`.
6. Verify password against `password_hash`.
7. Check `must_change_password`.
8. Resolve terminal via `module01_user_terminals` using `spreadsheet_id`/`terminal_id`.
9. Confirm terminal is active/allowed/assigned according to policy.
10. Load all active roles through `module01_user_roles`.
11. Resolve additive permission set.
12. Generate `menu_schema`.
13. Audit `LOGIN_SUCCESS` or `LOGIN_FAILED`.
14. Return auth response.

Success response must include:
- status = SUCCESS
- user object:
  - user_id
  - email
  - display_name
- roles[]
- permissions[]
- menu_schema
- must_change_password
- terminal:
  - terminal_id
  - spreadsheet_id
  - status
- session metadata if planned
- error = null

Failure response must include:
- status = FAILED
- error_code
- message
- source_field if applicable
- no password details
- no password_hash
- no reset_token_hash

Possible error codes:
- AUTH_EMAIL_NOT_FOUND
- AUTH_INVALID_PASSWORD
- AUTH_USER_DISABLED
- AUTH_USER_LOCKED
- AUTH_PASSWORD_CHANGE_REQUIRED
- AUTH_TERMINAL_REQUIRED
- AUTH_TERMINAL_NOT_FOUND
- AUTH_TERMINAL_NOT_ASSIGNED
- AUTH_NO_ACTIVE_ROLES
- AUTH_INTERNAL_ERROR

### POST /api/v1/auth/logout

Purpose:
Allow GAS terminal to clear local session/menu state.

Request:
- user_id or session token if future sessions exist
- terminal_id/spreadsheet_id
- request_id

Response:
- status = SUCCESS
- local_clear_required = true

### POST /api/v1/auth/change_password

Purpose:
Allow authenticated user to change password.

Request:
- email or user_id
- current_password
- new_password
- confirm_password
- terminal_id/spreadsheet_id

Validation:
- current password must be valid
- new password must meet policy
- update password_hash
- update password_updated_at
- set must_change_password = false
- reset failed_login_attempts
- audit PASSWORD_CHANGED

No implementation in this task.

### POST /api/v1/auth/request_password_reset

Purpose:
Request password reset through corporate email.

Request:
- email

Behavior:
- if user exists and active, generate reset token and send email
- response should not reveal whether email exists if security policy requires
- store reset_token_hash only
- never store raw token

No email implementation in this task.

### POST /api/v1/auth/admin_reset_password

Purpose:
Allow admin to reset user password or force password change.

Requires:
- admin role/permission
- target user id/email
- audit ADMIN_PASSWORD_RESET

No implementation in this task.

## Permission Resolution Doctrine

API must resolve permissions from all active roles.

Rule:
- permissions are additive by default
- final permissions = union of permissions from all active roles
- duplicates removed server-side
- DIRECTOR is not automatic all-access
- if user needs multiple functional abilities, assign multiple roles

Future possible conflict logic:
- explicit deny not active in MVP
- if introduced later, must be separately audited

## Menu Schema Doctrine

API returns menu_schema to GAS.

GAS renders menu_schema only.

menu_schema should include:
- menu_group_id
- label
- action_id
- enabled
- order
- optional tooltip
- optional required_permission

GAS must not decide:
- whether user is allowed
- which role maps to which menu item
- whether DIRECTOR includes other role actions

## Terminal Enforcement

Request must include:
- spreadsheet_id from Google Sheet terminal
or
- terminal_id if already known

API resolves terminal through `module01_user_terminals`.

If terminal is unknown:
- return AUTH_TERMINAL_NOT_FOUND or AUTH_TERMINAL_NOT_ASSIGNED according to policy
- do not authorize

Google Session email must not be used as terminal/user proof.

## Session / Menu Revalidation

onOpen in GAS should call API or require re-auth according to future session model.

API plan should support:
- refresh authorization/menu
- returning updated menu_schema
- invalidating stale menus

A future endpoint may be:
`POST /api/v1/auth/refresh_menu`

No implementation in this task.

## Audit Requirements

Use `module01_audit_events` for:
- LOGIN_SUCCESS
- LOGIN_FAILED
- LOGOUT
- PASSWORD_CHANGED
- PASSWORD_RESET_REQUESTED
- PASSWORD_RESET_COMPLETED
- ADMIN_PASSWORD_RESET
- USER_LOCKED
- USER_UNLOCKED
- MENU_REFRESHED if needed

Audit metadata:
- actor_user_id if known
- target_user_id if relevant
- terminal_id if known
- spreadsheet_id if useful
- client_type = GAS
- request_id
- error_code if failed
- no secrets
- no passwords
- no password hashes
- no reset tokens

## Security Requirements

Forbidden:
- log raw passwords
- return password_hash
- return reset_token_hash
- store raw reset tokens
- use Google Session email as auth proof
- allow self-registration
- authorize without terminal_id/spreadsheet_id
- authorize from GAS-only logic
- hardcode role-to-menu access in GAS

Required:
- HTTPS only
- API-side password verification
- API-side permission resolution
- API-side menu_schema generation
- failed login counter
- lockout handling
- no secrets in logs

## Data Dependencies

API will read:
- module01_users
- module01_user_auth
- module01_user_roles
- module01_roles
- module01_user_terminals

API will write future audit events:
- module01_audit_events

API may update:
- module01_user_auth failed_login_attempts
- locked_until
- last_login_at
- last_login_terminal_id
- password_hash when password changes
- reset_token_hash/reset_token_expires_at during reset flow

No implementation in this task.

## Boundary

This plan does not authorize:
- API code
- GAS code
- Python code
- SQL migration
- DB writes
- password hashing implementation
- email sending implementation
- UI implementation
- production deployment

## Open Questions For Gemini

1. Should login endpoint return a session token, or should MVP be stateless with per-action revalidation?
2. Should `AUTH_PASSWORD_CHANGE_REQUIRED` be a failure status or success-with-required-action status?
3. Should terminal enforcement require pre-assigned terminal only, or allow first-login terminal claim by admin policy?
4. Should API return `permissions[]` and `menu_schema`, or only `menu_schema`?
5. Should failed login counter increment before or after terminal validation?
6. Should password reset reveal email existence or always return neutral message?
7. Should `refresh_menu` be separate endpoint or part of login response only?

## Recommended Next Step

Gemini audit of API Auth Endpoint Plan.

If PASS:
Create API Auth Endpoint Data Contract Plan or API Implementation Slice Plan.

Recommended next after PASS:
API Auth Endpoint Data Contract Plan.

## Gemini Audit Status

- final verdict: PASS
- plan status: CLOSED / APPROVED
- endpoint scope accepted (`login`, `logout`, `change_password`, `request_password_reset`, `admin_reset_password`)
- terminal enforcement doctrine accepted (`terminal_id` / `spreadsheet_id`)
- additive multi-role permission resolution accepted
- API-generated `menu_schema` doctrine accepted
- next allowed step: API Auth Endpoint Data Contract Plan
