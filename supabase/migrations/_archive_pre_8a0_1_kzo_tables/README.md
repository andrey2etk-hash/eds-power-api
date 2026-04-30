# Archived pre–Stage 8A.0.1 migration (superseded)

Stage **8A.0.1** replaced KZO-biased **`public.kzo_mvp_snapshots_v1`** naming with system-root **`public.calculation_snapshots`** + **`product_type`** discriminator.

## Historical file

- **`20260429120000_kzo_mvp_snapshots_v1_SUPERSEDED.sql`** — copy of the first draft DDL **before** root governance correction. **Do not apply** as a second migration; canonical **`calculation_snapshots`** DDL is **`../_pending_after_remote_baseline/20260429120000_calculation_snapshots_v1.sql`** (**held** pending **8A.0.2** baseline alignment).

## If already applied in a database

Operators who **already** ran the old migration must **not** assume `supabase db pull` alone fixes governance. Options (choose with DBA): one-time `ALTER TABLE … RENAME`/column add + data copy, or drop empty dev table and re-apply from repo. Record in `docs/AUDITS/` if done.
