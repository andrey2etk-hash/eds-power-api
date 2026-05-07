# EDS Power Module 01 Sidebar Technical Spec

## 1. Purpose

Define the **technical contract** for **Module 01 Sidebar — Iteration 01**, ready for a future **HTML/GAS** implementation slice after audits.

This document **prepares** implementation (registry hooks, payloads, endpoints concept, GAS boundaries, error codes, event map) but **does not** implement code, SQL, or deployments.

## 2. Source Planning

| Document / rule | Path |
|-----------------|------|
| Terminal UI Shell Doctrine | [`EDS_POWER_TERMINAL_UI_SHELL_DOCTRINE.md`](./EDS_POWER_TERMINAL_UI_SHELL_DOCTRINE.md) |
| Module 01 Sidebar Planning (design — **PASS / `SIDEBAR_DESIGN_LOCKED`**) | [`EDS_POWER_MODULE_01_SIDEBAR_PLANNING.md`](./EDS_POWER_MODULE_01_SIDEBAR_PLANNING.md) |
| Render Thinking / GAS Thin UI Rule | [`docs/00_SYSTEM/02_GLOBAL_RULES.md`](../00_SYSTEM/02_GLOBAL_RULES.md) |
| main.py Thin Router Rule | same file |
| GAS Deployment and Sync Doctrine | [`EDS_POWER_GAS_DEPLOYMENT_AND_SYNC_DOCTRINE.md`](./EDS_POWER_GAS_DEPLOYMENT_AND_SYNC_DOCTRINE.md) |

**Locked design decisions** (from planning audit):

- Sidebar opens via **backend registry action** (not ad hoc client-only entry).  
- **`active_calculation` truth** is **backend-owned**; every action **revalidates** server-side.  
- **GAS `DocumentProperties`** may cache **`active_calculation_id` only** — UI convenience, **not** authority.  
- **First modal** = **Create Calculation**; submit **immediately persists** a calculation record and returns **id/number**.  
- **UX:** avoid button overload — **grouping / collapsible sections** for full layout; Iteration 01 implements a **minimum** subset (see §6).

## 3. Sidebar Iteration 01 Scope

**Iteration 01 should include:**

- Open Module 01 sidebar from **registry/menu** action (`OPEN_MODULE_01_SIDEBAR`).  
- Show **module header**.  
- Show **session/user context** (from API).  
- Show **active calculation** block (or empty state).  
- Show **four primary actions** (per §7).  
- Support **Create Calculation** modal as the planned workflow entry (after sidebar shell, per §16 recommendation ordering).

**Iteration 01 must NOT include:**

- Real **calculation engine** or KZO **engineering** logic.  
- **BOM** logic.  
- **Snapshot** persistence **implementation** unless **separately** approved.  
- **Advanced search** (beyond placeholder/disabled).  
- **Production** shop-floor or ERP logic.

## 4. Registry Action Contract

**Planned** registry row concept ( **no SQL** in this task):

| Field | Value |
|--------|--------|
| `action_key` | `OPEN_MODULE_01_SIDEBAR` |
| `action_type` | `OPEN_SIDEBAR` |
| `menu_label` | Module 01 — Розрахунки |

**Metadata concept** (JSON-shaped; exact column/json shape follows future registry contract):

```json
{
  "target_module": "MODULE_01",
  "sidebar_id": "MODULE_01_CALCULATION_SIDEBAR",
  "requires_auth": true
}
```

**Note:** Physical insert = **manual SQL** (S01 patch or future S02 migration) — **out of scope** for this document.

## 5. Sidebar Initial State Payload

**Conceptual** backend response when opening / refreshing sidebar context (envelope aligns with EDS Power standard shape):

```json
{
  "status": "success",
  "data": {
    "sidebar": {
      "sidebar_id": "MODULE_01_CALCULATION_SIDEBAR",
      "module_code": "MODULE_01",
      "module_name": "Module 01 — Розрахунки",
      "environment_scope": "PRODUCTION",
      "user": {
        "user_id": "...",
        "display_name": "...",
        "role_code": "..."
      },
      "active_calculation": null,
      "sections": []
    }
  },
  "error": null,
  "metadata": {
    "request_id": "...",
    "menu_source": "registry"
  }
}
```

