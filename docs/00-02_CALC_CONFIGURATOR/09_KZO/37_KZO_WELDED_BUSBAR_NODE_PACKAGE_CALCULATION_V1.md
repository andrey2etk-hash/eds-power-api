# KZO WELDED BUSBAR NODE PACKAGE CALCULATION V1

## Status
MVP / PROTOTYPE / DOC-FIRST / NO IMPLEMENTATION

## Purpose
Define how the system calculates the physical node package after DOC 36 busbar selection.

DOC 36 answers:
Which busbar candidate is allowed?

DOC 37 answers:
What exact node package is required for production preparation?

A node package includes:
- selected busbar material
- phase quantity
- phase lengths
- total busbar length
- optional mass
- connection points
- joint stack thickness
- fasteners
- washers
- disc spring washers
- nuts
- failure / blocker status if required data is missing

## Position In Chain

Global Busbar Catalog
-> KZO Usage Registry
-> Busbar Node Matrix
-> Equipment Interface Registry
-> DOC 36 Busbar Evaluation Engine
-> DOC 37 Busbar Node Package Calculation
-> DOC 38 BOM Aggregation / Kit Issue

## Core Principle
A busbar node is not only a busbar.

A production-ready node package must describe:
- what busbar material is required
- how many phase bars are required
- what lengths are required
- where the node connects
- what joint stack thickness exists at every connection group
- what fastener package is required for each connection group

## MVP Registry Governance
For MVP:
- all engineering registries are manual code-based constants / JSON-like registries
- admin panel is out of scope
- DB registry editing is out of scope
- algorithm must read registry truth
- algorithm must not hide engineering truth inside decision logic

Required future registry families:
- Fastener Registry
- Joint Stack Rule Registry
- Washer Package Rule Registry
- Optional Mass Property Registry if not inside Global Material Catalog

Contract dependency:
DOC 37 depends on DOC 33 contracts for Fastener Registry, Joint Stack Rule Registry, and Washer Package Rule Registry.

## Required Inputs

### From DOC 36
- status
- selected_material_catalog_id
- selected_usage_id
- package_id
- registry_versions

Rule:
If DOC 36 status is not PASS, DOC 37 cannot return PASS.

### From Busbar Node Matrix
- busbar_node_id
- node_type
- cell_type
- phase_count
- phase_length_l1_mm
- phase_length_l2_mm
- phase_length_l3_mm
- connection_point_groups

### From Equipment Interface Registry
- equipment_id
- terminal_thickness_mm
- terminal_width_mm
- terminal_hole_diameter_mm
- allowed_bolt_diameter
- equipment_connection_side

### From Global Material Catalog
- material
- width_mm
- thickness_mm
- density_kg_m3 OR kg_per_meter

### From Fastener Registry
- bolt_type
- bolt_diameter
- bolt_length
- washer_type
- disc_spring_washer_type
- nut_type
- allowed_stack_thickness_min_mm
- allowed_stack_thickness_max_mm

## Node Geometry Rule

For MVP:
phase_count = 3

Required:
- L1
- L2
- L3

total_busbar_length_mm = L1 + L2 + L3

If any phase length is missing:
status = INCOMPLETE
failure_code = PHASE_LENGTH_MISSING

## Busbar Mass Governance

For MVP:
busbar_mass_kg may be calculated only if the selected material catalog provides:
- kg_per_meter

If kg_per_meter is missing:
busbar_mass_kg = null
status cannot be PASS if mass is mandatory for the requested output
failure_code = MASS_DATA_MISSING

DOC 37 must not calculate mass from density_kg_m3 + geometry in MVP.
Density-based calculation is deferred until explicit unit conversion and material property governance exist.

If a flow attempts density-based mass conversion in MVP:
status = INCOMPLETE
failure_code = UNIT_CONVERSION_UNSAFE or MASS_CALCULATION_UNSAFE

