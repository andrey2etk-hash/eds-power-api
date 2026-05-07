# EDS Power Module 01 — Create Calculation Modal V1 Planning

## 1. Purpose

Plan the first interactive modal workflow in Module 01: creating a calculation header/record.

This document defines contracts and flow only.

No implementation.

## 2. Starting Point

Module 01 **Sidebar Static Context V1** is **live validated** (`MODULE_01_SIDEBAR_STATIC_CONTEXT_V1_LIVE_PASS` — see `docs/AUDITS/2026-05-07_MODULE_01_SIDEBAR_STATIC_CONTEXT_V1_LIVE_OPERATOR_TEST.md`).

Current sidebar state:

- Authenticated user displayed
- `active_calculation` = null
- **No active calculation**
- Primary actions placeholder / disabled (including **Створити новий розрахунок**)

## 3. Workflow Goal

User clicks:

**Створити новий розрахунок**

Then modal opens:

**Створити розрахунок**

User fills required fields.

GAS sends an authenticated request to the backend.

Backend validates, creates a calculation record, returns `calculation_id` and human-visible calculation identifier(s).

Sidebar updates from **No active calculation** to active calculation context (after refresh).

## 4. Modal Fields

| # | Field id | Label | Required | Type | Notes |
|---|----------|-------|----------|------|--------|
| 1 | `calculation_title` | Назва розрахунку | **yes** | text | Backend validation: non-empty; max length **TBD** (audit) |
| 2 | `potential_customer` | Потенційний замовник | **TBD** (see §17) | text | Maps to existing column concept where persisted |
| 3 | `product_type` | Тип продукту | **yes** | select | V1 allowed: **KZO** only (see §5) |
| 4 | `comment` | Коментар | no | textarea | **Schema gap:** no dedicated column on `module01_calculations` in Slice 01 DDL — see §8 |
| 5 | `external_reference` | Об’єкт / заявка / примітка | no | text | **Schema gap:** no dedicated column — see §8 |

## 5. Product Type Scope

V1 must not imply broad product support.

**Recommended V1:** `product_type` enum:

- **KZO**

No KZO engineering logic in this slice.

`product_type` is a **classification** / routing field for the calculation header and future UX; persistence mapping must be confirmed against `public.module01_calculations` (see §8).

## 6. Request Contract

**Endpoint concept:**

`POST /api/module01/calculations/create`

**Request body concept:**

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

**Rules:**

- `user_id` must come from **Bearer token / session**, not from payload.
- Role must be **resolved by backend**.
- `terminal_id` / `spreadsheet_id` must be **verified by backend** (bound terminal, active session).
- GAS must **not** generate `calculation_base_number`, `calculation_version_number`, or any canonical server number.
- GAS must **not** decide permissions (button visibility ≠ authorization).

## 7. Backend Validation Rules

Backend validates:

- Authenticated session exists
- User is active
- Terminal is active and matches session
- User has permission for Module 01 **create calculation** action
- `product_type` is in the allowed set for V1
- Required fields are present and normalized
- Text fields meet length / safety rules (exact limits **TBD** at implementation)

**Possible machine-readable error codes (illustrative):**

- `MODULE01_CREATE_AUTH_REQUIRED`
- `MODULE01_CREATE_PERMISSION_DENIED`
- `MODULE01_CREATE_INVALID_PAYLOAD`
- `MODULE01_CREATE_PRODUCT_TYPE_UNSUPPORTED`
- `MODULE01_CREATE_TERMINAL_MISMATCH`
- `MODULE01_CREATE_BACKEND_UNAVAILABLE`

## 8. Persistence Planning

**Planning only.** No SQL execution in this task. No new tables.

**Existing tables (repo reference: `supabase/migrations/20260504190000_module01_schema_slice_01.sql`):**

| Table | Role |
|-------|------|
| `public.module01_calculations` | Calculation **header**: `id`, `calculation_base_number`, `title`, `potential_customer`, `sales_manager_user_id`, `created_by_user_id`, `current_status` (default **DRAFT**), `is_archived`, timestamps |
| `public.module01_calculation_versions` | **Version** rows per calculation: `calculation_id`, `version_suffix` (default **`-00`**, format `^-[0-9]{2}$`), `calculation_version_number` (unique), `status`, etc. |
| `public.module01_calculation_status_history` | Status transitions keyed by **`calculation_version_id`** (not calculation id alone) |

**Read-only schema observations relevant to Create V1:**

1. **`calculation_base_number`** is **required** and must satisfy **`^[0-9]{12}$`** (exactly **12 digits**). This **differs** from a human display pattern such as `YYYYMMDDHHMM-XX`; **display vs stored base number** must be resolved before implementation (see §9, §17).
2. **`module01_calculations`** has **`title`** and **`potential_customer`**; it does **not** define **`product_type`**, **`comment`**, or **`external_reference`** in Slice 01. Mapping options for implementation (after audit only): append to `title` / `notes` elsewhere / JSON in an approved column / separate migration — **not decided here**.
3. **`module01_calculation_status_history`** requires an existing **`module01_calculation_versions`** row.

**Open question (persistence):**

Should Create Calculation V1 persist **only** a header row in `module01_calculations`?

**Or** also create an **initial** row in `module01_calculation_versions` (suffix `-00` default exists in DDL)?

**Recommended planning direction:**

- **Immediate persist** of header with **`current_status` = `DRAFT`**.
- **`calculation_base_number`** generated **only** on backend, **collision-safe** vs unique constraint.
- **Initial version row:** create **if** implementation audit confirms a clean invariant (e.g. every calculation has at least one version for history/status APIs). If header-only is chosen, **`module01_calculation_status_history`** cannot be used until a version exists.

No SQL execution in this planning task.

## 9. Calculation Number

