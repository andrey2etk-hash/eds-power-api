# Stage 8B.1A — API `save_snapshot` contract hardening — governance + implementation plan

**Objective.** Harden **`POST /api/kzo/save_snapshot`** as the **canonical persistence authority** **before** **`TASK-2026-08B-011`** (**Stage 8B.1B** — GAS thin adapter). **No GAS/Sheet/UI work** in this slice.

**Final target (this document):** **`STAGE_8B_1A_API_CONTRACT_READY`** — plan approved; **implementation** is a **follow-on commit** gated by operator sign-off on this checklist.

---

## 1. Core principle

- **Calculation truth:** unchanged — remains **`prepare_calculation`**.
- **Persistence truth:** **`save_snapshot`** only — validate, optionally transform for storage, INSERT, structured response.
- **Anti–GAS-centrism:** the API **must not** silently accept loose bodies that invite clients to compensate with **implicit orchestration**. Stricter validation and a **uniform response** keep **every** future client (**GAS**, Web, Mobile) on identical contracts.

---

## 2. Current state vs gaps (facts from repository)

| Area | Today (`main.py`, `kzo_snapshot_persist.py`) | 8B.1A target |
| --- | --- | --- |
| **Top-level allow-list** | `_ALLOWED_TOP_KEYS` rejects unknown keys | Keep; tighten **semantic** validation (below) |
| **`SUCCESS`** layers | Requires five layer keys to be **`dict`** | Optionally require **non-empty** dicts and/or structural **shape** checks aligned with **`prepare_calculation`** (decision §4) |
| **`logic_version`** | Required non-empty **string** for **`SUCCESS`** | Add **cross-field traceability** vs **`request_metadata.logic_version`** (§3) |
| **`FAILED`** payloads | **`failure`** must be **dict**; layers optional | Optionally require **minimum failure keys** per **`11_KZO_MVP_SNAPSHOT_V1_CONTRACT.md`** (`error_code`, `message`, …) — explicit matrix §5 |
| **Partial / malformed** | Some cases return **`SNAPSHOT_UNKNOWN_FIELDS`** etc. | Single **`failure`** object in response (§6); clear codes for “rejected **before** insert” vs “insert failed” |
| **HTTP layer** | Not specified in MVP | Maintain **existing** semantics (avoid breaking callers); document recommended status codes §7 |
| **Response shape** | Success: **`status`**, **`snapshot_id`**, **`snapshot_version`**, **`persistence_status`**. Failure: **`error_code`** flat | Normalize to **`13_CLIENT_AGNOSTIC_PERSISTENCE_CONTRACT_V1.md`** **§4** + **`client_type`** **in response only** §6 |
| **`created_at`** | DB column **`DEFAULT NOW()`** exists; API **does not echo** | Return **`created_at`** on **SUCCESS** (from INSERT **RETURNING** or equivalent — **no** new DDL if **`created_at`** already present) |

**DDL:** **`public.calculation_snapshots`** already includes **`created_at`**. **`client_type`** is **not** a column — 8B.1A treats it as **response + request metadata** only (§6). **Optional** future column or JSON sidecar requires a **separate IDEA/migration**, not implied here.

---

## 3. `logic_version` traceability (required)

**Goal:** Every **stored** **`SUCCESS`** snapshot is attributable to an explicit logic line.

Planned rules (implementation):

1. **`SUCCESS`:** **`logic_version`** remains **mandatory**, non-whitespace **`str`** (existing).
2. **Consistency:** If **`request_metadata`** contains **`logic_version`**, it **must** equal **`logic_version`** (after normalizing whitespace / case per existing product enum rules). If **`request_metadata`** omits **`logic_version`** but other fields exist, **reject** with a dedicated code (e.g. **`SNAPSHOT_LOGIC_VERSION_METADATA_MISMATCH`**) or require full metadata subset — pick one policy and document in **`04_DATA_CONTRACTS.md`** on implementation.
3. **`FAILED`:** **`logic_version`** may be **`null`** per frozen snapshot contract; **do not** invent synthetic logic lines.

**Rationale:** Prevents “transport-only” snapshots with **untraceable** calc lineage — a common path to **client-side fixes** and **GAS orchestration** creep.

---

## 4. Strict envelope validation (incoming `KZO_MVP_SNAPSHOT_V1`)

**Baseline:** **`docs/00-02_CALC_CONFIGURATOR/09_KZO/11_KZO_MVP_SNAPSHOT_V1_CONTRACT.md`** remains **normative** for the **JSON body**.

**Ladder (recommended implementation order):**