Important:
Mass calculation is allowed only as material quantity estimate.
It is not final structural or thermal certification.

## Connection Point Model

DOC 37 must support at minimum two connection point groups:

### 1. BUSBAR_SIDE_CONNECTIONS
Connection between node busbar and main busbar.

### 2. EQUIPMENT_SIDE_CONNECTIONS
Connection between node busbar and equipment terminal:
- busbar disconnector
- circuit breaker
- other equipment interface

Each connection point group must define:
- group_id
- connection_point_count
- connected_part_a
- connected_part_b
- stack_thickness_formula
- bolt_diameter_rule
- fastener_package_rule

## Joint Stack Thickness Rule

joint_stack_thickness_mm means only the clamped conductive/mechanical parts before external fastener hardware.

### BUSBAR_SIDE_CONNECTIONS

joint_stack_thickness_mm =
node_busbar_thickness_mm + main_busbar_pack_thickness_mm

### EQUIPMENT_SIDE_CONNECTIONS

joint_stack_thickness_mm =
node_busbar_thickness_mm + equipment_terminal_thickness_mm

Fastener selection must additionally account for:
- hardware_stack_sum_mm
- thread_allowance_mm
- safety_margin_mm

These must come from Fastener Registry / Washer Package Rule Registry.

Do not silently include washers/nuts inside joint_stack_thickness_mm unless registry explicitly defines that convention.

If required thickness data is missing:
status = INCOMPLETE
failure_code = JOINT_STACK_THICKNESS_MISSING

## Fastener Truth Rule

DOC 37 must never invent fastener composition.

Fastener types, quantities, washer composition, disc spring washer composition, nut usage, and bolt length must come only from:
- Fastener Registry
- Joint Stack Rule Registry
- Washer Package Rule Registry

No default fastener package may produce PASS.

If no registry-backed fastener package exists:
status = INCOMPLETE
failure_code = FASTENER_RULE_MISSING

If a default placeholder is used for explanation, it must be marked:
ILLUSTRATIVE_ONLY / NOT_APPROVED_ENGINEERING_TRUTH

## Fastener Package Rule

For each connection point group:
1. resolve joint_stack_thickness_mm
2. resolve bolt diameter
3. select bolt length from Fastener Registry
4. calculate quantity by connection_point_count

For MVP, quantities per joint must be registry-backed.
DOC 37 may describe an illustrative package only, but must not define a universal default.

If registry does not define washer/nut/disc spring washer composition:
status = INCOMPLETE
failure_code = FASTENER_DEFAULT_NOT_APPROVED

Example:
3 BUSBAR_SIDE_CONNECTIONS:
- bolts = 3 (ILLUSTRATIVE_ONLY / NOT_APPROVED_ENGINEERING_TRUTH)
- nuts = 3 (ILLUSTRATIVE_ONLY / NOT_APPROVED_ENGINEERING_TRUTH)
- flat washers = 6 (ILLUSTRATIVE_ONLY / NOT_APPROVED_ENGINEERING_TRUTH)
- disc spring washers = 3 (ILLUSTRATIVE_ONLY / NOT_APPROVED_ENGINEERING_TRUTH)

3 EQUIPMENT_SIDE_CONNECTIONS:
- bolts = 3 (ILLUSTRATIVE_ONLY / NOT_APPROVED_ENGINEERING_TRUTH)
- nuts = 3 (ILLUSTRATIVE_ONLY / NOT_APPROVED_ENGINEERING_TRUTH)
- flat washers = 6 (ILLUSTRATIVE_ONLY / NOT_APPROVED_ENGINEERING_TRUTH)
- disc spring washers = 3 (ILLUSTRATIVE_ONLY / NOT_APPROVED_ENGINEERING_TRUTH)

Important:
DOC 37 may define the calculation doctrine,
but must not invent approved final bolt lengths without registry-backed rule.

## Bolt Length Selection Doctrine

Bolt length must be selected from Fastener Registry only.

