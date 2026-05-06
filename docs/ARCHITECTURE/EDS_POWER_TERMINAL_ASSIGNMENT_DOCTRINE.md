# EDS Power Terminal Assignment Doctrine

## 1. Purpose

Define how EDS Power terminals are assigned to users, roles, departments, locations, admin/test use, and how terminal mismatch is detected.

## 2. Core Principle

Terminal is not only a Google Sheet file.
Terminal is a controlled access point into EDS Power.

A valid request must be evaluated by:
- user_id
- session_token
- terminal_id
- terminal assignment policy
- backend validation

terminal_id alone is NOT authentication proof.

## 3. Terminal Identity

Each terminal should conceptually have:
- terminal_id
- spreadsheet_id
- spreadsheet_url
- terminal_name
- terminal_type
- status
- core_channel
- core_version
- last_seen_at

NOTE:
Do not create DB schema in this task.

## 4. Assignment Models

Supported conceptual terminal assignment types:
- PERSONAL_TERMINAL
- ROLE_TERMINAL
- DEPARTMENT_TERMINAL
- LOCATION_TERMINAL
- ADMIN_TERMINAL
- TEST_TERMINAL
- SHARED_TERMINAL

## 5. User-Terminal Assignment

A user may have:
- one primary terminal
- multiple allowed terminals
- admin/test terminals if role permits

A terminal may be:
- assigned to one user
- shared by role
- shared by department
- shared by location
- admin-only
- test-only
- revoked/inactive

## 6. Login / Request Evaluation Rule

Backend should be able to evaluate:
- valid session token
- user exists
- terminal exists
- terminal is active
- user is allowed to use this terminal
- requested module/action is allowed for this user/role/terminal

## 7. Terminal Mismatch Outcomes

Define conceptual outcomes:

TERMINAL_MATCH
User is using assigned personal terminal.

TERMINAL_ALLOWED_SHARED
User is using an allowed shared/role/department/location terminal.

TERMINAL_ADMIN_OVERRIDE
Admin/dev user is allowed to use non-standard terminal.

TERMINAL_MISMATCH_WARNING
User is not on primary terminal, but action is allowed and logged.

TERMINAL_NOT_ASSIGNED_BLOCKED
User is not allowed to use this terminal.

TERMINAL_UNKNOWN
Terminal is not registered.

TERMINAL_REVOKED
Terminal is registered but inactive/revoked.

## 8. Recommended MVP Policy

For early rollout:
- allow valid users on known active terminals
- log mismatch warnings
- block unknown terminals
- block revoked terminals
- block critical admin actions from non-admin terminals
- do not hard-block all mismatches immediately

Reason:
Avoid rollout disruption while still collecting audit data.

## 9. Audit Logging Requirement

Every authenticated request should be able to log:
- user_id
- terminal_id
- assignment_result
- module_id
- action_key
- timestamp
- request_id

Do NOT log:
- session token
- password
- token hash

## 10. Security Notes

A stolen session token should not be sufficient alone.
Backend should bind session validation to terminal context where applicable.

Terminal mismatch must be visible to admin.

## 11. What This Does NOT Implement

This document does not implement:
- DB schema
- terminal assignment tables
- terminal enforcement logic
- terminal admin UI
- blocking rules
- SQL migrations
- API changes
- GAS changes

## 12. Verdict

EDS Power Terminal Assignment Doctrine is required before broad terminal rollout.
