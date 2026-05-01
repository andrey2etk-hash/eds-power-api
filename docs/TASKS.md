# EDS Power — TASKS

Active work items. Governed by **`docs/00_SYSTEM/02_GLOBAL_RULES.md`** §13.

---

## TASK-ID continuity (**governance**)

**TASK numbers record chronology and slices**, not a contiguous sequence for readability. **`TASK-2026-08B-001`** names the **umbrella Stage 8B governance charter** while **`TASK-2026-08B-011` / `012` / `013`** name **later execution slices** — **gaps are normal**, not contradictory, unless **`TASK`** text explicitly forbids numbering reservations.

**CLOSED TASK IDs are immutable.** **Normalizer** drafts **must** diff against **`docs/TASKS.md`** before proposing IDs (**e.g. never map `8B.2` onto `TASK-2026-08B-012`**).

---

## TASK-2026-08B-001 — Stage 8B Client-Agnostic Persistence Flow Governance

| Field | Value |
| --- | --- |
| **ID** | TASK-2026-08B-001 |
| **IDEA** | **IDEA-0023** (`RIGHT_NOW` / `P1` / `TASK`) |
| **Module** | `00_SYSTEM` (cross-cutting persistence; affects `00-02_CALC_CONFIGURATOR` / KZO adapter) |
| **Status** | `GOVERNANCE_FOUNDATION_COMPLETE` (**`STAGE_8B_GOVERNANCE_FIXED`** — contract + TASK shell; audit/API-align sub-deliverables may remain **OPEN**) |

### Description

Define and freeze **client-agnostic persistence**: any client uses the same **API-orchestrated** path **`prepare_calculation` → validated snapshot → `save_snapshot` → `snapshot_id`**. Prevent **accidental GAS centralization** and **Sheet-as-truth** drift.

### Reason

Stage **8A** proved persistence exists. Stage **8B** must establish **platform architecture** so **Google Sheets** is only the **first adapter**, not the implicit orchestrator — preserving **client neutrality**, **API authority**, and **future web/mobile symmetry**.

### Deliverables

1. **Normative contract:** `docs/00_SYSTEM/13_CLIENT_AGNOSTIC_PERSISTENCE_CONTRACT_V1.md` (**done** — refine if API delta TASK changes fields).
2. **API alignment:** **`TASK-2026-08B-012`** (**Stage 8B.1A**) — **`STAGE_8B_1A_API_CONTRACT_IMPLEMENTED`** · **`docs/AUDITS/2026-04-30_STAGE_8B_1A_API_CONTRACT_IMPLEMENTATION.md`** (+ governance plan **`docs/AUDITS/2026-04-30_STAGE_8B_1A_API_SAVE_CONTRACT_GOVERNANCE_PLAN.md`**).
3. **`04_DATA_CONTRACTS.md` persistence mirror:** **`DEFERRED`** — **`§20`** routes **`save_snapshot`** truth to **`13_CLIENT_AGNOSTIC_PERSISTENCE_CONTRACT_V1.md`** until an explicit TASK activates duplicated field tables here (**no split-brain**).
4. **GAS:** **Thin Client Adapter V1** (**`TASK-2026-08B-011`**) — **`STAGE_8B_1B_OPERATOR_VERIFIED`** · **`docs/AUDITS/2026-04-30_STAGE_8B_1B_GAS_THIN_CLIENT_ADAPTER.md`**.
5. **Audit:** **`docs/AUDITS/2026-04-30_STAGE_8B_PLATFORM_PERSISTENCE_NOT_GAS_PERSISTENCE.md`** — thesis: **platform persistence**, not **GAS persistence** (**governance memo — satisfies charter slot**).
6. **Closure:** **`IDEA-0023`** → `IMPLEMENTED` in `12_IDEA_MASTER_LOG.md` after audit PASS.
7. **Stage 8B.2** — **`TASK-2026-08B-013`** (**`CLOSED`**) — canonical registry (**single parent gate narration**) **`docs/TASKS.md`** § **`TASK-2026-08B-013`** (**do not** duplicate slice paths here).

### Expected result

