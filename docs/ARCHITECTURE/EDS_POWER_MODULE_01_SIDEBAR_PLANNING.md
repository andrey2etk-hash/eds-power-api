# EDS Power Module 01 Sidebar Planning

## 1. Purpose

Define the **sidebar workspace** for **Module 01 — Calculation Module** inside the EDS Power Terminal UI Shell.

This document plans **UI/workflow** and **client–server boundaries** only. **No** GAS, backend, registry DDL, or calculation implementation is authorized by this artifact.

## 2. Architectural Context

Module 01 lives inside the **EDS Power Terminal UI Shell** ([`EDS_POWER_TERMINAL_UI_SHELL_DOCTRINE.md`](./EDS_POWER_TERMINAL_UI_SHELL_DOCTRINE.md)).

UI layers:

- **Custom menu** — global navigation, auth/session, and entry into modules (`active_module`).
- **Sidebar** — **active module workspace** (this document).
- **Modal windows** — focused operations: forms, confirmations, parameter entry ([Terminal UI Shell Doctrine §5](./EDS_POWER_TERMINAL_UI_SHELL_DOCTRINE.md)).

Normative boundaries:

- **Render Thinking / GAS Thin UI** — [`docs/00_SYSTEM/02_GLOBAL_RULES.md`](../00_SYSTEM/02_GLOBAL_RULES.md)
- **main.py Thin Router** — same file; logic in services/engines when implemented.
- **GAS deployment/sync** — [`EDS_POWER_GAS_DEPLOYMENT_AND_SYNC_DOCTRINE.md`](./EDS_POWER_GAS_DEPLOYMENT_AND_SYNC_DOCTRINE.md)

## 3. Module 01 Sidebar Role

The sidebar is the operator’s **working panel for calculations**. It should help the user:

- create a calculation  
- find an existing calculation  
- open **current** calculation context  
- prepare input data  
- run a **controlled** calculation request (when endpoints exist)  
- view status  
- save or review snapshots (when APIs exist)  

All **decisions** (permissions, validation, numbering, persistence) remain **backend-owned**.

## 4. Sidebar Layout Concept

### 4.1 Header

- **Module name:** Module 01 — **Розрахунки**  
- **User/session indicator** (display only — from last backend-validated session/call where applicable)  
- **Current environment:** PRODUCTION / DEV / TEMPLATE (from backend metadata or controlled config — not guessed in GAS)  
- **Active calculation indicator** (summary line: e.g. number or “none”)  

### 4.2 Current Calculation Context

Show (when backend provides / last known from API response):

- calculation number  
- calculation status  
- product type  
- revision/version  
- last saved time  
- current operator/user (as returned by API)  

If **no** calculation is selected: show **“No active calculation”** (or equivalent UA string).

### 4.3 Primary Actions

Buttons (labels UA as specified):

- **Створити новий розрахунок**  
- **Знайти розрахунок**  
- **Відкрити поточний розрахунок**  
- **Оновити статус**  

### 4.4 Input / Preparation Actions

Buttons:

- **Підготувати дані з таблиці**  
- **Перевірити вхідні дані**  
- **Показати помилки / попередження**  

### 4.5 Calculation Actions

Buttons:

- **Запустити preview-розрахунок**  
- **Зберегти snapshot**  
- **Переглянути результат**  
- **Переглянути історію**  

### 4.6 Support / Diagnostics

Buttons:

- **Перевірити сесію**  
- **Перевірити підключення**  
- **Показати debug context** — **only** if allowed by **environment / backend policy** (no client-side bypass)

## 5. First Modal Workflow — Create Calculation

**Modal title (concept):** “**Створити новий розрахунок**”

**Fields (operator-facing):**

- calculation title  
- potential customer  
- product type  
- comment / note  
- optional source object/order reference  

**Buttons:**

- **Створити**  
- **Скасувати**  

**Backend owns:**

- calculation **number** generation  
- **validation** and permission checks  
- **persistence** decision and authority  
- canonical **status** after create  

**GAS owns only:**

- render modal  
- collect input  
- send **authenticated** batch/request per future contract  
- display **backend** response (success/error envelope)  

## 6. Active Calculation State

**Concept:** `active_calculation` is the **current calculation context** reflected in the sidebar (labels, status line, enabled actions).

**Possible state source (planning):**

- **Backend response** after create/open/select (authoritative)  
- **Temporary GAS UI state** for display only — must be clearly subordinate to last server truth  
- **Future** persisted preference/session facet — backend-governed only  

