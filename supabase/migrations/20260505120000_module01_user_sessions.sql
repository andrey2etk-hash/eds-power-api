-- Module 01 opaque user sessions (MVP).
-- Raw session token is never stored in DB; only session_token_hash is stored.
-- Sessions are terminal-bound through terminal_id.
-- user_id and terminal_id use ON DELETE CASCADE for MVP cleanup behavior.
-- client_type is GAS-only in MVP.
-- ip_hash/user_agent_hash/metadata fields are intentionally deferred in MVP.

create table public.module01_user_sessions (
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
);

create index module01_user_sessions_user_id_idx
    on public.module01_user_sessions (user_id);

create index module01_user_sessions_terminal_id_idx
    on public.module01_user_sessions (terminal_id);

create index module01_user_sessions_expires_at_idx
    on public.module01_user_sessions (expires_at);

create index module01_user_sessions_revoked_at_idx
    on public.module01_user_sessions (revoked_at);

create index module01_user_sessions_last_seen_at_idx
    on public.module01_user_sessions (last_seen_at);

create index module01_user_sessions_user_terminal_idx
    on public.module01_user_sessions (user_id, terminal_id);

comment on table public.module01_user_sessions is
    'Module 01 opaque sessions. Raw token is never stored; only session_token_hash is persisted.';

comment on column public.module01_user_sessions.session_token_hash is
    'Hash of opaque session token only. Raw session token must never be stored.';

comment on column public.module01_user_sessions.terminal_id is
    'Terminal-bound session reference. API must revoke session on terminal mismatch.';

comment on column public.module01_user_sessions.user_id is
    'User reference with ON DELETE CASCADE for MVP cleanup.';

comment on column public.module01_user_sessions.client_type is
    'Client type in MVP is GAS only.';

comment on column public.module01_user_sessions.revoked_reason is
    'Broad-text revoke reason in MVP (e.g. USER_LOGOUT, TERMINAL_MISMATCH).';

-- Verification queries (do not execute in this migration file).
-- select to_regclass('public.module01_user_sessions') as table_exists;
-- select column_name from information_schema.columns
-- where table_schema = 'public' and table_name = 'module01_user_sessions'
-- order by ordinal_position;
-- select indexname, indexdef
-- from pg_indexes
-- where schemaname = 'public' and tablename = 'module01_user_sessions'
-- order by indexname;
-- select conname, pg_get_constraintdef(c.oid) as constraint_def
-- from pg_constraint c
-- join pg_class t on t.oid = c.conrelid
-- join pg_namespace n on n.oid = t.relnamespace
-- where n.nspname = 'public' and t.relname = 'module01_user_sessions'
-- order by conname;
-- select count(*) as seeded_rows from public.module01_user_sessions;
-- select table_name
-- from information_schema.tables
-- where table_schema = 'public'
--   and table_name in ('module01_users', 'module01_user_auth', 'module01_user_terminals')
-- order by table_name;
