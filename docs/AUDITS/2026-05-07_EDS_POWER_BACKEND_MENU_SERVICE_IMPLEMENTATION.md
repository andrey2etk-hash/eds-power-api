# EDS Power Backend Menu Service Implementation

## Objective

Implement FastAPI backend reading for the DB-driven dynamic menu registry (`public.eds_power_*` tables, SQL Registry S01) and connect `GET /api/module01/auth/menu` to real Supabase data with fail-closed errors. No GAS changes, no DB migrations, no product/calculation logic.

## Scope

- `MenuRegistryService` with joined registry query and grouping.
- Authenticated menu endpoint (Bearer session); role from session context only.
- Standard success/error envelope; documented error codes.
- Flattened `data.menus` for existing GAS `EDSPowerCore` contract (plus `data.modules` for API contract).

## Source plan

- `docs/ARCHITECTURE/EDS_POWER_DB_DRIVEN_MENU_BACKEND_INTEGRATION_PLAN.md` (Gemini **PASS / READY_FOR_IMPLEMENTATION_TASKING** per task gate).

## Files changed

- `main.py` — session helper `_auth_validate_session_context`, `_auth_resolve_primary_role_id`, `_menu_registry_error_response`, `_menu_flatten_for_gas`, `module01_auth_menu` DB path, `module01_auth_session_status` refactored to shared session validation; `EDS_MENU_FORCE_MOCK` dev escape (authenticated only).
- `services/__init__.py` — package marker.
- `services/menu_registry_service.py` — new service.
- `tests/test_module01_auth_menu_endpoint.py` — menu endpoint tests.
- `tests/test_menu_registry_service.py` — service/filter unit tests.

## Service summary

- **`MenuRegistryService`** — queries `eds_power_role_module_access` with embedded `eds_power_modules`, `eds_power_module_actions`, `module01_roles!inner`, filtered by `role_id`, `visible`, `enabled`, `environment_scope`, then filters `is_active` / action `enabled` in Python. Groups actions under modules; sorts by module and action `sort_order`.
- **`resolve_menu_environment_scope()`** — reads **`EDS_MENU_ENVIRONMENT_SCOPE`** (default **`PRODUCTION`**); invalid values → `MENU_ENVIRONMENT_SCOPE_INVALID`.

## Endpoint summary

- **`GET /api/module01/auth/menu`**
  - **Authorization:** `Bearer <session_token>` (required).
  - **Success:** `status: success`, `data.modules` (nested registry shape), `data.menus` (flat list for GAS: `menu_label`, `action_key`, `action_type`, `visibility`, `enabled`, `sort_order`, optional `module_id` / `module_name` / `module_status` for non–`SYSTEM_SHELL`).
  - **Metadata:** `menu_source` = `registry` or `mock_dev_fallback`; `environment_scope`; `auth_enforcement` = `authenticated`.

## Query/filter logic

- Join path: `acc` → `m` → `a` → `r` (via PostgREST select embedding + `module01_roles!inner`).
- Filters on query: `acc.role_id`, `acc.visible = true`, `acc.enabled = true`, `acc.environment_scope` = configured scope.
- Post-fetch: `m.is_active`, `a.enabled`, role row `id` matches.

## Error handling

| `error_code` | When |
|--------------|------|
| `AUTH_*` | Missing/invalid token, session, user, terminal (unchanged auth contract). |
| `MENU_ENVIRONMENT_SCOPE_INVALID` | Invalid `EDS_MENU_ENVIRONMENT_SCOPE`. |
| `MENU_ROLE_NOT_FOUND` | No resolvable `module01_roles` id for user. |
| `MENU_REGISTRY_QUERY_FAILED` | Supabase client/query exception or bad response shape. |
| `MENU_REGISTRY_UNAVAILABLE` | Config claims ready but registry returns unusable state. |
| `MENU_NO_ALLOWED_ACTIONS` | No actions after filters (machine-readable; no silent empty success). |

Errors use `status: error`, `data: null`, standard `error` object and timed `metadata`.

## Security boundary

- Service role via existing `_auth_get_supabase_client()` pattern only on server.
- No `role_id` from client; derived from `module01_user_roles` / `module01_roles` for authenticated `user_id`.
- Response does not expose raw `eds_power_role_module_access` rows.

## Tests performed

- `unittest`: `tests.test_module01_auth_menu_endpoint`, `tests.test_menu_registry_service`, full `tests` discovery (123 tests) — **PASS** in local run.
- Live Supabase / Render / operator menu refresh: **NOT TESTED** in this change (pending deployment + operator check).

## What was NOT changed

- GAS (`gas/**`).
- Supabase SQL / migrations.
- Render configuration and env secrets (documented env **names** only: `EDS_MENU_ENVIRONMENT_SCOPE`, `EDS_MENU_FORCE_MOCK`).
- KZO, demo calculations, snapshot persistence, product modules.

## Verdict

**DB_DRIVEN_MENU_BACKEND_SERVICE_IMPLEMENTED — pending Render + authenticated operator menu test**
