# MODULE 01 USER AUTH REMOTE APPLY EXECUTION PLAN

## Status
DOC ONLY / REMOTE APPLY PLANNING / NO EXECUTION

## Purpose
Plan controlled remote application of `module01_user_auth` migration through Supabase SQL Editor.

## Source Of Truth
Approved migration file:
`supabase/migrations/20260505110000_module01_user_auth.sql`

Rules:
- SQL must be copied from this file only
- migration file must not be edited during apply
- no invented SQL
- no partial custom DDL
- no seed passwords
- no real secrets

## Remote Target
- project: EDSPower Database
- ref: mvcxtwoxhopumxcryxlc
- schema: public

## Pre-Apply Checks

Before execution, operator must confirm:
1. Correct Supabase project selected:
   EDSPower Database / mvcxtwoxhopumxcryxlc
2. SQL Editor opened.
3. Source migration file copied fully.
4. SQL contains no passwords, tokens, or secrets.
5. SQL contains no INSERT seed auth rows.
6. SQL targets only:
   `public.module01_user_auth`
   indexes/comments for `module01_user_auth`
7. SQL does not modify:
   `module01_users`
   `module01_roles`
   `module01_user_roles`
   `module01_user_terminals`
   `module01_calculations`
   `module01_calculation_versions`
   `module01_calculation_status_history`
   `module01_audit_events`
8. SQL does not touch:
   `supabase_migrations.schema_migrations`
9. `db push` is not used.
10. migration repair is not used.

## Apply Scope

Allowed:
- execute only SQL from:
  `supabase/migrations/20260505110000_module01_user_auth.sql`

Expected new table:
- `public.module01_user_auth`

Expected indexes:
- user_id index / unique user_id constraint
- locked_until index
- reset_token_expires_at index
- partial unique reset_token_hash index
- optional last_login_terminal_id index if present in migration

Expected constraints:
- password_hash non-empty
- password_algorithm IN ('ARGON2ID', 'BCRYPT')
- failed_login_attempts >= 0
- reset token consistency check
- user_id FK ON DELETE CASCADE
- last_login_terminal_id FK ON DELETE SET NULL

Forbidden:
- no seed auth rows
- no real passwords
- no reset tokens
- no API/GAS/Python code
- no schema_migrations insert in this apply step
- no migration repair
- no db push

## Execution Steps

1. Open Supabase Dashboard.
2. Select EDSPower Database.
3. Open SQL Editor.
4. Paste full SQL from approved migration file.
5. Visually confirm:
   - starts and ends as expected
   - contains only module01_user_auth DDL/index/comment statements
   - contains no secrets
   - contains no auth seed rows
   - contains no schema_migrations insert
6. Execute once.
7. If execution fails:
   - stop immediately
   - do not rerun blindly
   - capture error text
   - do not patch manually
   - create FAIL/BLOCKED result
8. If execution succeeds:
   - run verification queries only.

## Verification Queries

### 1. Verify table exists

```sql
select table_name
from information_schema.tables
where table_schema = 'public'
  and table_name = 'module01_user_auth';
```

Expected:
1 row.

### 2. Verify columns exist

```sql
select column_name, data_type, is_nullable
from information_schema.columns
where table_schema = 'public'
  and table_name = 'module01_user_auth'
order by ordinal_position;
```

Expected:
all planned fields.

### 3. Verify no auth rows seeded

```sql
select count(*) as auth_row_count
from public.module01_user_auth;
```

Expected:
0 rows.

### 4. Verify indexes

```sql
select indexname
from pg_indexes
where schemaname = 'public'
  and tablename = 'module01_user_auth'
order by indexname;
```

Expected:
approved indexes including partial unique reset_token_hash index.

### 5. Verify constraints

```sql
select conname, contype
from pg_constraint
where conrelid = 'public.module01_user_auth'::regclass
order by conname;
```

Expected:
PK, FK, unique user_id, and check constraints.

### 6. Verify existing Module 01 base tables remain present

```sql
select table_name
from information_schema.tables
where table_schema = 'public'
  and table_name in (
    'module01_users',
    'module01_roles',
    'module01_user_roles',
    'module01_user_terminals',
    'module01_calculations',
    'module01_calculation_versions',
    'module01_calculation_status_history',
    'module01_audit_events'
  )
order by table_name;
```

Expected:
8 rows.

## Evidence To Capture

Operator result must record:
- execution timestamp
- project ref
- source migration file path
- SQL Editor result PASS/FAIL
- table verification result
- columns verification result
- auth row count
- indexes verification result
- constraints verification result
- base tables safety confirmation
- db push not used
- migration repair not used
- schema_migrations not touched

Do not capture:
- passwords
- service_role keys
- full connection strings with secrets
- password hashes
- reset tokens

## Failure Handling

If SQL apply fails:
- stop
- do not rerun blindly
- do not patch manually
- document exact error
- return to planning

If verification fails:
- stop
- document mismatch
- do not patch manually
- return to planning

## Migration History Alignment

Not part of this execution.

After successful apply + verification:
Open separate audited step:
Module 01 User Auth Migration History Alignment Decision / Execution Plan.

Possible future path:
- manual `schema_migrations` alignment, consistent with previous successful Module 01 Slice 01 approach
- no automatic db push
- no migration repair unless separately re-approved

## Boundary

This plan does not authorize:
- SQL execution
- DB writes
- db push
- migration repair
- schema_migrations insert
- API/GAS/Python implementation
- password hashing implementation
- email service implementation
- production auth rollout

## Next Allowed Step

Gemini audit of User Auth Remote Apply Execution Plan.

If PASS:
Module 01 User Auth Remote Apply Execution as separate operator task.

## Gemini Audit Status

- final verdict: PASS
- plan status: CLOSED / APPROVED
- next allowed step: Module 01 User Auth Remote Apply Execution
- `db push` not allowed
- migration repair not allowed
- `schema_migrations` alignment deferred
- no API/GAS/Python implementation
