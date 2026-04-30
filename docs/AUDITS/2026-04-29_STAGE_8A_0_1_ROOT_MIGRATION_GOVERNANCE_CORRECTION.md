# Stage 8A.0.1 — Root migration governance correction (CRITICAL)

## Purpose

Remove **KZO-as-table-root** bias from the first persistence migration so Supabase remains **EDS Power system memory**; **KZO** is **first consumer** on the **row** (`product_type`), not owner of the root table name.

## Issue addressed

- **Before:** `public.kzo_mvp_snapshots_v1` (product-coded table name).
- **After:** `public.calculation_snapshots` + **`product_type = 'KZO'`** + unchanged **`snapshot_version = KZO_MVP_SNAPSHOT_V1`** (Stage **7B** contract id — **not** a table namespace).

## Proof: Stage 7B payload unchanged

| Item | Status |
| --- | --- |
| JSON snapshot body (`KZO_MVP_SNAPSHOT_V1`) | **Unchanged** — still no `product_type` in client JSON; API sets **`KZO`** on INSERT |
| `snapshot_version`, layer JSONB columns | **Preserved** |
| `prepare_calculation` | **Unchanged** |

## Evidence (repo)

| Artifact | Change |
| --- | --- |
| Migration | **`supabase/migrations/_pending_after_remote_baseline/20260429120000_calculation_snapshots_v1.sql`** (**canonical DDL** — **held** pending **Stage 8A.0.2** baseline; previously at `migrations/` root until **IDEA-0020**) |
| Superseded draft | **`supabase/migrations/_archive_pre_8a0_1_kzo_tables/`** |
| Persist module | **`kzo_snapshot_persist.py`** → table **`calculation_snapshots`**, **`product_type`** **`KZO`** |

## Operational note

If **`kzo_mvp_snapshots_v1`** was **already** created from the old migration in a DB, **do not** blindly `db push` a second genesis — use manual migration / dev reset documented in **`supabase/migrations/README.md`**.

## Governance rule (explicit)

**`TABLE = SYSTEM`**, **`ROW = PRODUCT`**. Root tables MUST NOT encode a product line; product specificity only via discriminators (**`product_type`**, **`snapshot_version`**, envelope JSON).

## References

- **IDEA-0019** — `docs/00_SYSTEM/12_IDEA_MASTER_LOG.md`
- **`supabase/README.md`**, **`domains/snapshots/README.md`**
- **`13_KZO_MVP_SNAPSHOT_V1_SQL_MAPPING.md`**
