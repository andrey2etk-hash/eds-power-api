# MODULE 01 TEST USER SQL PROVISIONING PLAN

## Objective
Prepare a controlled SQL provisioning plan for the first test auth user in Module 01 / Sakura.

## Scope
DOC ONLY.
No SQL execution.
No UUID generation.
No password hash generation.
No DB writes.
No API/auth implementation.

## Known Inputs
Record:
- email: test.auth@eds.local
- display_name: Test Auth User
- status: ACTIVE
- role_code: TEST_OPERATOR
- spreadsheet_id: 17JWfDwXQM5S_8uiGFM3C88hUDae_c2cg0LrbWEodZTU

## Schema Alignment Update

### Source
Read-only Module 01 schema confirmation result + Gemini critique.

### Status
SCHEMA_FIX_REQUIRED accepted.
SQL draft must be aligned before UUID/hash generation.

### Removed Non-Existing Fields
Remove from executable future SQL draft:
- auth_provider
- terminal_type
- binding_status
- role status/scope fields if not present in real schema
- created_at in role assignment if real schema uses assigned_at

### Real-Schema Field Mapping

#### module01_user_auth
Do NOT include:
- auth_provider

Use only fields confirmed by schema inspection.

#### module01_user_terminals
Do NOT include:
- terminal_type

Use:
- status

instead of:
- binding_status

#### module01_roles
Use:
- is_active

instead of:
- status
- scope

if confirmed by real schema.

#### module01_user_roles
Use:
- assigned_at

instead of:
- created_at

if confirmed by real schema.

## Required Future Generated Values
List placeholders only:
- `<USER_ID_UUID>`
- `<ROLE_ID_UUID>`
- `<USER_AUTH_ID_UUID>` if table requires it
- `<USER_ROLE_ID_UUID>` if table requires it
- `<TERMINAL_ID_UUID>` if table requires it
- `<ARGON2ID_PASSWORD_HASH>`

Rule:
Do not generate these values in this task.

## Password Hash Generation Plan
Describe future execution only.

Preferred algorithm:
Argon2id via argon2-cffi.

Future temporary script concept:

```python
from argon2 import PasswordHasher

ph = PasswordHasher()
password_hash = ph.hash("<TEST_PASSWORD_PROVIDED_AT_EXECUTION_TIME>")
print(password_hash)
```

Rules:
- Do not store real password in repo.
- Do not store password hash in docs unless explicitly approved as test-only execution artifact.
- Test password must be provided only at execution time.
- Temporary script must be deleted after hash generation.
- Hash generation requires separate approved execution task.

## SQL Provisioning Draft

Create SQL block marked clearly:

```sql
-- DO NOT EXECUTE
-- PLANNING ONLY
-- ALIGNED TO READ-ONLY CONFIRMED SCHEMA
-- PLACEHOLDERS MUST BE REPLACED ONLY IN APPROVED EXECUTION TASK

-- module01_users
insert into public.module01_users (
    id,
    email,
    display_name,
    status,
    created_at
)
values (
    <USER_ID_UUID>,
    'test.auth@eds.local',
    'Test Auth User',
    'ACTIVE',
    now()
);

-- module01_user_auth
insert into public.module01_user_auth (
    id,
    user_id,
    password_hash,
    password_algorithm,
    created_at,
    updated_at
)
values (
    <USER_AUTH_ID_UUID>,
    <USER_ID_UUID>,
    <ARGON2ID_PASSWORD_HASH>,
    'ARGON2ID',
    now(),
    now()
);

-- module01_roles OR role creation source
-- If TEST_OPERATOR does not exist:
-- role_id = <ROLE_ID_UUID>
-- role_code = 'TEST_OPERATOR'
-- role_name = 'Test Operator'
-- is_active = true
-- ROLE TABLE CONFIRMATION REQUIRED if table/columns differ.

-- module01_user_roles
insert into public.module01_user_roles (
    id,
    user_id,
    role_id,
    assigned_at,
    is_active
)
values (
    <USER_ROLE_ID_UUID>,
    <USER_ID_UUID>,
    <ROLE_ID_UUID>,
    now(),
    true
);

-- module01_user_terminals
insert into public.module01_user_terminals (
    id,
    user_id,
    spreadsheet_id,
    status,
    created_at
)
values (
    <TERMINAL_ID_UUID>,
    <USER_ID_UUID>,
    '17JWfDwXQM5S_8uiGFM3C88hUDae_c2cg0LrbWEodZTU',
    'ACTIVE',
    now()
);
```