Google Sheets, Web, Mobile, agents, or any future client all persist snapshots through the **same** API pathway; **no** direct DB writes from clients; **no** GAS-only persistence ownership.

### Forbidden

GAS as orchestration core; Sheet as system truth store; client-side persistence ownership; web/mobile divergence in save path; BOM; pricing; production transfer; analytics; auth expansion (per **IDEA-0023**).

---

## TASK-2026-08B-012 — Stage **8B.1A** API `save_snapshot` contract hardening

| Field | Value |
| --- | --- |
| **ID** | TASK-2026-08B-012 |
| **IDEA** | **IDEA-0023** (API authority slice) |
| **Module** | `main.py`, `kzo_snapshot_persist.py`, `docs/00_SYSTEM/` (contracts) |
| **Status** | **`CLOSED`** · **`STAGE_8B_1A_LIVE_VERIFIED`** (**2026-04-30**) — closeout **`docs/AUDITS/2026-04-30_STAGE_8B_1A_LIVE_GATE.md`** |

### Purpose

Harden **`POST /api/kzo/save_snapshot`** **before** **`TASK-2026-08B-011`**: strict **`KZO_MVP_SNAPSHOT_V1`** validation, **`logic_version`** traceability, standardized response (**`status`**, **`snapshot_id`**, **`persistence_status`**, **`snapshot_version`**, **`created_at`**, **`client_type`**, unified **`failure`**), reject malformed/partial **SUCCESS** payloads.

### Forbidden

GAS/UI/Sheet coupling; **`prepare_calculation`** calls inside **`save_snapshot`**; direct DB/schema expansion **except** **`created_at`** echo using existing column; alternate persistence paths.

---

## TASK-2026-08B-011 — Stage **8B.1B** Thin Client Adapter V1 (GAS) *(was “8B.1”)*

| Field | Value |
| --- | --- |
| **ID** | TASK-2026-08B-011 |
| **IDEA** | **IDEA-0023** (operational slice) |
| **Module** | `gas/` + `00-02_CALC_CONFIGURATOR` (KZO transport only) |
| **Status** | **`CLOSED`** · **`STAGE_8B_1B_OPERATOR_VERIFIED`** — operator manual **PASS** (**`docs/AUDITS/2026-04-30_STAGE_8B_1B_GAS_THIN_CLIENT_ADAPTER.md`**) |
| **Prerequisite** | **`TASK-2026-08B-012`** **`STAGE_8B_1A_LIVE_VERIFIED`** (**satisfied** — **`docs/AUDITS/2026-04-30_STAGE_8B_1A_LIVE_GATE.md`**) |

### Purpose

First **real** client adapter: **GAS** calls the **same** API persistence pathway as any future client (**`13_CLIENT_AGNOSTIC_PERSISTENCE_CONTRACT_V1.md`**).

### Allowed

- `POST /api/calc/prepare_calculation`
- `POST /api/kzo/save_snapshot`
- Display **`snapshot_id`**, **`status`**, **`persistence_status`**, errors

### Forbidden

- Business / engineering logic in GAS (beyond existing **pre-flight** input hygiene)
- Direct Supabase or DB writes
- GAS as **orchestrator** (no new “brain” flows; sequence = API calls + display only)
- API redesign; DB redesign; mobile/web fork

### Implementation path (**landed — operator verified**)

1. Entry: **`runStage8B1BGasThinClientAdapterFlow()`** — **`gas/Stage3D_KZO_Handshake.gs`** (uses **Stage 4C** preflight → **`prepare_calculation`**).
2. Envelope: **`buildKzoMvpSnapshotV1EnvelopeFromPrepareResponse_()`** — copies API **`data`** / **`metadata`** into **`KZO_MVP_SNAPSHOT_V1`** (no engineering math).
3. Save: **`urlFetchKzoSaveSnapshot_()`** / **`saveKzoSnapshotV1()`** — **`POST /api/kzo/save_snapshot`** + **`X-EDS-Client-Type: GAS`**.
4. Sheet: **`Stage4A_MVP!H2:I9`** — **`snapshot_id`**, **`persistence_status`**, **`created_at`**, **`snapshot_version`**, **`error_code`**, **`failure_message`** (display-only).

