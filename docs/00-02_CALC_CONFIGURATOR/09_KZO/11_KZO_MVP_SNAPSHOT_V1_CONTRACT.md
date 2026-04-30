# KZO MVP snapshot contract — `KZO_MVP_SNAPSHOT_V1`

## Purpose

Freeze **one canonical JSON object** representing a **successful KZO MVP end-to-end outcome** (post-**Stage 7A** operational verification) **before** any **Stage 8A** persistence work (e.g. Supabase).

**Governance law:** *Freeze before persistence.* If a field is **not** declared in **`KZO_MVP_SNAPSHOT_V1`**, it **must not** appear as a **required** persisted column in Stage 8A unless a **new snapshot version** (see [Versioning](#versioning-policy)) introduces it through a **separate governed TASK**.

This document is **normative** for Stage 7B / Stage 8A boundary — **Stage 7B** freezes the textual contract **only** (no mandatory DB implementation wording in 7B); **Stage 8A** provides the matching **insert-only** persistence.

---

## Naming alignment (API truth)

Field names under **`KZO_MVP_SNAPSHOT_V1`** intentionally mirror **`POST /api/calc/prepare_calculation`** **`data.*`** keys on **success** (`structural_composition_summary`, …), so that a snapshot can be constructed by **composition** of validated response payload **without renaming** engineering layers.

Legacy alias **“structural_summary”** is **not** used — the canonical key is **`structural_composition_summary`**.

---

## Canonical object — `KZO_MVP_SNAPSHOT_V1`

```json
{
  "snapshot_version": "KZO_MVP_SNAPSHOT_V1",
  "run_status": "SUCCESS",
  "timestamp_basis": "2026-04-29T12:00:00.000Z",
  "logic_version": "KZO_MVP_V1",
  "request_metadata": {
    "request_id": "string",
    "api_version": "0.1.0",
    "logic_version": "KZO_MVP_V1",
    "execution_time_ms": 0
  },
  "normalized_input": {},
  "structural_composition_summary": {},
  "physical_summary": {},
  "physical_topology_summary": {},
  "engineering_class_summary": {},
  "engineering_burden_summary": {}
}
```

### Required fields (success)

| # | Field | Meaning |
| --- | --- | --- |
| 1 | **`snapshot_version`** | Literal **`KZO_MVP_SNAPSHOT_V1`** for this contract revision. |
| 2 | **`run_status`** | **`SUCCESS`** — end state of the run that produced this snapshot. |
| 3 | **`timestamp_basis`** | Single **RFC 3339** / ISO-8601 **UTC** timestamp at which the snapshot is **bound** (producer may use client wall clock when **`status === "success"`** is observed; API metadata does not yet emit a canonical server **completed_at** — see *Timestamp note* below). |
| 4 | **`logic_version`** | Copy of **`data.logic_version`** / normalized payload product logic (e.g. **`KZO_MVP_V1`**). |
| 5 | **`request_metadata`** | Subset aligned with top-level **`metadata`** from **`prepare_calculation`** (`request_id`, `api_version`, `logic_version`, `execution_time_ms`). |
| 6 | **`normalized_input`** | Copy of **`data.normalized_payload`** after successful validation. |
| 7 | **`structural_composition_summary`** | **`data.structural_composition_summary`** — Stage 5A structural meaning. |
| 8 | **`physical_summary`** | **`data.physical_summary`** — Stage 5B footprint scale (MVP). |
| 9 | **`physical_topology_summary`** | **`data.physical_topology_summary`** — Stage 5C topology. |
| 10 | **`engineering_class_summary`** | **`data.engineering_class_summary`** — Stage 6B classification. |
| 11 | **`engineering_burden_summary`** | **`data.engineering_burden_summary`** — Stage 6C burden. |

**Not in V1 envelope (explicit non-inclusion for anti-drift):**

- **`basic_result_summary`**, **`validation_status`**, product **`status`** duplicates — consumers may still read them from raw API **`data`** during transport; **Stage 8A** row design must either **embed** this snapshot as a **JSON column** blob or **materialize** **only** keys listed here as first-class columns (**no** silent addition of pricing/BOM/DB IDs).

### Timestamp note

Until the API adds an explicit **`completed_at`** on **`metadata`**, **`timestamp_basis`** is **governance-owned** at the **producer** (client or orchestration) at success time. Stage 8A persistence may add **`stored_at`** independently.

---

## Versioning policy

| Artifact | Rule |
| --- | --- |
| **`snapshot_version`** | **Monotonic string** labels. **`KZO_MVP_SNAPSHOT_V1`** is the first frozen contract. **`KZO_MVP_SNAPSHOT_V2`** (or later) requires a **normalized IDEA** + updated contract doc; **no silent field add** to V1. |
| **Product `logic_version`** | Continues to follow existing KZO payload enums (e.g. **`KZO_MVP_V1`**). Snapshot version and product logic version are **orthogonal** — both must be recorded. |
| **Compatibility** | Persisted rows **must** store **`snapshot_version`**; readers **must** reject or migrate unknown versions per governance, not ad-hoc SQL. |

---

## Run success / failure states

### `run_status: "SUCCESS"`

- **`run_status`** = **`SUCCESS`**.
- All **required** layers (7–11) are **non-null objects** as returned by **`prepare_calculation`** on **`status: "success"`**.
- **`snapshot_version`** = **`KZO_MVP_SNAPSHOT_V1`**.

### `run_status: "FAILED"`

Use when the **canonical success object cannot be asserted** (validation error, API non-success, transport failure, incomplete **data**).

**Minimum failure envelope** (still **`KZO_MVP_SNAPSHOT_V1`**-versioned for auditability):

```json
{
  "snapshot_version": "KZO_MVP_SNAPSHOT_V1",
  "run_status": "FAILED",
  "timestamp_basis": "2026-04-29T12:00:00.000Z",
  "logic_version": null,
  "failure": {
    "api_status": "validation_error",
    "http_code": 200,
    "error_code": "KZO_REQUIRED_FIELD_MISSING",
    "message": "human-readable",
    "source_field": "payload.field_name"
  },
  "request_metadata": {},
  "normalized_input": null,
  "structural_composition_summary": null,
  "physical_summary": null,
  "physical_topology_summary": null,
  "engineering_class_summary": null,
  "engineering_burden_summary": null
}
```

**Rules:**

- **Do not** invent partial engineering layers on failure.
- **`failure.api_status`** aligns with top-level **`status`** from API when present (`validation_error`, …).
- If **no response body** (network), **`failure`** holds transport-level code only — still **`FAILED`**.

---

## Optional later (explicitly out of V1)

These **must not** be required in **`KZO_MVP_SNAPSHOT_V1`**:

- Pricing, BOM, procurement, exact kg, CAD refs  
- Database primary keys / Supabase **`uuid`**  
- Revision graph / ECO chain  

They may arrive only under a **future** **`snapshot_version`** plus **IDEA** approval.

---

## Stage 8A (Supabase persistence MVP) relationship

Normative guidance:

- **`POST /api/kzo/save_snapshot`** (see `main.py`) accepts a **full** **`KZO_MVP_SNAPSHOT_V1`** JSON body, validates allow-listed keys, and **INSERT**s one row into **`calculation_snapshots`** with **`product_type`** = **`KZO`** (DDL: `supabase/migrations/_pending_after_remote_baseline/20260429120000_calculation_snapshots_v1.sql` — held until **`LEGACY_REMOTE_BASELINE`** baseline migration precedes **`db push`**, Stage **8A.0.2**).
- Persistence **stores contract JSON verbatim** (`JSONB` columns) — **no** BOM/pricing/engineering decomposition, **no** mutation endpoint.
- **Environment:** **`SUPABASE_URL`** + **`SUPABASE_SERVICE_ROLE_KEY`** required on API host — see **`.env.example`**.
- **IDEA:** **IDEA-0017** **`ACTIVE`** (operative **`PENDING_SUPABASE_VERIFICATION`** until **`docs/AUDITS/2026-04-29_STAGE_8A_SUPABASE_LIVE_VERIFICATION_GATE.md`** records **LIVE PASS**); mapping **`13_KZO_MVP_SNAPSHOT_V1_SQL_MAPPING.md`**; separation **`14_CALC_TRUTH_VS_PERSISTENCE_STAGE_8A.md`**.

---

## References

- `main.py` — `prepare_calculation` success **`data`** shape  
- **`docs/AUDITS/2026-04-29_STAGE_7B_KZO_MVP_SNAPSHOT_CONTRACT_FREEZE.md`** — “freeze before persistence” audit  
- **`docs/AUDITS/2026-04-29_STAGE_7A_KZO_END_TO_END_MVP_STABILIZATION.md`** — operational cohesion prerequisite  