**Rules:**

- GAS **may display** `active_calculation` for UX.  
- **Backend** remains **source of truth** for identity, status, and permissions.  
- **No** calculation identity should be **trusted** if it originates **only** from GAS without server confirmation.  

## 7. Sidebar State Mapping

**Sidebar status indicators** (UX labels — illustrative):

- No active calculation  
- Draft calculation loaded  
- Input prepared  
- Validation error  
- Preview ready  
- Snapshot saved  
- Calculation locked / archived  

These are **display states only**. **Backend** decides actual status and allowed transitions.

## 8. Backend Actions Required Later

**Future** endpoints may include (planning placeholders — **do not implement** now):

- `POST /api/module01/calculations/create`  
- `GET /api/module01/calculations/search`  
- `GET /api/module01/calculations/{id}`  
- `POST /api/module01/calculations/prepare-input`  
- `POST /api/module01/calculations/preview`  
- `POST /api/module01/calculations/snapshots`  

Aligned with calc slice planning, a **`POST /api/module01/calculations/prepare`** style path may remain a separate bounded slice — unify contracts under a future audit.

## 9. Registry Implications

**Future** registry `action_key` concepts (no DDL in this task):

**Top menu:**

- `OPEN_MODULE_01_SIDEBAR`  

**Sidebar actions:**

- `MODULE01_CREATE_CALCULATION`  
- `MODULE01_SEARCH_CALCULATION`  
- `MODULE01_PREPARE_INPUT`  
- `MODULE01_RUN_PREVIEW`  
- `MODULE01_SAVE_SNAPSHOT`  

**Modal entry / modal-scoped:**

- `MODULE01_CREATE_CALCULATION_MODAL`  
- `MODULE01_PRODUCT_TYPE_SELECT_MODAL`  

Future metadata (`ui_surface`, `opens_modal`, etc.) per Terminal UI Shell Doctrine §7.

## 10. GAS Thin Client Boundary

**GAS may:**

- open sidebar  
- open modal  
- collect form fields  
- call backend (authenticated)  
- render results and errors  

**GAS must NOT:**

- generate calculation number  
- validate engineering rules  
- decide permissions  
- execute product/calculation logic  
- query Supabase directly  
- save snapshots directly  
- interpret product registries as authority  

## 11. Render Thinking Boundary

**Render/backend owns:**

- permission checks  
- calculation creation and lifecycle  
- validation  
- calculation status  
- snapshot persistence  
- product/calculation logic (when approved)  
- final response envelope  

## 12. main.py Thin Router Boundary

Future implementation must **not** add large logic into `main.py`.

**Expected direction:**

- route in `main.py` or a dedicated router module  
- service in e.g. `services/module01_calculations_service.py` (name illustrative)  
- calculation logic in engines/modules when approved  
- repositories if DB persistence is active  

**No** implementation in this task.

## 13. First Implementation Candidate After Audit

**Recommended** next implementation candidate, **after** Gemini audit and **user approval**:

**Minimal:**

- `OPEN_MODULE_01_SIDEBAR` (or equivalent) opens a **static sidebar shell**  
- sidebar shows session/user/module context from **backend**  
- **no** calculation execution yet  

**Alternative:**

- **Create Calculation** modal + one backend **create** path (still gated — not planned as implemented here)  

**Decision remains open** pending audit and explicit task.

## 14. Open Questions

- Should the sidebar be opened from a **top menu** action only, a **registry** action only, or both?  
- Should `active_calculation` be stored in **UserProperties**, **DocumentProperties**, or **backend only** (display cache in GAS)?  
- What is the **first** real modal to implement after shell: **Create Calculation** only, or another?  
- Should **Create Calculation** **persist** immediately on **Створити**, or only **prepare** a draft until explicit save?  
- Which **product types** are allowed in the **first** sidebar version (generic vs KZO-only)?  
- Should Module 01 start with a **generic calculation shell** before KZO-specific UI?  

## 15. Out of Scope

- GAS HTML sidebar implementation  
- Modal HTML implementation  
- Backend endpoints  
- Calculation / engineering logic  
- KZO-specific engineering logic  
- BOM logic  
- SQL migrations  
- Registry schema changes  
- Render deployment  

## 16. Verdict

**`MODULE_01_SIDEBAR_PLAN_READY_FOR_AUDIT`**