### Deliverable for closeout (**met**)

- Operator verification **PASS** + audit **`docs/AUDITS/2026-04-30_STAGE_8B_1B_GAS_THIN_CLIENT_ADAPTER.md`** (**`STAGE_8B_1B_OPERATOR_VERIFIED`**).
- **Next:** **`IDEA-0024 = IMPLEMENTED_LIVE_VERIFIED`** for bounded API prototype tuple — live report **`docs/AUDITS/2026-05-01_KZO_LAYERED_NODE_PROTOTYPE_API_LIVE_VERIFICATION.md`** (`KZO_WELDED` + `VACUUM_BREAKER` + `LEFT_END` + `INSULATOR_SYSTEM`; no expansion).

---

## TASK-2026-08B-013 — Stage **8B.2** Client-Agnostic Flow Stabilization / Error Handling Gate

| Field | Value |
| --- | --- |
| **ID** | TASK-2026-08B-013 |
| **IDEA** | **IDEA-0023** |
| **Normative handle (**Idea Normalizer**)** | **`STAGE_8B_2_CLIENT_AGNOSTIC_FLOW_STABILIZATION`** |
| **Module** | **Верифікація відповідності канону V1** (**`TASK-013`**, **`IDEA-0023`**, **`STAGE` 8B.2**) — робочий канон **`13_` + `11_KZO`**; **`04_DATA_CONTRACTS`** лише процес **`§19`**, **не** ціль patch полів канону без окремого **TASK** |
| **Status** | **`CLOSED`** (**`STAGE_8B_2_GOVERNANCE_CLOSED`**) — full governance gate closeout lodged in **`docs/AUDITS/2026-05-01_STAGE_8B_2_GOVERNANCE_CLOSEOUT.md`** |
| **Label** | **`STAGE_8B_2_GOVERNANCE_CLOSED`** |
| **Slice progression (`TASK-013`)** | **`8B.2A` CLOSED** — **`STAGE_8B_2A_GEMINI_FOCUSED_AUDIT_PASS`** **`·`** **`8B.2B` CLOSED** — focused audit pass logged **`·`** **`8B.2C` CLOSED** — doctrine + focused audit closeout **`·`** **`8B.2D` CLOSED** — doctrine + focused audit request completed; governance gate frozen (**no `8B.2E` opening**) |
| **Prerequisite** | **`STAGE_8B_1B_OPERATOR_VERIFIED`** (**`TASK-2026-08B-011` CLOSED**); dossier **`docs/AUDITS/2026-04-30_STAGE_8B_2_PRE_GATE_SCOPE.md`** |

**Normalizer execution decomposition (**governance-only handles**):** **`STAGE_8B_2_GOVERNANCE_SUBSTAGES_DECOMPOSED`** — **`docs/AUDITS/2026-04-30_STAGE_8B_2_GOVERNANCE_SUBSTAGES_DECOMPOSITION.md`** — slices **`2A`→`2E`** (**not** new TASK IDs **unless** репо явно реєструє окремо).

| Slice | Handle |
| --- | --- |
| **2A** | **`STAGE_8B_2A_IDEMPOTENCY_DUPLICATE_GOVERNANCE`** |
| **2B** | **`STAGE_8B_2B_PREPARE_SAVE_SPLIT_OUTCOME_GOVERNANCE`** |
| **2C** | **`STAGE_8B_2C_MACHINE_READABLE_PERSISTENCE_ERROR_DOCTRINE`** |
| **2D** | **`STAGE_8B_2D_SNAPSHOT_INTEGRITY_VALIDATION_GOVERNANCE`** |
| **2E** | **`STAGE_8B_2E_CLIENT_NEUTRALITY_VERIFICATION`** |

**ID governance:** Some normalizer drafts label **8B.2** as **`TASK-2026-08B-012`** — **`REJECTED`**: **`012`** is **CLOSED** **Stage 8B.1A**; **8B.2** = **`013`** **only**.

### Stage **8B.2A** boundary (**documentation doctrine only**)

**Canonical dossier (**primary canon** — stage slice, не глобальний `00_SYSTEM` текст):**

