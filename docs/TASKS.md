# EDS Power — TASKS

Active work items. Governed by **`docs/00_SYSTEM/02_GLOBAL_RULES.md`** §13.

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
3. **Data contracts:** patch `docs/00_SYSTEM/04_DATA_CONTRACTS.md` for persistence envelopes when API is final.
4. **GAS:** **Thin Client Adapter V1** (**`TASK-2026-08B-011`**) — **`STAGE_8B_1B_OPERATOR_VERIFIED`** · **`docs/AUDITS/2026-04-30_STAGE_8B_1B_GAS_THIN_CLIENT_ADAPTER.md`**.
5. **Audit:** `docs/AUDITS/YYYY-MM-DD_STAGE_8B_PLATFORM_PERSISTENCE_NOT_GAS_PERSISTENCE.md` — thesis: **platform persistence**, not **GAS persistence**.
6. **Closure:** **`IDEA-0023`** → `IMPLEMENTED` in `12_IDEA_MASTER_LOG.md` after audit PASS.
7. **Next doc gate (post–8B.1):** **Stage 8B.2** — **`TASK-2026-08B-013`** (**`PLANNED`**) — **`docs/AUDITS/2026-04-30_STAGE_8B_2_PRE_GATE_SCOPE.md`** (pre-gate scope registry; **implementation** only when TASK leaves **`PLANNED`**).

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
- **Next:** **`TASK-2026-08B-013`** — **`docs/AUDITS/2026-04-30_STAGE_8B_2_PRE_GATE_SCOPE.md`** (**governance framing**).

---

## TASK-2026-08B-013 — Stage **8B.2** Client-Agnostic Flow Stabilization / Error Handling Gate

| Field | Value |
| --- | --- |
| **ID** | TASK-2026-08B-013 |
| **IDEA** | **IDEA-0023** |
| **Module** | `00_SYSTEM`, API contracts (**when implemented** — **not** in pre-gate registry commit) |
| **Status** | **`PLANNED`** |
| **Prerequisite** | **`STAGE_8B_1B_OPERATOR_VERIFIED`** (**`TASK-2026-08B-011` CLOSED**); pre-gate scope **`docs/AUDITS/2026-04-30_STAGE_8B_2_PRE_GATE_SCOPE.md`** |

### Purpose (**governance framing only in this milestone**)

Freeze **accepted** Gemini readiness themes into **implementable gates** without product expansion: duplicate/orphan persistence drift, bounded **prepare→save** outcomes, neutral machine-readable persistence errors, **snapshot integrity**, **client neutrality**.

### Required deliverables (**governance artefacts first**)

1. **Idempotency governance definition** (+ duplicate-request / duplicate-insert **policy**, not assumed implementation)
2. **Duplicate snapshot prevention policy** (aligned with idempotency doc)
3. **Partial success / partial failure contract** (**`prepare` OK + `save` fail** narration + operator semantics)
4. **Snapshot integrity validation governance** (contract-level checklist vs **`KZO_MVP_SNAPSHOT_V1`**)
5. **Client neutrality verification** (WEB/GAS symmetry at contract boundary)
6. **Audit dossier** — implementation gate audit **after** code (**separate dated file**, **outside** pre-gate scope doc)

### Forbidden (**Stage 8B.2 stabilization lane**)

- New client platforms; UI work; queue/async fabric; DB redesign beyond stabilization; advanced auth/rate systems; persistent “failed snapshot” archival subsystem (**deferred** per pre-gate scope)

---

## Completed

- **TASK-2026-08B-011** — Stage **8B.1B** Thin GAS Client Adapter **V1** — **`STAGE_8B_1B_OPERATOR_VERIFIED`** (**`docs/AUDITS/2026-04-30_STAGE_8B_1B_GAS_THIN_CLIENT_ADAPTER.md`**)
- **TASK-2026-08B-012** — Stage **8B.1A** API **`save_snapshot`** hardening + LIVE **E5** — **`STAGE_8B_1A_LIVE_VERIFIED`** · **`STAGE_8B_1A_CLOSEOUT_LOGGED`** (**`docs/AUDITS/2026-04-30_STAGE_8B_1A_LIVE_GATE.md`**)
