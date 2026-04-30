# Stage **8A.0.5** — Local tooling precheck + operator setup plan

## Purpose

Record **what is missing** on the operator machine to complete **Stage 8A.0.4** (remote **`public`** schema-only capture + local replay), and give a **safe install order** without touching the database or migrations.

**Environment checked:** Windows (**`win32`**), operator profile **`Kubantsev`** (same session as **8A.0.4** tooling check).

## Final status

**`READY_FOR_OPERATOR_TOOLING_INSTALL`**

(None of the mandatory CLI tools were available on PATH at check time; **`winget`** was present and can be used for some packages.)

---

## CURRENT BLOCKERS

| Tool | Status on PATH | Notes |
| --- | --- | --- |
| **Supabase CLI** (`supabase`) | **missing** | Needed for linked-project workflows, `db dump`, and local **`supabase db reset`** after baseline DDL exists. |
| **`pg_dump`** (PostgreSQL client tools) | **missing** | Mandatory alternative path: schema-only dump from **`DATABASE_URL`** without Supabase CLI. |
| **`npm` / `npx`** | **missing** | Common install vector for Supabase CLI (`npm install -g supabase` or **`npx supabase`**). Cursor-bundled **`node.exe`** alone does **not** provide **`npx`**. |
| **Docker** (`docker`) | **missing** | **Optional** for capture; **recommended** for full local Supabase stack (`supabase start` / **`db reset`** against local containers). |

**Present (helper):** **`winget`** — `C:\Users\Kubantsev\AppData\Local\Microsoft\WindowsApps\winget.exe`

---

## REQUIRED TOOLS

### Mandatory

- **Supabase CLI** — project link, dumps aligned with Supabase workflow, local migration replay.
- **`pg_dump`** — at minimum, run **`pg_dump --schema-only`** (with **`--no-owner --no-acl`**) against the **Supabase Postgres** connection string after capture policy is agreed.

### Optional (recommended)

- **Docker Desktop** — enables **`supabase start`** and **`supabase db reset`** in the documented way on Windows.

---

## SAFE INSTALL ORDER

Use an elevated **PowerShell** or **cmd** only when an installer requires it. Prefer **LTS** releases. **Do not** paste production secrets into logs or tickets.

1. **Install Node.js LTS** (unlocks **`npm`** / **`npx`**)  
   - Download: `https://nodejs.org/` (Windows installer), **or** search winget:  
     `winget search OpenJS.NodeJS.LTS`  
   - After install, **close and reopen** the terminal, then verify:  
     `node --version` and `npm --version`

2. **Install Supabase CLI**  
   - Recommended: `npm install -g supabase`  
   - Alternative: official install options in Supabase docs — `https://supabase.com/docs/guides/cli/getting-started`  
   - Verify: `supabase --version`

3. **Install PostgreSQL client tools** (provides **`pg_dump`**)  
   - Full Windows installer (includes server + **`bin\pg_dump`**): `https://www.postgresql.org/download/windows/`  
   - During setup, note **“Command Line Tools”** / add **`...\PostgreSQL\<ver>\bin`** to **PATH**, or call **`pg_dump`** with full path.  
   - Verify: `pg_dump --version`

4. **(Optional) Install Docker Desktop**  
   - `https://docs.docker.com/desktop/setup/install/windows-install/`  
   - After install, reboot if prompted; enable **WSL2** backend if required by Docker.  
   - Verify: `docker --version`

5. **Repository prep (no DB changes)**  
   - From repo root **`eds-power-api`**: `supabase --version` (and link/login per your org policy when you are ready for **capture** — that step belongs to **8A.0.4** rerun, not this precheck).

---

## VERIFICATION COMMANDS

Run in a **new** terminal after installs:

```powershell
supabase --version
pg_dump --version
docker --version
```

**Expected:** each prints a version string. If **`supabase`** or **`pg_dump`** is still not found, fix **PATH** or use the full path to the binary (e.g. `C:\Program Files\PostgreSQL\17\bin\pg_dump.exe`).

---

## SAFE NEXT STEP

After tools work (and **without** **`db push`** to production):

1. Obtain **read-only** **`DATABASE_URL`** (or pooler URL) for the **Supabase** project from the dashboard or your secret store (ref only in repo: `supabase/.temp/linked-project.json` — **no password there**).
2. **Schema-only capture** (pick one):
   - **`pg_dump`** — e.g. `$env:PGPASSWORD='...'; pg_dump --schema-only --schema=public --no-owner --no-acl -h <host> -p <port> -U <user> -d postgres` then **filter** statements to **`objects`**, **`bom_links`**, **`ncr`**, **`production_status`**, and all **`public.v_*`** views; **no** `COPY` / `INSERT` / data.
   - **Supabase CLI** — use **`db dump`** (schema-only) per current CLI docs; same filtering rules.
3. Paste the result into **`supabase/migrations/20260429110000_remote_legacy_baseline.sql`** **only** in a dedicated **8A.0.4** rerun (no guessed DDL).
4. Run **local** replay: e.g. **`supabase db reset`** on a **disposable** local project — **reject** any prompt to push to **production**.

---

## FORBIDDEN

- **No** **`db push`** to production / no remote schema mutation for this precheck.
- **No** Dashboard **manual schema** edits to replace a proper dump.
- **No** guessed or hand-invented DDL.
- **No** moving or activating **`calculation_snapshots`** until **8A.0.4** records **`BASELINE_REPLAY_VERIFIED`**.

---

## References

- **`docs/AUDITS/2026-04-29_STAGE_8A_0_4_BASELINE_REPLAY_TEST.md`** — prior **`BLOCKED_BY_LOCAL_TOOLING`** record.
- **`supabase/migrations/20260429110000_remote_legacy_baseline.sql`** — target file for a future operator paste (do not edit during **8A.0.5**).
