# Stage 8A.0.8 — Cursor local Supabase connectivity verification

## Audit date

2026-04-30

## Trigger

TASK **STAGE 8A.0.8** — verify builder environment can actively interact with a **running local** Supabase stack after Docker + baseline replay unblock.

## Scope guard (honored)

- **No** production / remote Postgres connect as part of verification actions.
- **No** `db push`.
- **No** remote Supabase mutation.
- **No** `calculation_snapshots` DDL promotion / activation (table must remain absent until deliberate next gate).

## Environment (observed)

- **Host:** Windows (PowerShell), repo `eds-power-api`.
- **Supabase CLI:** `2.95.4` (`supabase --version`).
- **Local APIs (reported by `supabase status`):**
  - Project URL: `http://127.0.0.1:54321` (matches TASK known local API).
  - DB URL: `postgresql://postgres:postgres@127.0.0.1:54322/postgres` (matches TASK known local DB).
- **Docker:** `supabase_db_eds-power-api` container reachable; Postgres image `postgres:17.6.1.084`, port map `54322->5432`.

## 1. Local Supabase CLI operational state

**PASS.** `supabase status` completes and reports **local development setup is running**, with Studio / Kong / REST endpoints on expected localhost ports.

Note: output listed **stopped** optional services: `supabase_imgproxy_eds-power-api`, `supabase_pooler_eds-power-api` — non-blocking for DB + API gateway verification.

## 2. Builder read of local migration state

**PASS when using `--local`.**

Command:

```bash
supabase migration list --local
```

Observed:

- **Local:** `20260429110000` applied.
- **Remote column** displayed `20260429110000` in this run — CLI compares versions; **no remote connect or mutation was performed** for schema application (read-only list).

**Operational note:** Running `supabase migration list` **without** `--local` attempted “Initialising login role…” and exited with HTTP 400 / Postgres permission error altering `cli_login_postgres`. For CI/builder shells without linked remote credentials, **prefer `--local`** for deterministic local-only verification.

Applied migration row (SQL):

```text
SELECT version, name FROM supabase_migrations.schema_migrations ORDER BY version;
-- 20260429110000 | remote_legacy_baseline
```

This matches migration file `supabase/migrations/20260429110000_remote_legacy_baseline.sql`.

## 3. Legacy `public` objects required by TASK

Verified via **`docker exec`** into local DB (`psql` is **not** on the builder host PATH; SQL inspection used container-local `psql`).

Existence predicates (`information_schema.tables`, `table_schema = public`):

| Object              | Present |
|---------------------|--------|
| `objects`           | yes    |
| `bom_links`         | yes    |
| `ncr`               | yes    |
| `production_status`| yes    |

## 4. `v_*` views

**PASS.** Count of views matching `public` + name `v_%`: **23**.

Alphabetical list:

- `v_assembly_composition`
- `v_assembly_layers`
- `v_assembly_plan`
- `v_assembly_roadmap`
- `v_assembly_roadmap_actual`
- `v_assembly_sequence`
- `v_bom_assemblies`
- `v_bom_expanded`
- `v_bom_leaf_items`
- `v_bom_leaf_items_actual`
- `v_bom_tree`
- `v_bom_tree_actual`
- `v_dispatch_queue`
- `v_final_assembly_plan`
- `v_object_progress`
- `v_objects_actual`
- `v_production_items`
- `v_production_status_live`
- `v_production_status_ordered`
- `v_ready_to_start`
- `v_required_items_summary`
- `v_stage_readiness`
- `v_subassembly_plan`

Set aligns with baseline DDL authored in `20260429110000_remote_legacy_baseline.sql`.

## 5. Baseline replay confirmation

**PASS.** Exactly one migration applied in `supabase_migrations.schema_migrations`: **`remote_legacy_baseline`** at **`20260429110000`**.  

**Hold check:** `public.calculation_snapshots` **does not exist** (`EXISTS … = false`) — consistent with **`_pending_after_remote_baseline/`** governance; **no promotion** in this TASK.

## 6. Blockers

**None for this verification path.**  

Minor limitation documented: host `psql` unavailable; **`docker exec supabase_db_eds-power-api psql …`** used instead — acceptable where Docker CLI matches Supabase local stack naming.

---

## Gemini / GPT critique

Not in scope for 8A.0.8 (local connectivity dossier only).

## Cursor actions performed

- `supabase --version`, `supabase status`
- `supabase migration list --local` (and noted failure mode without `--local`)
- `docker exec` + `psql` catalog queries against local Postgres only

## User final decision

Recorded by operator TASK acceptance via repository audit filing.

## Status

**`CURSOR_LOCAL_STACK_VERIFIED`**
