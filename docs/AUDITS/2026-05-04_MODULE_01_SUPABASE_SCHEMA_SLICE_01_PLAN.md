# MODULE 01 SUPABASE SCHEMA SLICE 01 PLAN

## Status

DOC ONLY / SCHEMA PLANNING / NO SQL

## Purpose

Define the first narrow physical schema slice for Module 01 in Supabase.

This document prepares future SQL/migration implementation, but does not create SQL.

## Source of Truth Reminder

Supabase is the single source of truth.

Google Sheets is only a personal terminal.
GAS is only a thin client.
API is the only gateway to Supabase.

## Slice 01 Scope

Included conceptual tables:
1. `users`
2. `roles`
3. `user_roles`
4. `user_terminals`
5. `calculations`
6. `calculation_versions`
7. `calculation_status_history`
8. `audit_events`

Excluded from Slice 01:
- commercial_products
- calculation_product_items
- product_composition_items
- module_routes
- object_conversion_links
- calculation_locks
- pricing
- procurement
- warehouse
- ERP/1C
- CAD

Reason:
Slice 01 focuses only on identity, access, personal terminals, base calculation shell, versions, statuses, and audit traceability.

Product composition must be a later slice.

## Table Plan: users

Purpose:
Represent application users.

Planned fields:
- id
- email
- display_name
- status
- created_at
- updated_at

Planned constraints:
- id primary key
- email unique
- status required

Allowed statuses:
- ACTIVE
- DISABLED
- ARCHIVED

Notes:
- Do not overdefine authentication implementation.
- Supabase Auth integration may be planned separately.

## Table Plan: roles

Purpose:
Represent system roles.

Planned fields:
- id
- role_code
- role_name
- description
- is_active
- created_at
- updated_at

Planned constraints:
- id primary key
- role_code unique
- role_code required

Initial role codes:
- OWNER
- ADMIN
- DIRECTOR
- SALES_MANAGER
- CALCULATION_ENGINEER
- CONSTRUCTOR
- TECHNOLOGIST
- PRODUCTION
- KITTING

## Table Plan: user_roles

Purpose:
Map users to one or more roles.

Planned fields:
- id
- user_id
- role_id
- assigned_by_user_id
- assigned_at
- is_active

Planned constraints:
- id primary key
- user_id foreign key to users.id
- role_id foreign key to roles.id
- assigned_by_user_id optional foreign key to users.id
- unique active user/role pair if feasible

Rules:
- GAS menu visibility may use roles.
- API/Supabase must enforce permissions.
- GAS menu visibility is not security.

## Table Plan: user_terminals

Purpose:
Represent personal Google Sheet terminals assigned to users.

Planned fields:
- id
- user_id
- spreadsheet_id
- spreadsheet_url
- status
- assigned_by_user_id
- assigned_at
- last_seen_at
- created_at
- updated_at

Planned constraints:
- id primary key
- user_id foreign key to users.id
- spreadsheet_id unique if one sheet may belong to only one terminal
- user_id unique for MVP if one user = one terminal
- status required

Allowed statuses:
- ACTIVE
- DISABLED
- REPLACED
- ARCHIVED

Rules:
- terminal is not source of truth
- terminal may display cached output only
- terminal cannot store authoritative calculation history

## Table Plan: calculations

Purpose:
Represent base calculation shell.

Planned fields:
- id
- calculation_base_number
- title
- potential_customer
- sales_manager_user_id
- created_by_user_id
- current_status
- is_archived
- created_at
- updated_at

Planned constraints:
- id primary key
- calculation_base_number unique
- calculation_base_number required
- created_by_user_id foreign key to users.id
- sales_manager_user_id optional foreign key to users.id
- current_status required

calculation_base_number format:
YYYYMMDDHHMM

Rules:
- calculation is not object_number
- calculation is not production order
- calculation may never become sale
- object_number must not exist here in Slice 01

## Table Plan: calculation_versions

Purpose:
Represent controlled calculation versions.

Planned fields:
- id
- calculation_id
- version_suffix
- calculation_version_number
- status
- created_by_user_id
- source_version_id
- locked_at
- locked_by_user_id
- lock_reason
- notes
- created_at
- updated_at

Planned constraints:
- id primary key
- calculation_id foreign key to calculations.id
- version_suffix required
- calculation_version_number unique
- created_by_user_id foreign key to users.id
- source_version_id optional foreign key to calculation_versions.id
- locked_by_user_id optional foreign key to users.id

version_suffix format:
-00 or -01 / -02 / -03

Need decision:
Should initial version be:
A. base number without suffix
B. -00
C. -01

