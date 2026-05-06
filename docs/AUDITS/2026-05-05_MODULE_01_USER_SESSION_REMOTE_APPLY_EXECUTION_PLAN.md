# MODULE 01 USER SESSION REMOTE APPLY EXECUTION PLAN

## Status
DOC ONLY / REMOTE APPLY PLANNING / NO EXECUTION

## Purpose
Plan controlled remote application of `module01_user_sessions` migration through Supabase SQL Editor.

## Source Of Truth
Approved migration file:
`supabase/migrations/20260505120000_module01_user_sessions.sql`

Rules:
- SQL must be copied from this file only
- migration file must not be edited during apply
- no invented SQL
- no partial custom DDL
- no seed sessions
- no real tokens
- no secrets

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
4. SQL contains no tokens, token hashes, passwords, or secrets.
5. SQL contains no INSERT seed session rows.
6. SQL targets only:
   `public.module01_user_sessions`
   indexes/comments for `module01_user_sessions`
7. SQL does not modify:
   `module01_users`
   `module01_user_auth`
   `module01_user_terminals`
   `module01_roles`
   `module01_user_roles`
   `module01_audit_events`
8. SQL does not touch:
   `supabase_migrations.schema_migrations`
9. `db push` is not used.
10. migration repair is not used.

## Apply Scope

Allowed:
- execute only SQL from:
  `supabase/migrations/20260505120000_module01_user_sessions.sql`

Expected new table:
- `public.module01_user_sessions`

Expected fields:
- id
- user_id
- terminal_id
- session_token_hash
- token_algorithm
- created_at
- expires_at
- revoked_at
- last_seen_at
- client_type
- created_request_id
- revoked_request_id
- revoked_reason

Expected constraints:
- session_token_hash globally UNIQUE
- session_token_hash non-empty
- token_algorithm in ('SHA256', 'HMAC_SHA256')
- client_type in ('GAS')
- expires_at > created_at
- revoked_at is null or revoked_at >= created_at
- last_seen_at is null or last_seen_at >= created_at
- user_id FK ON DELETE CASCADE
- terminal_id FK ON DELETE CASCADE

Expected indexes:
- user_id
- terminal_id
- expires_at
- revoked_at
- last_seen_at
- user_id + terminal_id composite
- unique session_token_hash

Forbidden:
- no seed session rows
- no real tokens
- no token hashes
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
   - contains only module01_user_sessions DDL/index/comment statements
   - contains no secrets/tokens
   - contains no seed session rows
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
  and table_name = 'module01_user_sessions';
```

Expected:
1 row.

### 2. Verify columns exist

```sql
select column_name, data_type, is_nullable
from information_schema.columns
where table_schema = 'public'
  and table_name = 'module01_user_sessions'
order by ordinal_position;
```

Expected:
all planned fields.

### 3. Verify no session rows seeded

```sql
select count(*) as session_row_count
from public.module01_user_sessions;
```

Expected:
0 rows.

### 4. Verify indexes

```sql
select indexname
from pg_indexes
where schemaname = 'public'
  and tablename = 'module01_user_sessions'
order by indexname;
```

Expected:
approved indexes including unique session_token_hash index and user_terminal composite index.

### 5. Verify constraints

```sql
select conname, contype
from pg_constraint
where conrelid = 'public.module01_user_sessions'::regclass
order by conname;
```

Expected:
PK, FK, unique session_token_hash, and check constraints.

### 6. Verify dependent base tables remain present

```sql
select table_name
from information_schema.tables
where table_schema = 'public'
  and table_name in (
    'module01_users',
    'module01_user_auth',
    'module01_user_terminals',
    'module01_roles',
    'module01_user_roles',
    'module01_audit_events'
  )
order by table_name;
```

Expected:
6 rows.

## Evidence To Capture

Operator result must record:
- execution timestamp
- project ref
- source migration file path
- SQL Editor result PASS/FAIL
- table verification result
- columns verification result
- session row count
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
- raw session tokens
- session_token_hash values

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
Module 01 User Session Migration History Alignment Decision / Execution Plan.

Possible future path:
- manual `schema_migrations` alignment, consistent with previous successful Module 01 approach
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
- session implementation
- production auth rollout

## Next Allowed Step

Gemini audit of User Session Remote Apply Execution Plan.

If PASS:
Module 01 User Session Remote Apply Execution as separate operator task.

## Gemini Audit Status

- final verdict: PASS
- plan status: CLOSED / APPROVED
- next allowed step: Module 01 User Session Remote Apply Execution
- `db push` not allowed
- migration repair not allowed
- `schema_migrations` alignment deferred
- no API/GAS/Python implementation
