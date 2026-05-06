# EDS Power Dynamic Menu Mock Integration

Date: 2026-05-06  
Mode: bounded backend + GAS core integration (mock pipe only)

## Objective

Implement and recover the first bounded EDS Power dynamic menu transport/rendering pipe:
`MASTER_TERMINAL_TEMPLATE` requests mock menu payload from backend and renders Google Sheets custom menu through `EDSPowerCore`.

## Scope

- In scope: mock backend menu endpoint + EDSPowerCore menu transport/rendering + documentation closeout.
- Out of scope: DB schema changes, SQL, Supabase role-module access, calculation/engineering logic, module runtime, admin/terminal provisioning, production rollout.

## Approved prerequisites

- EDS Power Terminal Fleet Governance finalized.
- EDS Power Minimal Local Bootstrap Contract passed.
- EDS Power Client Core Contract passed.
- EDS Power Dynamic Menu Payload Contract passed.
- EDS Power Master Terminal Template Handshake passed.

## Provider error recovery note

- Provider error interrupted the initial implementation attempt.
- Recovery check confirmed code is syntactically valid and bounded.
- Missing documentation/state updates were completed in this recovery continuation.
- Follow-up diagnostic review identified a false-positive risk: fallback menu looked too similar to expected dynamic menu.
- Initial visual operator result was reclassified as **`DYNAMIC_MENU_NOT_VERIFIED — FALLBACK_FALSE_POSITIVE_RISK`** until diagnostic evidence became available.

## Backend mock endpoint summary

- Added endpoint: `GET /api/module01/auth/menu`.
- Returns standard envelope with mock data payload for menu rendering.
- No new DB tables, no SQL, no role-module registry queries, no calculation calls.
- Endpoint returns no session token, token hash, password hash, or secrets.

## Mock payload summary

- `menu_version = EDS_POWER_MENU_V1`
- mock user context (`Mock User`, `MOCK_OPERATOR`, non-admin)
- template terminal context (`terminal_id = TERMINAL_TEMPLATE`, `terminal_status = TEMPLATE`)
- core compatibility block (`required_core_version = EDS_POWER_CORE_FOUNDATION_V1`)
- bounded menu actions:
  - `REFRESH_MENU`
  - `SESSION_STATUS`
  - `PLACEHOLDER_DISABLED` (Module 01 planned placeholder)
  - `LOGOUT`

## EDSPowerCore rendering summary

- `EDSPowerCore_refreshMenu(context)` now:
  - calls backend `GET /api/module01/auth/menu`
  - parses and validates envelope (`data.menus` required)
  - renders menu named `EDS Power`
  - renders only `VISIBLE` items
  - maps only approved action types in this slice
  - renders placeholder item safely as planned/unavailable action
- Local role/access decisions are not implemented in GAS core.

## Governance drift discovered and corrected

- Drift 1: GAS appended `(planned)` locally for placeholder menu item, which violated backend label ownership.
- Drift 2: fallback menu used a different title (`EDS Power Fallback`), which could leave two visible custom menus in one sheet session.
- Previous two-menu visual state is **not** accepted as final PASS.

Applied correction:

- Backend now owns final placeholder label text (`Module 01 — Розрахунки (planned)`).
- GAS no longer mutates placeholder labels locally.
- Fallback and dynamic states now use one canonical menu title: `EDS Power`.
- Fallback is distinguished by setup-only items and diagnostics (`menu_source = fallback_static`), not by separate menu title.

Behavioral drift decision (`EDSPowerCore_onTerminalOpen`):

- `onTerminalOpen` now renders a safe bootstrap/fallback `EDS Power` menu.
- This is accepted for this slice because it does not introduce business/module logic.
- Dynamic menu transport remains under explicit `edsPowerRefreshMenu()` path.

## Local bootstrap boundary

- `edsPowerRefreshMenu()` remains thin and delegates to `EDSPowerCore_refreshMenu(context)`.
- No local business logic expansion was introduced.

## Auth enforcement status: deferred / mock pipe only

- Auth enforcement for `/api/module01/auth/menu` is explicitly deferred in this mock slice.
- Defer marker is returned in metadata (`auth_enforcement = DEFERRED_FOR_MOCK_SLICE`).
- This is temporary and not a permanent auth bypass design.

## False-positive risk note

Observed visual menu (`EDS Power` with expected items) is no longer accepted as sufficient verification because fallback and dynamic states were not clearly separated.

Reclassified status (intermediate state):

- **`DYNAMIC_MENU_NOT_VERIFIED — FALLBACK_FALSE_POSITIVE_RISK`**

## Updated PASS criteria

Dynamic Menu Mock Integration PASS now requires all of:

1. Script Property `MODULE01_API_BASE_URL` is present.
2. Refresh diagnostic shows `endpoint_http_status = 200`.
3. Refresh diagnostic shows `menu_source = mock_backend`.
4. Refresh diagnostic shows `rendered_items > 0`.
5. Fallback menu (`EDS Power Fallback`) is not displayed.
6. No token/secrets are logged.

## Operator verification evidence (PASS)

Manual operator verification completed in `EDS Power — MASTER TERMINAL TEMPLATE`.

Execution log evidence:

```json
{
  "stage": "EDS_POWER_DYNAMIC_MENU_REFRESH",
  "menu_source": "mock_backend",
  "base_url_present": true,
  "endpoint_path": "/api/module01/auth/menu",
  "endpoint_http_status": 200,
  "rendered_items": 4,
  "terminal_id_mode": "template_marker",
  "terminal_id_present": true,
  "core_version": "EDS_POWER_CORE_FOUNDATION_V1",
  "error_code": null,
  "error_message": null
}
```

Rendered menu evidence:

- Menu title: `EDS Power`
- Menu items:
  - `Оновити меню`
  - `Статус сесії`
  - `Module 01 — Розрахунки (planned)`
  - `Вийти`

Fallback separation evidence:

- Same menu title rule: `EDS Power`
- Fallback-only items:
  - `⚠ Setup Required`
  - `Refresh Setup Check`

Confirmed:

- backend mock menu payload reached EDSPowerCore
- `endpoint_http_status = 200`
- menu rendered from backend mock payload
- false-positive fallback risk fixed
- fallback no longer looks like success menu
- Module 01 remains placeholder/planned only

## Security confirmation

- No secrets or token values are returned by mock endpoint.
- No token logging added in GAS/core code path.
- No DB schema writes introduced in this slice.

## What was NOT implemented

- DB-driven role/module registry
- Supabase `role_module_access` model
- real module action execution
- calculation or engineering endpoints
- admin provisioning
- terminal provisioning
- production rollout behavior

## Important limitation

This PASS confirms mock backend transport/render pipe only. It does not prove:

- DB-driven role/module access
- production RBAC
- real module availability registry
- calculation module execution
- admin provisioning

## Verdict: CORRECTION_PENDING_OPERATOR_RETEST

Governance correction for label ownership and single-menu-title behavior is implemented.
Operator retest is required to reconfirm PASS under corrected menu ownership rules.
