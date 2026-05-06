-- Module 01 user auth storage.
-- Auth/security state is separated from profile identity on purpose.
-- No plaintext passwords: password_hash is API-managed only.
-- reset_token_hash stores hashed reset tokens only.
-- updated_at remains API-managed in this slice (no triggers in this migration).

create table public.module01_user_auth (
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
);

create index module01_user_auth_user_id_idx
    on public.module01_user_auth (user_id);

create index module01_user_auth_locked_until_idx
    on public.module01_user_auth (locked_until);

create index module01_user_auth_reset_token_expires_at_idx
    on public.module01_user_auth (reset_token_expires_at);

create unique index module01_user_auth_reset_token_hash_unique_idx
    on public.module01_user_auth (reset_token_hash)
    where reset_token_hash is not null;

create index module01_user_auth_last_login_terminal_id_idx
    on public.module01_user_auth (last_login_terminal_id);

comment on table public.module01_user_auth is
    'Module 01 auth/security state separated from module01_users profile.';

comment on column public.module01_user_auth.password_hash is
    'API-managed password hash only. Never store plaintext passwords.';

comment on column public.module01_user_auth.reset_token_hash is
    'Hashed reset token only. Raw reset tokens must never be stored.';

comment on column public.module01_user_auth.updated_at is
    'API-managed timestamp in this slice. No DB trigger is introduced here.';

-- Verification queries (do not execute in this migration file).
-- select to_regclass('public.module01_user_auth') as table_exists;
-- select column_name from information_schema.columns
-- where table_schema = 'public' and table_name = 'module01_user_auth'
-- order by ordinal_position;
-- select indexname, indexdef
-- from pg_indexes
-- where schemaname = 'public' and tablename = 'module01_user_auth'
-- order by indexname;
-- select conname, pg_get_constraintdef(c.oid) as constraint_def
-- from pg_constraint c
-- join pg_class t on t.oid = c.conrelid
-- join pg_namespace n on n.oid = t.relnamespace
-- where n.nspname = 'public' and t.relname = 'module01_user_auth'
-- order by conname;
-- select count(*) as seeded_rows from public.module01_user_auth;