When `active_calculation` is non-null, it is a **server-provided** object (shape to be frozen with implementation — e.g. `calculation_id`, `calculation_number`, `status`, `title`, `product_type`).

`sections` may carry **grouping** metadata for collapsible UI (labels, order, collapsed default) — optional for Iteration 01 minimum UI.

## 6. Sidebar Sections

**Recommended** sections (full product UX, with grouping/collapsible to reduce clutter):

1. Header  
2. Session / operator status  
3. Current Calculation Context  
4. Primary Actions  
5. Input Preparation  
6. Calculation Actions  
7. Diagnostics  

**Iteration 01 implementable minimum** (per locked scope):

- Header  
- Current Calculation Context  
- Primary Actions  
- Diagnostics  

Session/operator may be **merged into Header** for Iteration 01 if layout requires. Input Preparation and Calculation Actions may appear as **collapsed** or omitted until a later slice.

## 7. Primary Actions — Iteration 01

| # | Label (UA) | `action_key` | Behavior |
|---|------------|--------------|----------|
| 1 | Створити новий розрахунок | `MODULE01_CREATE_CALCULATION` | Opens **Create Calculation** modal. |
| 2 | Знайти розрахунок | `MODULE01_SEARCH_CALCULATION` | **Placeholder** — disabled or “planned” only in Iteration 01. |
| 3 | Відкрити поточний розрахунок | `MODULE01_OPEN_ACTIVE_CALCULATION` | If server/cache implies an active id, **refresh context** / show **active_calculation**; else empty state + message. |
| 4 | Оновити статус | `MODULE01_REFRESH_CONTEXT` | **GET** sidebar context from backend; **revalidate** `active_calculation`. |

## 8. First Modal — Create Calculation

**Modal name (operator):** Create Calculation  

**Fields:**

- `calculation_title`  
- `potential_customer`  
- `product_type`  
- `comment`  
- optional **external / object** reference (single field or split per implementation contract)  

**Buttons:**

- **Створити**  
- **Скасувати**  

**On submit:**

- GAS sends **one** authenticated **POST** (see §9).  

**Backend owns:** validation, permission, **calculation number** generation, **persistence**, canonical **status** (e.g. `DRAFT`), response envelope.  

**GAS owns:** render modal, collect fields, display result/error, update UI from **`sidebar_update`** / refreshed context only.

## 9. Create Calculation Request Contract

**Conceptual endpoint:** `POST /api/module01/calculations/create`

**Conceptual body:**

```json
{
  "source_client": "GAS",
  "terminal_id": "...",
  "spreadsheet_id": "...",
  "payload": {
    "calculation_title": "...",
    "potential_customer": "...",
    "product_type": "KZO",
    "comment": "...",
    "external_reference": "..."
  }
}
```

**Mandatory rules:**

- **`user_id`** (and role resolution) comes from **Bearer session** — **not** from payload.  
- **Role / permission** resolved **only** on backend.  
- **Calculation number** generated **only** on backend.  
- Terminal/sheet ids in body are **diagnostic/context** — must not override session identity.

## 10. Create Calculation Response Contract

**Conceptual success:**

```json
{
  "status": "success",
  "data": {
    "calculation": {
      "calculation_id": "...",
      "calculation_number": "YYYYMMDDHHMM-01",
      "status": "DRAFT",
      "product_type": "KZO",
      "title": "...",
      "created_at": "..."
    },
    "sidebar_update": {
      "active_calculation_id": "...",
      "active_calculation_display": "..."
    }
  },
  "error": null,
  "metadata": {
    "request_id": "...",
    "api_version": "..."
  }
}
```

GAS may write **`active_calculation_id`** to `DocumentProperties` **only** as convenience **after** success; next **any** backend call must **revalidate** (see §11).

## 11. Active Calculation State

**Truth:** backend is **source of truth**.

**Allowed GAS cache:**

- **`DocumentProperties`** key (proposed): **`EDS_POWER_MODULE01_ACTIVE_CALCULATION_ID`**  
- Value: **UI convenience only** — must be **cleared or ignored** when server says missing, locked, forbidden, or wrong terminal.

**Rules:**

