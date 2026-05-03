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
Define canonical busbar contract split between global material facts and product usage interpretation.

### Global Busbar Material Catalog (v1 placeholder)
- `registry_version`
- `items[]`
- `id`
- `material`
- `section_designation`
- `section_width_mm`
- `section_thickness_mm`
- `strip_count`
- `rated_current_a`
- `mass_kg_per_m`
- `source_basis`
- `status`

Path:

- `src/constants/global/busbar_material_catalog_v1.json`

### Product Busbar Usage Registry (KZO v1 placeholder)
- `registry_version`
- `items[]`
- `usage_id`
- `product_code`
- `material_catalog_id`
- `allowed_node_types`
- `usage_context`
- `package_id`
- `kzo_constraints`
- `status`

Path:

- `src/constants/09_KZO/busbar_usage_registry_v1.json`

## Product-Scoped Registry Rule

Engineering registries that contain product-specific interpretation rules must be namespaced by product code.

For KZO:

- `src/constants/09_KZO/busbar_usage_registry_v1.json`

Reason:

- Busbar as material may be global,
- but busbar usage, selection, geometry, package assignment, and validation are product-specific.

Rule:

- GLOBAL catalog may describe raw materials.
- PRODUCT registry describes how that material is used in a given product family.

Formula:

GLOBAL MATERIAL CATALOG -> PRODUCT USAGE REGISTRY -> PRODUCT CALCULATION RULE

## MVP Registry Governance Rule

For MVP, engineering registries are code-based/manual registry constants.

Explicitly out of scope for MVP:
- admin panel
- registry CRUD UI
- dynamic runtime registry editors

Mandatory rule:
- evaluation algorithms must read registry contracts as source truth
- engineering truth must not be hidden inside decision logic branches
- registry changes must be visible through versioned registry constants and changelog entries

## Busbar Node Matrix Registry

Path:

- `src/constants/09_KZO/busbar_node_matrix_v1.json`

Rule:
Node matrix defines where busbars exist and which constraints apply.
It does not replace global material catalog or product usage registry.

## Equipment Interface Registry

Path:

- `src/constants/09_KZO/equipment_interface_registry_v1.json`

Purpose:
Defines equipment-driven physical compatibility constraints.

## Evaluation Engine Doctrine Reference

Path:

- `docs/00-02_CALC_CONFIGURATOR/09_KZO/36_KZO_WELDED_BUSBAR_EVALUATION_ENGINE_V1.md`

Purpose:
Defines deterministic busbar candidate evaluation flow across node matrix, usage registry, material catalog, and equipment interface constraints.

## Node Package Doctrine Reference (DOC 37)

Path:

- `docs/00-02_CALC_CONFIGURATOR/09_KZO/37_KZO_WELDED_BUSBAR_NODE_PACKAGE_CALCULATION_V1.md`

Purpose:
Defines doctrine for turning DOC 36 selected busbar candidate into node package calculation outputs:
- phase lengths and total length
- joint stack thickness per connection group
- fastener package lines with registry-backed bolt length selection
- material quantity estimate for node package preparation

Registry family implications introduced by DOC 37:
- Fastener Registry
- Joint Stack Rule Registry
- Washer Package Rule Registry
- fastener package rules and registry-backed bolt length selection

## Fastener And Joint Package Registries

Purpose:
Support DOC 37 node package calculation by providing registry-backed truth for:
- bolt selection
- nut usage
- washer stack
- disc spring washer usage
- allowed joint stack ranges
- package composition

Rule:
DOC 37 may only calculate fastener packages from these registries.
No algorithm may invent fastener composition or bolt length.

### Fastener Registry

Purpose:
Defines available fastener items and their technical attributes.

Required conceptual fields:
- `fastener_id`
- `item_type`
- `standard_family`
- `diameter_mm`
- `thread_pitch_mm`
- `length_mm`
- `item_height_mm`
- `material`
- `coating`
- `strength_class`
- `is_active`
- `registry_version`
- `notes`

Allowed `item_type` examples:
- `BOLT`
- `NUT`
- `FLAT_WASHER`
- `DISC_SPRING_WASHER`
- `STUD`
- `THREADED_INSERT`

Rules:
- bolt length must be selected only from active `BOLT` records
- `thread_pitch_mm` is mandatory for `BOLT` / `STUD` / `THREADED_INSERT` where thread allowance is needed
- `thread_pitch_mm` must come from registry; algorithm must not infer thread pitch from diameter or standard family
- `length_mm` is mandatory for `BOLT` / `STUD`; not applicable for washers unless registry explicitly defines otherwise
- `item_height_mm` is mandatory for `NUT` / `FLAT_WASHER` / `DISC_SPRING_WASHER`
- `item_height_mm` may be optional for `BOLT` unless head height is required by a future rule
- algorithm must not infer item height from DIN/ISO standards
- nut is a separate fastener item: nut height must come from `NUT.item_height_mm`
- algorithm must not treat nut height as a bolt property unless a registry-backed package explicitly defines it
- if required fastener data is missing, DOC 37 must return `INCOMPLETE`
- real values are not defined in DOC 33 unless a separate registry-data task is explicitly approved

## Fastener Single Source Of Truth Rule

All fastener geometry required for DOC 37 must come from registries.

The algorithm must not infer:
- thread pitch
- nut height
- washer thickness
- disc spring washer thickness
- bolt length
- washer package composition
- fallback fastener package

If any required fastener geometry is missing:
- `status = INCOMPLETE`
- `failure_code = FASTENER_DATA_MISSING`

