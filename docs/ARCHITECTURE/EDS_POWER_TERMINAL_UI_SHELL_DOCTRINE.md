# EDS Power Terminal UI Shell Doctrine

## 1. Purpose

Define the intended UI architecture of the EDS Power Google Sheets terminal as a **controlled interactive shell**: not a spreadsheet with ad hoc menu items only, but a layered presentation model (global menu, module sidebar, operation modals) that stays aligned with backend-owned permissions and registry truth.

This document is **planning / architecture only**. It does not authorize implementation.

## 2. User Vision

The terminal is **not only** a spreadsheet-attached custom menu or a menu-triggered calculation tool.

It is a **controlled UI shell** with three cooperating surfaces:

- **Global custom menu** — session and fleet-wide navigation.
- **Module sidebar** — primary working panel for whichever module is active.
- **Modal windows** — focused operations: forms, confirmations, parameters, and execution dialogs.

DB-driven menu registry is **live validated**; this doctrine describes how terminal UX should **compose** registry-driven and client-rendered elements without moving product or engineering logic into the client.

## 3. UI Layer 1 — Custom Menu

**Purpose:** Global navigation and session control.

**Menu responsibilities:**

- Authorize the user (invoke login / session establishment flows as defined by existing auth doctrine).
- Logout and session lifecycle actions (e.g. refresh session awareness).
- Show **session status** (as provided by backend-validated checks; not self-declared client state as source of truth).
- **Refresh menu** (re-fetch registry-backed or backend-resolved menu/module visibility).
- Show **available modules** (as returned by the API for the authenticated principal and terminal context).
- **Open the selected module sidebar** (set active module and show that module’s working menu — not every deep action in the top menu).

**Menu must NOT:**

- Contain every detailed module function (those belong in the **module sidebar** or **modals**).
- Run complex multi-step workflows directly when a **sidebar** or **modal** pattern is more appropriate.
- **Compute** engineering, BOM, costing, or any product calculation logic.

## 4. UI Layer 2 — Module Sidebar

**Purpose:** Main working panel for the **currently selected module**.

**Sidebar responsibilities:**

- Show **module title** and short context (which module is active).
- Show **available module actions** (commands relevant to that module).
- Show **workflow steps** or grouped actions where helpful (readability; not a second source of permission truth).
- Show **current context / status** (e.g. “no calculation loaded”, “calculation X selected”), fed by API responses — not inferred rules in GAS.
- Provide **buttons or entries** that open **modals** or trigger **explicit batch** server requests (per existing batch-request architecture rule).

**Examples for Module 01 Calculation (illustrative only — not an implementation checklist):**

- Create calculation  
- Find calculation  
- Open current calculation  
- Prepare input  
- Run calculation preview  
- Save snapshot  
- View status / history  

## 5. UI Layer 3 — Modal Windows

**Purpose:** Focused, task-scoped dialogs so the sheet grid does not become the only input surface.

**Modal responsibilities:**

- **Data entry** and structured **parameter forms**.
- **Confirmations** before destructive or batch operations.
- **Selection** (e.g. pick product type, pick record).
- **Action-specific execution** UIs (short-lived dialogs tied to one server action or batch).

**Examples (illustrative):**

- Create calculation modal  
- Product type selection modal  
- Confirmation modal  
- Error / details modal  
- Result preview modal  

## 6. Active Module Concept

The terminal maintains an **`active_module`** (or equivalent client state): the module whose **sidebar** is shown.

- **Sidebar content depends on `active_module`.**  
  Example: if the user selects **Calculation Module**, the sidebar shows **Calculation Module** actions; selecting another module **replaces** sidebar content accordingly.

**`active_module` may be selected from:**

- The **custom menu** (user picks a module).
- A **backend/registry** action payload that implies module focus (e.g. “open_module” with module id).
- **Future persisted user state** (e.g. last module per user/terminal — planning only; no persistence mandated here).

The backend remains authoritative on **whether** a module is visible/allowed; the client only reflects that truth.

## 7. DB-Driven Registry Implications

**Current state (S01):** Registry supports **menu** actions suitable for **custom menu** rendering.

**Future evolution (conceptual — no schema change in this task):** Registry may need to distinguish where an action **surfaces** in the UI:

- Top **menu** actions  
- **Sidebar** actions  
- **Modal** entry points  
- **Hidden / backend-only** actions (no direct operator menu row)

**Possible future metadata fields (illustrative only):**

- `ui_surface`  
- `opens_sidebar`  
- `opens_modal`  
- `modal_type`  
- `sidebar_section`  
- `action_group`  
- `requires_batch_payload`  

Any such fields require a **separate** contract audit and approved migration — **not** part of this doctrine deliverable.

## 8. GAS Thin Client Boundary

**GAS may:**

- Render the **custom menu**, **sidebar**, and **modals** (presentation).
- **Collect** form and dialog input.
- Send **authenticated batch requests** to the backend.
- **Render** responses (including errors) per API envelopes.

**GAS must NOT:**

- **Decide permissions** or role outcomes (server decides; client displays).
- **Execute** engineering, BOM, or product **calculation** logic.
- **Query Supabase** directly or embed business/schema rules.
- **Store** canonical business rules or registry truth locally.
- **Bypass** the backend registry for module/action visibility where the architecture requires API resolution.

## 9. Backend Responsibility

The backend **decides** and **enforces**:

- Which **modules** exist and are **visible** to the caller.
- Which **actions** are allowed (per user, role, terminal, environment).
- **Action metadata** delivered to the client (labels, ordering hints, flags — within future contract limits).
- **Environment visibility** (e.g. diagnostic vs production behavior).
- Whether an action is purely navigational (**sidebar**), opens a **modal**, or triggers a **batch workflow** — as encoded in API contracts and (future) registry fields.

The client renders; it does not **reinterpret** permission or module truth.

## 10. First Module Application — Module 01 Calculations

**Planning note:** Before calculation **implementation**, Module 01 should define its **sidebar structure** (grouping of actions, default empty state, which actions open modals vs fire batch calls) and the **first modal workflow** (e.g. create calculation — form fields, validation display, confirm step).

This doctrine **does not** implement calculation logic, persistence, or API endpoints.

## 11. Out of Scope

- GAS implementation  
- Sidebar HTML / implementation  
- Modal HTML / implementation  
- New SQL registry schema or migrations  
- Calculation engine or product/BOM logic  
- Render deployment or environment changes  

## 12. Next Planning Step

After this doctrine is audited:

1. Plan **Module 01 sidebar structure** (sections, actions, mapping to future API/registry).  
2. Plan the **first modal workflow** (single bounded flow — e.g. create calculation — doc-only until approved).

Calculation **implementation** remains gated by explicit user approval and prior calc-slice planning artifacts; terminal shell planning **precedes** deepening calc-only implementation tasks.

## 13. Verdict

**`TERMINAL_UI_SHELL_DOCTRINE_READY_FOR_AUDIT`**
