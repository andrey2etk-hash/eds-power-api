# Stage **8B.1A** — LIVE verification gate (`save_snapshot`)

**Purpose.** Close **`TASK-2026-08B-012`** **E5** operator gate after **Gemini pre-live PASS** (**`docs/AUDITS/2026-04-30_STAGE_8B_1A_GEMINI_PRELIVE_AUDIT.md`**) and **Render** deployment of **`main`** at **`551ce87`** (**Stage 8B.1A** API hardening).

## Preconditions

| # | Gate |
| --- | --- |
| G1 | **Gemini pre-live verdict = PASS** (human-recorded attestation linked to Gemini output) |
| G2 | **Render** build points at **`main`** **≥** **`551ce87`** (`Implement Stage 8B.1A API save_snapshot hardening and governance audits`) |
| G3 | **No** DDL / migrations in this TASK; **`SUPABASE_URL`** + **`SUPABASE_SERVICE_ROLE_KEY`** configured on Render (same pattern as **`STAGE_8A`** live gate) |
| G4 | **No** GAS / client orchestration tests in this dossier (**STRICT** scope) |

## Deploy note

**2026-04-30:** Changes **committed + pushed**: **`551ce87`** (`origin/main`).  
**Automated Cursor smoke** immediately after push against **`https://eds-power-api.onrender.com`** did **not** yet show **8B.1A** HTTP envelope fields (**`client_type`**, **`failure`**, richer success body) → treat as **either** stale build / cold deploy latency **or** **`SNAPSHOT_PERSISTENCE_UNAVAILABLE`** (Supabase env on host).  
**Operator must re-run Sections A–E** after Dashboard confirms deploy + env.

---

## Canonical response reminders (avoid doc drift)

- Top-level **`status`** is **`SUCCESS`** or **`FAILED`** — **not** `REJECTED` at this field. **`persistence_status`** carries **`STORED`** / **`REJECTED`** / **`ERROR`**.
- **L3 reject** canonical **`error_code`:** **`SNAPSHOT_SUCCESS_LAYER_INVALID`** ( **`physical_topology_summary: null`** or empty layer ).
- **L4 traceability reject** canonical **`error_code`:** **`SNAPSHOT_LOGIC_VERSION_METADATA_MISMATCH`** ( root **`logic_version`** ≠ **`request_metadata.logic_version`** ).

(Informal synonyms like “INVALID_SNAPSHOT_STRUCTURE” / “LOGIC_VERSION_MISMATCH” are **not** emitted by **`main`** **551ce87**.)

---

## A — Valid **`SUCCESS`** body + **`X-EDS-Client-Type: GAS`**

**HTTP:** `POST /api/kzo/save_snapshot`  
**Headers:** `Content-Type: application/json`, **`X-EDS-Client-Type: GAS`**

Minimal **contract-valid** **L3+L4** body (engineering layers deliberately minimal but **non-empty** objects):

```json
{
  "snapshot_version": "KZO_MVP_SNAPSHOT_V1",
  "run_status": "SUCCESS",
  "timestamp_basis": "2026-04-30T18:00:00.000Z",
  "logic_version": "KZO_MVP_V1",
  "request_metadata": {
    "request_id": "live-gate-A-001",
    "api_version": "0.1.0",
    "logic_version": "KZO_MVP_V1",
    "execution_time_ms": 1
  },
  "normalized_input": { "_note": "smoke" },
  "structural_composition_summary": { "smoke": true },
  "physical_summary": { "smoke": true },
  "physical_topology_summary": { "smoke": true },
  "engineering_class_summary": { "smoke": true },
  "engineering_burden_summary": { "smoke": true }
}
```

**PASS if** JSON contains:

| Field | Expected |
| --- | --- |
| **`status`** | **`SUCCESS`** |
| **`persistence_status`** | **`STORED`** |
| **`snapshot_id`** | non-null UUID |
| **`snapshot_version`** | **`KZO_MVP_SNAPSHOT_V1`** |
| **`created_at`** | ISO-8601 |
| **`client_type`** | **`GAS`** |
| **`failure`** | **`null`** |

---

## B — Header telemetry — **`WEB`**

Same **valid** **`SUCCESS`** body as **A**, header **`X-EDS-Client-Type: WEB`**.  
**PASS if** **`client_type`** **`WEB`** **and** persistence outcome matches **A** (assuming Supabase OK).

---

## C — **L3** negative (**null** layer )

Start from **A** payload; set **`physical_topology_summary`** **`null`**.

**PASS if:**

| Field | Expected |
| --- | --- |
| **`status`** | **`FAILED`** |
| **`persistence_status`** | **`REJECTED`** |
| **`snapshot_version`** | **`KZO_MVP_SNAPSHOT_V1`** (version label passed **L1** before layer check) |
| **`error_code`** | **`SNAPSHOT_SUCCESS_LAYER_INVALID`** |
| **`failure`** | Object with **`error_code`**, **`message`**, **`details`** mirroring **`error_code`** |
| **`client_type`** | Echo (e.g. **`GAS`** if header sent) |

---

## D — **L4** negative (logic mismatch)

Same as **A** but **`request_metadata.logic_version`** ≠ root **`logic_version`** (example: root **`KZO_MVP_V1`**, metadata **`OTHER`**).

**PASS if:** **`FAILED`**, **`REJECTED`**, **`error_code`** **`SNAPSHOT_LOGIC_VERSION_METADATA_MISMATCH`**, structured **`failure`**, echoed **`client_type`**.

---

## E — DB verification (**Supabase SQL / dashboard**)

For **`snapshot_id`** from **successful** **A or B**:

```sql
select id,
       snapshot_version,
       created_at,
       run_status,
       logic_version,
       timestamp_basis
from   public.calculation_snapshots
where  id = '<snapshot_id from response>';
```

**PASS if:**

- Exactly **one** row;
- **`created_at`** is consistent with **`created_at`** in HTTP response (**same instant**, allowing string formatting/timezone normalization).

(Service role REST already used server-side — **operator** verifies read-only.)

---

## Automated probe log (Cursor, **2026-04-30**)

| Probe | Observation |
| --- | --- |
| **Timing** | Within minutes of **`551ce87`** **`git push`** (Render redeploy latency not guaranteed saturated) |
| **A/B shape** | Response body ** lacked** **`client_type`**, **`failure`**, **`created_at`** fields → **production did not yet expose **`8B.1A`** envelope** OR response path bypassed hardened handler |
| **A** | **`SNAPSHOT_PERSISTENCE_UNAVAILABLE`** (flat **`error_code`**) — persisted env / deploy state **or** stale build |
| **C** (null layer) | Legacy-style **`SNAPSHOT_SUCCESS_LAYER_MISSING`** string observed on first batch — inconsistent with **`551ce87`** codebase (**→ stale image**) |

**Action:** Repeat **Sections A–E** after Render Dashboard shows successful deploy + **`SUPABASE_*`** healthy.

---

## Final status registry

| Label | Meaning |
| --- | --- |
| **`STAGE_8B_1A_LIVE_VERIFIED`** | Operator signed **A–E** **PASS** on live host serving **551ce87** envelope + Gemini **G1** |
| **`STAGE_8B_1A_LIVE_VERIFICATION_PENDING`** | Push complete; prod smoke incomplete or inconclusive (**this dossier baseline after Cursor probe**) |

---

## Next

**Stage 8B.1B** — **`TASK-2026-08B-011`** Thin GAS Client Adapter (**`X-EDS-Client-Type: GAS`** mandatory on saves).

_End of Stage 8B.1A LIVE gate dossier._