- **`docs/AUDITS/2026-04-30_STAGE_8B_2A_IDEMPOTENCY_DUPLICATE_GOVERNANCE.md`** (**`STAGE_8B_2A_DOCTRINE_PUBLISHED`**)

**`00_SYSTEM/`:** **no premature** повне перенесення доктрини **2A**. Після прийняття та (**якщо**) правило стає **platform-wide constitutional** — лише **distilled** експорт окремим **TASK**-патчем (**напр.** **`04_DATA_CONTRACTS.md`**).

**In scope (**2A**):** ідемпотентність / duplicate-request / replay boundaries / governance outcome categories (**без** `error_code`) — **`docs/AUDITS/2026-04-30_STAGE_8B_2_GOVERNANCE_SUBSTAGES_DECOMPOSITION.md`**.

**Forbidden inside 8B.2A (hard stop):**

- **`main.py`**, **API**/routes, **`gas/`**, **DB**/migrations
- Нові **transport** ключі (**`X-Idempotency-Key`** тощо) як **mandate**/специфіка імплементації; **retry engine** / черги у межах **`8B.2`** lane — **немає**
- Другий конкуруючий authoritative **2A** dossier (**exactly one**)

### Stage **8B.2B** boundary (**documentation doctrine only**)

**Canonical dossier (**`2B`**):** **`docs/AUDITS/2026-04-30_STAGE_8B_2B_PREPARE_SAVE_SPLIT_OUTCOME_GOVERNANCE.md`** (**`STAGE_8B_2B_DOCTRINE_PUBLISHED`**)

**In scope:** phased **`prepare_calculation`** vs **`save_snapshot`** stewardship tags (**dossier §§8–11**), orphan boundaries, replay-after-partial narratives keyed off **`2A`**.

**Forbidden inside 8B.2B:** код · API redesign · **GAS** logic · DDL · машинна таксономія / **`error_code`** (**`2C`**) · **`KZO_MVP_SNAPSHOT_V1`** / integrity redesign (**`2D`**) · async · черги

### Stage **8B.2C** boundary (**documentation doctrine only**)

**Current state:** **`CLOSED`** (**doctrine + focused audit closed; no further edits inside `2C` lane**).

**Idea normalization artifact (**required before dossier**):** **`docs/AUDITS/2026-04-30_STAGE_8B_2C_MACHINE_READABLE_PERSISTENCE_ERROR_IDEA_NORMALIZATION.md`**

**Doctrine dossier status:** **authoring active** — **`docs/AUDITS/2026-04-30_STAGE_8B_2C_MACHINE_READABLE_PERSISTENCE_ERROR_DOCTRINE.md`**.

**Gemini focused audit REQUEST:** prepare-only after doctrine authoring is approved and completed; closeout lodges **`docs/AUDITS/YYYY-MM-DD_GEMINI_STAGE_8B_2C_FOCUSED_AUDIT.md`**

**In scope (**`2C`**):** canonical **`error_code`** / category taxonomy · **phase**-aware grouping (**prepare** vs **save** — references **`8B.2B`**) · retryable vs terminal · duplicate-aware · orphan-aware readings · client-neutral interpretation framework · thin-client-safe machine-readable envelope governance (**normative shapes in dossier**, **not** mandatory code edits in **`2C`**).

**Depends on (**cite, do not redefine**):** **`8B.2A`**, **`8B.2B`**.

**Forbidden inside 8B.2C:** **`main.py`**, routes, **`gas/`**, migrations; subsystem implementation; **`2D`** **`KZO_MVP_SNAPSHOT_V1`** integrity stance authoring (**`8B.2D` owns**); rewriting **`2A`/`2B`** doctrines; retry engine · async · AUTH · UI expansion.

**Gemini sequencing (**`TASK-013` slice gates** — canonical slice paths above**):**

