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
4. **GAS:** document or implement **Thin Client Adapter V1** only (no orchestration core) — reference **IDEA-0023** notes in `12_IDEA_MASTER_LOG.md`.
5. **Audit:** `docs/AUDITS/YYYY-MM-DD_STAGE_8B_PLATFORM_PERSISTENCE_NOT_GAS_PERSISTENCE.md` — thesis: **platform persistence**, not **GAS persistence**.
6. **Closure:** **`IDEA-0023`** → `IMPLEMENTED` in `12_IDEA_MASTER_LOG.md` after audit PASS.

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
| **Status** | **`STAGE_8B_1A_API_CONTRACT_IMPLEMENTED`** — **`main.py`**, **`kzo_snapshot_persist.py`**; operator **E5** LIVE smoke after deploy (see implementation audit) |

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
| **Status** | `SHELL` — API hardening (**`TASK-2026-08B-012`**) **landed**; implement GAS path when tasked (**`X-EDS-Client-Type: GAS`**) |
| **Prerequisite** | **`STAGE_8B_1A_API_CONTRACT_IMPLEMENTED`** (code on `main`); **E5** LIVE smoke recommended before broad GAS rollout |

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

### Implementation path (register only)

1. Entry: dedicated stub function name TBD (e.g. `runStage8B1ThinPersistenceAdapterFlow_`) next to existing KZO GAS flows in **`gas/Stage3D_KZO_Handshake.gs`** (or split file if separate TASK).
2. Build **`KZO_MVP_SNAPSHOT_V1`** body from **`prepare_calculation`** success payload per **`11_KZO_MVP_SNAPSHOT_V1_CONTRACT.md`** (transport-level assembly only).
3. Call **`saveKzoSnapshotV1()`** / equivalent `UrlFetchApp` to **`/api/kzo/save_snapshot`** with **`X-EDS-Client-Type: GAS`** (per **8B.1A** plan).
4. Log **`snapshot_id`** + HTTP metadata for operator audit; writeback to Sheet **optional** and **display-only** (not system truth).

### Deliverable for closeout

- Operator verification note + optional audit file **`docs/AUDITS/YYYY-MM-DD_STAGE_8B_1_THIN_CLIENT_ADAPTER_V1.md`**

---

## Completed

- *(none listed here yet — archive closed TASKS below when introduced)*
