# MODULE 01 USER SESSION MIGRATION HISTORY ALIGNMENT FINAL INSERT EXECUTION PLAN

## Status
DOC ONLY / FINAL INSERT PLANNING / NO SQL EXECUTION

## Purpose
Plan one controlled write to `supabase_migrations.schema_migrations` to align migration history for version `20260505120000` after manual SQL Editor apply.

## Source Of Truth
Approved migration file:
`supabase/migrations/20260505120000_module01_user_sessions.sql`

Target history row:
- version: `20260505120000`
- name: `module01_user_sessions`
- statements: array of SQL statements from approved migration file

## Confirmed Preconditions
- `public.module01_user_sessions` physically applied
- 13 columns verified
- 8 indexes verified
- 10 constraints verified
- `session_row_count = 0`
- 6 dependent Module 01 tables still present
- `schema_migrations` structure known
- `db push` not used
- migration repair not used

## Insert Strategy
Use Supabase SQL Editor.

The INSERT must:
- target only `supabase_migrations.schema_migrations`
- insert exactly one row
- use `version = '20260505120000'`
- use `name = 'module01_user_sessions'`
- use statements array derived from approved migration file
- not modify `public.module01_user_sessions`
- not modify dependent Module 01 tables
- not run migration repair
- not run db push

## Safe SQL Construction Requirement
Use PostgreSQL dollar-quoted strings for statements to avoid quote escaping errors.

Important:
- Do not include secrets.
- Do not include unrelated SQL.
- Do not include DDL execution for `module01_user_sessions` in this insert step.
- The `module01_user_sessions` DDL was already applied earlier.

## Pre-Insert Read-only Checks

Before INSERT, run:

1. Confirm target version absent:

```sql
select *
from supabase_migrations.schema_migrations
where version = '20260505120000';
```

Expected:
`0` rows.

2. Confirm `public.module01_user_sessions` still exists.

3. Confirm `session_row_count = 0`.

If any check fails:
STOP. Do not insert.

## Final INSERT SQL
Prepare exact INSERT SQL using statements from:
`supabase/migrations/20260505120000_module01_user_sessions.sql`

Required wrapper for future execution:
`BEGIN;`
`INSERT ...`
`COMMIT;`

Do not execute it in this planning task.

```sql
begin;

insert into supabase_migrations.schema_migrations (version, statements, name)
values (
  '20260505120000',
  array[
    $stmt$create table public.module01_user_sessions (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references public.module01_users(id) on delete cascade,
    terminal_id uuid not null references public.module01_user_terminals(id) on delete cascade,
    session_token_hash text not null,
    token_algorithm text not null,
    created_at timestamptz not null default now(),
    expires_at timestamptz not null,
    revoked_at timestamptz,
    last_seen_at timestamptz,
    client_type text not null,
    created_request_id text,
    revoked_request_id text,
    revoked_reason text,
    constraint module01_user_sessions_session_token_hash_key unique (session_token_hash),
    constraint module01_user_sessions_session_token_hash_nonempty_check
        check (btrim(session_token_hash) <> ''),
    constraint module01_user_sessions_token_algorithm_check
        check (token_algorithm in ('SHA256', 'HMAC_SHA256')),
    constraint module01_user_sessions_client_type_check
        check (client_type in ('GAS')),
    constraint module01_user_sessions_expires_after_created_check
        check (expires_at > created_at),
    constraint module01_user_sessions_revoked_at_check
        check (revoked_at is null or revoked_at >= created_at),
    constraint module01_user_sessions_last_seen_at_check
        check (last_seen_at is null or last_seen_at >= created_at)
);$stmt$,
    $stmt$create index module01_user_sessions_user_id_idx
    on public.module01_user_sessions (user_id);$stmt$,
    $stmt$create index module01_user_sessions_terminal_id_idx
    on public.module01_user_sessions (terminal_id);$stmt$,
    $stmt$create index module01_user_sessions_expires_at_idx
    on public.module01_user_sessions (expires_at);$stmt$,
    $stmt$create index module01_user_sessions_revoked_at_idx
    on public.module01_user_sessions (revoked_at);$stmt$,
    $stmt$create index module01_user_sessions_last_seen_at_idx
    on public.module01_user_sessions (last_seen_at);$stmt$,
    $stmt$create index module01_user_sessions_user_terminal_idx
    on public.module01_user_sessions (user_id, terminal_id);$stmt$,
    $stmt$comment on table public.module01_user_sessions is
    'Module 01 opaque sessions. Raw token is never stored; only session_token_hash is persisted.';$stmt$,
    $stmt$comment on column public.module01_user_sessions.session_token_hash is
    'Hash of opaque session token only. Raw session token must never be stored.';$stmt$,
    $stmt$comment on column public.module01_user_sessions.terminal_id is
    'Terminal-bound session reference. API must revoke session on terminal mismatch.';$stmt$
  ],
  'module01_user_sessions'
);

commit;
```

Expected statements_count after future execution:
`10`

## Post-Insert Verification

After future execution, run:

1. Confirm target row exists:

```sql
select version, name, cardinality(statements) as statements_count
from supabase_migrations.schema_migrations
where version = '20260505120000';
```

Expected:
- version = `20260505120000`
- name = `module01_user_sessions`
- statements_count = `10`

2. Confirm no duplicate:

```sql
select version, count(*) as row_count
from supabase_migrations.schema_migrations
where version = '20260505120000'
group by version;
```

Expected:
`row_count = 1`.

3. Confirm `public.module01_user_sessions` still exists.

4. Confirm `session_row_count = 0`.

5. Confirm `db push` was not used.

## Failure Handling

If INSERT fails:
- stop immediately
- do not retry blindly
- capture exact error
- do not manually patch
- return to planning

If duplicate exists:
- stop
- do not insert
- record already-aligned / investigate

If post-insert verification fails:
- stop
- document mismatch
- do not patch blindly
- return to planning

## Forbidden
- no SQL execution in this planning task
- no `schema_migrations` insert in this planning task
- no migration repair
- no db push
- no DDL/table creation
- no API/GAS/Python changes
- no migration file edits
- no secrets

## Next Allowed Step
Gemini audit of this FINAL INSERT Execution Plan.

If PASS:
User Session Migration History Alignment FINAL INSERT Execution as separate operator task.

## Gemini Audit Status

- final verdict: PASS
- plan status: CLOSED / APPROVED
- next allowed step: User Session Migration History Alignment FINAL INSERT Execution
- expected `statements_count = 10`
- `BEGIN` / `COMMIT` wrapper required
- dollar-quoting required
- no `db push`
- no migration repair
