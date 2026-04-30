# Stage 8A.1 — `calculation_snapshots` migration promotion test (local)

## Audit date

2026-04-30

## Precondition

- **Stage 8A.0.8** — `CURSOR_LOCAL_STACK_VERIFIED` (`docs/AUDITS/2026-04-30_STAGE_8A_0_8_CURSOR_LOCAL_CONNECTIVITY.md`).
- Git working tree clean before TASK start (operator).
- **No** production `db push`, **no** remote DB mutation performed in this TASK.

## Objective

Promote **`20260429120000_calculation_snapshots_v1.sql`** from **`_pending_after_remote_baseline/`** into active **`supabase/migrations/`** after verified local legacy baseline replay, then prove clean **`supabase db reset`** replay.

## Actions performed

1. **Move (git-tracked):**  
   `_pending_after_remote_baseline/20260429120000_calculation_snapshots_v1.sql` → `supabase/migrations/20260429120000_calculation_snapshots_v1.sql`

2. **Migration order:** Timestamps **`20260429110000`** `<` **`20260429120000`** — lexicographic apply order preserves **baseline → snapshots**.

3. **Local replay:**  
   `supabase db reset` — completed without migration failure.

CLI apply log (verbatim pattern):

```text
Applying migration 20260429110000_remote_legacy_baseline.sql...
Applying migration 20260429120000_calculation_snapshots_v1.sql...
NOTICE (42710): extension "pgcrypto" already exists, skipping
Finished supabase db reset on branch main.
```

4. **`supabase migration list --local`** after reset: **`20260429110000`**, **`20260429120000`** present on Local column.

## Verification (PostgreSQL catalog)

Queries via **`docker exec supabase_db_eds-power-api psql`** (same method as **8A.0.8**).

### schema_migrations

| version | name |
|--------|------|
| 20260429110000 | remote_legacy_baseline |
| 20260429120000 | calculation_snapshots_v1 |

### Legacy tables (`public`)

| Table | EXISTS |
|-------|--------|
| objects | true |
| bom_links | true |
| ncr | true |
| production_status | true |

### Legacy views

- Count of **`public`** views matching **`v_%`**: **23** (matches baseline dossier).

### New table

- **`public.calculation_snapshots`**: **true**.

No schema redesign beyond the promoted file (DDL unchanged substantively — header comments-only edit for promotion narrative).

## Scope guard (honoured)

- **No** guessed DDL.
- **No** remote mutation / production apply.
- **`calculation_snapshots`** DDL is unchanged from canonical hold file (comments at top adjusted for active migration only).

## Status

**`FIRST_PERSISTENCE_READY_NON_PROD`**
