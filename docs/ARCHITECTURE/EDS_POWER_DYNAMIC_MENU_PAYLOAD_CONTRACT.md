# EDS Power Dynamic Menu Payload Contract

## 1. Purpose

Define the response contract for API-driven EDS Power terminal menus.

The menu is not hardcoded in local terminal scripts.
The menu is determined by backend truth:
- user
- session
- terminal
- role
- module access
- module status
- core compatibility

## 2. Core Principle

GAS renders menu.
API decides menu.

EDSPowerCore must not decide module access locally.

## 3. Request Context

Menu request must include or derive:
- session token from Authorization header
- terminal_id
- spreadsheet_id
- client_type = GAS
- core_version
- bootstrap_version

Do NOT include:
- password
- token hash
- raw secrets in logs

## 4. Backend Resolution Responsibilities

Backend must resolve:
- valid session
- user_id
- user role(s)
- terminal exists
- terminal active/revoked
- terminal assignment result
- module access
- module status
- allowed actions
- required core version compatibility

## 5. Menu Response Envelope

All menu responses must use standard envelope:

{
  "status": "success",
  "data": {
    "menu_version": "EDS_POWER_MENU_V1",
    "user_context": {},
    "terminal_context": {},
    "core_compatibility": {},
    "menus": []
  },
  "error": null,
  "metadata": {}
}

## 6. user_context

Conceptual fields:
- user_id
- email
- display_name
- primary_role
- roles
- is_admin
- session_expires_at

Do NOT include:
- session token
- password hash
- token hash

## 7. terminal_context

Conceptual fields:
- terminal_id
- terminal_name
- terminal_type
- terminal_status
- assignment_result
- core_channel
- location
- department

## 8. core_compatibility

Conceptual fields:
- required_core_version
- current_core_version
- bootstrap_version
- compatibility_status

Allowed statuses:
- COMPATIBLE
- CORE_UPDATE_RECOMMENDED
- CORE_UPDATE_REQUIRED
- BOOTSTRAP_UPDATE_REQUIRED

## 9. Menu Item Structure

Each menu item should conceptually include:
- menu_id
- parent_menu_id
- module_id
- module_name
- menu_label
- action_key
- action_type
- visibility
- enabled
- module_status
- required_role
- sort_order
- metadata

Allowed action_type:
- OPEN_DIALOG
- OPEN_SIDEBAR
- RUN_BATCH_ACTION
- REFRESH_MENU
- LOGOUT
- SESSION_STATUS
- PLACEHOLDER_DISABLED

## 10. Module Status Values

Allowed:
- RELEASED
- ADMIN_TEST
- DEV
- DISABLED
- MAINTENANCE
- HIDDEN
- PLANNED

Rules:
- production users see only RELEASED modules/actions allowed by role.
- admin/dev users may see ADMIN_TEST or DEV if registry allows.
- HIDDEN modules must not be rendered.
- DISABLED / MAINTENANCE may render as disabled if API says so.
- PLANNED may render only for admin if API allows.

## 11. Visibility / Enabled Rules

API decides:
- whether item is visible
- whether item is enabled
- reason if disabled

EDSPowerCore renders according to API response only.

## 12. Error Contract

Menu endpoint must return machine-readable errors:

AUTH_MISSING_TOKEN
AUTH_INVALID_TOKEN
AUTH_SESSION_EXPIRED
AUTH_SESSION_REVOKED
TERMINAL_UNKNOWN
TERMINAL_REVOKED
TERMINAL_NOT_ASSIGNED_BLOCKED
MENU_NO_ACCESS
CORE_VERSION_UNSUPPORTED

Use standard error envelope.

## 13. EDSPowerCore Rendering Rules

EDSPowerCore may:
- request menu payload
- parse menu JSON
- create Google Sheets menu
- render disabled/fallback items if API instructs
- show safe error message

EDSPowerCore must NOT:
- decide module access
- show hidden modules
- invent actions
- hardcode production module menu
- bypass API on failure except emergency fallback
- execute disabled action

## 14. Emergency Fallback Menu

If API or Core unavailable, local/bootstrap may show only safe fallback:
- Login
- Refresh Menu
- Session Status
- Help / System unavailable

No module actions in fallback unless explicitly approved later.

## 15. Admin vs Production Isolation

Admin may see:
- released modules
- admin test modules
- dev placeholders

Production users see:
- released modules only
- only actions allowed by role

New modules must not break old modules.

## 16. What This Does NOT Implement

This document does not implement:
- backend endpoint
- Supabase schema
- menu rendering code
- module access registry
- admin panel
- calculation modules

## 17. Verdict

Gemini audit verdict:
- `DYNAMIC_MENU_PAYLOAD_CONTRACT_PASS`

Status:
- `PASS`

Confirmed:
- backend owns menu truth
- GAS renders menu only
- user/session/terminal/role/module context is defined
- module statuses are defined
- machine-readable menu errors are defined
- no implementation drift

Implementation gate:
- dynamic menu mock integration is unlocked as the next bounded implementation step
- DB-driven role/module registry remains deferred

EDS Power Dynamic Menu Payload Contract is CLOSED / PASS.
