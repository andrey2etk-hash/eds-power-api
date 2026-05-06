# MODULE 01 SESSION TABLE SQL CREATION PLAN

## Objective
Prepare SQL creation plan for Module 01 DB session table.

## Context
DB Session strategy approved for MVP Sakura.
Session schema plan audited PASS by Gemini.

## Planned Table
module01_user_sessions

## Gemini Audit Alignment

Status:
PASS WITH FIXES accepted.

Applied fixes:
- public schema qualification
- temporal integrity check
- rollback safety warning
- RLS/backend-only access note
- updated_at trigger deferred
- no cascade delete retained

## Final Aligned SQL Creation Packet

```sql
-- FINAL ALIGNED SQL PACKET
-- MANUAL DB BRIDGE ONLY
-- DO NOT EXECUTE UNTIL USER APPROVAL

create table public.module01_user_sessions (
    id uuid primary key,
    user_id uuid not null,
    terminal_id uuid not null,
    session_token_hash text not null unique,
    issued_at timestamptz not null default now(),
    expires_at timestamptz not null,
    revoked_at timestamptz null,
    last_seen_at timestamptz null,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),

    constraint chk_module01_user_sessions_expiry
        check (expires_at > issued_at),

    constraint fk_module01_user_sessions_user
        foreign key (user_id)
        references public.module01_users(id),

    constraint fk_module01_user_sessions_terminal
        foreign key (terminal_id)
        references public.module01_user_terminals(id)
);
```

## SQL Creation Draft

Include DOC-ONLY SQL draft for:

```sql
-- DOC ONLY / DO NOT EXECUTE IN THIS TASK
create table module01_user_sessions (
    id uuid primary key,
    user_id uuid not null,
    terminal_id uuid not null,
    session_token_hash text not null unique,
    issued_at timestamptz not null default now(),
    expires_at timestamptz not null,
    revoked_at timestamptz null,
    last_seen_at timestamptz null,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),

    constraint fk_module01_user_sessions_user
        foreign key (user_id)
        references module01_users(id),

    constraint fk_module01_user_sessions_terminal
        foreign key (terminal_id)
        references module01_user_terminals(id)
);
```

## Planned Indexes

Include SQL draft for:

- idx_module01_user_sessions_user_id
- idx_module01_user_sessions_terminal_id
- idx_module01_user_sessions_expires_at
- idx_module01_user_sessions_revoked_at

Recommended composite indexes:
- user_id + revoked_at + expires_at
- terminal_id + revoked_at + expires_at

```sql
-- DOC ONLY / DO NOT EXECUTE IN THIS TASK
create index idx_module01_user_sessions_user_id
    on module01_user_sessions(user_id);

create index idx_module01_user_sessions_terminal_id
    on module01_user_sessions(terminal_id);

create index idx_module01_user_sessions_expires_at
    on module01_user_sessions(expires_at);

create index idx_module01_user_sessions_revoked_at
    on module01_user_sessions(revoked_at);

-- Recommended composite indexes
create index idx_module01_user_sessions_user_state
    on module01_user_sessions(user_id, revoked_at, expires_at);

create index idx_module01_user_sessions_terminal_state
    on module01_user_sessions(terminal_id, revoked_at, expires_at);
```

## Session Token Rule

Document:
- raw token never stored
- only session_token_hash stored
- session_token_hash must be UNIQUE

## Verification SQL

Prepare verification SELECT examples:

- table exists
- indexes exist
- unique constraint exists
- foreign keys exist

```sql
-- VERIFICATION ONLY / MANUAL USE ONLY
select tablename
from pg_tables
where schemaname = 'public'
  and tablename = 'module01_user_sessions';

select indexname
from pg_indexes
where schemaname = 'public'
  and tablename = 'module01_user_sessions'
order by indexname;

select conname, contype
from pg_constraint c
join pg_class t on t.oid = c.conrelid
join pg_namespace n on n.oid = t.relnamespace
where n.nspname = 'public'
  and t.relname = 'module01_user_sessions'
  and c.contype in ('u', 'f')
order by conname;
```

## Rollback SQL

Prepare:
DROP TABLE IF EXISTS module01_user_sessions;

Mark clearly:
ROLLBACK ONLY / MANUAL USE ONLY
Rollback is allowed only before real session usage or with explicit operator approval.

```sql
-- ROLLBACK ONLY / MANUAL USE ONLY
drop table if exists public.module01_user_sessions;
```

## Open Questions

- Should ON DELETE CASCADE be used?
- Should updated_at trigger be added later?
- Should cleanup/expiration job be deferred?
- Should session history retention policy be defined later?

## Recommended Decisions

For MVP:
- no cascade delete
- no auto cleanup job yet
- no trigger yet
- explicit revoke only
- `updated_at` trigger is deferred and must be tracked as follow-up hardening

## RLS / Access Note

Session table must not be exposed to client/GAS.
Backend-only access is intended for create/validate/revoke flows.
RLS policy decision is deferred and must be documented before production hardening.

## Manual DB Bridge Reminder

Execution must follow:
1. Cursor prepares SQL
2. User executes manually in Supabase SQL Editor
3. User returns result
4. Architect/Critic validate

## Boundary Confirmation

Confirm:
- no SQL executed
- no table created
- no DB writes
- no API implementation
- no GAS changes
- no Render changes

## Verdict

SESSION_TABLE_SQL_CREATION_PLAN_PREPARED / PENDING_GEMINI_AUDIT
