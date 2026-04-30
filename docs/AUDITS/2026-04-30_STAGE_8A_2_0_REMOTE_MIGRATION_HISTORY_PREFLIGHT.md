# Stage 8A.2.0 — Remote migration history alignment preflight

## Audit date

2026-04-30

## Objective

Prepare a **live-safe** path to align Supabase **remote** migration history with the repo **without** blindly running `db push` against a database that already contains legacy **`public`** objects from **`20260429110000_remote_legacy_baseline.sql`**.

## Preconditions (accepted)

- **Stage 8A.1** — local **`FIRST_PERSISTENCE_READY_NON_PROD`** (baseline **`110000`** then **`120000`** on disposable/local stack).
- Remote project **already reflects** legacy schema (tables **`objects`**, **`bom_links`**, **`ncr`**, **`production_status`**, **`v_*`** views) — reproduced from factual capture (**8A.0.6**), not invented in this TASK.

## Scope guard (honoured)

- **No** `db push`.
- **No** remote schema mutation via this audit or builder session tools.
- **No** applying **`calculation_snapshots`** live DDL yet (beyond planning text).
- **No** **`supabase migration repair`** execution in Cursor/builder unless operator explicitly runs commands below.

---

## 1. Remote migration history inspection (read-only theory)

Purpose: decide whether **`20260429110000`** must be **recorded as applied** in **`supabase_migrations.schema_migrations`** on remote **without re-executing** the baseline file (would conflict with **`CREATE TABLE` / `CREATE VIEW`** that already exist).

### 1.A. Expected healthy outcomes

| Observation on remote | Interpretation |
|----------------------|----------------|
| **`schema_migrations`** already contains **`20260429110000`** (`remote_legacy_baseline` name may vary by CLI labeling) | **Repair not needed** for baseline; pending work is only **`20260429120000`** alignment + controlled apply later. |
| Legacy **`public`** objects exist **but** **`20260429110000`** **missing** from **`schema_migrations`** | Typical ** drift **: schema came from Dashboard / manual / pre-migration-history era. **`migration repair --status applied 20260429110000`** is the **safest bookkeeping** alignment *if operator confirms DDL equivalence* (§3). |

### 1.B. Builder session attempt (honest blocker)

Commands run from repo **`supabase/`** directory:

```bash
supabase migration list
```

**Result (2026-04-30 builder):** fails during **Initialising login role …** with Postgres **`42501` permission denied** altering role **`cli_login_postgres`**; CLI advises **`SUPABASE_DB_PASSWORD`**.

Interpretation:

- This environment **cannot** read remote **`schema_migrations`** through the CLI until operator supplies a **Dashboard database password** (or equivalent **`--password` / `SUPABASE_DB_PASSWORD`**) **and** the database role allows the CLI bootstrap path Supabase expects.
- Escalation (operator / Supabase support): ensure linked DB user / pooler credentials match Supabase Dashboard **Settings → Database**; some orgs resolve **`cli_login_postgres`** issues via project role privileges or Support.

Therefore: **remote row-level truth was not queried in-repo by the agent.** Alignment **decision** (repair vs skip) defaults to **`migration list` + SQL editor sanity check`** by operator §2.

---

## 2. Operator command sequence — verify link (read-only)

Run in **`eds-power-api`** repo root (`supabase/` child present).

### Step A — Confirm linked project

```bash
cd /path/to/eds-power-api
supabase projects list
```

Verify the row with **`LINKED ●`** matches **EDSPower Database** (or the **explicit** production/staging instance intended for Stage 8A live gate).

**Observation (CLI snapshot, builder):** linked project **`EDSPower Database`**, reference id **`mvcxtwoxhopumxcryxlc`** (dashboard / API “project ref”). Operator must visually reconfirm before any mutation step in a future TASK.

### Step B — Prefer password in env for non-interactive sessions

Unix-style:

```bash
export SUPABASE_DB_PASSWORD='<Database password from Supabase Dashboard>'
```

PowerShell-style:

```powershell
$env:SUPABASE_DB_PASSWORD = '<Database password from Supabase Dashboard>'
```

### Step C — Migration diff (read-only compare)

```bash
supabase migration list
```

Expected columns: **Local** vs **Remote** vs timestamp. Record:

- Does **Remote** show **`20260429110000`**?
- Does **Remote** show **`20260429120000`**?

Optional cross-check (**read-only**) in Dashboard **SQL Editor**:

```sql
SELECT version, name
FROM supabase_migrations.schema_migrations
ORDER BY version;
```

(If **`name`** differs from local migration labels, rely on **`version`** / timestamp **`20260429110000`** / **`20260429120000`**.)

---

## 3. When to use `migration repair` for baseline (**operator confirmation gate**)

**Do not execute** the repair until **all** are true:

1. Operator confirms **`supabase migration list`** shows **`20260429110000`** locally and **Legacy exists on remote**.
2. Remote **does not** list **`20260429110000`** as applied **or** history is inconsistent with known legacy import.
3. Operator attests (**doc / ticket**) that remote legacy DDL is **materially equivalent** to **`supabase/migrations/20260429110000_remote_legacy_baseline.sql`** (same captured baseline — **no guessed DDL**, **8A.0.6** lineage). If schemas diverged manually after capture, **`repair`** alone is insufficient; reconcile via separate governance TASK before live apply.

### Command (**not run by builder**):

```bash
supabase migration repair --status applied 20260429110000 --linked
```

If env password is not picked up interactively:

```bash
supabase migration repair --status applied 20260429110000 --linked -p "$SUPABASE_DB_PASSWORD"
```

Repair **updates migration history bookkeeping only**; it **does not** run the SQL body of **`110000`** again. That is why it is suitable when objects already exist.

---

## 4. Apply **only** `20260429120000` after history alignment (future TASK; dry-run first)

Still **no execution** in **8A.2.0**; this sequence documents **live-safe apply** once operator accepts repair/list state.

### Step D — Dry run (shows what push would send)

```bash
supabase db push --dry-run --linked
```

Operator verifies output lists **only** pending migrations — ideally **single** **`20260429120000_calculation_snapshots_v1`**. If **`110000`** appears as pending despite existing tables, stop: return to §3 (repair) or resolve drift — **never** `--yes` blindly.

### Step E — Actual push (**only after** separate explicit operator TASK approving live mutation)

```bash
supabase db push --linked
```

Use **staging / verification project first** where policy allows — **never** contradict org change management.

---

## 5. Forbidden shortcuts (recap)

| Action | Reason |
|--------|--------|
| `db push` before **`migration list` + equivalence check** | May attempt **`110000`** DDL against existing objects → hard failures / partial states. |
| `migration repair applied` **without** operator sign-off | Governance breach; hides real drift. |
| Apply **`120000`** while **`110000`** missing from remote history | CLI may reorder or reject; ambiguous state risk. |

---

## 6. Status

### Final status label

**`READY_FOR_OPERATOR_REMOTE_HISTORY_REPAIR`**

### Auxiliary builder note (**not** a second final status token)

Automated **`supabase migration list`** remote read — **`BLOCKED_WITH_REASON`** in this session: **`cli_login_postgres` ALTER ROLE denied + `SUPABASE_DB_PASSWORD` not supplied** until operator configures credentials. Operational closure requires operator-run §2–§4.
