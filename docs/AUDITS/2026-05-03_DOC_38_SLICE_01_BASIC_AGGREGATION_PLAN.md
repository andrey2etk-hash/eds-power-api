# DOC 38 SLICE 01 BASIC AGGREGATION PLAN

## Status
PLANNING ONLY / NO IMPLEMENTATION

## Scope

Included:
- DOC 37 node output PASS validation
- source line required field validation
- source_line_id uniqueness validation
- traceability_ref validation
- quantity numeric validation
- quantity > 0 validation
- aggregation identity grouping
- quantity summation
- registry version consistency check
- traceability preservation
- kit_issue_lines output

Excluded:
- final ERP BOM
- warehouse reservation
- warehouse write-off
- procurement
- supplier selection
- pricing
- CAD
- API/GAS/DB
- admin panel
- registry data creation
- DOC 36 Slice 02

## Required Inputs

From DOC 37 node outputs:
- status
- busbar_node_id
- node_material_lines
- node_fastener_lines
- registry_versions
- failure_code
- notes

Each node line must include:
- source_line_id
- traceability_ref
- item_id
- item_type
- quantity
- unit
- source_node_id
- source_group
- registry_source
- registry_version
- issue_context if applicable

Aggregation context:
- aggregation_scope
- product_type
- product_id
- calculation_id

Allowed aggregation_scope for Slice 01:
- DEMO_MVP
- SINGLE_CELL
- CELL_GROUP

## Planned Function Boundary

Proposed function name:
aggregate_kzo_node_package_lines(evaluation_input)

Function type:
- pure deterministic function
- no side effects
- no DB/API/GAS access
- no registry loading
- no procurement/warehouse behavior

Preferred location:
src/engines/kzo_welded/bom_aggregation_engine.py

## Planned Flow

1. Validate aggregation context.
   Required:
   - aggregation_scope
   - product_type
   - product_id
   - calculation_id

2. Validate source DOC 37 node outputs.
   Every source node output must have:
   status = PASS

   If any node output is not PASS:
   status = INCOMPLETE
   failure_code = NODE_OUTPUT_NOT_PASS

3. Extract source lines:
   - node_material_lines
   - node_fastener_lines

4. Pre-aggregation validation for every line.
   Required:
   - source_line_id
   - traceability_ref
   - item_id
   - item_type
   - quantity
   - unit
   - source_node_id
   - registry_source
   - registry_version

5. Validate quantity.
   If quantity is non-numeric:
   status = INCOMPLETE
   failure_code = NON_NUMERIC_QUANTITY

   If quantity <= 0:
   status = FAIL
   failure_code = ZERO_OR_NEGATIVE_QUANTITY

6. Validate duplicate source_line_id.
   If duplicate:
   status = FAIL
   failure_code = DUPLICATE_SOURCE_LINE

7. Validate aggregation identity.

   Lines may be aggregated only when identity keys match:
   - item_id
   - item_type
   - unit
   - registry_source
   - registry_version
   - issue_context if present

   For material lines:
   also require selected_material_catalog_id.

   No silent merge allowed.

8. Group lines by aggregation identity.

9. Sum quantities.

10. Preserve traceability:
   each kit_issue_line must include:
   - source_line_ids
   - source_node_ids
   - source_groups
   - traceability_refs
   - source_line_count
   - traceability_ref_count

11. Return kit_issue_lines.

## Planned Output

Required output fields:
- status
- aggregation_scope
- product_type
- product_id
- calculation_id
- kit_issue_lines
- source_node_count
- source_nodes
- registry_versions
- failure_code
- notes

Each kit_issue_line:
- item_id
- item_type
- total_quantity
- unit
- registry_source
- registry_version
- issue_context
- source_node_ids
- source_groups
- source_line_ids
- traceability_refs
- source_line_count
- traceability_ref_count

For material kit issue lines:
- selected_material_catalog_id

## Status Rules

