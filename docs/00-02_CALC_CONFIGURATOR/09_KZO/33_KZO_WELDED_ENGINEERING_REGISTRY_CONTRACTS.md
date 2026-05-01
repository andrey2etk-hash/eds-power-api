# KZO WELDED ENGINEERING REGISTRY CONTRACTS

## Status
MVP / PROTOTYPE / ARCHITECTURE CONTRACT FOUNDATION

## Purpose
Define canonical registry contracts as Single Source of Truth for data-driven KZO element calculation.

This document is architecture-only and does not authorize implementation.

## Section 1: Versioning Doctrine

### Contract Versioning
- Registry contracts use semantic version labels (`v1`, `v2`, ...).
- Any breaking field mutation requires next major contract version.
- Non-breaking additive changes require explicit changelog entry and contract note.

### Deprecation Rules
- Deprecated fields remain readable for one transition window.
- New calculation logic must bind to the latest active contract version.
- Deprecated contracts must be marked with replacement target and freeze date.

## Section 2: Busbar Registry Contract

### Contract Intent
Define canonical busbar data fields for package selection and engineering evaluation.

### Contract Skeleton (v1 placeholder)
- `registry_version`
- `material`
- `section_designation`
- `section_width_mm`
- `section_thickness_mm`
- `rated_current_a`
- `mass_kg_per_m` (placeholder)
- `thermal_factor` (placeholder)
- `dynamic_factor` (placeholder)
- `notes` (placeholder)

## Section 3: Insulator Registry Contract

### Contract Intent
Define canonical insulator data fields for spacing/count and compatibility evaluation.

### Contract Skeleton (v1 placeholder)
- `registry_version`
- `insulator_type`
- `rated_voltage_kv`
- `short_circuit_class_ka` (placeholder)
- `recommended_spacing_mm` (placeholder)
- `max_supported_span_mm` (placeholder)
- `mounting_family` (placeholder)
- `notes` (placeholder)

## Section 4: Group Signature Model

### Model Intent
Define identity logic for grouping identical cells into one multiplier group.

### Signature Skeleton
- `constructive_family`
- `cell_type`
- `cell_role`
- `switching_type`
- `node_activation_signature`
- `boundary_position_flag`
- `pairing_context` (for SV/SR and topology exceptions)

### Grouping Rule
Cells with identical signature belong to one group unless exception split rules apply.

## Section 5: TABU & Override Policy

### Policy Intent
Define governance priority between global defaults, constraints, and local overrides.

### Priority Rule (MVP Contract Skeleton)
1. Customer TABU (hard boundary)
2. Engineering TABU (safety/validity boundary)
3. Explicit local override
4. Global default

### Required Policy Fields
- `is_customer_tabu`
- `is_engineering_tabu`
- `allowed_variants`
- `override_scope` (placeholder)
- `override_reason` (placeholder)

## Governance Warning
Registry contracts in this document are skeleton-only.
No full formulas, full catalogs, or implementation logic are authorized at this stage.
