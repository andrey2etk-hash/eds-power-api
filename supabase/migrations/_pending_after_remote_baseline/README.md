# Pending: `calculation_snapshots` DDL (**hold** until remote baseline aligned)

Stage **8A.0.2** freezes **`supabase db push`** on this DDL until **`LEGACY_REMOTE_BASELINE.md`** governance is honoured and a **`legacy_baseline` migration is generated/imported** into **`../`** (numbered **before** restoring this file).

## Contents

| File | Role |
| --- | --- |
| **`20260429120000_calculation_snapshots_v1.sql`** | Canonical **`calculation_snapshots`** migration from **Stage 8A.0.1** (unchanged DDL). |

## Restore workflow (operators)

1. **Do not skip baseline.** Generate or import authoritative baseline SQL for **`public`** including legacy tables/views (**no destructive DDL** unless separate IDEA explicitly approves remediation).
2. Place baseline migration files in **`supabase/migrations/`** using timestamps **lower than** **`20260429120000`** (or reorganise timestamps so baseline clearly precedes **`calculation_snapshots`** — Supabase executes lexicographically by filename **version**).
3. **Move or copy** this SQL file **back into** **`supabase/migrations/`** (same name or **`YYYYMMDD…_calculation_snapshots_v1.sql`** strictly **after** baseline files).
4. Only then **`supabase db push`** against a non-production verification project or after dry-run checklist.

---

**Strict Stage 8A.0.2:** repo-only governance + hold — **zero** destructive remote mutations from this TASK.
