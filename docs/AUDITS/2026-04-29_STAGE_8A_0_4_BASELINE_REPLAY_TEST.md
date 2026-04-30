# Stage **8A.0.4** — Baseline DDL fill + local replay test

## Objective

Replace the noop body of **`supabase/migrations/20260429110000_remote_legacy_baseline.sql`** with **schema-only** DDL mirrored from live remote **`public`**, then verify **`migrate` / `db reset`** on a **local or disposable** database — **no production `db push`**, no data dumps.

## Strict boundary (this audit)

| Constraint | Result |
| --- | :---: |
| Production remote **`db push`** | **not performed** |
| Remote schema mutation | **none** |
| Data / `COPY` / `INSERT` in baseline | **none** (N/A — DDL not committed) |
| **`calculation_snapshots_v1.sql`** moved to `migrations/` root | **no** — remains **`_pending_after_remote_baseline/`** |
| KZO-specific DB expansion | **none** |

---

## DDL source method (intended vs actual)

| Role | Method / outcome |
| --- | --- |
| **Intended** | `pg_dump "$DATABASE_URL" --schema-only --schema=public --no-owner --no-acl` (filter to `objects`, `bom_links`, `ncr`, `production_status`, all `public.v_*`) **or** Supabase CLI **`db dump`** schema-only equivalent |
| **Actual (this session)** | **Not executed** — agent host **`BLOCKED_BY_LOCAL_TOOLING`**: `supabase`, `docker`, `npx`, and **`pg_dump`** were **not available** on PATH (PowerShell **`Get-Command`** / **`where.exe`**). |

---

## Captured objects

**Not captured in repo** — baseline file body is still the **noop `DO` block**. Declared baseline set (registry / remote contract) unchanged:

- **`public.objects`**, **`public.bom_links`**, **`public.ncr`**, **`public.production_status`**
- **`public.v_*`** views (explicit names TBD from remote introspection)

---

## Schema-only confirmation

**N/A** — no factual DDL was appended. When operator runs capture: enforce **schema-only**; strip **roles/owner** lines if noisy; forbid **`COPY`** / **`INSERT`**.

---

## Replay result

**Not run** — depends on factual DDL + local Supabase (**`supabase db reset`**) or equivalent disposable Postgres. **`calculation_snapshots`** must **not** be applied until baseline replay **PASS** is recorded in a superseding audit amendment or new operator note.

---

## May **`calculation_snapshots` move next?**

**No.** **`BASELINE_REPLAY_VERIFIED`** was **not** achieved; **`calculation_snapshots_v1.sql`** stays in **`supabase/migrations/_pending_after_remote_baseline/`** until **`8A.0.4`** is re-run successfully with tooling.

---

## Final stage status (**8A.0.4**)

**`BLOCKED_BY_LOCAL_TOOLING`**

Interpretation:

- Repo governance and ordering remain valid (**8A.0.3** scaffold slot).
- **Operator unblock:** install Postgres client / Supabase CLI + Docker (or run dump from CI with **`DATABASE_URL`** secret), paste filtered DDL into **`20260429110000_remote_legacy_baseline.sql`**, then **`supabase db reset`** locally and re-audit **`PASS`** / **`FAIL`**.

---

## References

- **`supabase/schema_registry/LEGACY_REMOTE_BASELINE.md`**
- **`docs/AUDITS/2026-04-29_STAGE_8A_0_3_REMOTE_BASELINE_CAPTURE.md`**
- Linked project ref (no secrets): **`supabase/.temp/linked-project.json`**
