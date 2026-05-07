# Module 01 Sidebar Static Context V1 — Implementation Closeout

## Objective

Deliver **`MODULE_01_SIDEBAR_STATIC_CONTEXT_V1`**: authenticated **`GET /api/module01/sidebar/context`**, thin **`main.py`** wiring, **`services/module01_sidebar_service.py`**, and minimal **GAS + HTML** sidebar shell with **loading** and **error** states (no blank panel). **No** calculation, product, KZO, BOM, snapshot, or registry SQL execution.

## Source spec

- **`docs/ARCHITECTURE/EDS_POWER_MODULE_01_SIDEBAR_TECHNICAL_SPEC.md`** (Gemini **PASS / `TECH_SPEC_LOCKED`**)
- Global: Render Thinking / GAS Thin UI, **main.py** Thin Router, GAS Deployment and Sync doctrine

## Files changed / added

| Path | Role |
|------|------|
| `main.py` | Route **`GET /api/module01/sidebar/context`**, auth via `_auth_validate_session_context`, errors via `_module01_sidebar_error_response` |
| `services/module01_sidebar_service.py` | Assemble static `sidebar` DTO (no engine) |
| `tests/test_module01_sidebar_context_endpoint.py` | Endpoint + thin-route checks |
| `gas/AuthTransport.gs` | **`module01SidebarContextTransport_`**, **`MODULE01_SIDEBAR_CONTEXT_ENDPOINT_PATH`**, **`module01AuthResolveSidebarContextUrl_`** |
| `gas/Module01Sidebar.gs` | **`edsPowerOpenModule01Sidebar`**, **`module01SidebarServerGetContext`**, **`module01SidebarBuildSafeContext_`** |
| `gas/Module01Sidebar.html` | Loading, error, main panels; placeholder disabled buttons |
| `gas/core/EDSPowerCore.gs` | Menu callback: **`OPEN_SIDEBAR`** / action_key **`OPEN_MODULE_01_SIDEBAR`** → **`edsPowerOpenModule01Sidebar`** |

## Backend endpoint summary

- **Path:** `GET /api/module01/sidebar/context`
- **Auth:** `Authorization: Bearer <session>`; **no** `user_id` / `role` from client body
- **Success:** `status: success`, `data.sidebar` with `sidebar_id`, `module_code`, `module_name`, `environment_scope`, `user`, `session` (`authenticated`, `expires_at`, `remaining_seconds`), `active_calculation: null`, `sections`
- **Auth errors:** existing **`auth_error`** envelope (`AUTH_MISSING_TOKEN`, `AUTH_INVALID_TOKEN`, `AUTH_SESSION_EXPIRED`, …) with `action: sidebar_context`
- **Module errors:** `status: error`, `MODULE01_PERMISSION_DENIED`, `MODULE01_SIDEBAR_CONTEXT_UNAVAILABLE` (incl. env scope / build failure); **`metadata.menu_source`:** `registry`

## Backend service summary

- **`build_module01_sidebar_data`** reads **active** `module01_users` row (incl. optional `display_name`), picks primary **`role_code`**, computes **`remaining_seconds`**, returns static sections; **no** DB writes.

## GAS files added

- **`Module01Sidebar.gs`** / **`Module01Sidebar.html`** — open sidebar, fetch context via transport, display result or **visible** error.
- **V1:** **no** `DocumentProperties` cache for `active_calculation` (always null from API); namespaced cache deferred.

## HTML sidebar behavior

- Default **loading** panel (blue info style).
- On failure: **error** panel (red) with message — **not** an empty white surface.
- On success: header **Module 01 — Розрахунки**, session/user lines (expiry + remaining seconds when present), **No active calculation**, four **disabled** primary actions + note that V1 is placeholders.

## Error handling / no blank sidebar

- Transport / HTTP ≥500 → Ukrainian “server unavailable” message.
- `auth_error` / `error` envelopes mapped to short operator-facing strings (incl. expired session).
- **Risk control:** no silent empty UI; loading shown until `google.script.run` completes.

## Registry action status

**Not applied by Cursor** (Manual SQL Apply Governance). Operator may add row later if `eds_power_module_actions` supports needed columns.

**Illustrative INSERT** (verify `module_id`, `action_type`, environment, and FKs against live schema before running):

```sql
-- OPERATOR-ONLY: adjust UUIDs, module_id, action_id, role bindings, environment_scope to match S01 registry.
-- DO NOT run from Cursor/agents.

-- Example pattern (placeholder):
-- INSERT INTO eds_power_module_actions (...)
-- VALUES (..., 'OPEN_MODULE_01_SIDEBAR', 'OPEN_SIDEBAR', 'Module 01 — Розрахунки', ...);
```

If schema cannot represent **`OPEN_SIDEBAR`** cleanly, track as **registry blocker** and open S02 planning. Until the menu item exists, operators can call **`edsPowerOpenModule01Sidebar`** from the Apps Script editor for smoke tests.

## Tests performed

- `python -m pytest tests/test_module01_sidebar_context_endpoint.py -v` — **PASS**
- `python -m pytest tests/ -q` — **131 passed** (full suite at time of closeout)

## What was NOT changed

- **No** SQL execution, migrations, Supabase DDL/DML by Cursor  
- **No** Render env changes  
- **No** Create Calculation / modal / calculation endpoints  
- **No** auth protocol changes (reuse existing session validation)  
- **No** secrets logged  

## Verdict

**`MODULE_01_SIDEBAR_STATIC_CONTEXT_V1_IMPLEMENTED_PENDING_OPERATOR_TEST`**

Next: operator **sync** `Module01Sidebar.gs`, `Module01Sidebar.html`, `AuthTransport.gs`, `EDSPowerCore.gs` per **`docs/ARCHITECTURE/EDS_POWER_GAS_DEPLOYMENT_AND_SYNC_DOCTRINE.md`**; deploy API; login; open sidebar (menu entry when registry ready, or manual `edsPowerOpenModule01Sidebar`).
