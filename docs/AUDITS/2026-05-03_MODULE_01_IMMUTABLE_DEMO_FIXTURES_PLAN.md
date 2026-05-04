# MODULE 01 IMMUTABLE DEMO FIXTURES PLAN

## Status
PLANNING ONLY / NO FIXTURE CREATION

## Purpose

Define exact demo fixture content for Module 01 local KZO engineering demo.

The demo must show:

DOC 36 PASS
-> DOC 37 Slice 01 PASS
-> DOC 37 Slice 02 PASS
-> DOC 38 Slice 01 PASS
-> kit_issue_lines generated

## Fixture Boundary

Fixtures are:
- immutable prepared input objects
- local-only
- demo-only
- not loaded from DB
- not production registry data
- not edited live

Fixtures are NOT:
- real ERP BOM
- procurement data
- warehouse data
- pricing data
- CAD data
- production release data

## Registry Metadata Requirement

Every fixture group must include registry metadata.

Required metadata fields:
- registry_version
- last_updated
- display_name

Registry metadata groups:
- global_material_catalog_version
- kzo_usage_registry_version
- busbar_node_matrix_version
- equipment_interface_registry_version
- fastener_registry_version
- joint_stack_rule_registry_version
- washer_package_rule_registry_version

Example metadata structure:

```json
{
  "registry_version": "demo_v1",
  "last_updated": "2026-05-03",
  "display_name": "Demo Fastener Registry V1"
}
```

## Human-Readable Labels

Every major demo object must include:
- display_name
- short_description

Required objects:
- product
- Node A
- Node B
- busbar material
- equipment interface
- selected bolt
- washer package
- kit_issue_line

Purpose:
Allow the demo to be understandable for management without reading technical IDs only.

## Demo Product

Product:
- product_id: KZO_DEMO_PRODUCT_001
- display_name: KZO Demo Cell / Node Group
- short_description: Controlled two-node KZO scenario for local engineering logic demonstration
- product_type: KZO
- aggregation_scope: DEMO_MVP
- calculation_id: DEMO_CALC_001

## Node A Plan

Node ID:
KZO_DEMO_NODE_A

display_name:
Node A — Main Busbar To Breaker Connection

short_description:
Primary branch from main busbar to breaker A with standard connection stack.

Expected flow:
- DOC 36 = PASS
- DOC 37 Slice 01 = PASS
- DOC 37 Slice 02 = PASS

Geometry planned values:
- phase_count = 3
- L1_mm = 420.0
- L2_mm = 380.0
- L3_mm = 360.0
- node_busbar_thickness_mm = 10.0
- main_busbar_pack_thickness_mm = 10.0
- equipment_terminal_thickness_mm = 8.0

Connection groups:
- BUSBAR_SIDE_CONNECTIONS
- EQUIPMENT_SIDE_CONNECTIONS

Expected outputs:
- total_busbar_length_mm = 1160.0
- BUSBAR_SIDE_CONNECTIONS joint_stack_thickness_mm = 20.0
- EQUIPMENT_SIDE_CONNECTIONS joint_stack_thickness_mm = 18.0
- local node_fastener_lines generated
- source_line_id values generated (stable deterministic IDs)
- traceability_ref values generated (node + group based)

Planned line identity examples:
- source_line_id: KZO_DEMO_NODE_A_FASTENER_BUSBAR_SIDE_BOLT_M12
- source_line_id: KZO_DEMO_NODE_A_FASTENER_EQUIP_SIDE_BOLT_M12
- traceability_ref: TRACE_KZO_DEMO_NODE_A_BUSBAR_SIDE
- traceability_ref: TRACE_KZO_DEMO_NODE_A_EQUIP_SIDE

## Node B Plan

Node ID:
KZO_DEMO_NODE_B

display_name:
Node B — Second Main Busbar To Breaker Connection

short_description:
Secondary branch configured to reuse the same fastener family for aggregation demonstration.

Expected flow:
- DOC 36 = PASS
- DOC 37 Slice 01 = PASS
- DOC 37 Slice 02 = PASS

Purpose:
Create repeated fastener lines that can aggregate with Node A in DOC 38.

Geometry planned values:
- phase_count = 3
- L1_mm = 410.0
- L2_mm = 390.0
- L3_mm = 350.0
- node_busbar_thickness_mm = 10.0
- main_busbar_pack_thickness_mm = 10.0
- equipment_terminal_thickness_mm = 8.0

Expected outputs:
- total_busbar_length_mm = 1150.0
- BUSBAR_SIDE_CONNECTIONS joint_stack_thickness_mm = 20.0
- EQUIPMENT_SIDE_CONNECTIONS joint_stack_thickness_mm = 18.0
- local node_fastener_lines generated
- source_line_id values generated (stable deterministic IDs)
- traceability_ref values generated (node + group based)