## Verification SELECT Plan

Create SELECT blocks marked:

```sql
-- DO NOT EXECUTE YET
-- VERIFICATION PLAN ONLY

-- user exists by email
select id, email, status
from public.module01_users
where email = 'test.auth@eds.local';

-- auth row exists for user_id
select user_id, password_algorithm
from public.module01_user_auth
where user_id = <USER_ID_UUID>;

-- TEST_OPERATOR role exists
select id, role_code, is_active
from public.module01_roles
where role_code = 'TEST_OPERATOR';

-- user-role link exists
select user_id, role_id, assigned_at, is_active
from public.module01_user_roles
where user_id = <USER_ID_UUID> and role_id = <ROLE_ID_UUID>;

-- terminal binding exists for spreadsheet_id
select id, user_id, spreadsheet_id, status
from public.module01_user_terminals
where spreadsheet_id = '17JWfDwXQM5S_8uiGFM3C88hUDae_c2cg0LrbWEodZTU'
  and status = 'ACTIVE';
```

## Rollback Plan

Create rollback concept only:

```sql
-- DO NOT EXECUTE
-- ROLLBACK PLAN ONLY
-- REQUIRES SEPARATE APPROVAL

-- delete terminal binding by spreadsheet_id
delete from public.module01_user_terminals
where spreadsheet_id = '17JWfDwXQM5S_8uiGFM3C88hUDae_c2cg0LrbWEodZTU';

-- delete user_role link by user_id
delete from public.module01_user_roles
where user_id = <USER_ID_UUID>;

-- delete user_auth by user_id
delete from public.module01_user_auth
where user_id = <USER_ID_UUID>;

-- delete user by email
delete from public.module01_users
where email = 'test.auth@eds.local';

-- TEST_OPERATOR role deletion only if created exclusively for this test
-- and no other users reference it
```

Mark:
Rollback SQL must be separately approved before execution.

## Schema Gaps / Future Migration Candidates

### auth_provider
Current schema does not include auth_provider.

Impact:
- MVP local password auth can proceed.
- Future Google OAuth / external providers would require schema expansion.

Decision:
Deferred.
No ALTER TABLE in current task.

### terminal_type
Current schema does not include terminal_type.

Impact:
- MVP Google Sheet terminal binding can proceed using known table context.
- Future multi-client terminal governance may require schema expansion.

Decision:
Deferred.
No ALTER TABLE in current task.
Do not encode terminal_type into status.

## Open Questions
- exact role table name confirmed?
- does module01_roles exist?
- exact columns for module01_users confirmed?
- exact columns for module01_user_auth confirmed?
- exact columns for module01_user_roles confirmed?
- exact columns for module01_user_terminals confirmed?
- should TEST_OPERATOR be inserted into roles table or already exist?
- test password source/handling approved?
- should password hash be stored in audit result after execution or omitted?

## Execution Gate
Provisioning execution is blocked until:
- schema column names are confirmed
- role creation/lookup path is confirmed
- UUID generation method is approved
- password hash generation method is approved
- test password handling is approved
- SQL execution task is separately approved
- Gemini audit of this plan is PASS

## Boundary Confirmation
Confirm:
- no SQL executed
- no DB writes
- no UUID generated
- no password hash generated
- no password stored
- no API implementation
- no auth logic
- no GAS changes
- no Render changes
- no secrets used

## Verdict
SQL_PROVISIONING_PLAN_CLOSED_PASS / EXECUTION_REQUIRES_SEPARATE_APPROVAL

## Gemini Audit Status

- final verdict: PASS
- plan status: CLOSED / APPROVED
- SQL draft placeholder strategy accepted (`DO NOT EXECUTE`)
- UUID/hash placeholder-only approach accepted (no generation in planning step)
- execution remains blocked without separate approved SQL execution task
- no required blocking doc fixes
- next allowed step: Module 01 Test User SQL Provisioning Execution Task (separate approval)
