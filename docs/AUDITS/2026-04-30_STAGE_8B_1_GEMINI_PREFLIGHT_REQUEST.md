# GEMINI STAGE 8B.1 — Thin Client Adapter V1 (GAS) Preflight (External Audit Request)

**Purpose.** Prompt for **external auditor Gemini** (independent critic). This is a **governance-first pre-implementation** review. Gemini **does not** write **`gas/`** code, **API** handlers, **Supabase** DDL, or migrations. Gemini **audits whether the planned Stage 8B.1 slice is safe to implement** under **IDEA-0023** and **Client-Agnostic Persistence Contract V1**, **before** **`TASK-2026-08B-011`** moves from shell to code.

**Strict:** Analysis and verdict only — **no implementation**, **no repository patches**, **no new architecture**.

---

## Status (repository)

| Tag | Meaning |
| --- | --- |
| **`STAGE_8B_1_AUDIT_REQUEST_READY`** | This document is the **formal** Gemini preflight package for **Stage 8B.1** |

---

## Section 1 — Current state

### 1.1 What Stage 8A achieved

- **Legacy baseline** captured and replay verified (local tooling + migration discipline per project audits).
- **`public.calculation_snapshots`** DDL promoted and verified **non-prod** and **live**.
- **`POST /api/kzo/save_snapshot`** operational; **API-mediated** persistence to Supabase **proven**.
- **`prepare_calculation`** remains the **calculation truth** entry; persistence is a **separate** orchestrated step after a **contract-shaped** snapshot body.
- **Closure posture:** **`STAGE_8A_COMPLETE`** (**`IDEA-0017`** **`IMPLEMENTED`**).

### 1.2 What Stage 8B achieved

- **`IDEA-0023`** registered — **client-agnostic persistence** governance.
- **`docs/00_SYSTEM/13_CLIENT_AGNOSTIC_PERSISTENCE_CONTRACT_V1.md`** — **V1** canonical flow: **Any client → `prepare_calculation` → snapshot → `save_snapshot` → `snapshot_id`**; clients **never** write the DB directly.
- **API** = **canonical orchestrator** for calculation validation, snapshot acceptance rules, and **`save_snapshot`**.
- **Google Apps Script** role locked to **thin client adapter** — **not** system orchestrator.
- **Next gate shell:** **`TASK-2026-08B-011`** (**Stage 8B.1**) — implementation path registered; **coding not started** pending this preflight.

### 1.3 Why GAS is the first client only

- **Sheets** are the **current operator surface** and the **first** integration that must **not** accidentally become the **persistence brain** or **source of engineering truth**.
- Proving **one** thin adapter on a constrained runtime **first** forces the **same HTTP contract** that Web/Mobile will reuse — **no special-case “Sheet persistence”**.

### 1.4 Why future Web/Mobile compatibility matters

- **Product goal:** multiple clients ( Sheets, web, mobile, agents ) **must** share **one** persistence path and **one** snapshot contract version family (**e.g.** **`KZO_MVP_SNAPSHOT_V1`**).
- **Drift risk:** if Stage 8B.1 hides logic in GAS, **Web/Mobile** either **re-duplicate** behaviour or **fork** the platform — both violate **IDEA-0023**.

---

## Section 2 — Proposed Stage 8B.1 (planned GAS capabilities)

**Scope:** **`TASK-2026-08B-011`** — Thin Client Adapter **V1** (GAS).

**Planned capabilities (high level):**

1. **Send** normalized input / payload to **`POST /api/calc/prepare_calculation`** (Existing pre-flight **form** hygiene only — **not** new engineering truth ).
2. **Receive** validated **`prepare_calculation`** result ( success / failure envelopes as today’s API defines ).
3. **Assemble** the **canonical snapshot envelope** (**`KZO_MVP_SNAPSHOT_V1`**) from the **API success payload** — **transport-level mapping** per **`11_KZO_MVP_SNAPSHOT_V1_CONTRACT.md`** (no re-derivation of engineering layers in GAS ).
4. **Call** **`POST /api/kzo/save_snapshot`** ( e.g. reuse / align with existing **`saveKzoSnapshotV1()`** transport ).
5. **Display** to the operator **`snapshot_id`**, **`persistence_status`**, and related **`save_snapshot`** **`status`** / errors in the **Sheet** ( **display + optional writeback** — **not** system record of truth; contract **§3** in **`13_..._CONTRACT_V1.md`**).

**Explicit non-goals for 8B.1:** API redesign, DB redesign, new snapshot version, parallel persistence channel, Supabase from client, retrieval/analytics UI.

---

## Section 3 — Forbidden (hard constraints for Gemini to enforce in review)

| Rule | Rationale |
| --- | --- |
| **No business logic in GAS** | Engineering / calc truth stays in **API**; GAS is **adapter + display** only. |
| **No direct Supabase writes** | **§1** Client-Agnostic Persistence Contract V1. |
| **No alternate persistence path** | One pathway to **`calculation_snapshots`** for this MVP slice. |
| **No GAS-owned orchestration** | No new “brain” that sequences **hidden** rules beyond **call API → call API → show result**. |
| **No product logic duplication** | No second implementation of burden / class / topology semantics in **`gas/`**. |
| **No GAS as architecture center** | Sheets must not become the **implicit** spec for how persistence works platform-wide. |

