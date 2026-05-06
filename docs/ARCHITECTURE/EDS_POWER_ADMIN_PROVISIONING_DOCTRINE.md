# EDS Power Admin Provisioning Doctrine

## 1. Purpose

Define how admin should create and manage users, terminals, and user-terminal bindings without manually working inside Supabase during normal operation.

## 2. Core Principle

Supabase is the source of truth.
Supabase is NOT the daily admin interface.

Admin should operate through:
Admin Terminal / Admin Module UI
↓
Render API provisioning flow
↓
Supabase registry + Google Sheet terminal creation/copy where applicable

## 3. Admin Provisioning Flow Concept

Future conceptual flow:

1. Admin opens Admin Module.
2. Admin opens modal/dialog: Create User.
3. Admin enters:
   - full name
   - corporate email
   - role
   - department/location if needed
   - terminal assignment model
4. GAS sends one authenticated provisioning request to API.
5. Backend validates current admin session and permissions.
6. Backend creates user record.
7. Backend assigns role.
8. Backend creates or registers terminal.
9. If required, system copies MASTER_TERMINAL_TEMPLATE Google Sheet.
10. Backend binds user ↔ terminal.
11. Backend writes audit event.
12. API returns safe result:
   - user created
   - terminal registered
   - terminal link
   - temporary status / next action

## 4. Admin Terminal Responsibilities

Admin terminal may:
- show provisioning modal/dialog
- collect input data
- send authenticated request to API
- display result
- display terminal link
- show errors

Admin terminal must NOT:
- write directly to Supabase
- make final permission decisions
- generate security truth locally
- store passwords in Sheet
- store session tokens in docs/logs
- create DB records locally
- bypass backend validation

## 5. Backend Responsibilities

Backend/API must own:
- admin permission validation
- user creation
- role assignment
- terminal registration
- terminal-user binding
- audit event creation
- safe response envelope
- error contract

## 6. Supabase Responsibilities

Supabase stores source-of-truth records conceptually:
- users
- roles
- terminals
- terminal_user_assignments
- terminal_role_assignments
- sessions
- audit_events

NOTE:
No schema creation in this task.

## 7. Google Drive / Sheet Template Concept

Future terminal creation may use:
MASTER_TERMINAL_TEMPLATE

Conceptual flow:
- copy template Sheet
- assign spreadsheet_id
- assign terminal_id
- register terminal in backend/DB
- bind terminal to user
- return terminal URL to admin

Open decision:
Whether terminal copying is performed by:
- Apps Script
- backend service
- Google Drive API
- admin manual copy + registration
- hybrid flow

Do not decide implementation in this document unless already approved later.

## 8. Initial Password / Access Concept

Future provisioning must define:
- how initial password is issued
- whether user must change password on first login
- password reset/reminder flow
- corporate email notification flow

Do NOT implement in this task.

## 9. Audit Requirements

Every provisioning action should be auditable:
- admin_user_id
- created_user_id
- terminal_id
- role_assigned
- action
- timestamp
- request_id
- result

Do NOT log:
- password
- session token
- token hash
- password hash

## 10. Failure Modes / Risks

Document risks:
- duplicate user email
- duplicate terminal_id
- failed terminal copy
- user created but terminal failed
- terminal created but DB bind failed
- admin lacks permissions
- template version mismatch
- accidental production access to dev module

## 11. Recommended MVP Policy

For first phase:
- admin should not use Supabase manually for routine user creation
- provisioning may start as guided/manual hybrid
- backend must still own final registry writes
- failed provisioning must be visible and auditable
- terminal creation can be staged before full automation

## 12. What This Does NOT Implement

This document does not implement:
- admin UI
- modal dialog
- API endpoint
- DB schema
- SQL migrations
- Google Drive copy automation
- password reset
- email notifications
- terminal copy flow
- user creation logic

## 13. Verdict

EDS Power Admin Provisioning Doctrine is required before building production-scale user and terminal onboarding.
