# Module 01 — Create Calculation V1 Implementation

## Objective

Implement the first real Module 01 transaction: **Create Calculation V1** — HTTP **`POST /api/module01/calculations/create`**, transactional inserts (header + initial version **`-00`** + status history), structured **`notes`** for `product_type` / comment / reference, GAS modal shell, and sidebar refresh path — **without** engineering calculation, KZO, BOM, snapshots, DB schema changes, or SQL execution by Cursor.

## Source technical spec

- `docs/ARCHITECTURE/EDS_POWER_MODULE_01_CREATE_CALCULATION_TECHNICAL_SPEC.md`

## Files changed

| Area | Path |
|------|------|
| Backend service | `services/module01_calculations_service.py` |
| Sidebar (active calculation) | `services/module01_sidebar_service.py` |
| API route (thin) | `main.py` |
| Tests | `tests/test_module01_calculations_create_endpoint.py`, `tests/test_module01_calculations_service.py` |
| Sidebar test mock | `tests/test_module01_sidebar_context_endpoint.py` |
| GAS transport | `gas/AuthTransport.gs` |
| GAS modal | `gas/Module01CreateCalculationModal.gs`, `gas/Module01CreateCalculationModalHtml.html` |
| GAS sidebar UI | `gas/Module01SidebarHtml.html` |

## Backend endpoint summary

- **`POST /api/module01/calculations/create`**
- **Auth:** `Authorization: Bearer` session token; **`user_id` / `role` never** taken from JSON body.
- **Body:** `source_client` (**`GAS_TERMINAL_V1`**), `terminal_id`, `spreadsheet_id`, nested **`payload`** (`calculation_title`, `potential_customer`, `product_type` = **KZO**, optional `comment`, `external_reference`).
- **Errors:** `MODULE01_CREATE_*` codes per technical spec; auth failures mapped to **`MODULE01_CREATE_AUTH_REQUIRED`**.

## Backend service summary

- **`services/module01_calculations_service.py`**
- **`build_structured_notes_v1`:** `EDS_POWER_CALC_NOTES_V1` + `PRODUCT_TYPE:` + optional `EXTERNAL_REFERENCE:` / `COMMENT:`.
- **Numbering:** UTC **`YYYYMMDDHHMM`** → **`calculation_base_number`** (12 digits); **`calculation_version_number`** = `{base}-00`; **`version_suffix`** **`-00`**.
- **Permission:** **`MODULE01_CREATE_CALCULATION`** must appear in **`eds_power_role_module_access`** / **`eds_power_module_actions`** for the user’s resolved role (via **`MenuRegistryService`**). Missing registry row → **`MODULE01_CREATE_PERMISSION_DENIED`** (operator DML required).
- **Terminal:** **`spreadsheet_id`** must match **`module01_user_terminals`** row for session **`terminal_id`**.

## Transaction behavior

- **Supabase/PostgREST** (Python client) does **not** expose a single multi-statement SQL transaction here without new DB functions.
- **Approach:** sequential **`insert`** with **compensating `delete`** on failure (`_delete_calculation_cascade`: history → version → calculation) so a failed version/history insert does not leave a stranded header when cleanup succeeds.
- **Collision:** bounded retry on unique violations by advancing UTC minute bucket (see service **`CALC_NUMBER_MAX_ATTEMPTS`**).

## GAS modal summary

- **`Module01CreateCalculationModalHtml.html`** — form + loading/double-submit guard; success summary then auto-close.
- **`Module01CreateCalculationModal.gs`** — `edsPowerModule01OpenCreateCalculationModal`, `module01CreateCalculationBootstrap_` (session status + `SpreadsheetApp.getActiveSpreadsheet().getId()`), `module01CreateCalculationSubmit`, optional **`EDS_POWER_<spreadsheet_id>_MODULE01_ACTIVE_CALCULATION_ID`** in **DocumentProperties**.
- **`Module01SidebarHtml.html`** — “Створити новий розрахунок” opens modal; **Оновити** reloads sidebar context from **`GET /api/module01/sidebar/context`**.
- **Apps Script naming:** modal uses **`.html`** file **`Module01CreateCalculationModalHtml`** (distinct from **`.gs`** basename).

## Registry action / DML status

**Cursor did not execute SQL.** Backend **denies create** until action **`MODULE01_CREATE_CALCULATION`** exists and is granted to the operator’s role(s).

### Operator DML (template — adjust `role_code` / environment as governed)

```sql
-- 1) Action row (MODULE_01 module)
insert into public.eds_power_module_actions (
    module_id,
    action_key,
    action_type,
    menu_label,
    visibility,
    enabled,
    sort_order,
    requires_auth,
    metadata
)
select
    m.id,
    'MODULE01_CREATE_CALCULATION',
    'OPEN_DIALOG',
    'Створити новий розрахунок',
    'VISIBLE',
    true,
    15,
    true,
    '{}'::jsonb
from public.eds_power_modules m
where m.module_code = 'MODULE_01'
on conflict (action_key) do nothing;

-- 2) Bind to TEST_OPERATOR (example — extend per governance)
insert into public.eds_power_role_module_access (
    role_id,
    module_id,
    action_id,
    access_level,
    visible,
    enabled,
    environment_scope
)
select
    r.id,
    a.module_id,
    a.id,
    'USE',
    true,
    true,
    'PRODUCTION'
from public.module01_roles r
cross join public.eds_power_module_actions a
where r.role_code = 'TEST_OPERATOR'
  and r.is_active = true
  and a.action_key = 'MODULE01_CREATE_CALCULATION'
on conflict on constraint uq_eds_power_role_module_access_role_action_env do update set
    visible = excluded.visible,
    enabled = excluded.enabled,
    access_level = excluded.access_level;
```

**Note:** Constraint name **`uq_eds_power_role_module_access_role_action_env`** must match live DB (from `20260507100000_eds_power_dynamic_menu_registry_s01.sql`). If conflict syntax differs, use operator-approved upsert pattern.

## Tests performed

- **`python -m pytest`** — **142** passed (full suite), including:
  - Create endpoint: missing/invalid token → **`MODULE01_CREATE_AUTH_REQUIRED`**
  - Invalid `product_type`, missing title, permission denied, success envelope shape
  - **`main.module01_calculations_create`** AST line-count thin check
  - Service: structured notes, payload validation, mocked happy-path create

## What was NOT changed

- No migrations / DDL / remote Supabase / Render env / secrets in repo.
- No KZO engineering, BOM, snapshot, or product configurator logic.
- No `main.py` transaction or notes-formatting implementation beyond route wiring and error mapping.

## Risks / blockers

- **Registry gap:** Without operator DML, **`MODULE01_CREATE_PERMISSION_DENIED`** in production.
- **PostgREST atomicity:** Compensating deletes are **best-effort**; crash between inserts could theoretically leave orphans (low probability; mitigated by cleanup on known failures).
- **Sidebar refresh:** After modal success, operator/user should use **«Оновити»** on sidebar (or reopen) to reload **`GET /api/module01/sidebar/context`**.
- **Active calculation display:** Sidebar shows **latest** non-archived calculation for **`created_by_user_id`** (simplification for V1).

## Verdict

**`MODULE_01_CREATE_CALCULATION_V1_IMPLEMENTATION_PENDING_OPERATOR_DML_AND_LIVE_TEST`**

Next: **operator applies registry DML** + **live create** smoke + optional Gemini audit.