Required calculated minimum length:

required_bolt_length_mm =
joint_stack_thickness_mm
+ hardware_stack_sum_mm
+ thread_allowance_mm
+ safety_margin_mm

Where:
thread_allowance_mm = 2 * thread_pitch_mm unless registry defines another rule.

The engine must not invent bolt length.
It must compare required_bolt_length_mm against available bolt lengths in Fastener Registry.

Rules:
- If no bolt length satisfies the required minimum:
  - status = INCOMPLETE
  - failure_code = BOLT_LENGTH_NOT_FOUND

- If multiple bolt lengths satisfy the rule and no selection policy exists:
  - status = SELECTION_REQUIRED
  - failure_code = BOLT_LENGTH_AMBIGUOUS

- If hardware_stack_sum_mm, safety_margin_mm, or thread_pitch_mm is missing:
  - status = INCOMPLETE
  - failure_code = FASTENER_DATA_MISSING

Fastener geometry and hardware stack sums are controlled by DOC 33 registry contracts.

## Phase And Connection Count Rule

For MVP:
phase_count = 3.

For default three-phase busbar node:
connection_point_count for each required phase connection group must equal phase_count.

If connection_point_count != phase_count:
status = INCOMPLETE or ENGINEERING_REQUIRED
failure_code = PHASE_CONNECTION_MISMATCH

Allowed exceptions require explicit registry-backed override.

## Output Contract

Required output fields:
- status
- busbar_node_id
- selected_material_catalog_id
- package_id
- phase_count
- phase_lengths
- total_busbar_length_mm
- busbar_mass_kg
- connection_point_groups
- node_fastener_lines
- node_material_lines
- failure_code
- notes
- registry_versions

Rule:
DOC 37 output is local node package specification only.
It is not final BOM.
Final aggregation belongs to DOC 38.

Failure note:
If a downstream system treats DOC 37 output as final BOM, this is a governance breach.

Example below is illustrative only.
IDs and numeric values in the example are NOT approved engineering truth.
Real values must come from registries.

Example output:

{
  "status": "PASS",
  "busbar_node_id": "KZO_NODE_MAIN_TO_BREAKER_A",
  "selected_material_catalog_id": "BUSBAR_CU_SHMT_60X10_1",
  "package_id": "KZO_BUSBAR_MAIN_PACKAGE_V1",
  "phase_count": 3,
  "phase_lengths": {
    "L1_mm": 420,
    "L2_mm": 420,
    "L3_mm": 420
  },
  "total_busbar_length_mm": 1260,
  "busbar_mass_kg": 6.72,
  "connection_point_groups": [
    {
      "group_id": "BUSBAR_SIDE_CONNECTIONS",
      "connection_point_count": 3,
      "joint_stack_thickness_mm": 20,
      "fastener_package_id": "FASTENER_PACKAGE_FROM_REGISTRY_A"
    },
    {
      "group_id": "EQUIPMENT_SIDE_CONNECTIONS",
      "connection_point_count": 3,
      "joint_stack_thickness_mm": 18,
      "fastener_package_id": "FASTENER_PACKAGE_FROM_REGISTRY_B"
    }
  ],
  "node_fastener_lines": [
    {
      "item_id": "BOLT_FROM_FASTENER_REGISTRY_A",
      "quantity": 3,
      "source_group": "BUSBAR_SIDE_CONNECTIONS"
    },
    {
      "item_id": "BOLT_FROM_FASTENER_REGISTRY_B",
      "quantity": 3,
      "source_group": "EQUIPMENT_SIDE_CONNECTIONS"
    },
    {
      "item_id": "WASHER_FROM_WASHER_PACKAGE_REGISTRY",
      "quantity": 12
    },
    {
      "item_id": "DISC_SPRING_WASHER_FROM_WASHER_PACKAGE_REGISTRY",
      "quantity": 6
    },
    {
      "item_id": "NUT_FROM_FASTENER_REGISTRY",
      "quantity": 6
    }
  ],
  "node_material_lines": [
    {
      "item_id": "BUSBAR_CU_SHMT_60X10_1",
      "quantity_type": "MASS",
      "quantity": 6.72,
      "unit": "kg"
    }
  ],
  "failure_code": null,
  "notes": [],
  "registry_versions": {
    "global_material_catalog_version": "string",
    "kzo_usage_registry_version": "string",
    "busbar_node_matrix_version": "string",
    "equipment_interface_registry_version": "string",
    "fastener_registry_version": "string",
    "joint_stack_rule_registry_version": "string",
    "washer_package_rule_registry_version": "string"
  }
}

