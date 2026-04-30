# Stage 8A — Supabase first persistence MVP (audit)

## Purpose

Establish **trusted storage** for **`KZO_MVP_SNAPSHOT_V1`**:

- Single system table **`calculation_snapshots`**, **`product_type = 'KZO'`** for MVP (**append-only**, **JSONB** payload columns). **8A.0.1** superseded **`kzo_mvp_snapshots_v1`** naming — see **`2026-04-29_STAGE_8A_0_1_ROOT_MIGRATION_GOVERNANCE_CORRECTION.md`**. **8A.0.2:** canonical DDL **held** (**`_pending_after_remote_baseline/`**) until remote **legacy baseline** migrations align repo with non-empty **`public`** — **`2026-04-29_STAGE_8A_0_2_SUPABASE_REMOTE_BASELINE_ALIGNMENT.md`** / **`LEGACY_REMOTE_BASELINE.md`**.
- **Persistence without redesign**: `POST /api/kzo/save_snapshot` does **not** call `prepare_calculation` logic and does **not** expand the MVP calculation contract.

## Proof: persistence without redesign

| Check | Evidence |
| --- | --- |
| Separation of endpoints | **`/api/calc/prepare_calculation`** unchanged for calculation truth; **`/api/kzo/save_snapshot`** validates + INSERT only |
| No new engineering parameters | Payload allow-list matches **`KZO_MVP_SNAPSHOT_V1`** (`kzo_snapshot_persist.validate_kzo_mvp_snapshot_v1`) |
| Frozen V1 only | **`snapshot_version`** CHECK = **`KZO_MVP_SNAPSHOT_V1`** |
| Anti-inflation | Rejects unknown top-level keys on snapshot body |
| System root table | **`calculation_snapshots`** — product on **`product_type`** row |
| No retrieval / analytics route | Endpoint returns **`snapshot_id`** + status only |

## Operational requirements

Set **`SUPABASE_URL`** + **`SUPABASE_SERVICE_ROLE_KEY`** on the API host (e.g. Render).

Apply **`calculation_snapshots`** DDL only **after Stage 8A.0.2** remote baseline migrations exist in **`supabase/migrations/`** ahead of ordering: DDL source (**currently held**) — **`supabase/migrations/_pending_after_remote_baseline/20260429120000_calculation_snapshots_v1.sql`** — see **`supabase/schema_registry/LEGACY_REMOTE_BASELINE.md`**, audit **`docs/AUDITS/2026-04-29_STAGE_8A_0_2_SUPABASE_REMOTE_BASELINE_ALIGNMENT.md`**.

Without env + table → **`SNAPSHOT_PERSISTENCE_UNAVAILABLE`** (insert rejected).

**Live verification:** **`docs/AUDITS/2026-04-29_STAGE_8A_SUPABASE_LIVE_VERIFICATION_GATE.md`** (`IDEA-0017` **`IMPLEMENTED`** only after PASS recorded there).

## References

- **`supabase/schema_registry/LEGACY_REMOTE_BASELINE.md`**
- **`docs/AUDITS/2026-04-29_STAGE_8A_0_2_SUPABASE_REMOTE_BASELINE_ALIGNMENT.md`**
- **`docs/00-02_CALC_CONFIGURATOR/09_KZO/11_KZO_MVP_SNAPSHOT_V1_CONTRACT.md`**
- **`docs/00-02_CALC_CONFIGURATOR/09_KZO/13_KZO_MVP_SNAPSHOT_V1_SQL_MAPPING.md`**
- **`docs/00-02_CALC_CONFIGURATOR/09_KZO/14_CALC_TRUTH_VS_PERSISTENCE_STAGE_8A.md`**
- **`kzo_snapshot_persist.py`**, **`main.py`** `save_snapshot`