If specifically nut data is missing:
- `failure_code = NUT_DATA_MISSING`

If specifically washer data is missing:
- `failure_code = WASHER_DATA_MISSING`

No fallback default fastener package is allowed.

### Joint Stack Rule Registry

Purpose:
Defines how stack thickness and bolt length are interpreted for a specific connection type.

Required conceptual fields:
- `joint_stack_rule_id`
- `connection_group_type`
- `connected_part_a_type`
- `connected_part_b_type`
- `allowed_bolt_diameter_mm`
- `washer_package_rule_id`
- `required_nut_type`
- `required_bolt_type`
- `thread_allowance_rule`
- `safety_margin_mm`
- `allowed_stack_thickness_min_mm`
- `allowed_stack_thickness_max_mm`
- `selection_policy`
- `is_active`
- `registry_version`
- `notes`

Allowed `connection_group_type` examples:
- `BUSBAR_SIDE_CONNECTIONS`
- `EQUIPMENT_SIDE_CONNECTIONS`
- `INTER_CELL_BUSBAR_CONNECTIONS`
- `BRIDGE_CONNECTIONS`

Rules:
- `joint_stack_thickness_mm` is calculated from connected conductive/mechanical parts only
- washer/nut/thread allowance are used for bolt length selection, not hidden inside stack thickness
- `safety_margin_mm` is registry-backed allowance used to avoid selecting bolt length "in contact with limit"
- `safety_margin_mm` may be zero only if explicitly defined in registry
- algorithm must not invent safety margin
- if more than one rule matches and no selection policy exists:
  - `status = SELECTION_REQUIRED`
  - `failure_code = FASTENER_PACKAGE_AMBIGUOUS`

### Washer Package Rule Registry

Purpose:
Defines washer and disc spring washer composition per one bolted joint.

Required conceptual fields:
- `washer_package_rule_id`
- `flat_washer_count`
- `flat_washer_fastener_id`
- `disc_spring_washer_count`
- `disc_spring_washer_fastener_id`
- `nut_fastener_id`
- `hardware_stack_sum_mm`
- `allowed_bolt_diameter_mm`
- `usage_context`
- `is_active`
- `registry_version`
- `notes`

Rules:
- washer quantities must not be assumed by algorithm
- if washer package is missing:
  - `status = INCOMPLETE`
  - `failure_code = FASTENER_DEFAULT_NOT_APPROVED`
- `hardware_stack_sum_mm` is registry-backed total height of washer/nut hardware stack required for bolt length selection
- `hardware_stack_sum_mm` must include all washer heights and nut height according to washer package rule
- algorithm must not calculate hidden default washer/nut stack from assumed standards
- if `hardware_stack_sum_mm` is missing:
  - `status = INCOMPLETE`
  - `failure_code = HARDWARE_STACK_SUM_MISSING`
- no default washer package may produce `PASS`

### Bolt Length Selection Contract

Formula:
`required_bolt_length_mm = joint_stack_thickness_mm + hardware_stack_sum_mm + thread_allowance_mm + safety_margin_mm`

Where:
`thread_allowance_mm = 2 * thread_pitch_mm`
unless Joint Stack Rule Registry defines another approved rule.

Rules:
- required data:
  - `joint_stack_thickness_mm`
  - `hardware_stack_sum_mm`
  - `thread_pitch_mm` OR registry-defined `thread_allowance_mm`
  - `safety_margin_mm`
  - active bolt length list from Fastener Registry
- engine must compare `required_bolt_length_mm` only against active bolt lengths in Fastener Registry
- if any required data is missing:
  - `status = INCOMPLETE`
  - `failure_code = FASTENER_DATA_MISSING` (or specific code below)
  - `failure_code = NUT_DATA_MISSING`
  - `failure_code = WASHER_DATA_MISSING`
  - `failure_code = HARDWARE_STACK_SUM_MISSING`
  - `failure_code = THREAD_PITCH_MISSING`
  - `failure_code = SAFETY_MARGIN_MISSING`
- if no active bolt satisfies required length:
  - `failure_code = BOLT_LENGTH_NOT_FOUND`
- if multiple active bolts satisfy and no selection policy exists:
  - `failure_code = BOLT_LENGTH_AMBIGUOUS`
  - `status = SELECTION_REQUIRED`
- engine must not invent bolt length

Failure codes used by fastener contracts:
- `FASTENER_DATA_MISSING`
- `NUT_DATA_MISSING`
- `WASHER_DATA_MISSING`
- `HARDWARE_STACK_SUM_MISSING`
- `THREAD_PITCH_MISSING`
- `SAFETY_MARGIN_MISSING`
- `BOLT_LENGTH_NOT_FOUND`
- `BOLT_LENGTH_AMBIGUOUS`
- `FASTENER_PACKAGE_AMBIGUOUS`
- `FASTENER_DEFAULT_NOT_APPROVED`
- `FASTENER_REGISTRY_VERSION_MISSING`

### Registry Versioning Requirement

DOC 37 output must include:
- `fastener_registry_version`
- `joint_stack_rule_registry_version`
- `washer_package_rule_registry_version`

If any are missing:
- `status = INCOMPLETE`
- `failure_code = FASTENER_REGISTRY_VERSION_MISSING`

### MVP Boundary For These Registries

For MVP:
- registries are code-based/manual constants
- admin panel is out of scope
- DB registry editing is out of scope
- only registry contracts are defined here
- no real fastener data is created by this task

## Referential Integrity Rule

Any `material_catalog_id` used in product registry must exist in:

- `src/constants/global/busbar_material_catalog_v1.json`

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
