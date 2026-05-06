# MODULE 01 USER AUTH MIGRATION HISTORY ALIGNMENT FINAL INSERT EXECUTION PLAN

## Status
DOC ONLY / FINAL INSERT PLANNING / NO SQL EXECUTION

## Purpose
Plan one controlled write to `supabase_migrations.schema_migrations` to align migration history for version `20260505110000` after manual SQL Editor apply.

## Source Of Truth
Approved migration file:
`supabase/migrations/20260505110000_module01_user_auth.sql`

Target history row:
- version: `20260505110000`
- name: `module01_user_auth`
- statements: array of SQL statements from approved migration file

## Confirmed Preconditions
- `public.module01_user_auth` physically applied
- 15 columns verified
- 7 indexes verified
- 8 constraints verified
- `auth_row_count = 0`
- 8 base Module 01 tables still present
- `schema_migrations` structure known
- `db push` not used
- migration repair not used

## Insert Strategy
Use Supabase SQL Editor.

The INSERT must:
- target only `supabase_migrations.schema_migrations`
- insert exactly one row
- use `version = '20260505110000'`
- use `name = 'module01_user_auth'`
- use statements array derived from approved migration file
- not modify `public.module01_user_auth`
- not modify base Module 01 tables
- not run migration repair
- not run db push

## Safe SQL Construction Requirement
Use PostgreSQL dollar-quoted strings for statements to avoid quote escaping errors.

Important:
- Do not include secrets.
- Do not include unrelated SQL.
- Do not include DDL execution for `module01_user_auth` in this insert step.
- The `module01_user_auth` DDL was already applied earlier.

## Pre-Insert Read-only Checks
Before INSERT, run:

1. Confirm target version absent:

```sql
select *
from supabase_migrations.schema_migrations
where version = '20260505110000';
```

Expected:
`0` rows.

2. Confirm `public.module01_user_auth` still exists.
3. Confirm `auth_row_count = 0`.

If any check fails:
STOP. Do not insert.

## Final INSERT SQL
Prepare exact INSERT SQL using statements from:
`supabase/migrations/20260505110000_module01_user_auth.sql`

Required wrapper for future execution:
`BEGIN;`
`INSERT ...`
`COMMIT;`

Do not execute it in this planning task.

```sql
begin;

insert into supabase_migrations.schema_migrations (version, statements, name)
values (
  '20260505110000',
  array[
    $stmt$create table public.module01_user_auth (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references public.module01_users(id) on delete cascade,
    password_hash text not null,
    password_algorithm text not null,
    password_updated_at timestamptz,
    must_change_password boolean not null default true,
    reset_token_hash text,
    reset_token_expires_at timestamptz,
    reset_requested_at timestamptz,
    failed_login_attempts integer not null default 0,
    locked_until timestamptz,
    last_login_at timestamptz,
    last_login_terminal_id uuid references public.module01_user_terminals(id) on delete set null,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    constraint module01_user_auth_user_id_key unique (user_id),
    constraint module01_user_auth_password_hash_nonempty_check
        check (btrim(password_hash) <> ''),
    constraint module01_user_auth_password_algorithm_check
        check (password_algorithm in ('ARGON2ID', 'BCRYPT')),
    constraint module01_user_auth_failed_login_attempts_nonnegative_check
        check (failed_login_attempts >= 0),
    constraint module01_user_auth_reset_token_consistency_check
        check (reset_token_hash is null or reset_token_expires_at is not null)
);$stmt$,
    $stmt$create index module01_user_auth_user_id_idx
    on public.module01_user_auth (user_id);$stmt$,
    $stmt$create index module01_user_auth_locked_until_idx
    on public.module01_user_auth (locked_until);$stmt$,
    $stmt$create index module01_user_auth_reset_token_expires_at_idx
    on public.module01_user_auth (reset_token_expires_at);$stmt$,
    $stmt$create unique index module01_user_auth_reset_token_hash_unique_idx
    on public.module01_user_auth (reset_token_hash)
    where reset_token_hash is not null;$stmt$,
    $stmt$create index module01_user_auth_last_login_terminal_id_idx
    on public.module01_user_auth (last_login_terminal_id);$stmt$,
    $stmt$comment on table public.module01_user_auth is
    'Module 01 auth/security state separated from module01_users profile.';$stmt$,
    $stmt$comment on column public.module01_user_auth.password_hash is
    'API-managed password hash only. Never store plaintext passwords.';$stmt$,
    $stmt$comment on column public.module01_user_auth.reset_token_hash is
    'Hashed reset token only. Raw reset tokens must never be stored.';$stmt$,
    $stmt$comment on column public.module01_user_auth.updated_at is
    'API-managed timestamp in this slice. No DB trigger is introduced here.';$stmt$
  ],
  'module01_user_auth'
);

commit;
```

## Post-Insert Verification
After future execution, run:

1. Confirm target row exists:

```sql
select version, name, cardinality(statements) as statements_count
from supabase_migrations.schema_migrations
where version = '20260505110000';
```

Expected:
`1` row.

2. Confirm no duplicate:

```sql
select version, count(*) as row_count
from supabase_migrations.schema_migrations
where version = '20260505110000'
group by version;
```

Expected:
`row_count = 1`.

3. Confirm `public.module01_user_auth` still exists.
4. Confirm `auth_row_count = 0`.
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
User Auth Migration History Alignment FINAL INSERT Execution as separate operator task.

## Gemini Audit Status

- final verdict: PASS
- plan status: CLOSED / APPROVED
- next allowed step: User Auth Migration History Alignment FINAL INSERT Execution
- expected `statements_count = 10`
- `BEGIN` / `COMMIT` wrapper required
- no `db push`
- no migration repair
