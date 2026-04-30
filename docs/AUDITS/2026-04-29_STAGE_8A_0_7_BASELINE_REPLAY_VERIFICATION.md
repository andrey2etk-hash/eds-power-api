# Stage **8A.0.7** — Baseline local replay verification

## Objective

Confirm **`supabase/migrations/20260429110000_remote_legacy_baseline.sql`** replays cleanly via **local** Supabase (**`supabase db reset`**) or an equivalent **disposable** Postgres — **no production `db push`**, **no remote schema changes**, **no** promoting **`calculation_snapshots_v1.sql`** yet.

## Tooling check (this session)

| Tool | On PATH | Notes |
| --- | :---: | --- |
| **Docker** (`docker --version`) | **no** | `docker` not found (Windows PowerShell **`Get-Command`**) |
| **Supabase CLI** (`supabase --version`) | **no** | `supabase` not found |

## Replay command (when unblocked)

From repo root **`eds-power-api`** (with Docker Desktop running):

```powershell
supabase start   # if stack not up
supabase db reset
```

**Do not** approve prompts that **push** or **link-apply** to **production**.

## Final stage status

**`BLOCKED_BY_DOCKER`**

(Requires **Docker Desktop** + **Supabase CLI** per **`docs/AUDITS/2026-04-29_STAGE_8A_0_5_LOCAL_TOOLING_PRECHECK.md`**. Until then, **`BASELINE_REPLAY_VERIFIED`** is **not** asserted.)

---

## Disposable staging alternative (no prod)

If local Docker is undesirable, use either:

1. **Ephemeral Postgres 17 container** — apply only **`20260429110000_remote_legacy_baseline.sql`** to empty DB (**`PGPASSWORD`**, **`psql -v ON_ERROR_STOP=1 -f`**); extensions as needed (baseline **`gen_random_uuid()`** ok on PG **17**).
2. **Separate Supabase “staging” project** — link only to **non-prod** ref; run migration apply there; amend this audit with **PASS**.

Either path must stay **outside** production.

---

## Verification checklist (**after** successful replay — operator)

- **Tables:** `public.objects`, `bom_links`, `ncr`, `production_status`
- **Views:** **`public`** views named **`v_*`** (**23** per **8A.0.6**)
- **Functions:** `get_bom_tree`, `get_leaf_summary`, `set_updated_at`
- **Triggers:** `trg_bom_links_updated_at`, `trg_ncr_updated_at`, `trg_objects_updated_at`
- **FKs / indexes** per migration DDL

---

## Strict (respected)

| Rule | Status |
| --- | :---: |
| Production **`db push`** | **not performed** |
| Production remote DDL | **unchanged** |
| **`calculation_snapshots`** in **`migrations/`** root | **no** |

---

## Next gate (after **`BASELINE_REPLAY_VERIFIED`**)

**Stage 8A.0.8** — **`calculation_snapshots`** migration promotion test.

---

## References

- **`supabase/migrations/20260429110000_remote_legacy_baseline.sql`**
- **`docs/AUDITS/2026-04-29_STAGE_8A_0_6_ACTUAL_REMOTE_BASELINE_CAPTURE.md`**
