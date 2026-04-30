# Stage **8A.0.3** — Remote baseline capture

## Objective

Establish a **migration slot** representing live Supabase **`public`** legacy schema **without** altering the remote database. **Capture-only**: operator pastes factual schema-only DDL before **Stage 8A.0.4** replay.

## Strict execution boundary (THIS stage)

| Action | Allowed in repo / agent session |
| --- | :---: |
| Live **`db push`** / apply migrations to remote | **no** |
| New prod tables beyond legacy mirror | **no** |
| `calculation_snapshots` promotion from **`_pending_after_remote_baseline/`** | **no** |

---

## Gemini / governance prerequisite

Upstream **Stage 8A.0.2** (remote baseline alignment) passed **Gemini audit** — this stage proceeds under additive / no-destructive rules.

---

## Baseline migration artifact

| Field | Value |
| --- | --- |
| **Filename** | **`supabase/migrations/20260429110000_remote_legacy_baseline.sql`** |
| **Ordering** | **`20260429110000` < `20260429120000`** (before **`calculation_snapshots_v1`**) |
| **`calculation_snapshots`** | Still **held** in **`supabase/migrations/_pending_after_remote_baseline/20260429120000_calculation_snapshots_v1.sql`** |

### Capture status (truthful)

Cursor agent session **cannot** run **Supabase CLI** or **`npx supabase`** (tooling absent on PATH). Migration file commits a **PostgreSQL-valid scaffold** (**`DO … NULL`**) plus **paste instructions**.

**Operator must replace** scaffold body with **schema-only** DDL from **`pg_dump`** / Supabase **dump** for:

- **`public.objects`**
- **`public.bom_links`**
- **`public.ncr`**
- **`public.production_status`**
- All **`public.v_*`** views (explicit **`CREATE VIEW`** list)

until then, **baseline DDL is NOT yet replay-verified**.

---

## Remote freeze rule (operators)

Until factual DDL is committed and verified on **staging** (**8A.0.4**): **no** manual Supabase Dashboard **DDL** edits to listed legacy **`public`** objects (data CRUD unrelated to DDL may continue per local policy).

---

## Risks / next gate

| Risk | Mitigation |
| --- | --- |
| Scaffold committed without pasted DDL breaks **meaningful** `migrate` parity | Paste dump before **`db push`** / CI migration on clean DB (**8A.0.4**) |
| Full `public` dump noise | Filter dump to retained objects only; document filter in IDEA notes |

**Next stage:** **`8A.0.4` — Local replay / staging verification** (`migrate`/`db push` to disposable project).

---

## Final status (**Stage**)

**`BASELINE_CAPTURED_PENDING_REPLAY_TEST`** — interpreted as:

- Repo contains **ordering-correct baseline migration shell** + **freeze / procedure** documented;
- **Factual** remote DDL **embedded** pending operator CLI (same stage ID until **`8A.0.4` PASS**).

---

## References

- **`supabase/schema_registry/LEGACY_REMOTE_BASELINE.md`**
- **`docs/AUDITS/2026-04-29_STAGE_8A_0_2_SUPABASE_REMOTE_BASELINE_ALIGNMENT.md`**