Planned line identity examples:
- source_line_id: KZO_DEMO_NODE_B_FASTENER_BUSBAR_SIDE_BOLT_M12
- source_line_id: KZO_DEMO_NODE_B_FASTENER_EQUIP_SIDE_BOLT_M12
- traceability_ref: TRACE_KZO_DEMO_NODE_B_BUSBAR_SIDE
- traceability_ref: TRACE_KZO_DEMO_NODE_B_EQUIP_SIDE

## Shared Demo Registry Truth

Define planned demo registry objects conceptually.

Important:
Do not create actual registry files in this task.

### Busbar Material
Required planned fields:
- selected_material_catalog_id: BUSBAR_CU_SHMT_60X10
- display_name: Copper Busbar 60x10
- short_description: Demo copper busbar profile for both nodes
- material: CU
- width_mm: 60.0
- thickness_mm: 10.0
- kg_per_meter: 5.35
- registry_version: global_material_catalog_demo_v1
- last_updated: 2026-05-03

### Equipment Interface
Required planned fields:
- equipment_id: KZO_BREAKER_INTERFACE_STD
- display_name: KZO Breaker Terminal Standard Interface
- short_description: Standard terminal constraints for demo breaker connection
- terminal_thickness_mm: 8.0
- allowed_bolt_diameter_mm: 12.0
- registry_version: equipment_interface_demo_v1
- last_updated: 2026-05-03

### Fastener
Required planned fields:
- fastener_id: BOLT_HEX_M12_L45_8_8
- display_name: Hex Bolt M12x45 8.8
- short_description: Shared bolt candidate to be selected in both nodes
- item_type = BOLT
- diameter_mm: 12.0
- length_mm: 45.0
- thread_pitch_mm: 1.75
- is_active = true
- registry_version: fastener_registry_demo_v1
- last_updated: 2026-05-03

### Washer Package Rule
Required planned fields:
- washer_package_rule_id: WASHER_PKG_M12_STD
- display_name: M12 Standard Washer Package
- short_description: Standard washer stack used for both node groups
- hardware_stack_sum_mm: 6.0
- registry_version: washer_rule_demo_v1
- last_updated: 2026-05-03

### Joint Stack Rule
Required planned fields:
- joint_stack_rule_id: JOINT_RULE_STD_M12
- display_name: Standard Joint Rule For M12
- short_description: Joint stack governance rule for selected M12 hardware
- allowed_bolt_diameter_mm: 12.0
- safety_margin_mm: 2.0
- washer_package_rule_id: WASHER_PKG_M12_STD
- registry_version: joint_stack_rule_demo_v1
- last_updated: 2026-05-03

## Expected DOC 38 Aggregation Result

Expected:
- status = PASS
- kit_issue_lines generated
- repeated fastener lines from Node A and Node B are aggregated
- source_line_ids preserved
- traceability_refs preserved
- registry_versions visible

Required kit issue line presentation fields:
- item_id
- display_name
- total_quantity
- unit
- source_node_ids
- source_line_ids
- traceability_refs
- registry_version
- note: production-preparation only, not final ERP BOM

Planned aggregation demonstration:
- Node A and Node B both produce bolt item_id `BOLT_HEX_M12_L45_8_8`
- DOC 38 merges repeated compatible lines into one aggregated `kit_issue_line`
- merged line keeps both node IDs and both source references

## Audit Trail Sample Plan

Prepare one audit trail sample for Node A.

Required audit trail steps:
1. DOC 36 accepted busbar candidate.
2. DOC 37 Slice 01 calculated total length and joint stack.
3. DOC 37 Slice 02 selected bolt from registry truth.
4. DOC 38 included Node A line in aggregated kit_issue_lines.

Each step must include:
- input summary
- decision made
- status
- failure_code = null
- registry_version used

## Optional Backup Safety Fixture Plan

This is NOT part of the main demo flow.

Backup fixture:
- node_id: KZO_DEMO_NODE_BACKUP_INCOMPLETE
- display_name: Backup Safety Fixture — Missing Phase Length
- short_description: Backup-only safety check for missing geometry input
- expected status: INCOMPLETE
- failure_code: PHASE_LENGTH_MISSING
- expected_failure_reason:
  "The system blocks calculation because one required phase length is missing."

Rules:
- not shown in main demo
- used only if asked how system handles incomplete data
- must not distract from main PASS flow

## Management Narrative Data

Plan must prepare simple labels for presentation:

- Joint Stack:
  "товщина пакету з’єднання"

- Kit Issue:
  "комплект видачі на виробництво"

- Registry Truth:
  "затверджені інженерні довідники"

- Traceability:
  "можливість побачити, з якого вузла прийшла кожна позиція"

- Not Final BOM:
  "це ще не закупівля і не складське списання"

## Success Criteria

Fixture planning is successful if:
- Node A and Node B have complete planned fixture content
- both nodes are PASS-focused
- repeated lines can aggregate
- display_name exists for management readability
- registry_version and last_updated are visible
- traceability is demonstrable
- optional safety fixture remains backup only
- no fixture files are created yet