## Failure Codes

- PHASE_LENGTH_MISSING
- MASS_DATA_MISSING
- JOINT_STACK_THICKNESS_MISSING
- EQUIPMENT_TERMINAL_THICKNESS_MISSING
- MAIN_BUSBAR_THICKNESS_MISSING
- FASTENER_RULE_MISSING
- FASTENER_CANDIDATE_NOT_FOUND
- CONNECTION_POINT_COUNT_MISSING
- FASTENER_REGISTRY_VERSION_MISSING
- NODE_PACKAGE_INCOMPLETE
- DOC36_SELECTION_NOT_PASS
- BOLT_LENGTH_NOT_FOUND
- BOLT_LENGTH_AMBIGUOUS
- FASTENER_PACKAGE_AMBIGUOUS
- FASTENER_DEFAULT_NOT_APPROVED
- FASTENER_DATA_MISSING
- NUT_DATA_MISSING
- WASHER_DATA_MISSING
- HARDWARE_STACK_SUM_MISSING
- THREAD_PITCH_MISSING
- SAFETY_MARGIN_MISSING
- UNIT_CONVERSION_UNSAFE
- PHASE_CONNECTION_MISMATCH
- MASS_CALCULATION_UNSAFE

## Status Rules

DOC 37 may return:
- PASS
- INCOMPLETE
- ENGINEERING_REQUIRED
- SELECTION_REQUIRED
- FAIL

PASS is allowed only if:
- DOC 36 selected busbar status is PASS
- all phase lengths are known
- total length is resolved
- stack thicknesses are known
- fastener package is resolved
- registry versions are present

If any required fastener registry version is missing (`fastener_registry_version`, `joint_stack_rule_registry_version`, `washer_package_rule_registry_version`):
status = INCOMPLETE
failure_code = FASTENER_REGISTRY_VERSION_MISSING

If DOC 36 output is not PASS:
status = INCOMPLETE or ENGINEERING_REQUIRED
failure_code = DOC36_SELECTION_NOT_PASS

## MVP Boundary

DOC 37 does NOT:
- release final BOM
- perform procurement
- perform pricing
- perform CAD validation
- certify short-circuit strength
- certify thermal behavior
- modify DOC 36 selection logic
- create admin panel
- create DB registry editing

DOC 37 may only define doctrine for:
- node geometry
- connection point groups
- joint stack thickness
- fastener package calculation
- material quantity estimate

## Governance

DOC 37 is doctrine only.
Implementation requires separate approved task.
Slice 01 planning boundary covers node geometry and joint stack only; fastener selection remains a future slice.
Slice 02 planning boundary covers local node fastener selection only; final BOM aggregation and kit issue remain under DOC 38.

DOC 37 must not weaken DOC 36.
If DOC 36 output is not PASS, DOC 37 cannot return PASS.

DOC 37 must preserve registry-source boundary:
engineering values belong in registries, not hidden inside algorithm branches.

## Gemini Re-Audit Status

- Final verdict: **PASS**.
- DOC 37 is approved as doctrine standard.
- No implementation performed in this closeout.
- Next implementation requires a separate approved narrow slice.
- Registry dependency safety note:
  - if required registry values are missing, `INCOMPLETE` is the correct and safe outcome.