Recommended:
Use `-00` for initial version to keep all versions structurally consistent.

Example:
base calculation:
202605041530

initial version:
202605041530-00

next revisions:
202605041530-01
202605041530-02

Rules:
- each version is separate record
- locked version cannot be edited
- changes after lock require new version
- locking must be enforced by API/Supabase, not GAS only

## Table Plan: calculation_status_history

Purpose:
Track status changes for calculation versions.

Planned fields:
- id
- calculation_version_id
- old_status
- new_status
- changed_by_user_id
- changed_at
- reason
- notes
- request_id
- source_client

Planned constraints:
- id primary key
- calculation_version_id foreign key to calculation_versions.id
- new_status required
- changed_by_user_id foreign key to users.id
- request_id optional but strongly recommended

Allowed statuses:
- DRAFT
- CALCULATED
- SENT_TO_CLIENT
- REVISED
- APPROVED
- CONVERTED_TO_OBJECT
- CANCELLED
- ARCHIVED

Rules:
- status changes must be traceable
- production-facing versions require status history
- converted status should lead to lock in later slice or API policy

## Table Plan: audit_events

Purpose:
Generic traceability log.

Planned fields:
- id
- entity_type
- entity_id
- event_type
- actor_user_id
- event_at
- request_id
- source_client
- metadata

Planned constraints:
- id primary key
- actor_user_id optional foreign key to users.id
- entity_type required
- entity_id required
- event_type required
- event_at required
- request_id strongly recommended

Initial event types:
- user_terminal_assigned
- calculation_created
- calculation_version_created
- calculation_status_changed
- calculation_locked
- calculation_viewed
- calculation_search_executed

Rules:
- audit_events must not replace status history
- status history is specific lifecycle trace
- audit_events is general operational trace

## Relationship Map

Document relationships:

- users -> user_roles
- roles -> user_roles
- users -> user_terminals
- users -> calculations.created_by_user_id
- users -> calculations.sales_manager_user_id
- calculations -> calculation_versions
- calculation_versions -> calculation_status_history
- calculation_versions -> calculation_versions.source_version_id
- users -> calculation_versions.created_by_user_id
- users -> calculation_versions.locked_by_user_id
- users -> calculation_status_history.changed_by_user_id
- users -> audit_events.actor_user_id

## Integrity Rules

1. Personal Sheet is not source of truth.
2. GAS must not write business truth locally.
3. API must be the only write gateway.
4. calculation_base_number must be unique.
5. calculation_version_number must be unique.
6. calculation_base_number is not object_number.
7. object_number is out of Slice 01.
8. Locked version cannot be edited.
9. Status changes must be recorded.
10. Audit events must include actor and request_id where possible.
11. Role visibility in menu is not security.
12. Supabase/API must enforce permissions.

## Open Decisions

List unresolved decisions for audit:

1. Initial version suffix:
-00 vs -01 vs no suffix

Recommended:
-00

2. User auth source:
Supabase Auth vs custom users table mapping

Recommended:
Do not decide in Slice 01 plan; keep auth integration separate.

3. RLS timing:
Should Row Level Security be part of first migration or separate security slice?

Recommended:
Plan RLS separately after table structure is approved.

4. Calculation number generation:
Generated by API or database function?

Recommended:
API generates for MVP, DB uniqueness constraint enforces no duplicate.

5. Role permissions matrix:
Include in this slice or separate role/access doctrine?

Recommended:
Separate role/access doctrine.

## Slice 01 Exclusions

Explicitly excluded:
- product composition
- object conversion links
- production object numbers
- actual locking trigger implementation
- RLS policies
- database functions
- API implementation
- GAS implementation
- pricing
- procurement
- warehouse
- ERP/1C
- CAD

## Future Slice Suggestions

Slice 02:
- object_conversion_links
- calculation_locks
- lock enforcement planning

Slice 03:
- commercial_products
- calculation_product_items
- product_composition_items
- module_routes

Slice 04:
- role permissions matrix
- RLS policy planning

## Governance Boundary

This plan does not authorize:
- SQL
- migration
- table creation
- DB writes
- API implementation
- GAS implementation
- production deployment

## Next Allowed Step

After this plan:
- Gemini audit of Supabase Schema Slice 01 Plan
- if PASS: Supabase Schema Slice 01 SQL/Migration Planning
- implementation only after separate approval

## Gemini Audit Status

- final verdict: PASS
- plan status: CLOSED / APPROVED
- required fixes: none
- Slice 01 scope accepted
- next allowed step: Supabase Schema Slice 01 SQL/Migration Planning
- no SQL / DDL / migration / table creation performed
