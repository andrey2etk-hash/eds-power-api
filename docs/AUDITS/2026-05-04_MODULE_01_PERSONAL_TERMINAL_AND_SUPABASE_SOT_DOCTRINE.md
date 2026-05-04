# MODULE 01 PERSONAL TERMINAL AND SUPABASE SOURCE OF TRUTH DOCTRINE

## Status

DOC ONLY / ARCHITECTURE DOCTRINE / NO IMPLEMENTATION

## Purpose

Define the future UI architecture for Module 01 calculation entry.

This doctrine defines:
- personal Google Sheet as user terminal
- GAS as thin client
- API as the only access gateway
- Supabase as the single source of truth

## Core Principle

One user has one personal Google Sheet terminal.

The personal Google Sheet is not the database.
It is not the archive.
It is not the source of truth.

It is only:
- user interface
- temporary display surface
- modal form host
- API request client
- API response display surface

## Source of Truth Rule

Supabase is the single source of truth for:
- calculations
- calculation versions
- calculation statuses
- product composition
- role/access data
- object conversion links
- production-transfer markers

Google Sheets must not store authoritative calculation history.

GAS must not write business truth locally.

All persistent operations must go through API.

## Access Chain

Personal Google Sheet
-> GAS thin client
-> API
-> Supabase
-> API response
-> GAS writeback
-> Personal Google Sheet

## Personal Terminal Deployment Model

Rule:
One user = one assigned personal Google Sheet.

Admin gives the user a link to their personal terminal.

The terminal menu adapts to the user role.

The same terminal may show different menu items depending on:
- user role
- enabled modules
- access rights
- current system stage

## Role-Aware Menu Doctrine

Main menu:
EDS Power

Current module:
Модуль розрахунків

Initial menu items:
- Створити новий розрахунок
- Переглянути існуючий розрахунок

Future role-based menu expansion:
- admin
- director
- sales manager
- calculation engineer
- constructor
- technologist
- production / kitting roles

Important:
GAS may display role-based menu items, but final permission must be checked by API/Supabase.

GAS menu visibility is not security.

## Calculation As Primary Entity

The system starts from a calculation, not an object.

Reason:
Not every calculation becomes a sale.
Not every calculation becomes a production object.
One future object may have many calculation versions.

Therefore:
calculation_id is not object_number.

## calculation_id Rule

Base calculation ID format:
YYYYMMDDHHMM

Example:
202605041530

Revision/version suffix:
-01
-02
-03

Examples:
202605041530-01
202605041530-02
202605041530-03

The base calculation record and versions must be stored in Supabase.

## Calculation Version Doctrine

Each version is a separate controlled record.

A version must have:
- version_id
- parent calculation_id
- version_suffix
- status
- created_by
- created_at
- optional object_number link after conversion

Suggested statuses:
- DRAFT
- CALCULATED
- SENT_TO_CLIENT
- REVISED
- APPROVED
- CONVERTED_TO_OBJECT
- CANCELLED
- ARCHIVED

## Locking Policy

If a calculation version is converted to object / transferred to production:
- it becomes locked
- it cannot be edited
- changes require a new version

The lock must be enforced by API/Supabase, not by GAS only.

## First Calculation Module Screen

When user enters the calculation module, the first screen is:

1. Find existing calculation
2. Create new calculation

This is handled through modal windows, not direct table editing.

## Create New Calculation Modal

Initial modal purpose:
Create a new calculation shell.

Fields:
- calculation_id generated automatically
- created_at generated automatically
- created_by resolved automatically
- calculation name / short description
- potential customer
- sales manager if known
- comment

Product details may be added after shell creation.

Recommended approach:
Step 1: create empty calculation shell.
Step 2: add product / commercial item composition.

## Find Existing Calculation Modal

Search by:
- calculation number
- date
- customer
- object name / potential object name
- sales manager
- product type
- object_number if converted

Search result must show:
- base calculation
- all versions
- version status
- locked/unlocked state
- object_number if version was converted to production/object

## Object Number Rule

object_number appears only after commercial/production conversion.

Before conversion:
calculation has no production object number.

After conversion:
the converted version stores object_number link.

## Product Composition Foundation

The system must support:
1. simple product calculation
2. composite commercial product

Simple example:
Calculation -> KZO

Composite example:
Calculation -> KTP
KTP contains:
- KZO x3
- ShchO x3
- ShVP x1
- transformer thermoregulation cabinet x1
- ASKOE cabinet x1

Important:
Commercial product and calculation module are not always the same thing.

## Product Module Routing

Each product or subproduct may route to a different calculation module.

Examples:
- KZO -> KZO module
- ShchO -> ShchO module
- ShVP -> ShVP module
- ASKOE -> ASKOE module

MVP:
Only KZO is active.

But architecture must support future modules.

## Modal UI Doctrine

Main user interaction should happen through modal windows.

Modal windows should follow one visual language:
- Google Forms-like clarity
- minimal direct cell editing
- clear fields
- clear action buttons
- validation messages
- status messages

Future modal types:
- create calculation
- search calculation
- view calculation versions
- add commercial product
- add subproduct
- open product module

## Personal Sheet Cache Boundary

Personal sheet may display:
- search results
- calculation summary
- version list
- last opened calculation
- output blocks

But it must not become:
- authoritative archive
- version database
- registry database
- access-control database

## API-First Rule

All actions must go through API:
- create calculation
- create version
- search calculation
- update status
- convert to object
- lock version
- add product composition

GAS must not bypass API.

## Supabase Planning Boundary

This doctrine does not create Supabase schema.

It only defines required future entities:
- users
- roles
- user_terminals
- calculations
- calculation_versions
- calculation_status_history
- commercial_products
- product_composition
- object_conversion_links

Actual Supabase schema requires separate planning and audit.

## Governance Boundary

This document does not authorize:
- GAS implementation
- API implementation
- Supabase migration
- DB schema creation
- production deployment
- procurement/warehouse/ERP behavior
- pricing/CAD behavior

## Next Allowed Step

After this doctrine:
- Gemini audit of this doctrine
- Supabase data model planning only
- Calculation entry modal planning only
- Role-aware menu planning only

## Gemini Audit Status

- final verdict: PASS
- doctrine status: CLOSED / APPROVED
- required fixes: none
- next allowed step: Supabase Data Model Planning
- no GAS/API/Supabase implementation performed
