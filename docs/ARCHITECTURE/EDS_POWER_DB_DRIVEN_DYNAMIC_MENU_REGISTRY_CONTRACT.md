# EDS Power DB-Driven Dynamic Menu Registry Contract

## 1. Purpose

Define how EDS Power dynamic menu data will be stored, resolved, and returned from Supabase through the backend.

This contract replaces hardcoded mock menu payload only after approval.

## 2. Current State

Current menu flow:  
Google Sheet terminal  
-> EDSPowerCore  
-> GET /api/module01/auth/menu  
-> hardcoded mock backend payload  
-> EDSPowerCore renders menu

Current status:  
Mock pipe verified.

Not yet implemented:
- DB-driven module registry
- DB-driven action registry
- DB-driven role access
- production RBAC
- terminal-aware menu filtering

## 3. Core Principle

Backend decides menu.  
Supabase stores registry truth.  
EDSPowerCore renders only.

GAS must not decide:
- module access
- role access
- terminal access
- module status
- production/dev visibility
- final labels

## 4. Registry Concepts

Define conceptual entities:

### modules

Represents system modules.

Conceptual fields:
- module_id
- module_code
- module_name
- module_status
- module_version
- description
- sort_order
- is_active

Allowed module_status:
- RELEASED
- ADMIN_TEST
- DEV
- DISABLED
- MAINTENANCE
- HIDDEN
- PLANNED

### module_actions

Represents actions inside modules or system shell.

Conceptual fields:
- action_id
- module_id
- action_key
- action_type
- menu_label
- visibility
- enabled
- sort_order
- requires_auth
- required_core_version
- metadata

Allowed action_type:
- OPEN_DIALOG
- OPEN_SIDEBAR
- RUN_BATCH_ACTION
- REFRESH_MENU
- LOGOUT
- SESSION_STATUS
- PLACEHOLDER_DISABLED

### role_module_access

Maps roles to modules/actions.

Conceptual fields:
- role_id
- module_id
- action_id
- access_level
- visible
- enabled
- environment_scope
- created_at
- updated_at

Allowed access_level:
- NONE
- VIEW
- USE
- ADMIN
- DEV_TEST

### terminal_module_access / terminal policy override

Optional future concept.

Purpose:  
Allow terminal-specific restriction/override.

Examples:
- admin terminal may see dev modules
- production terminal may hide dev modules
- revoked terminal sees nothing

Do NOT implement unless approved later.

## 5. Menu Resolution Inputs

Backend menu endpoint must resolve using:
- Authorization: Bearer session token
- user_id from session
- user roles
- terminal_id
- terminal status
- terminal assignment result
- module registry
- action registry
- role access registry
- core_version / bootstrap_version compatibility

## 6. Menu Resolution Rules

Backend must:

1. Validate session.
2. Validate terminal context.
3. Resolve user roles.
4. Resolve terminal assignment status.
5. Load modules/actions allowed by role and terminal policy.
6. Filter hidden/disabled items.
7. Apply module lifecycle status.
8. Return final menu labels.
9. Return final visibility/enabled state.
10. Return standard response envelope.

## 7. Admin vs Production Visibility

Production users:
- see only RELEASED modules/actions allowed by role
- do not see DEV/HIDDEN modules
- may see MAINTENANCE/DISABLED only if backend explicitly returns disabled item

Admin/dev users:
- may see RELEASED
- may see ADMIN_TEST
- may see DEV if role/terminal allows
- may see PLANNED placeholders if backend allows

Rule:  
Admin testing must not expose unfinished modules to production roles.

## 8. Terminal-Aware Menu Governance

Terminal is part of access context.

Backend must be able to distinguish:
- PERSONAL_TERMINAL
- ROLE_TERMINAL
- DEPARTMENT_TERMINAL
- ADMIN_TERMINAL
- TEST_TERMINAL
- MASTER_TEMPLATE

Special rule:  
MASTER_TERMINAL_TEMPLATE may receive mock/test menus only.  
It must not be treated as production terminal.

## 9. Response Contract

Response must follow existing dynamic menu payload contract:

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

The menus array must contain final display-ready labels.

GAS must not append lifecycle/status text locally.

## 10. Error Contract

Machine-readable errors:

- AUTH_MISSING_TOKEN
- AUTH_INVALID_TOKEN
- AUTH_SESSION_EXPIRED
- AUTH_SESSION_REVOKED
- TERMINAL_UNKNOWN
- TERMINAL_REVOKED
- TERMINAL_NOT_ASSIGNED_BLOCKED
- MENU_NO_ACCESS
- ROLE_ACCESS_NOT_DEFINED
- MODULE_REGISTRY_EMPTY
- CORE_VERSION_UNSUPPORTED
- CORE_VERSION_DEPRECATED

CORE_VERSION_DEPRECATED meaning:
- terminal core version is too old for current menu/action contract
- core update is required before menu/action execution

## 11. Migration Boundary

This document does NOT create SQL.

Before SQL implementation:
- this contract must pass audit
- migration must be designed as separate bounded task
- existing legacy schema must be checked
- no guessed DDL

## 12. Backend Implementation Boundary

Backend implementation is blocked until:
- registry contract approved
- SQL/migration plan approved
- existing Supabase schema checked
- error contract confirmed

## 13. GAS Boundary

No GAS rendering change should be required for DB-driven menu if payload contract is preserved.

EDSPowerCore should continue to:
- call endpoint
- parse envelope
- render menus array

EDSPowerCore must not:
- query Supabase
- interpret role access
- mutate labels
- decide access
- persist or cache menu payload between sessions

EDSPowerCore menu freshness rule:
- each onOpen/refresh menu flow must request fresh menu data from backend
- temporary in-memory rendering during a single execution is allowed
- persistent menu cache is forbidden in ScriptProperties/UserProperties/DocumentProperties

## 14. What This Does NOT Implement

This document does not implement:
- SQL tables
- DB migrations
- backend DB queries
- role_module_access logic
- admin panel
- module runtime
- calculation actions
- terminal provisioning

## 15. Verdict

DB-driven dynamic menu requires registry contract before SQL/backend implementation.