- Every **backend action** must **revalidate** calculation state (session + id + permission).  
- GAS **must never** treat cached id as **permission** or **existence**.  
- On `MODULE01_CALCULATION_NOT_FOUND` or equivalent, clear active context in UI and **clear** cache (see §12).

## 12. Error Handling UI

Sidebar **must** surface backend errors — **no silent empty UI**.

| Code / token (concept) | Operator UX |
|------------------------|-------------|
| `AUTH_MISSING_TOKEN` | Prompt login / session expired. |
| `MENU_REGISTRY_UNAVAILABLE` | Registry unavailable; retry. |
| `MODULE01_PERMISSION_DENIED` | Permission denied. |
| `MODULE01_CALCULATION_NOT_FOUND` | Clear active context + cache; show message. |
| `MODULE01_INVALID_CREATE_PAYLOAD` | Field-level or summary validation error. |
| `MODULE01_BACKEND_UNAVAILABLE` | Retry / server unavailable. |

Exact machine codes must match implementation error contract audit.

## 13. Event Map

| UI / flow | GAS callback (illustrative name) | Backend (concept) |
|-----------|-----------------------------------|-------------------|
| Open Module 01 Sidebar | `edsPowerOpenModule01Sidebar` | `GET /api/module01/sidebar/context` |
| Create Calculation (submit) | `edsPowerModule01OpenCreateCalculationModal` + submit handler | `POST /api/module01/calculations/create` |
| Refresh Context | `edsPowerModule01RefreshSidebarContext` | `GET /api/module01/sidebar/context` |

**No** code in this task — names are **candidates** for implementation slice.

## 14. Backend Service Boundary

Future backend layout (**no** `main.py` bloat):

- Route wiring in `main.py` or a **router** module only.  
- **`services/module01_sidebar_service.py`** — assemble sidebar DTO.  
- **`services/module01_calculations_service.py`** — create / validate / persist calculation.  
- **Repository** helpers only if DB persistence is implemented.

**`main.py` must not** contain sidebar **business** logic.

## 15. GAS Boundary

Future files (illustrative):

- `Module01Sidebar.gs`  
- `Module01SidebarHtml.html`  
- `Module01CreateCalculationDialog.html`  

**Bound Apps Script:** a `.gs` and `.html` file cannot share the same base name in one project; sidebar HTML uses **`Module01SidebarHtml.html`** and **`HtmlService.createHtmlOutputFromFile("Module01SidebarHtml")`**.

GAS stays **thin:** no calculation, permission, engineering validation, or Supabase access.

## 16. Implementation Slice Candidate After Audit

| Candidate | Scope |
|-----------|--------|
| **`MODULE_01_SIDEBAR_STATIC_CONTEXT_V1`** | Registry/menu opens sidebar; **shell** HTML; session/module context from API; buttons **placeholder** or non-functional **except** Refresh if wired; **no** create yet. |
| **`MODULE_01_CREATE_CALCULATION_MODAL_V1`** | Full create flow — **higher** risk / dependency on DB contract. |

**Recommendation:** Start with **`MODULE_01_SIDEBAR_STATIC_CONTEXT_V1`**, then **`MODULE_01_CREATE_CALCULATION_MODAL_V1`** once context + envelope are stable.

## 17. Open Questions

- Add `OPEN_MODULE_01_SIDEBAR` via **manual SQL** on current registry S01 vs **S02 migration**?  
- Should **`GET /api/module01/sidebar/context`** ship **before** registry row exists (bootstrap order)?  
- **`DocumentProperties` cache** for `active_calculation_id` — **on** in Iteration 01 or defer until create flow exists?  
- Does **Create Calculation** persist to **existing** `module01_calculations` / versions tables, or a stub table (separate approval)?  
- **Product types** allowed in Iteration 01 (`KZO` only vs enum)?  
- Module 01 **generic** shell vs **KZO-specific** labels first?

## 18. Out of Scope

- Implementation of any kind  
- HTML/CSS/GAS/Python/SQL  
- New migrations  
- Real calculation engine  
- KZO engineering, BOM, snapshot logic (unless separately approved)

## 19. Verdict

**`MODULE_01_SIDEBAR_TECH_SPEC_READY_FOR_AUDIT`**