PASS allowed only if:
- aggregation context is valid
- all source DOC 37 outputs are PASS
- all source lines pass pre-aggregation validation
- no duplicate source_line_id exists
- no non-numeric or <=0 quantity exists
- no mixed unit conflict exists
- no registry version conflict exists within aggregation identity
- traceability is preserved

If any node output is not PASS:
status = INCOMPLETE
failure_code = NODE_OUTPUT_NOT_PASS

If source_line_id is missing:
status = INCOMPLETE
failure_code = SOURCE_LINE_ID_MISSING

If traceability_ref is missing:
status = INCOMPLETE
failure_code = TRACEABILITY_REF_MISSING

If quantity is non-numeric:
status = INCOMPLETE
failure_code = NON_NUMERIC_QUANTITY

If quantity <= 0:
status = FAIL
failure_code = ZERO_OR_NEGATIVE_QUANTITY

If duplicate source_line_id:
status = FAIL
failure_code = DUPLICATE_SOURCE_LINE

If same item_id appears with different units:
status = INCOMPLETE
failure_code = MIXED_UNIT_CONFLICT

If same item_id appears with different registry_source:
status = INCOMPLETE
failure_code = MIXED_REGISTRY_SOURCE_CONFLICT

If material line lacks selected_material_catalog_id:
status = INCOMPLETE
failure_code = SELECTED_MATERIAL_CATALOG_ID_MISSING

## Failure Codes

Required:
- NODE_OUTPUT_NOT_PASS
- TRACEABILITY_MISSING
- ITEM_ID_MISSING
- ITEM_TYPE_MISSING
- QUANTITY_MISSING
- UNIT_MISSING
- REGISTRY_SOURCE_MISSING
- REGISTRY_VERSION_MISSING
- AGGREGATION_SCOPE_MISSING
- SOURCE_NODE_ID_MISSING
- SOURCE_LINE_ID_MISSING
- TRACEABILITY_REF_MISSING
- DUPLICATE_SOURCE_LINE
- DUPLICATE_TRACEABILITY_REF
- NON_NUMERIC_QUANTITY
- ZERO_OR_NEGATIVE_QUANTITY
- MIXED_UNIT_CONFLICT
- MIXED_REGISTRY_SOURCE_CONFLICT
- REGISTRY_VERSION_MISMATCH
- SELECTED_MATERIAL_CATALOG_ID_MISSING
- KIT_ISSUE_AGGREGATION_INCOMPLETE
- UNSUPPORTED_AGGREGATION_SCOPE

## Test Plan

Required future tests:
1. PASS aggregation with two nodes and same bolt item.
2. Node output not PASS returns NODE_OUTPUT_NOT_PASS.
3. Missing source_line_id returns SOURCE_LINE_ID_MISSING.
4. Duplicate source_line_id returns DUPLICATE_SOURCE_LINE.
5. Missing traceability_ref returns TRACEABILITY_REF_MISSING.
6. Non-numeric quantity returns NON_NUMERIC_QUANTITY.
7. Zero quantity returns ZERO_OR_NEGATIVE_QUANTITY.
8. Negative quantity returns ZERO_OR_NEGATIVE_QUANTITY.
9. Mixed unit for same item_id returns MIXED_UNIT_CONFLICT.
10. Mixed registry_source for same item_id returns MIXED_REGISTRY_SOURCE_CONFLICT.
11. Material line missing selected_material_catalog_id returns SELECTED_MATERIAL_CATALOG_ID_MISSING.
12. Aggregated line preserves source_line_ids and traceability_refs.
13. Output kit_issue_lines are not final ERP BOM.
14. No API/GAS/DB access occurs.
15. No procurement/warehouse/pricing/CAD behavior occurs.

## Governance Boundary

Slice 01 is not full DOC 38 implementation.
Slice 01 is only basic aggregation of verified DOC 37 local node lines.

DOC 38 Slice 01 output is:
production-preparation kit issue aggregation only.

It is NOT:
- final ERP BOM
- warehouse reservation
- purchase request
- procurement order
- stock write-off
- pricing output
- CAD output
- API/GAS/DB integration

Any attempt to treat kit_issue_lines as final ERP BOM is governance breach.
