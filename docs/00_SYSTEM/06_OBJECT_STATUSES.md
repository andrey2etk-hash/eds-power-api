# Object Statuses

## Purpose

This file defines global lifecycle statuses for business objects in EDS Power.

These statuses apply across modules and must be used for analytics and cross-module governance.

## Global lifecycle statuses

### DRAFT

Object is editable and not finalized.

### VALIDATED

Object passed validation.

### LOCKED

Object is frozen for downstream use.

### SENT_TO_NEXT_MODULE

Object was transferred to another module.

### ARCHIVED

Object is no longer active.

### ERROR

Object has blocking error.

## Rules

- every business object must have one lifecycle status
- modules may define local statuses only if they map to global lifecycle statuses
- analytics must use global lifecycle statuses
- changing status requires explicit action and must be logged

## Allowed transitions

- DRAFT → VALIDATED
- VALIDATED → LOCKED
- LOCKED → SENT_TO_NEXT_MODULE
- ANY → ERROR
- ERROR → DRAFT
- ANY → ARCHIVED

## Forbidden transitions

- ARCHIVED → active states
- LOCKED → DRAFT without revision process

## Note

Detailed workflow may expand later.
