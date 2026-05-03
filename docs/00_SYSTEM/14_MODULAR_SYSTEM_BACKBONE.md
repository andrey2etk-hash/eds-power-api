# EDS POWER MODULAR SYSTEM BACKBONE

## Status
SYSTEM ARCHITECTURE CONTRACT / MVP CONTEXT

## Purpose
Define EDS Power as:
Shared Backbone + Module-Specific Workflows

## Core Rule
Modules may differ in permissions and workflows,
but must not create separate sources of truth.

## Shared Backbone Entities
- object_id
- product_id
- calculation_id
- snapshot_id
- status
- version
- registry_version
- event_log
- user_id
- role
- permissions

## Module 01 — Calculation Configurator
Current active MVP module.

Purpose:
Create engineering calculation snapshot and prepare product for next stages.

Module 01 does NOT own the whole object.
It enriches shared object truth with engineering calculation data.

## Engineering Ready Status
Define:
ENGINEERING_READY = calculation snapshot is complete enough to be transferred to proposal / approval / production transfer workflow.

This is a handoff trigger, not final production approval.

## Future Modules — Declarative Only
- Module 02: Commercial Proposal + Approval + Production Transfer
- Module 03: Technical Department
- Module 04: Supply Chain
- Module 05: Kitting
- Module 06: Production
- Module 07: VTK / QA
- Module 08: Warehouse / Shipping
- Module 09: Analytics

Important:
Do not define internal logic of future modules here.

## Registry Layer Rule
DOC 33 and engineering registries are shared architecture assets.
Future modules may consume registry outputs,
but must not redefine engineering truth.

MVP clarification:
- engineering registries are code-based/manual registry constants
- admin panel for registry management is out of scope
- algorithms must consume registry truth rather than embedding hidden engineering truth in logic branches

Module 01 engineering truth includes:
- engineering registries
- node matrices
- equipment interface constraints

## Anti-Pattern Rules
Forbidden:
- parallel truth tables
- module-specific duplicate object identity
- department-local isolated logic
- rewriting calculation truth in downstream modules

## MVP Boundary
Current MVP only proves Module 01.
Future modules are strategic extension points.

## Next Technical Return Path
After this backbone contract:
return to KZO Module 01 technical work:
- DOC 35 Equipment Interface Registry
- DOC 36 Busbar Evaluation Engine
