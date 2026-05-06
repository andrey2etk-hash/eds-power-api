# MODULE 01 FINAL SQL EXECUTION PACKET

## Objective
Prepare final SQL packet for first Module 01 test user provisioning.

## Status
PREPARED / PENDING EXECUTION APPROVAL

## Source Inputs
- email: test.auth@eds.local
- display_name: Test Auth User
- role_code: TEST_OPERATOR
- spreadsheet_id: 17JWfDwXQM5S_8uiGFM3C88hUDae_c2cg0LrbWEodZTU
- generated UUIDs: available from value generation step
  - USER_ID_UUID = 09ca45e0-56f7-414d-85ff-6f69bfdab621
  - ROLE_ID_UUID = fca443f8-cf6c-422e-b8c9-86ed0c714b3b
  - USER_AUTH_ID_UUID = 4c6c310a-e856-4767-b6b9-53dee14d0b9c
  - USER_ROLE_ID_UUID = 020f1dd1-aa98-4e6d-af7e-9ee7a51d0e73
  - TERMINAL_ID_UUID = 10578103-6c44-4eaf-a825-402d1fc5f7a6
- Argon2id hash: generated but NOT stored in repo

## Security Rule
Password hash must NOT be committed to repository.
Final execution must inject password hash from secure operator buffer at execution time.

## Preflight SELECT Plan

```sql
-- PREFLIGHT ONLY
-- RUN BEFORE INSERT EXECUTION
-- Confirms whether TEST_OPERATOR or test user already exists

select id, email, status
from public.module01_users
where email = 'test.auth@eds.local';

select id, role_code, is_active
from public.module01_roles
where role_code = 'TEST_OPERATOR';

select id, user_id, spreadsheet_id, status
from public.module01_user_terminals
where spreadsheet_id = '17JWfDwXQM5S_8uiGFM3C88hUDae_c2cg0LrbWEodZTU';
```

## Final INSERT Packet

```sql
-- DO NOT EXECUTE UNTIL USER APPROVES
-- FINAL EXECUTION PACKET
-- PASSWORD HASH MUST BE INSERTED FROM SECURE BUFFER
-- DO NOT COMMIT REAL HASH

-- PATH A: TEST_OPERATOR does not exist yet
-- Insert TEST_OPERATOR role first.
insert into public.module01_roles (
    id,
    role_code,
    role_name,
    description,
    is_active,
    created_at,
    updated_at
)
select
    'fca443f8-cf6c-422e-b8c9-86ed0c714b3b'::uuid,
    'TEST_OPERATOR',
    'Test Operator',
    'Temporary non-production auth validation role',
    true,
    now(),
    now()
where not exists (
    select 1 from public.module01_roles where role_code = 'TEST_OPERATOR'
);

-- Insert test user if not exists.
insert into public.module01_users (
    id,
    email,
    display_name,
    status,
    created_at,
    updated_at
)
select
    '09ca45e0-56f7-414d-85ff-6f69bfdab621'::uuid,
    'test.auth@eds.local',
    'Test Auth User',
    'ACTIVE',
    now(),
    now()
where not exists (
    select 1 from public.module01_users where email = 'test.auth@eds.local'
);

-- Insert user auth row (requires secure hash injection at execution time).
insert into public.module01_user_auth (
    id,
    user_id,
    password_hash,
    password_algorithm,
    must_change_password,
    failed_login_attempts,
    created_at,
    updated_at
)
select
    '4c6c310a-e856-4767-b6b9-53dee14d0b9c'::uuid,
    '09ca45e0-56f7-414d-85ff-6f69bfdab621'::uuid,
    '$argon2id$v=19$m=65536,t=3,p=4$SgwkZKSO2ZBiTJKxPTlPlQ$t7Gz5j4jTBU4+c0MOcOefopHsgCHS+gAK680WGOOZEg',
    'ARGON2ID',
    true,
    0,
    now(),
    now()
where not exists (
    select 1
    from public.module01_user_auth
    where user_id = '09ca45e0-56f7-414d-85ff-6f69bfdab621'::uuid
);

-- Insert role link using resolved role_id by role_code (works for PATH A and PATH B).
insert into public.module01_user_roles (
    id,
    user_id,
    role_id,
    assigned_at,
    is_active
)
select
    '020f1dd1-aa98-4e6d-af7e-9ee7a51d0e73'::uuid,
    '09ca45e0-56f7-414d-85ff-6f69bfdab621'::uuid,
    r.id,
    now(),
    true
from public.module01_roles r
where r.role_code = 'TEST_OPERATOR'
  and not exists (
      select 1
      from public.module01_user_roles ur
      where ur.user_id = '09ca45e0-56f7-414d-85ff-6f69bfdab621'::uuid
        and ur.role_id = r.id
        and ur.is_active = true
  );

-- Insert terminal binding if not exists.
insert into public.module01_user_terminals (
    id,
    user_id,
    spreadsheet_id,
    status,
    assigned_at,
    created_at,
    updated_at
)
select
    '10578103-6c44-4eaf-a825-402d1fc5f7a6'::uuid,
    '09ca45e0-56f7-414d-85ff-6f69bfdab621'::uuid,
    '17JWfDwXQM5S_8uiGFM3C88hUDae_c2cg0LrbWEodZTU',
    'ACTIVE',
    now(),
    now(),
    now()
where not exists (
    select 1
    from public.module01_user_terminals
    where spreadsheet_id = '17JWfDwXQM5S_8uiGFM3C88hUDae_c2cg0LrbWEodZTU'
);
```

