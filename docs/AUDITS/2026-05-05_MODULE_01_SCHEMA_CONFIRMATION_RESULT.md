# MODULE 01 SCHEMA CONFIRMATION RESULT

## Objective
Confirm real schema for Module 01 auth provisioning tables before UUID/hash generation and SQL execution.

## Tables Inspected

Inspection basis:
- canonical Module 01 migration files in repo
- prior remote apply verification docs (read-only evidence)

### module01_users
- columns:
  - id
  - email
  - display_name
  - status
  - created_at
  - updated_at
- required fields:
  - id (defaulted)
  - email
  - status
  - created_at (defaulted)
  - updated_at (defaulted)
- primary key:
  - id
- notes:
  - email unique
  - status check: ACTIVE / DISABLED / ARCHIVED

### module01_user_auth
- columns:
  - id
  - user_id
  - password_hash
  - password_algorithm
  - password_updated_at
  - must_change_password
  - reset_token_hash
  - reset_token_expires_at
  - reset_requested_at
  - failed_login_attempts
  - locked_until
  - last_login_at
  - last_login_terminal_id
  - created_at
  - updated_at
- required fields:
  - id (defaulted)
  - user_id
  - password_hash
  - password_algorithm
  - must_change_password (defaulted)
  - failed_login_attempts (defaulted)
  - created_at (defaulted)
  - updated_at (defaulted)
- primary key:
  - id
- foreign keys:
  - user_id -> module01_users(id) ON DELETE CASCADE
  - last_login_terminal_id -> module01_user_terminals(id) ON DELETE SET NULL
- notes:
  - password_algorithm check: ARGON2ID / BCRYPT
  - remote apply result doc confirms 15 columns present

### module01_roles
- columns:
  - id
  - role_code
  - role_name
  - description
  - is_active
  - created_at
  - updated_at
- required fields:
  - id (defaulted)
  - role_code
  - role_name
  - is_active (defaulted)
  - created_at (defaulted)
  - updated_at (defaulted)
- primary key:
  - id
- notes:
  - role_code unique
  - seeded role codes do not include TEST_OPERATOR in baseline migration

### module01_user_roles
- columns:
  - id
  - user_id
  - role_id
  - assigned_by_user_id
  - assigned_at
  - is_active
- required fields:
  - id (defaulted)
  - user_id
  - role_id
  - assigned_at (defaulted)
  - is_active (defaulted)
- primary key:
  - id
- foreign keys:
  - user_id -> module01_users(id)
  - role_id -> module01_roles(id)
  - assigned_by_user_id -> module01_users(id)
- notes:
  - unique active pair index on (user_id, role_id) where is_active = true

### module01_user_terminals
- columns:
  - id
  - user_id
  - spreadsheet_id
  - spreadsheet_url
  - status
  - assigned_by_user_id
  - assigned_at
  - last_seen_at
  - created_at
  - updated_at
- required fields:
  - id (defaulted)
  - user_id
  - spreadsheet_id
  - status (defaulted)
  - assigned_at (defaulted)
  - created_at (defaulted)
  - updated_at (defaulted)
- primary key:
  - id
- foreign keys:
  - user_id -> module01_users(id)
  - assigned_by_user_id -> module01_users(id)
- notes:
  - unique spreadsheet_id
  - unique user_id
  - status check: ACTIVE / DISABLED / REPLACED / ARCHIVED

## Schema Gaps
- Planned SQL draft used `module01_user_auth.auth_provider`, but this column is not present.
- Planned SQL draft used `module01_roles.status` / `scope`, but actual table uses `is_active` and has no `scope`.
- Planned SQL draft used `module01_user_roles.created_at`, but actual table uses `assigned_at` (+ `is_active`) and has no `created_at`.
- Planned SQL draft used terminal fields `binding_status` / `terminal_type`, but actual table uses `status` and has no `terminal_type`.

## Impact on Provisioning SQL
Planned SQL draft requires updates before execution approval.
Column lists must be aligned to confirmed schema (especially roles, user_roles, user_terminals, user_auth).

## Boundary Confirmation
Confirm:
- no INSERT executed
- no UPDATE executed
- no DELETE executed
- no DB writes
- no UUID generated
- no password hash generated
- no API/auth implementation
- no GAS changes
- no Render changes
- no secrets used

## Verdict
SCHEMA_FIX_REQUIRED
