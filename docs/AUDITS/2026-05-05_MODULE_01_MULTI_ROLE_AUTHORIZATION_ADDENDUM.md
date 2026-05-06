# MODULE 01 MULTI-ROLE AUTHORIZATION ADDENDUM

## Status
DOC ONLY / AUTHORIZATION ADDENDUM / NO IMPLEMENTATION

## Purpose
Define how Module 01 handles users with multiple roles.

## Core Rule
Users may have multiple active roles through `module01_user_roles`.

Example:
A director may have:
- `DIRECTOR`
- `SALES_MANAGER`
- `CALCULATION_ENGINEER`

The final permission set is the union of permissions from all active roles.

## Director Example
Do not define `DIRECTOR` as automatically "all permissions".

Instead:
- `DIRECTOR` gives director-specific permissions such as dashboards and overview
- `SALES_MANAGER` gives sales-related permissions
- `CALCULATION_ENGINEER` gives calculation permissions
- `ADMIN` gives administration permissions

If one person needs all of them, assign multiple roles.

## API Responsibility
API must:
- load all active roles for user
- resolve permission set
- resolve menu schema
- handle conflicts centrally
- return `roles[]`, `permissions[]`, and `menu_schema` to GAS

## GAS Responsibility
GAS must:
- render only `menu_schema` from API
- not hardcode role hierarchy
- not decide permissions locally
- refresh menu through API on `onOpen` or refresh command

## Conflict Resolution
Future permission logic should define:
- additive permissions by default
- deny/restricted rules only if explicitly introduced later
- no hidden implicit "superrole" unless separately defined

## Current Data Model Compatibility
No schema change required now.
`module01_user_roles` already supports multi-role assignment.

## Boundary
This addendum does not authorize:
- SQL
- migration
- API implementation
- GAS implementation
- UI implementation
- DB writes

## Next Allowed Step
Gemini audit of Multi-Role Authorization Addendum.

## Gemini Audit Status

- final verdict: PASS
- addendum status: CLOSED / APPROVED
- additive role model accepted
- `DIRECTOR` is not superrole
- API-side permission resolution accepted
- GAS rendering-only rule accepted
- next allowed step: API Auth Endpoint Plan
