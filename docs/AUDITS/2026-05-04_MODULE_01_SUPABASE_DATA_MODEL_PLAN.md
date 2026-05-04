# MODULE 01 SUPABASE DATA MODEL PLAN

## Status

DOC ONLY / DATA MODEL PLANNING / NO MIGRATION

## Purpose

Define the conceptual Supabase data model for Module 01 calculation entry and personal terminal architecture.

This plan translates the approved Personal Terminal + Supabase Source of Truth doctrine into future database entities.

## Source of Truth Principle

Supabase is the single source of truth.

Google Sheets is only:
- UI terminal
- temporary display surface
- modal form host
- API request client
- API response display surface

GAS must not store business truth.

API is the only gateway to Supabase.

## Scope

This plan covers future conceptual entities for:
- users
- roles
- user terminals
- calculations
- calculation versions
- status history
- product composition
- module routing
- object conversion links
- locking policy

This plan does NOT create:
- SQL
- migrations
- actual tables
- policies
- triggers
- API endpoints
- GAS implementation

## Conceptual Entity List

Define the following conceptual entities:

1. `users`
2. `roles`
3. `user_roles`
4. `user_terminals`
5. `calculations`
6. `calculation_versions`
7. `calculation_status_history`
8. `commercial_products`
9. `calculation_product_items`
10. `product_composition_items`
11. `module_routes`
12. `object_conversion_links`
13. `calculation_locks`
14. `audit_events`

## Entity: users

Purpose:
Represent system users.

Conceptual fields:
- user_id
- email
- display_name
- status
- created_at
- updated_at

Notes:
- user authentication details may depend on future auth strategy.
- do not overdefine auth implementation in this document.

## Entity: roles

Purpose:
Define available roles.

Conceptual fields:
- role_id
- role_code
- role_name
- description
- is_active

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

## Entity: user_roles

Purpose:
Map users to roles.

Conceptual fields:
- user_id
- role_id
- assigned_by
- assigned_at
- is_active

Rule:
Role visibility in GAS menu is not security.
Final permissions must be enforced by API/Supabase.

## Entity: user_terminals

Purpose:
Represent personal Google Sheet terminals assigned to users.

Conceptual fields:
- terminal_id
- user_id
- spreadsheet_id
- spreadsheet_url
- status
- assigned_by
- assigned_at
- last_seen_at

Rules:
- one user may initially have one personal terminal
- future architecture may allow multiple terminals if explicitly approved
- terminal is not source of truth

## Entity: calculations

Purpose:
Represent base calculation records.

Conceptual fields:
- calculation_id
- calculation_number
- calculation_base_number
- title
- potential_customer
- sales_manager_user_id
- created_by_user_id
- created_at
- updated_at
- current_status
- is_archived

Rules:
- calculation_number base format: YYYYMMDDHHMM
- calculation is not object_number
- calculation is not production order
- calculation may never become sale

## Entity: calculation_versions

Purpose:
Represent controlled versions/revisions of a calculation.

Conceptual fields:
- calculation_version_id
- calculation_id
- version_suffix
- calculation_version_number
- status
- created_by_user_id
- created_at
- updated_at
- locked_at
- locked_by_user_id
- lock_reason
- source_version_id
- notes

Rules:
- version suffix format: -01, -02, -03
- each version is a separate controlled record
- converted/production version must be locked
- changes after conversion require new version

## Entity: calculation_status_history

Purpose:
Track lifecycle status changes.

Conceptual fields:
- status_event_id
- calculation_version_id
- old_status
- new_status
- changed_by_user_id
- changed_at
- reason
- notes

Suggested statuses:
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
- status history is not optional for production-facing versions

## Entity: commercial_products

Purpose:
Represent sellable commercial product types.

Conceptual fields:
- commercial_product_id
- product_code
- product_name
- description
- is_composite
- is_active

Examples:
- KZO
- KTP
- ShchO
- ShVP
- ASKOE

Rule:
Commercial product is not always identical to calculation module.

## Entity: calculation_product_items

Purpose:
Represent product items inside a calculation version.

Conceptual fields:
- calculation_product_item_id
- calculation_version_id
- commercial_product_id
- display_name
- quantity
- unit
- parent_item_id
- sort_order
- module_route_id
- status