---

## Section 4 — Gemini questions (must answer explicitly)

**Q1.** Does this plan **preserve client-agnostic architecture** ( same contract + same API sequence for any future client )?

**Q2.** Does this plan **risk GAS governance drift** ( e.g. creeping “just one small rule in the Sheet” ) — what **concrete** drift signatures should the owner **ban**?

**Q3.** Is **snapshot assembly in GAS** ( mapping **`prepare_calculation` → `KZO_MVP_SNAPSHOT_V1` body ) **acceptable** under V1 governance, or should the **API own more** of that assembly — what are the **trade-offs** and **failure modes**?

**Q4.** What are the **top anti-patterns** to prevent during implementation ( ordered by severity )?

**Q5.** Is **Stage 8B.1** the **correct next step** after **`STAGE_8B_GOVERNANCE_FIXED`**, or should a **different** gate ( e.g. **`save_snapshot`** response **§4** alignment only ) precede full GAS wiring?

**Q6.** What would **break Web/Mobile future compatibility** if done wrong in 8B.1 ( naming, error handling, coupling to Sheet ranges, implicit state in cells, etc. )?

---

## Section 5 — Required output format

Gemini **must** respond using **exactly** these markdown `##` headings **in order**:

```markdown
# GEMINI STAGE 8B.1 THIN CLIENT ADAPTER V1 PREFLIGHT AUDIT

## VERDICT

## GOVERNANCE RISKS

## SCOPE DRIFT RISKS

## RECOMMENDED HARDENING

## CORRECT NEXT IMPLEMENTATION ORDER

## SUPPLEMENTARY NOTES (optional — max 10 bullets)
```

### 5.1 Verdict line (mandatory)

Immediately under **`## VERDICT`**, Gemini must print **exactly one line** ( choose one ):

- `PASS`
- `PASS WITH GUARDRAILS`
- `FAIL`

**Semantics (advisory):**

- **PASS** — Plan is **aligned** with client-agnostic persistence; GAS thin-adapter role **clear**; assembly location **defensible**; **no** material blockers to start **`TASK-2026-08B-011`** implementation under stated forbiddens.
- **PASS WITH GUARDRAILS** — Proceed, but Gemini must list **explicit guardrails** ( process, code structure, doc checkpoints, or sequencing ) without expanding scope into new architecture.
- **FAIL** — Material conflict with **IDEA-0023**, **thin client** mandate, or **unbounded** GAS responsibility — **must** resolve governance or sequencing **before** coding.

### 5.2 Body sections

Under each heading, use **bullet lists** or **short numbered lists**; avoid large code dumps.

- **`GOVERNANCE RISKS`** — where **policy** could be violated post-implementation.
- **`SCOPE DRIFT RISKS`** — feature creep, “temporary” Sheet truth, duplicate logic.
- **`RECOMMENDED HARDENING`** — **actionable** checks ( human or automated ) **without** inventing new services.
- **`CORRECT NEXT IMPLEMENTATION ORDER`** — **ordered steps** ( e.g. verify response contract parity, then transport-only GAS path, then operator display ) **without** API/DB redesign.

---

## Files for review (repository paths)

| Path | Why |
| --- | --- |
| `docs/00_SYSTEM/13_CLIENT_AGNOSTIC_PERSISTENCE_CONTRACT_V1.md` | **V1** canonical flow; roles; allowed/forbidden clients |
| `docs/TASKS.md` — **`TASK-2026-08B-011`** | Stage 8B.1 shell — allowed endpoints and implementation path |
| `docs/00-02_CALC_CONFIGURATOR/09_KZO/11_KZO_MVP_SNAPSHOT_V1_CONTRACT.md` | Snapshot envelope **`KZO_MVP_SNAPSHOT_V1`** |
| `docs/00_SYSTEM/12_IDEA_MASTER_LOG.md` — **`IDEA-0023`** | Governance intent |
| `docs/AUDITS/2026-04-29_STAGE_8A_SUPABASE_LIVE_VERIFICATION_GATE.md` | Live persistence proof context |
| `docs/AUDITS/2026-04-30_STAGE_8A_2_1_LIVE_DEPLOY_CALCULATION_SNAPSHOTS.md` | Stage 8A closeout |
| `docs/NOW.md` | Current stage posture (**8B / 8B.1** gate) |

---

## Auditor constraints

- Do **not** implement or pseudo-code **production** GAS or API.
- Do **not** propose **new persistence tables**, **new public routes** for MVP, or **mobile/web-specific** persistence forks.
- Treat **`POST /api/kzo/save_snapshot`** response **§4** alignment ( **`created_at`**, **`failure`** ) as a **known** possible **sub-step** under **`TASK-2026-08B-001`** — flag **ordering** only; **do not** expand into full API redesign.

_End of Gemini Stage 8B.1 preflight audit request._
