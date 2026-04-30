# `KZO_MVP_SNAPSHOT_V1` ↔ `calculation_snapshots` (Stage 8A / 8A.0.1)

## Rule

Persistence **stores the contract verbatim** as JSON-compatible columns (`JSONB`). **No** ERP-style decomposition into separate normalized tables.

**Governance (Stage 8A.0.1):** **`TABLE = SYSTEM`**, **`ROW = PRODUCT`**. The Postgres table is **`public.calculation_snapshots`** (neutral). **KZO** is the first consumer via the **`product_type`** column (`'KZO'`), not via a KZO-prefixed table name. **`snapshot_version`** remains the frozen contract id **`KZO_MVP_SNAPSHOT_V1`** (Stage 7B).

| Canonical snapshot field (`KZO_MVP_SNAPSHOT_V1`) | Postgres column |
| --- | --- |
| _(API-injected for MVP)_ | `product_type` TEXT — **`'KZO'`** (system root; product on row) |
| _(generated UUID)_ | `id` UUID `DEFAULT gen_random_uuid()` |
| `snapshot_version` | `snapshot_version` TEXT CHECK `KZO_MVP_SNAPSHOT_V1` |
| `run_status` | `run_status` TEXT |
| `timestamp_basis` | `timestamp_basis` TIMESTAMPTZ |
| `logic_version` | `logic_version` TEXT (`NULL` allowed for FAILED envelopes) |
| `request_metadata` | `request_metadata` JSONB |
| `normalized_input` | `normalized_input` JSONB |
| `structural_composition_summary` | `structural_composition_summary` JSONB |
| `physical_summary` | `physical_summary` JSONB |
| `physical_topology_summary` | `physical_topology_summary` JSONB |
| `engineering_class_summary` | `engineering_class_summary` JSONB |
| `engineering_burden_summary` | `engineering_burden_summary` JSONB |
| `failure` | `failure` JSONB (NULL on SUCCESS) |
| _(server `NOW()`)_ | `created_at` TIMESTAMPTZ DEFAULT NOW() |

**API:** `POST /api/kzo/save_snapshot` — body is the JSON snapshot object (not the `prepare_calculation` envelope). **`product_type`** is **not** sent in the snapshot JSON; the API sets **`KZO`** on insert.

Migration DDL (canonical, **currently held — Stage 8A.0.2** — move to **`migrations/`** after legacy baseline migrations): **`supabase/migrations/_pending_after_remote_baseline/20260429120000_calculation_snapshots_v1.sql`**.  
Legacy draft (do not apply): `supabase/migrations/_archive_pre_8a0_1_kzo_tables/20260429120000_kzo_mvp_snapshots_v1_SUPERSEDED.sql`.