| Level | Behavior | Notes |
| --- | --- | --- |
| **L0** | JSON object, allow-listed keys only | Existing |
| **L1** | **`snapshot_version`**, **`run_status`**, **`timestamp_basis`**, branch rules | Existing |
| **L2** | **`SUCCESS`:** all required keys present; **`failure`**** must be absent | Existing |
| **L3** | **`SUCCESS`:** each engineering layer is **`dict`** and **non-empty** (or **min key set** per contract doc table) | **New** — eliminates “empty shell” persistence |
| **L4** | **`request_metadata`** contains required sub-keys: **`request_id`**, **`api_version`**, **`logic_version`**, **`execution_time_ms`** (types per **`04_DATA_CONTRACTS.md`**) | **New** — aligns snapshot with **`prepare_calculation`** **`metadata`** |
| **L5** | Optional deep validation (typed keys inside layers) | **Out of scope** for 8B.1A unless explicitly tasked — risks coupling to internal calc evolution |

**Policy call (record at implementation):** Adopt **L3 + L4** for MVP hardening unless performance or backward compatibility blocks; document any **temporary** waiver in **`CHANGELOG`** with sunset.

**Rejected bodies:** Never INSERT when validation fails — **preserve** single authority (API says no).

---

## 5. Failed runs and partial snapshots

- **`run_status: "FAILED"`** per **§7B contract** may still be **valid** for **audit INSERT** — **if** **`failure`** is well-formed.
- **“Partial SUCCESS”** (e.g. some layers populated but **`run_status`** claims **`SUCCESS`**) → **reject** (**`SNAPSHOT_SUCCESS_LAYER_INVALID`** or similar).
- **Ambiguous payloads** (`SUCCESS` **`failure`** non-null — already rejected) remain blocked.

Optional governance toggle (document choice in implementation PR): **`INSERT` only `SUCCESS` rows for product MVP**, return **`REJECTED`** for **`FAILED`** snapshot bodies — only if stakeholders want **narrower DB contents**. Default recommendation: **keep** **`FAILED`** inserts **only** when envelope matches contract, for audit parity with Stage 7B.

---

## 6. Standardized response (canonical)

**Applies to all clients.** Snapshot **JSON body** remains **`KZO_MVP_SNAPSHOT_V1`** unchanged — **do not** add **`client_type`** into the persisted blob from the API unless a **future** governed contract says so.

### 6.1 `client_type` (transport)

- **Source:** HTTP header **`X-EDS-Client-Type`** (recommended) — allow-list e.g. **`GAS`**, **`WEB`**, **`MOBILE`**, **`AGENT`**, **`UNKNOWN`**.
- **Default:** **`UNKNOWN`** if header absent or invalid (**never** infer from UA in MVP).
- **Echo:** **`client_type`** field on **every** response (success/failure).

This preserves **client-agnostic** payloads while giving **telemetry** without Sheet coupling.

### 6.2 Success response fields (producer must supply)

| Field | Requirement |
| --- | --- |
| **`status`** | **`SUCCESS`** |
| **`snapshot_id`** | UUID string |
| **`persistence_status`** | **`STORED`** |
| **`snapshot_version`** | **`KZO_MVP_SNAPSHOT_V1`** |
| **`created_at`** | ISO-8601 from DB row (**authoritative**) |
| **`client_type`** | Echo normalized header |
| **`failure`** | **`null`** |

Optional additive fields tolerated by clients per **`13_...`** stability rules.

### 6.3 Failure response fields (reject or persistence error)

| Field | Requirement |
| --- | --- |
| **`status`** | **`FAILED`** |
| **`persistence_status`** | **`REJECTED`** or **`ERROR`** (distinguish **validation** vs **DB/infra** failure — implementers pick second enum consistently) |
| **`snapshot_id`** | **`null`** |
| **`snapshot_version`** | Present if **`snapshot_version`** in body passed **L1**; else **`null`** |
| **`created_at`** | **`null`** on reject before insert |
| **`client_type`** | Echo |
| **`failure`** | Single object — see §8 |

**Deprecation:** **`error_code`** at top level → fold into **`failure.code`** / **`failure.error_code`** (one scheme) and mirror in **`04_DATA_CONTRACTS.md`**; maintain **temporary** dual-field only ifneeded for backwards compatibility (**one release** deprecation note).

---

## 7. HTTP semantics (non-breaking recommendation)

| Case | Recommended |
| --- | --- |
| Validation rejection | **`200`** with **`status: FAILED`** **or** **`422`** — **choose globally** with **`main.py`** error handler consistency |
| Persistence unavailable | **`503`** or **`200`** + **`failure`** — align with **`prepare_calculation`** precedent |
Record the choice in **`04_DATA_CONTRACTS.md`** — **avoid** undocumented split behavior.

