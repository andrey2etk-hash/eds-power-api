# Stage **8B.1A** — API `save_snapshot` contract implementation

**Purpose.** Record **`TASK-2026-08B-012`** code landed per **`docs/AUDITS/2026-04-30_STAGE_8B_1A_API_SAVE_CONTRACT_GOVERNANCE_PLAN.md`**.

## Status

**`STAGE_8B_1A_API_CONTRACT_IMPLEMENTED`**

Exit **E5** (live/staging smoke with **`created_at`** + **`client_type`**) remains **operator-owned** after deploy — run **`POST /api/kzo/save_snapshot`** against a **`SUCCESS`** **`KZO_MVP_SNAPSHOT_V1`** body that satisfies **L3 + L4** (see validation rules below).

---

## What changed (code)

| Area | Detail |
| --- | --- |
| **`kzo_snapshot_persist.validate_kzo_mvp_snapshot_v1`** | Returns **`(row, error_code, aux)`** with **`aux.l1_snapshot_version_ok`** for response **`snapshot_version`** on reject. **L3:** five engineering layers are non-empty **`dict`**. **L4 (SUCCESS only):** **`request_metadata`** must include **`request_id`**, **`api_version`**, **`logic_version`**, **`execution_time_ms`** (non-negative **`int`**; **`request_id`** / version strings non-empty). **Traceability:** top-level **`logic_version`** must equal **`request_metadata.logic_version`** (trimmed). **FAILED:** **`failure.error_code`** and **`failure.message`** required; **`request_metadata`** / **`normalized_input`** type guards if present. |
| **`kzo_snapshot_persist.insert_snapshot_row`** | Returns **`(snapshot_id, created_at_iso, error_code)`** — reads **`created_at`** from insert response or follow-up **`select`**. |
| **`main.py` `save_snapshot`** | Reads **`X-EDS-Client-Type`**, normalizes to **`GAS` \| `WEB` \| `MOBILE` \| `AGENT` \| `UNKNOWN`**. **Success:** **`status`**, **`snapshot_id`**, **`persistence_status`**, **`snapshot_version`**, **`created_at`**, **`client_type`**, **`failure: null`**, **`error_code: null`**. **Failure:** **`persistence_status`** **`REJECTED`** (validation) or **`ERROR`** (insert / unavailable); unified **`failure`** object; top-level **`error_code`** mirrors **`failure.error_code`** for legacy consumers (e.g. GAS logger). **No** call to **`prepare_calculation`**. |

## Normative docs updated

- **`docs/00_SYSTEM/13_CLIENT_AGNOSTIC_PERSISTENCE_CONTRACT_V1.md`** **§4** — **`client_type`**, clarified success/failure, removed “runtime lags normative target” caveat for these fields.

## Explicit non-scope (unchanged)

- **No** GAS / Sheet / Web / Mobile changes in this TASK.
- **No** DDL / migration (**`created_at`** already on **`calculation_snapshots`**).

## Operator smoke (post-deploy)

Use a **`SUCCESS`** body built from **`prepare_calculation`** success **`data`**, with **`snapshot_version`**, **`run_status`** **`SUCCESS`**, **`timestamp_basis`**, mirrored **`logic_version`** in top-level + **`request_metadata`**, **`normalized_input`** copy of **`normalized_payload`**, all five summaries **non-empty** objects. Optionally set **`X-EDS-Client-Type: GAS`**.

Verify JSON includes **`created_at`** and **`client_type`**.

---

_End of Stage 8B.1A API contract implementation dossier._
