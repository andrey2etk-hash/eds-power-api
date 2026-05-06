# MODULE 01 AUTH TEST USER PROVISIONING PLAN

## Objective
Define how the first controlled test user will be prepared for future Module 01 Auth login validation.

## Scope
Planning only.
No database writes.
No SQL execution.
No password hash generation execution.
No API implementation.

## Test User Profile

Define planned test identity:

- email: test.auth@eds.local
- display_name: Test Auth User
- status: ACTIVE
- role: TEST_OPERATOR or BASIC_USER
- purpose: controlled login/auth smoke testing only

Note:
This is a test identity, not a real employee account.

## Required Tables

Plan future records for:

- module01_users
- module01_user_auth
- module01_user_roles
- module01_terminal_bindings or equivalent if already defined in repo

If exact table names differ, record:
TABLE NAME CONFIRMATION REQUIRED BEFORE SQL.

## Password Hash Plan

Define future hash generation method:

- use already verified auth dependency
- preferred algorithm must be selected explicitly before execution:
  - argon2id via argon2-cffi
  - bcrypt as fallback only if approved

Do NOT generate hash in this task.

## Spreadsheet / Terminal Binding Plan

Define required future field:

- spreadsheet_id
- terminal_type
- binding_status
- user_email or user_id link

Record:
Actual spreadsheet_id must be provided/approved before provisioning.

## Future SQL Plan

Create SQL as PLANNED / NOT EXECUTED only.

Include placeholder SQL block with obvious placeholders:

```sql
-- DO NOT EXECUTE
-- PLANNING ONLY
-- Values must be confirmed before use

-- module01_users
insert into public.<module01_users_table> (...)
values (...);

-- module01_user_auth
insert into public.<module01_user_auth_table> (...)
values (...);

-- module01_user_roles
insert into public.<module01_user_roles_table> (...)
values (...);

-- terminal binding table (if applicable)
insert into public.<module01_terminal_binding_table> (...)
values (...);
```

Required inserts conceptually:
- module01_users
- module01_user_auth
- module01_user_roles
- terminal binding table if applicable

## Safety Rules

- No real password in repo
- No password hash in repo unless explicitly approved as test-only artifact
- No real employee personal data
- No production role assignment
- No Render secret changes
- No Supabase write until explicit execution task

## Open Questions

- exact table names confirmed?
- role enum confirmed?
- terminal binding table confirmed?
- password algorithm selected?
- test email approved?
- spreadsheet_id approved?

## Finalization Status

### Table Name Confirmation

CONFIRMED:
- module01_users
- module01_user_auth
- module01_user_roles
- module01_user_terminals

### Role Confirmation

- planned_role_code: TEST_OPERATOR
- role_id: PENDING_DB_CREATION_OR_LOOKUP

### Spreadsheet Terminal Confirmation

- spreadsheet_id: 17JWfDwXQM5S_8uiGFM3C88hUDae_c2cg0LrbWEodZTU
- note: TEST_OPERATOR is doc-defined only and not yet created in DB.
- note: Spreadsheet ID was provided by user and recorded as test terminal input only. No terminal binding was created in DB.

## Provisioning Execution Gate

Provisioning execution is blocked until all are confirmed:

- table names confirmed
- role code confirmed
- role_id confirmed or documented as lookup-required
- spreadsheet_id provided by user
- password algorithm confirmed
- hash generation method approved
- SQL execution task separately approved

Status:

PROVISIONING_EXECUTION_BLOCKED_PENDING_FINAL_INPUTS

## Success Condition

Plan is ready for Gemini audit and later controlled provisioning execution.

## Failure Condition

Any SQL executed or hash generated during this planning task.

## Verdict

PLANNED / FINAL INPUTS PENDING / EXECUTION BLOCKED
