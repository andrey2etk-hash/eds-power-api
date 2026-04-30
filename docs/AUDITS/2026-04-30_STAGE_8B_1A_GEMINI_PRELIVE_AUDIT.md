# GEMINI STAGE **8B.1A** — API `save_snapshot` contract implementation (Pre-Live External Audit Request)

**Purpose.** Prompt for **external auditor Gemini** (independent technical + governance critic). **Stage 8B.1A** code is **implemented locally** (`STAGE_8B_1A_API_CONTRACT_IMPLEMENTED`). Gemini **audits whether it is safe to deploy live** and whether it **preserves** Stage **8A** persistence integrity, **`13_CLIENT_AGNOSTIC_PERSISTENCE_CONTRACT_V1`**, backward compatibility, and **anti-orchestration** posture — **before** operator LIVE deploy / broad client use.

**Strict:** **Analysis and verdict only** — Gemini **does not** patch **`main.py`**, **`kzo_snapshot_persist.py`**, **`gas/`**, Supabase DDL, or run deploys. Human owner applies Gemini output to gate **E5** / production promotion.

---

## Status (repository)

| Tag | Meaning |
| --- | --- |
| **`STAGE_8B_1A_PRELIVE_AUDIT_READY`** | This document is the **formal** Gemini pre-live audit package for **Stage 8B.1A** implementation review |

---

## Section 1 — Implementation summary (facts for reviewer)

Recorded in **`docs/AUDITS/2026-04-30_STAGE_8B_1A_API_CONTRACT_IMPLEMENTATION.md`**; governed by **`docs/AUDITS/2026-04-30_STAGE_8B_1A_API_SAVE_CONTRACT_GOVERNANCE_PLAN.md`**.

| Topic | Implemented behavior |
| --- | --- |
| **Validation** | **`validate_kzo_mvp_snapshot_v1`** — **L3** (five SUCCESS engineering layers non-empty **`dict`**), **L4** (SUCCESS-only **`request_metadata`** sub-keys: **`request_id`**, **`api_version`**, **`logic_version`**, **`execution_time_ms`** as non-negative **`int`**), **`logic_version`** must match **`request_metadata.logic_version`** (trimmed); **FAILED** requires **`failure.error_code`** + **`failure.message`**; type guards on optional **`request_metadata`** / **`normalized_input`** |
| **Response** | **Success:** **`status`**, **`snapshot_id`**, **`persistence_status`**, **`snapshot_version`**, **`created_at`**, **`client_type`**, **`failure: null`**; **`error_code: null`**. **Failure:** **`REJECTED`** vs **`ERROR`**, **`failure`** object (**`error_code`**, **`message`**, **`details`**), **`snapshot_version`** echo when L1 version check passed; legacy top-level **`error_code`** mirror |
| **Transport** | HTTP header **`X-EDS-Client-Type`** → normalized echo **`GAS` \| `WEB` \| `MOBILE` \| `AGENT` \| `UNKNOWN`** (invalid/absent → **`UNKNOWN`**) |
| **Persistence** | **`insert_snapshot_row`** returns **`created_at`** from insert / follow-up **select**; **no** new DDL (uses existing **`created_at`** on **`calculation_snapshots`**) |
| **Coupling** | **`save_snapshot`** does **not** call **`prepare_calculation`** |
| **Non-scope** | **No** GAS / Sheet / Web / Mobile changes in this TASK |

---

## Section 2 — Audit objectives (what Gemini must defend or challenge)

1. **Stage 8A persistence integrity** — insert-only semantics, contract JSON storage, no hidden mutation of engineering truth inside **`save_snapshot`**.
2. **`13_CLIENT_AGNOSTIC_PERSISTENCE_CONTRACT_V1`** — response shape, single pathway, client never DB.
3. **Backward compatibility** — existing **`save_snapshot`** consumers (e.g. **`saveKzoSnapshotV1()`** logging **`error_code`**) must not be silently broken; additive fields tolerated.
4. **Anti-orchestration** — API remains canonical persistence authority; validation does not invite client-side “fix-up” ownership.
5. **Future portability** — same contract for GAS / Web / Mobile; header echo does not fork persistence semantics.

---

## Section 3 — Files for review (repository paths)