Rules:
- supports simple product calculation
- supports composite product structure
- parent_item_id enables nesting

Examples:
Simple:
Calculation Version -> KZO x1

Composite:
Calculation Version -> KTP x1
KTP contains:
- KZO x3
- ShchO x3
- ShVP x1
- transformer thermoregulation cabinet x1
- ASKOE x1

## Entity: product_composition_items

Purpose:
Represent standard/default composition rules for composite products.

Conceptual fields:
- composition_item_id
- parent_commercial_product_id
- child_commercial_product_id
- default_quantity
- unit
- is_required
- sort_order
- notes

Rule:
This entity defines reusable product composition templates.
Actual calculation-specific composition lives in `calculation_product_items`.

## Entity: module_routes

Purpose:
Map product types to calculation modules.

Conceptual fields:
- module_route_id
- commercial_product_id
- module_code
- module_name
- is_active
- route_config

Examples:
- KZO -> MODULE_01_KZO
- ShchO -> MODULE_SHCHO
- ShVP -> MODULE_SHVP
- ASKOE -> MODULE_ASKOE

MVP:
Only KZO route is active.

## Entity: object_conversion_links

Purpose:
Link a calculation version to future object/order/production identity after conversion.

Conceptual fields:
- conversion_link_id
- calculation_version_id
- object_number
- converted_by_user_id
- converted_at
- conversion_status
- notes

Rules:
- object_number appears only after conversion
- conversion locks the calculation version
- conversion does not erase calculation history

## Entity: calculation_locks

Purpose:
Track explicit locking state.

Conceptual fields:
- lock_id
- calculation_version_id
- lock_type
- locked_by_user_id
- locked_at
- lock_reason
- is_active

Lock types:
- CONVERTED_TO_OBJECT
- MANUAL_LOCK
- ARCHIVED_LOCK

Rule:
Locks must be enforced by API/Supabase, not by GAS.

## Entity: audit_events

Purpose:
Generic traceability log for important actions.

Conceptual fields:
- audit_event_id
- entity_type
- entity_id
- event_type
- actor_user_id
- event_at
- request_id
- source_client
- metadata

Events:
- calculation_created
- version_created
- status_changed
- product_item_added
- composition_changed
- converted_to_object
- lock_created
- terminal_assigned

## Relationship Map

Document conceptual relationships:

- users -> user_roles
- users -> user_terminals
- calculations -> calculation_versions
- calculation_versions -> calculation_status_history
- calculation_versions -> calculation_product_items
- calculation_product_items -> commercial_products
- commercial_products -> product_composition_items
- commercial_products -> module_routes
- calculation_versions -> object_conversion_links
- calculation_versions -> calculation_locks
- all key actions -> audit_events

## Primary Integrity Rules

1. Personal Sheet is not source of truth.
2. GAS must not write business truth locally.
3. API must be the only write gateway.
4. calculation_id is not object_number.
5. object_number appears only after conversion.
6. Converted version is locked.
7. New changes after lock require new version.
8. Composite products must support nested items.
9. Product module routing must be data-driven.
10. Role-based menu visibility is not security.
11. Status history must be traceable.
12. Audit events must preserve request_id and actor.

## MVP Boundary

For MVP planning:
- only KZO module active
- one user may have one terminal
- roles may be simplified
- product composition may be basic
- no production ERP integration
- no procurement/warehouse behavior
- no pricing/CAD behavior

## Future Supabase Planning Boundary

This document does not authorize DDL.

Next possible planning document:
- Supabase Schema Slice 01 Planning

Suggested Slice 01:
- users / roles / user_terminals
- calculations
- calculation_versions
- status history

Do not include full product composition in first migration unless separately approved.

## Governance Boundary

This plan does not authorize:
- SQL
- migrations
- table creation
- RLS policies
- triggers
- API implementation
- GAS implementation
- production deployment

## Gemini Audit Status

- final verdict: PASS
- plan status: CLOSED / APPROVED
- required fixes: none
- next allowed step: Supabase Schema Slice 01 Planning
- no SQL / migration / table creation performed
