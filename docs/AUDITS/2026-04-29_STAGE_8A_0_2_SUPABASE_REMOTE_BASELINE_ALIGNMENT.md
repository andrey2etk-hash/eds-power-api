# Stage **8A.0.2** — Supabase remote baseline alignment (governance + hold)

## Purpose

The **production / live** Supabase project is **not empty**: **`public`** already contains **`legacy_baseline`** objects (manual or pre-repo). Local repo migrations historically **did not** reflect that baseline. Stage **8A.0.2** brings governance **documentation** and temporarily **holds** additive **`calculation_snapshots`** DDL from the **`migrations/`** root so **`db push`** is not casually run **without** baseline alignment.

## Strict execution boundary (THIS stage)

| Action | Allowed |
| --- | :---: |
| Modify live DB from this TASK | **no** |
| `supabase db push` | **no** |
| Drop / rename legacy tables or `v_*` views | **no** |
| KZO rollback of unrelated legacy artefacts | **no** |

---

## Problem statement

Remote **`public`** includes at minimum:

| Object | Classification |
| --- | --- |
| **`objects`** | `legacy_baseline` |
| **`bom_links`** | `legacy_baseline` |
| **`ncr`** | `legacy_baseline` |
| **`production_status`** | `legacy_baseline` |
| **`v_*`** views | `legacy_baseline` |

Canonical registry: **`supabase/schema_registry/LEGACY_REMOTE_BASELINE.md`** (**status** **`LEGACY_REMOTE_SCHEMA_DETECTED`**).

---

## Governance decisions

1. **`legacy_baseline`** — preserve until **separately audited** (dedicated IDEA if remediation ever needed).
2. **Additive only —** **`calculation_snapshots`** (**Stage 8A.0.1**) is **additive** with respect to legacy objects; MVP persistence must **not** depend on removing legacy schema.
3. **Hold canonical DDL —** **`20260429120000_calculation_snapshots_v1.sql`** relocated to **`supabase/migrations/_pending_after_remote_baseline/`** until baseline migration precedes it in **`migrations/`** root ordering.

---

## Deliverables implemented in repo

| Deliverable |
| --- |
| **`supabase/schema_registry/LEGACY_REMOTE_BASELINE.md`** |
| **`supabase/migrations/_pending_after_remote_baseline/`** (+ held SQL + README) |
| Updated **`supabase/README.md`**, **`supabase/migrations/README.md`** |

---

## Next safe technical step (NOT executed in **8A.0.2**)

1. **Against a clone / readonly snapshot** — export authoritative **`CREATE TABLE`/`CREATE VIEW`** (or `supabase db dump` scoped to `public`) for legacy objects listed in **`LEGACY_REMOTE_BASELINE.md`**.
2. **Author one or more migrations** numbered **before** **`calculation_snapshots`** restoring **parity** between remote and migration history (**no destructive DDL** unless future audited IDEA explicitly approves).
3. **Move** **`_pending_after_remote_baseline/20260429120000_calculation_snapshots_v1.sql`** into **`supabase/migrations/`** after baseline migrations.
4. **Dry-run `db push`** on a disposable Supabase branch or staging project — **still** **`no`** unreviewed **`db push`** to production inside this TASK.

---

## References

- **`supabase/schema_registry/LEGACY_REMOTE_BASELINE.md`**
- **`docs/AUDITS/2026-04-29_STAGE_8A_0_1_ROOT_MIGRATION_GOVERNANCE_CORRECTION.md`** (prior naming governance)
- **IDEA-0020** — **`docs/00_SYSTEM/12_IDEA_MASTER_LOG.md`**