Backend owns calculation number generation.

**Human-facing UX concept (prior narrative):** `YYYYMMDDHHMM-XX` style display.

**Existing DDL constraint:** `calculation_base_number` = **12 numeric digits** only; version table uses **`version_suffix`** like `-00`, `-01` and a separate **`calculation_version_number`**.

**Open question:**

Should suffix semantics start at **`-01`**, **`-00`**, or **revision-only later**?

For V1 this document defines **concept only**. **Implementation** must reconcile UX, API response shape, and **`^[0-9]{12}$`** / version-number uniqueness rules.

## 10. Response Contract

**Success response concept:**

```json
{
  "status": "success",
  "data": {
    "calculation": {
      "calculation_id": "...",
      "calculation_number": "202605071904-01",
      "status": "DRAFT",
      "product_type": "KZO",
      "title": "...",
      "created_at": "..."
    },
    "sidebar_update": {
      "active_calculation_id": "...",
      "active_calculation_display": "202605071904-01 — KZO — DRAFT"
    }
  },
  "error": null,
  "metadata": {
    "request_id": "...",
    "api_version": "..."
  }
}
```

**Note:** `calculation_number` / `active_calculation_display` above are **illustrative**. The backend may return `calculation_base_number`, `calculation_version_number`, or a composed **display string** once the format audit is complete.

## 11. Sidebar Update After Success

After successful create:

- Modal closes (or shows a short success state — see §17).
- Sidebar **refreshes context** from backend (`GET /api/module01/sidebar/context` or equivalent).
- Active calculation block changes from **No active calculation** to: identifier(s), **DRAFT**, **KZO**, **title**, **created_at** (exact fields per sidebar contract).

GAS **may** cache:

`EDS_POWER_<spreadsheet_id>_MODULE01_ACTIVE_CALCULATION_ID`

Backend remains **source of truth**; cache is optional performance hint only.

## 12. Error Handling UI

Modal must show:

- Field-level validation errors (basic empty required + backend field errors)
- Backend error summary (fail-closed, readable message)
- **Retry** and **Cancel**

Sidebar must **not** silently change state on failed creation.

If backend fails:

- Modal stays open or shows a clear error state
- `active_calculation` unchanged until a successful create + refresh

## 13. GAS Thin Client Boundary

GAS **may:**

- Open modal
- Collect form input
- Send **one** authenticated request
- Display backend response
- Refresh sidebar after success

GAS **must NOT:**

- Generate calculation number
- Encode business rules beyond minimal UI hints (non-empty)
- Decide product permissions
- Run engineering / KZO logic
- Write to Supabase directly
- Create snapshots directly

## 14. Backend / main.py Boundary

`main.py` must remain **thin**.

Future implementation direction (not active):

- Route wiring in `main.py` or a router module
- Service: `services/module01_calculations_service.py` (name per technical spec trajectory)
- Repository / persistence helpers only if needed
- No calculation or product logic in `main.py`

## 15. Registry / Sidebar Action Implications

Sidebar placeholder **Створити новий розрахунок** maps to a future action handle, e.g. **`MODULE01_CREATE_CALCULATION`**.

Behavior: opens **Create Calculation** modal.

No registry schema change in **this** planning task.

**Open question:**

Should this action appear in the **Supabase menu registry** before implementation, or remain an **internal** sidebar-only action in V1?

## 16. Out of Scope

Explicitly exclude:

- Modal HTML implementation
- GAS implementation
- Backend endpoint implementation
- SQL execution
- Migrations
- New schema
- KZO engineering logic
- Calculation engine
- BOM logic
- Snapshot logic
- Production workflow beyond DRAFT header/create

## 17. Open Questions

1. Is **`potential_customer`** required or optional in V1?
2. Which table/column holds **product_type** for Slice 01, or is a migration/extension required later?
3. Where do **`comment`** and **`external_reference`** persist without new DDL?
4. Should an **initial `module01_calculation_versions`** row be created on create? If yes, suffix **` -00`** vs **`-01`**?
5. Exact **`calculation_base_number`** / **`calculation_version_number`** / **display string** rules vs **`^[0-9]{12}$`**?
6. Should **`product_type`** be fixed **KZO** only in UI or loaded from a **backend-provided** enum?
7. Should **Create Calculation** require a new **registry permission / action** row?
8. Should **`active_calculation_id`** be stored in **DocumentProperties** in V1 implementation?
9. Should modal close immediately after success or show a **success summary** step first?

## 18. Risk Register

| # | Risk | Mitigation (planning) |
|---|------|------------------------|
| 1 | **Persistence mismatch** — modal fields do not align with existing columns | Schema inspection + mapping doc before coding; possibly narrow V1 fields |
| 2 | **Client-side validation creep** — business rules duplicated in GAS | Thin client review; backend remains authoritative |
| 3 | **State drift** — sidebar stale after create | Mandatory refresh after success; optional ID cache documented |
| 4 | **Permission ambiguity** — visible button without backend allow | Enforce permission on every **POST**; fail closed |
| 5 | **Number collision** — concurrent creates | Server-side unique constraints + retry-safe generation |
| 6 | **Format contradiction** — UX wants `YYYYMMDDHHMM-XX` but DDL enforces 12-digit base | Resolve in audit before implementation |

## 19. Recommended Next Step After Audit

If this planning document passes audit:

Next bounded implementation candidate:

**`MODULE_01_CREATE_CALCULATION_MODAL_V1_IMPLEMENTATION`**

**Only after:**

- Schema / persistence target confirmation (read-only inspection + signed mapping)
- Audit approval
- Explicit user approval for implementation TASK

## 20. Verdict

**`MODULE_01_CREATE_CALCULATION_MODAL_V1_PLAN_READY_FOR_AUDIT`**