---

## 8. Unified `failure` object (proposal)

Minimal shape for **reject / infrastructure** responses:

```json
{
  "error_code": "SNAPSHOT_VALIDATION_REJECTED",
  "message": "human-readable",
  "details": {}
}
```

- **`validation`:** **`error_code`** from **`validate_kzo_mvp_snapshot_v1`** (machine).
- **`insert`:** **`SNAPSHOT_INSERT_FAILED`**, **`SNAPSHOT_PERSISTENCE_UNAVAILABLE`**.
- **`details`** optional (e.g. unknown keys list) — guarded to **no secrets**.

---

## 9. Orchestration leak checklist (explicit non-goals)

8B.1A **must not**:

- Call **`prepare_calculation`** from **`save_snapshot`**.
- Mutate engineering layers or “fill in” missing data.
- Accept **Sheet-specific** identifiers (range names, spreadsheet IDs) in this endpoint.
- Add **second** persistence path or **client-trusted** “pre-approved” insert.
- Expand GAS or any **UI**.

---

## 10. Implementation sequence (after plan sign-off)

1. **Spec sync:** Update **`docs/00_SYSTEM/13_CLIENT_AGNOSTIC_PERSISTENCE_CONTRACT_V1.md`** **§4** table to include **`client_type`**; update **`docs/00_SYSTEM/04_DATA_CONTRACTS.md`** with request header + response examples.
2. **Validation:** Extend **`validate_kzo_mvp_snapshot_v1`** per §3–§5 (L3/L4 + traceability).
3. **Persistence readback:** Adjust **`insert_snapshot_row`** to return **`created_at`** (Supabase **`.select()`** after insert or **RPC** — avoid breaking RLS patterns).
4. **Handler:** Refactor **`save_snapshot`** in **`main.py`** to build the **§6** envelope; parse **`X-EDS-Client-Type`**.
5. **Tests:** Unit tests for validation matrix + response shape (if test harness exists; else manual operator script in audit).
6. **Deploy note:** Render env unchanged except **no** new secrets; **re-run** minimal **LIVE** smoke **POST** after deploy.
7. **Gate:** Mark **`TASK-2026-08B-011`** **unblocked** only after §11 exit criteria.

**Follow-on:** **`Stage 8B.1B`** — GAS sends header **`X-EDS-Client-Type: GAS`**, consumes normalized **`failure`**, displays **`created_at`**.

---

## 11. Exit criteria — `STAGE_8B_1A_API_CONTRACT_READY`

| # | Criterion |
| --- | --- |
| E1 | This plan reviewed (owner + optional Gemini preflight if desired) |
| E2 | **`13_CLIENT_AGNOSTIC_PERSISTENCE_CONTRACT_V1.md`** and **`04_DATA_CONTRACTS.md`** list the **§6** response + header |
| E3 | Code implements **L3+** validation and **`logic_version`** traceability (**§3**) |
| E4 | **No** DDL change **or** migration filed **unless** **`created_at`** echo requires something beyond existing table (unlikely) |
| E5 | Live or staging smoke shows **SUCCESS** payload with **`created_at`** + **`client_type`** |

**Coding status tied to E2–E5:** until code lands, **`STAGE_8B_1A_API_CONTRACT_READY`** can mean **“plan READY”** only; optionally split label **`STAGE_8B_1A_API_CONTRACT_IMPLEMENTED`** when E5 passes — recommended in **`CHANGELOG`** on merge.

---

## 12. References

- **`kzo_snapshot_persist.py`** — `validate_kzo_mvp_snapshot_v1`, `insert_snapshot_row`
- **`main.py`** — `save_snapshot`
- **`docs/00_SYSTEM/13_CLIENT_AGNOSTIC_PERSISTENCE_CONTRACT_V1.md`**
- **`docs/00-02_CALC_CONFIGURATOR/09_KZO/11_KZO_MVP_SNAPSHOT_V1_CONTRACT.md`**
- **`supabase/migrations/20260429120000_calculation_snapshots_v1.sql`**
- **`docs/TASKS.md`** — **`TASK-2026-08B-001`**, **`TASK-2026-08B-012`**, **`TASK-2026-08B-011`**
- **`docs/AUDITS/2026-04-30_STAGE_8B_1_GEMINI_PREFLIGHT_REQUEST.md`** (optional ordering vs this hardening)

---

_End of Stage 8B.1A governance + implementation plan._