- **Before `2B` doctrine work:** **`STAGE_8B_2A_GEMINI_FOCUSED_AUDIT_PASS`** — lodged **`docs/AUDITS/2026-04-30_GEMINI_STAGE_8B_2A_FOCUSED_AUDIT.md`** (request history: **`docs/AUDITS/2026-04-30_GEMINI_STAGE_8B_2A_FOCUSED_AUDIT_REQUEST.md`**).
- **Before **`2C` canonical dossier authoring + Idea latch:** **`STAGE_8B_2B_GEMINI_FOCUSED_AUDIT_PASS`** lodges **`docs/AUDITS/YYYY-MM-DD_GEMINI_STAGE_8B_2B_FOCUSED_AUDIT.md`** (request **`docs/AUDITS/2026-04-30_GEMINI_STAGE_8B_2B_FOCUSED_AUDIT_REQUEST.md`**); **`STAGE_8B_2C_NORMALIZED_FOR_ACTIVE_SUBSTAGE`** lodges **`docs/AUDITS/2026-04-30_STAGE_8B_2C_MACHINE_READABLE_PERSISTENCE_ERROR_IDEA_NORMALIZATION.md`**.
- **Before `2D` integrity governance:** **`8B.2C` normalization completed** + **doctrine authored after approval** + **`STAGE_8B_2C_GEMINI_FOCUSED_AUDIT_PASS`** lodged in **`docs/AUDITS/YYYY-MM-DD_GEMINI_STAGE_8B_2C_FOCUSED_AUDIT.md`**.

### Purpose (**Stage 8B.2 = governance framing until TASK advances**)

Stabilize **persistence posture** (**idempotency**, **duplicate doctrines**, split **prepare/save** narration, machine-readable persistence **errors**, **snapshot integrity governance**, **client-neutral** verification) **without product/platform expansion**.

### Required deliverables

1. **Idempotency + duplicate doctrines** (**delivered in **`8B.2A`**) — **`docs/AUDITS/2026-04-30_STAGE_8B_2A_IDEMPOTENCY_DUPLICATE_GOVERNANCE.md`** + **`STAGE_8B_2A_GEMINI_FOCUSED_AUDIT_PASS`** — **`docs/AUDITS/2026-04-30_GEMINI_STAGE_8B_2A_FOCUSED_AUDIT.md`**
2. **Prepare/save split outcome doctrine** (**delivered in **`8B.2B`**) — **`docs/AUDITS/2026-04-30_STAGE_8B_2B_PREPARE_SAVE_SPLIT_OUTCOME_GOVERNANCE.md`** + **`STAGE_8B_2B_GEMINI_FOCUSED_AUDIT_PASS`** — lodges **`docs/AUDITS/YYYY-MM-DD_GEMINI_STAGE_8B_2B_FOCUSED_AUDIT.md`** (**REQUEST** **`docs/AUDITS/2026-04-30_GEMINI_STAGE_8B_2B_FOCUSED_AUDIT_REQUEST.md`**)
3. **Machine-readable persistence error doctrine (**`8B.2C`**) — `CLOSED`**
4. **Snapshot integrity governance (**`8B.2D`**) — `CLOSED`**
5. **Client neutrality audit (**`8B.2E`**) — `NOT OPENED` by this closeout**
6. **Stage governance closeout dossier** — **`docs/AUDITS/2026-05-01_STAGE_8B_2_GOVERNANCE_CLOSEOUT.md`**

### Forbidden (**Stage 8B.2 lane** — matches pre-gate scope)

Persistence rebuild disguised as “stabilization”; async/queues; full failed persistence subsystem; DB redesign; client platform rollout / web-mobile expansion ships; AUTH expansion tasks; UI expansion; **KZO**/product semantics inflation — see dossier **`FORBIDDEN`** section.

---

## Completed

- **TASK-2026-08B-011** — Stage **8B.1B** Thin GAS Client Adapter **V1** — **`STAGE_8B_1B_OPERATOR_VERIFIED`** (**`docs/AUDITS/2026-04-30_STAGE_8B_1B_GAS_THIN_CLIENT_ADAPTER.md`**)
- **TASK-2026-08B-012** — Stage **8B.1A** API **`save_snapshot`** hardening + LIVE **E5** — **`STAGE_8B_1A_LIVE_VERIFIED`** · **`STAGE_8B_1A_CLOSEOUT_LOGGED`** (**`docs/AUDITS/2026-04-30_STAGE_8B_1A_LIVE_GATE.md`**)
