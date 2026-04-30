# SQL migrations — rules

## Stage **8A.1** active chain (local verified)

| File | Role |
| --- | --- |
| **`20260429110000_remote_legacy_baseline.sql`** | Legacy **`public`** baseline (factual DDL from remote capture — **8A.0.6**). Applies **first**. |
| **`20260429120000_calculation_snapshots_v1.sql`** | **`public.calculation_snapshots`** — KZO-first row discriminator (`product_type = 'KZO'`); contract id **`KZO_MVP_SNAPSHOT_V1`**. Promoted from **`_pending_after_remote_baseline/`** after baseline replay (**8A.1** audit). Applies **second**. |

Lexicographic order (`YYYYMMDDHHMMSS`) = apply order (`110000` then `120000`).

**Freeze window:** no ad-hoc Dashboard edits to legacy objects listed in **`supabase/schema_registry/LEGACY_REMOTE_BASELINE.md`** during baseline governance unless a new IDEA/TASK explicitly remediates capture.

---

## Folder `_pending_after_remote_baseline/`

**`calculation_snapshots`** DDL — **promoted (8A.1)**. This folder remains for future **held** migrations that must trail an authoritative baseline — see **`README.md`** inside that folder.

## Conventions

- **Timestamp lexicographic order** dictates apply order (**`YYYYMMDDHHMMSS_*.sql`**).
- **`README.md`** files in **`migrations/`** are skipped by CLI (no timestamp prefix).

## Archive

**`_archive_pre_8a0_1_kzo_tables/`** — superseded **`kzo_mvp_snapshots_v1`** draft only.