| Path | Why |
| --- | --- |
| **`kzo_snapshot_persist.py`** | **`validate_kzo_mvp_snapshot_v1`**, **`insert_snapshot_row`** |
| **`main.py`** | **`save_snapshot`**, client-type normalization, envelope builders |
| **`docs/AUDITS/2026-04-30_STAGE_8B_1A_API_CONTRACT_IMPLEMENTATION.md`** | Implementation dossier |
| **`docs/AUDITS/2026-04-30_STAGE_8B_1A_API_SAVE_CONTRACT_GOVERNANCE_PLAN.md`** | Approved ladder / governance intent |
| **`docs/00_SYSTEM/13_CLIENT_AGNOSTIC_PERSISTENCE_CONTRACT_V1.md`** | Normative **§4** response |
| **`docs/00-02_CALC_CONFIGURATOR/09_KZO/11_KZO_MVP_SNAPSHOT_V1_CONTRACT.md`** | Incoming snapshot contract |
| **`docs/TASKS.md`** — **`TASK-2026-08B-012`** | Task boundary |
| **`gas/Stage3D_KZO_Handshake.gs`** ( **`saveKzoSnapshotV1`** only ) | **Backward-compat** consumer reference — **Gemini reads only**, **no edits** |

---

## Section 4 — Gemini questions (must answer explicitly)

**Q1.** Does the implementation **preserve client-agnostic architecture** (same HTTP persistence contract for any adapter; no client-class persistence fork)?

**Q2.** Is there **any orchestration leak** introduced (implicit sequencing, coupling to **`prepare_calculation`** inside **`save_snapshot`**, or validation that duplicates calc truth)?

**Q3.** What is the **backward compatibility risk** for existing **`save_snapshot`** clients (**JSON shape**, **`error_code`** location, new required request body constraints after **L3/L4**)?

**Q4.** Is **L3 + L4** validation **correctly scoped** relative to **`KZO_MVP_SNAPSHOT_V1`** / **`prepare_calculation`** metadata reality, or **overreaching** (e.g. rejects legitimate **`prepare_calculation`-derived** snapshots; **`execution_time_ms`** typing too strict)?

**Q5.** Is there **schema drift** or **unnecessary DB coupling** (**`created_at`** read-back, Supabase insert/select behavior assumptions, reliance on undocumented PostgREST return shape)?

**Q6.** Is **`client_type` echo via `X-EDS-Client-Type`** **governance-safe** (no PII creep, spoofing/abuse stance, **`UNKNOWN`** default appropriateness)?

**Q7.** Is deployment to **LIVE** **safe as-is**, or must the owner gate on specific preflight checks (**config**, **migration state**, **`SUPABASE_*`**, rollout order)?

**Q8.** What **exact LIVE smoke protocol** (step-by-step, pass/fail criteria, negative tests) should the operator run for **Stage 8B.1A** before signing **E5**?

---

## Section 5 — Required Gemini response format

Gemini **must** respond using **exactly** these markdown `##` headings **in order**:

```markdown
# GEMINI STAGE 8B.1A API CONTRACT IMPLEMENTATION PRE-LIVE AUDIT

## VERDICT

## GOVERNANCE FINDINGS

## TECHNICAL FINDINGS

## DRIFT RISKS

## DEPLOYMENT GUARDRAILS

## EXACT STAGE_8B_1A LIVE GATE PROTOCOL

## SUPPLEMENTARY NOTES (optional — max 10 bullets)
```

### 5.1 Verdict line (mandatory)

Immediately under **`## VERDICT`**, Gemini must print **exactly one line** (choose one):

- `PASS`
- `PASS WITH NOTES`
- `FAIL`

**Semantics (advisory):**

- **PASS** — Implementation matches contract and governance; **no material** live blockers; **E5** protocol can run with **low** residual risk if operator follows guardrails.
- **PASS WITH NOTES** — Deploy acceptable with **explicit** documented notes (compat, monitoring, or doc updates); **must** list under **DEPLOYMENT GUARDRAILS** / **LIVE GATE PROTOCOL**.
- **FAIL** — Material breach of persistence integrity, client-agnostic law, or **unsafe** live posture — **must** resolve before promoting build.

### 5.2 Section content expectations

- **`GOVERNANCE FINDINGS`** — **IDEA-0023**, thin-client boundary, API authority, Sheet-not-truth, single write path.
- **`TECHNICAL FINDINGS`** — validation, response envelope, Supabase interaction, edge cases.
- **`DRIFT RISKS`** — future contract evolution, client fork pressure, false reject rates.
- **`DEPLOYMENT GUARDRAILS`** — env, versioning, rollback, observability, **do / don’t** for first hours of live.
- **`EXACT STAGE_8B_1A LIVE GATE PROTOCOL`** — numbered steps, **SUCCESS** + **FAILED** + **reject** cases, header tests, **DB** correlation optional row check, **PASS** criteria.

---

## Section 6 — Auditor constraints

- Do **not** require **new features** in this audit (no BOM, pricing, retrieval, auth).
- Do **not** treat this as **Stage 8B.1B (GAS)** implementation review — at most **compatibility** implications for upcoming GAS work.
- Do **not** mandate **DDL** changes unless a **demonstrable** integrity gap exists (default: **8B.1A** stayed additive on API only).

_End of Gemini Stage 8B.1A pre-live audit request._