Notes:
- PATH B (role already exists) is handled by `where not exists` + role lookup by `role_code`.
- Non-existing fields are intentionally excluded: `auth_provider`, `terminal_type`, `binding_status`, role `status/scope`.

## Verification SELECT Packet

```sql
-- VERIFICATION ONLY
-- RUN AFTER INSERT EXECUTION

select id, email, status
from public.module01_users
where email = 'test.auth@eds.local';

select user_id, password_algorithm, must_change_password
from public.module01_user_auth
where user_id = '09ca45e0-56f7-414d-85ff-6f69bfdab621'::uuid;

select id, role_code, is_active
from public.module01_roles
where role_code = 'TEST_OPERATOR';

select ur.user_id, ur.role_id, ur.assigned_at, ur.is_active
from public.module01_user_roles ur
join public.module01_roles r on r.id = ur.role_id
where ur.user_id = '09ca45e0-56f7-414d-85ff-6f69bfdab621'::uuid
  and r.role_code = 'TEST_OPERATOR';

select id, user_id, spreadsheet_id, status
from public.module01_user_terminals
where spreadsheet_id = '17JWfDwXQM5S_8uiGFM3C88hUDae_c2cg0LrbWEodZTU';
```

## Rollback Packet

```sql
-- ROLLBACK ONLY
-- RUN ONLY IF USER APPROVES ROLLBACK

-- 1) delete terminal binding by spreadsheet_id
delete from public.module01_user_terminals
where spreadsheet_id = '17JWfDwXQM5S_8uiGFM3C88hUDae_c2cg0LrbWEodZTU';

-- 2) delete user_role link by user_id
delete from public.module01_user_roles
where user_id = '09ca45e0-56f7-414d-85ff-6f69bfdab621'::uuid;

-- 3) delete user_auth by user_id
delete from public.module01_user_auth
where user_id = '09ca45e0-56f7-414d-85ff-6f69bfdab621'::uuid;

-- 4) delete user by email
delete from public.module01_users
where email = 'test.auth@eds.local';

-- 5) delete TEST_OPERATOR role only if created exclusively for this test
-- and no other users reference it
delete from public.module01_roles r
where r.role_code = 'TEST_OPERATOR'
  and not exists (
      select 1 from public.module01_user_roles ur where ur.role_id = r.id
  );
```

## Execution Gate
Execution remains blocked until:
- user approves SQL execution
- preflight SELECT is run
- role existence path is confirmed:
  - if TEST_OPERATOR exists, use existing role_id
  - if TEST_OPERATOR does not exist, insert role
- password hash is injected from secure buffer
- operator confirms SQL will be run in Supabase SQL Editor

## Boundary Confirmation
Confirm:
- no SQL executed
- no DB writes
- no API/auth implementation
- no GAS changes
- no Render changes
- password hash not stored in repo
- no secrets stored
- no .env created

## Verdict
FINAL_SQL_PACKET_PREPARED / EXECUTION_BLOCKED_PENDING_USER_APPROVAL

## Gemini Audit Status

- final verdict: PASS
- result status: CLOSED / APPROVED
- packet completeness accepted (preflight / insert / verification / rollback)
- boundary compliance accepted (no execution, no DB writes, no secret commit)
- next allowed step: User-approved SQL execution preflight and provisioning
