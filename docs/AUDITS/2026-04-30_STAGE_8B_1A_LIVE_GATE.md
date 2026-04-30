# Stage **8B.1A** — LIVE verification gate (`save_snapshot`)

## Gate status (**closeout — 2026-04-30**)

**`STAGE_8B_1A_LIVE_VERIFIED`** · **`STAGE_8B_1A_CLOSEOUT_LOGGED`** · **`NEXT_GATE_READY: STAGE_8B_1B_GAS_THIN_CLIENT_ADAPTER`** (**`TASK-2026-08B-011`**)

Operator LIVE verification **PASS**; **`TASK-2026-08B-012`** **CLOSED**. Historical interim label **`LIVE_HOST_SYNCED_PENDING_SUPABASE_ENV`** superseded once **`SUPABASE_*`** was correct and Smoke **A**/**E** passed.

---

## Closeout evidence (operator-recorded — **no secrets**)

| Checkpoint | Result |
| --- | --- |
| **G1 Gemini pre-live** (**`2026-04-30_STAGE_8B_1A_GEMINI_PRELIVE_AUDIT.md`**) | **PASS** (human attestation) |
| **`POST /api/kzo/save_snapshot` (Render)** | **`status`** **`SUCCESS`**, **`persistence_status`** **`STORED`**, **`client_type`** **`GAS`**, **`failure`** **`null`** |
| **`snapshot_id` (HTTP)** | **`300d18c3-f8fe-4411-8dce-a4b698b6f5e3`** |
| **DB** **`public.calculation_snapshots`** | Same **`id`** present; **`snapshot_version`** **`KZO_MVP_SNAPSHOT_V1`**; **`logic_version`** **`KZO_MVP_V1`**; **`created_at`** **`2026-04-30 17:00:28.809012+00`** (**operator-confirmed** alignment with API **`created_at`** echo) |

---

## Gemini final audit summary (operator-recorded)

| Item | Note |
| --- | --- |
| **Verdict** | **PASS** |
| **Platform posture** | Persistence path treated as **platform/API-owned** (not client-owned); operator records crossing into **mature platform** execution for this slice |
| **Proceed** | **`TASK-2026-08B-011`** — **Stage 8B.1B** GAS Thin Client Adapter **V1** |
| **Guardrails** | **GAS = thin client only**; **transparent API errors** via unified **`failure`** + legacy **`error_code`** mirror; treat **`snapshot_id`** as **audit / correlation token**; **no** GAS orchestration core; **no** direct client Supabase writes |

**No** service-role key or other secrets recorded in this dossier.

---

**Purpose.** Close **`TASK-2026-08B-012`** **E5** operator gate after **Gemini pre-live PASS** (**`docs/AUDITS/2026-04-30_STAGE_8B_1A_GEMINI_PRELIVE_AUDIT.md`**) and **Render** deployment of **`main`** at **`551ce87`** (**Stage 8B.1A** API hardening).

## Preconditions

| # | Gate |
| --- | --- |
| G1 | **Gemini pre-live verdict = PASS** (human-recorded attestation linked to Gemini output) |
| G2 | **Render** build points at **`main`** **≥** **`551ce87`** (`Implement Stage 8B.1A API save_snapshot hardening and governance audits`) |
| G3 | **No** DDL / migrations in this TASK; **`SUPABASE_URL`** + **`SUPABASE_SERVICE_ROLE_KEY`** configured on Render (same pattern as **`STAGE_8A`** live gate) |
| G4 | **No** GAS / client orchestration tests in this dossier (**STRICT** scope) |

## Deploy + Render (**Supabase env unblock**)

**Commits (reference):** **`551ce87`** (**8B.1A** code) · **`fcfe04b`** (LIVE gate doc sync); **`origin/main`**.

### Required Render environment variables (**names only**)

Set in **Render Dashboard → Service → Environment** for the FastAPI worker:

| Variable | Role |
| --- | --- |
| **`SUPABASE_URL`** | Project API URL (**Supabase Dashboard → Settings → API**) |
| **`SUPABASE_SERVICE_ROLE_KEY`** | **Service role** secret used **only server-side** by **`kzo_snapshot_persist`** (never exposed to Sheets/clients) |

Same variable names as **`STAGE_8A`** (**`docs/AUDITS/2026-04-29_STAGE_8A_SUPABASE_LIVE_VERIFICATION_GATE.md`**).

### Secret hygiene (**STRICT**)

- **Do not** commit secrets to Git (**no** **`service_role`** in **`\.env`** tracked files, **no** keys in **`\.env.example`**).
- **Do not** paste **`SUPABASE_SERVICE_ROLE_KEY`** (or any bearer token) into **docs**, **PRs**, or **chat** / tickets.
- **Do not** add real keys to **`\.env.example`** — placeholders only elsewhere if ever needed (**this TASK** touches **none**).

If **`save_snapshot`** responses **still** omit **`client_type`** / **`failure`** after env setup, treat as **stale build**: Render **manual redeploy** or **Clear build cache** + redeploy; confirm Deploy **commit SHA** on **`origin/main`**.

After saving env vars, **redeploy / restart** the Render service so the process inherits new variables.

---

## Operator retest checklist (after Supabase env set)

1. **Render Dashboard** — confirm **`SUPABASE_URL`** + **`SUPABASE_SERVICE_ROLE_KEY`** present (values **not** copied into repo).
2. **Manual deploy / restart** — trigger redeploy if env changed (per Render UX).
3. **Smoke A** (**Section A** minimal **SUCCESS** + **`X-EDS-Client-Type: GAS`**) → expect **`status`** **`SUCCESS`**, **`persistence_status`** **`STORED`**, **`snapshot_id`**, **`created_at`**, **`client_type`** **`GAS`**, **`failure`** **`null`**.
4. **DB E** — verify row in **`public.calculation_snapshots`** by **`snapshot_id`**; **`created_at`** aligns with response.
5. **Regression negatives** — re-run **C** (L3 null layer) → **`SNAPSHOT_SUCCESS_LAYER_INVALID`** + full **`failure`**; **D** (logic mismatch) → **`SNAPSHOT_LOGIC_VERSION_METADATA_MISMATCH`**.

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

## Automated / manual probe log (Cursor, **2026-04-30**)

Chronology (summarized):

| Phase | Observation |
| --- | --- |
| Early post-push | Responses looked **legacy** (**flat** rejects; **`SNAPSHOT_SUCCESS_LAYER_MISSING`**) → **stale deploy** plausible |
| **Render sync verified** | **L3** negative (**`physical_topology_summary: null`**, **`X-EDS-Client-Type: GAS`**) returns **`SNAPSHOT_SUCCESS_LAYER_INVALID`**, **`client_type`**, structured **`failure`** → **`LIVE_HOST_SYNCED`** for **handler** behavior |
| **Persistence** | **Smoke A**-style valid **SUCCESS** still returns **`SNAPSHOT_PERSISTENCE_UNAVAILABLE`** (**`persistence_status`** **`ERROR`**) → **Supabase env** not configured on Render service |

**Resolved label (interim):** **`LIVE_HOST_SYNCED_PENDING_SUPABASE_ENV`** — **closed** upon operator LIVE **PASS** (see **Closeout evidence** above).

---

## Final status registry

| Label | Meaning |
| --- | --- |
| **`STAGE_8B_1A_LIVE_VERIFIED`** | **ACHIEVED (2026-04-30)** — operator Smoke **A** + DB **E** + Gemini **PASS** (**this dossier closeout**) |
| **`STAGE_8B_1A_CLOSEOUT_LOGGED`** | Repository logs (**NOW**, **CHANGELOG**, **TASKS**, **IDEA_MASTER_LOG**, **AUDIT_INDEX**) synced to **`STAGE_8B_1A_LIVE_VERIFIED`** |
| **`NEXT_GATE_READY: STAGE_8B_1B_GAS_THIN_CLIENT_ADAPTER`** | **`TASK-2026-08B-011`** — GAS-only transport/UI; **`X-EDS-Client-Type: GAS`** |
| **`LIVE_HOST_SYNCED_PENDING_SUPABASE_ENV`** | *(historical)* superseded once **`SUPABASE_*`** restored and Smoke **A**/**E** **PASS** |
| **`STAGE_8B_1A_LIVE_VERIFICATION_PENDING`** | *(historical)* open gate before closeout |

---

## Next

**Stage 8B.1B** — **`TASK-2026-08B-011`** Thin GAS Client Adapter (**`X-EDS-Client-Type: GAS`** mandatory on saves). **No** broad GAS implementation in **8B.1A** closeout TASK.

_End of Stage 8B.1A LIVE gate dossier._
