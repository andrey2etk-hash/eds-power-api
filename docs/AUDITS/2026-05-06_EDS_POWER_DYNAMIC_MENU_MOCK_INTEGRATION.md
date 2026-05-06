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

## Operator tests pending

Pending manual tests in `EDS Power — MASTER TERMINAL TEMPLATE`:

1. Run `edsPowerRefreshMenu()` and verify menu `EDS Power` updates from backend payload.
2. Run `edsPowerRefreshMenu()` again and verify clean redraw without menu duplication chaos.
3. Click Module 01 placeholder and verify safe message:
   `Module 01 is not active in this mock menu slice.`

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

## Verdict: IMPLEMENTATION_PENDING_OPERATOR_TEST

Dynamic menu mock transport/render pipe is implemented and recovered from provider interruption.  
Status: **`IMPLEMENTATION_PENDING_OPERATOR_TEST`**.
