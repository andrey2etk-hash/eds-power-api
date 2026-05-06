# MODULE 01 TEST_OPERATOR ROLE DEFINITION

## Objective
Define a test-only role for controlled Module 01 Auth login and terminal menu validation.

## Role Code
TEST_OPERATOR

## Classification
Test-only role.
Non-production.
Temporary / controlled auth validation role.

## Purpose
Used only for:
- auth.login smoke testing
- terminal binding validation
- menu refresh validation

## Allowed Actions
- auth.login
- auth.refresh_menu

## Forbidden Actions
TEST_OPERATOR must NOT:
- access production business data
- access KZO calculation logic
- create or modify calculations
- save snapshots
- access Supabase directly
- manage users
- manage roles
- access admin functions
- write to DB directly
- perform production actions

## Role ID Status
role_id: PENDING_DB_CREATION_OR_LOOKUP

Rule:
Do not invent UUID.
Role UUID must be generated/confirmed only in future controlled SQL provisioning step.

## Spreadsheet Binding
spreadsheet_id: 17JWfDwXQM5S_8uiGFM3C88hUDae_c2cg0LrbWEodZTU

Rule:
Spreadsheet ID must be provided by user before provisioning execution.
This spreadsheet_id is approved for future controlled test terminal binding planning only.

## Provisioning Status
TEST_OPERATOR is defined in docs only.
DB role creation is not approved in this task.
User provisioning remains blocked.

## Execution Gate
Before provisioning:
- TEST_OPERATOR role SQL creation plan must be prepared
- role_id must be generated/confirmed by controlled SQL task
- spreadsheet_id must be provided
- password hash generation must be separately approved
- test user SQL insert must be separately approved

## Boundary Confirmation
- no SQL executed
- no DB writes
- no hash generated
- no API/auth implementation
- no GAS changes
- no Render changes
- no secrets used

## Verdict
TEST_OPERATOR_DOC_DEFINED / PROVISIONING_STILL_BLOCKED
