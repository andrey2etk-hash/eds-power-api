# Stage 8A — Supabase live verification gate

## Purpose

Prove **end-to-end** that **`KZO_MVP_SNAPSHOT_V1`** persistence works against **live** Supabase and **live** API host (e.g. Render): migration applied, service role env present, **INSERT** succeeds, row visible in **`calculation_snapshots`** (`product_type` = **`KZO`**).

This gate is **verification only** — no schema changes, no contract changes, no new persistence features.

---

## Governance: when **IDEA-0017** may be **`IMPLEMENTED`**

Per master table **Status Values**, **`IDEA-0017`** stays **`ACTIVE`** with operative sub-state **`PENDING_SUPABASE_VERIFICATION`** until **all** items below are satisfied and recorded in this document under **Live PASS record**.

After **LIVE PASS** is recorded: set **`IDEA-0017`** to **`IMPLEMENTED`** in `docs/00_SYSTEM/12_IDEA_MASTER_LOG.md` and sync status docs.

---

## Preconditions (operator / deployer)

| Step | Check | Done |
| --- | --- | --- |
| 1 | **Baseline + `calculation_snapshots`** aligned per **Stage 8A.0.2**: legacy registry **`LEGACY_REMOTE_BASELINE.md`**; DDL file present (**held** pending baseline): **`supabase/migrations/_pending_after_remote_baseline/20260429120000_calculation_snapshots_v1.sql`** | ☐ (operator) |
| 2 | Migration **applied** in target Supabase project (SQL editor or `supabase db push`) | ☐ |
| 3 | Render (or API host) env: **`SUPABASE_URL`**, **`SUPABASE_SERVICE_ROLE_KEY`** set | ☐ |
| 4 | API **redeployed** after env + code that exposes `POST /api/kzo/save_snapshot` | ☐ |

---

## Canonical success response (deployed API)

The implementation in `main.py` returns **no** `snapshot_saved` field. Success envelope:

```json
{
  "status": "SUCCESS",
  "snapshot_id": "<UUID>",
  "snapshot_version": "KZO_MVP_SNAPSHOT_V1",
  "persistence_status": "STORED"
}
```

**LIVE PASS** requires: **`status`** = **`SUCCESS`**, **`persistence_status`** = **`STORED`**, non-empty **`snapshot_id`** (UUID string).

Validation / insert failure:

```json
{
  "status": "FAILED",
  "persistence_status": "REJECTED",
  "error_code": "<code>"
}
```

---

## Live POST (steps 5–6)

- **URL:** `POST https://<api-host>/api/kzo/save_snapshot`
- **Headers:** `Content-Type: application/json`
- **Body:** full **`KZO_MVP_SNAPSHOT_V1`** JSON (e.g. built from **`prepare_calculation`** success **`data`** + contract fields — see **`11_KZO_MVP_SNAPSHOT_V1_CONTRACT.md`**).

Minimal probes:

- **`run_status`** **`FAILED`** with valid **`failure`** object — validates transport (does **not** alone prove the **SUCCESS** path through all SUCCESS-only layers).

For full **SUCCESS** persistence proof, use a **`SUCCESS`** snapshot with required layer dicts and **`logic_version`** / **`request_metadata`** / **`normalized_input`** per `kzo_snapshot_persist.validate_kzo_mvp_snapshot_v1`.

---

## Database verification (step 7)

In Supabase **Table Editor** or SQL:

```sql
select id, product_type, snapshot_version, run_status, created_at
from public.calculation_snapshots
order by created_at desc
limit 5;
```

**LIVE PASS** requires at least **one** row whose **`id`** equals **`snapshot_id`** from the success response.

---

## Automated probe (Cursor environment, **not** a PASS)

**Date:** 2026-04-29  
**Target:** `POST https://eds-power-api.onrender.com/api/kzo/save_snapshot`  
**Payload:** minimal valid **`FAILED`** snapshot (contract-valid **`KZO_MVP_SNAPSHOT_V1`** shape).

**Result:** **HTTP 404 Not Found.**

**Interpretation:** the public Render deployment **did not** expose this route at probe time — most likely **stale deployment** (Stage 8A route not shipped) or incorrect service URL. **This is not LIVE PASS.**

---

## Live PASS record

**Status:** **PENDING**

When complete, fill:

| Field | Value |
| --- | --- |
| Date (UTC) | |
| Operator | |
| API base URL | |
| **`snapshot_id` returned** | |
| Row confirmed in **`calculation_snapshots`** (`product_type` = **`KZO`**) | yes / no |

**External reviewer note:** paste redacted **`snapshot_id`** only; omit secrets.

---

## References

- `docs/AUDITS/2026-04-29_STAGE_8A_0_2_SUPABASE_REMOTE_BASELINE_ALIGNMENT.md`
- `docs/AUDITS/2026-04-29_STAGE_8A_0_1_ROOT_MIGRATION_GOVERNANCE_CORRECTION.md`
- `docs/AUDITS/2026-04-29_STAGE_8A_SUPABASE_FIRST_PERSISTENCE_MVP.md`
- `docs/00-02_CALC_CONFIGURATOR/09_KZO/13_KZO_MVP_SNAPSHOT_V1_SQL_MAPPING.md`
- `docs/00-02_CALC_CONFIGURATOR/09_KZO/11_KZO_MVP_SNAPSHOT_V1_CONTRACT.md`
