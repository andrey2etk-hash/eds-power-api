# EDS Power Master Terminal Template Doctrine

## 1. Purpose
Define the master Google Sheet terminal template that will be copied for future EDS Power users.

## 2. Core Principle
The master template is not a user terminal.
It is the source template for future terminal provisioning.

## 3. Template Responsibilities
The master template may contain:
- local bound bootstrap
- connection to EDSPowerCore
- standard menus
- standard UI/sheet layout
- standard protected zones
- standard module placeholders
- test/handshake function

## 4. Template Must NOT Contain
- production terminal_id
- user-specific session
- user-specific token
- user-specific permissions
- role-specific hardcoded menu
- engineering logic
- calculation logic
- direct Supabase access

## 5. terminal_id Rule
MASTER_TERMINAL_TEMPLATE must not be copied with a real production terminal_id.

Allowed:
- terminal_id empty
- template_marker = TERMINAL_TEMPLATE

Copied terminal must receive unique terminal_id only during provisioning.

## 6. Provisioning Flow Preview
Future flow:
1. Admin creates user.
2. System copies MASTER_TERMINAL_TEMPLATE.
3. New copy receives unique terminal_id.
4. Backend registers terminal.
5. Backend binds terminal to user/role/department.
6. Admin receives terminal URL.

## 7. First Template Validation
The master template must pass:
- EDSPowerCore reachable
- local bootstrap wrappers present
- context builds
- spreadsheet_id present
- terminal_id missing/template-only handled safely
- no token logged
- no secrets logged
- no business logic executed

## 8. What This Does NOT Implement
This doctrine does not implement:
- terminal copy automation
- provisioning endpoint
- DB schema
- user creation
- dynamic menu
- calculations

## 9. Verdict
Master Terminal Template must be validated before copying terminals for users.

Temporary local-core handshake note:
If EDSPowerCore Library is not yet deployed, first handshake may use temporary local-core mode inside MASTER_TERMINAL_TEMPLATE.
This is allowed only for foundation handshake and must not become final architecture.
