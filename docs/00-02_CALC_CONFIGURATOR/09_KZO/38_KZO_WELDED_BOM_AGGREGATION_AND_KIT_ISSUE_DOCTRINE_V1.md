# KZO WELDED BOM AGGREGATION AND KIT ISSUE DOCTRINE V1

## Status
MVP / PROTOTYPE / DOC-FIRST / NO IMPLEMENTATION

## Purpose

Define how local node outputs from DOC 37 are aggregated into production-oriented kit issue lines.

DOC 37 answers:
What does one local busbar node need?

DOC 38 answers:
What does the product / cell / group of nodes need as a consolidated kit issue list?

Important:
DOC 38 is not procurement.
DOC 38 is not final ERP BOM.
DOC 38 is not warehouse write-off.
DOC 38 is a controlled aggregation doctrine for production preparation.

## Position In Chain

Global Busbar Catalog
-> KZO Usage Registry
-> Busbar Node Matrix
-> Equipment Interface Registry
-> DOC 36 Busbar Evaluation Engine
-> DOC 37 Busbar Node Package Calculation
-> DOC 38 BOM Aggregation / Kit Issue
-> Future Production / Warehouse / Procurement Modules

## Core Principle

DOC 38 aggregates only verified local node package outputs.

A local node package output may include:
- node_material_lines
- node_fastener_lines

DOC 38 must preserve traceability back to:
- busbar_node_id
- source connection group
- selected_material_catalog_id
- fastener_registry_version
- joint_stack_rule_registry_version
- washer_package_rule_registry_version
- DOC 36 result
- DOC 37 Slice 01/02 result

No source traceability = no PASS.

## Required Inputs

From DOC 37 local node outputs:
- status
- busbar_node_id
- node_material_lines
- node_fastener_lines
- registry_versions
- failure_code
- notes

Each node line must include:
- source_line_id
- item_id
- item_type
- quantity
- unit
- source_node_id
- source_group
- registry_source
- registry_version
- traceability_ref

Aggregation context:
- product_id or cell_id
- calculation_id
- object_id if available
- product_type = KZO
- aggregation_scope

Allowed aggregation_scope:
- SINGLE_NODE
- SINGLE_CELL
- CELL_GROUP
- PRODUCT_INSTANCE
- LINEUP
- DEMO_MVP

## Pre-Aggregation Validation

Before any quantity summation, each source line must be validated.

Required per source line:
- source_line_id
- traceability_ref
- item_id
- item_type
- quantity
- unit
- source_node_id
- registry_source
- registry_version
- issue_context if applicable

Rules:
- quantity must be numeric
- quantity must be > 0
- unit must be present
- item_type must be present
- source_line_id must be unique within one aggregation request
- traceability_ref must be unique or explicitly allowed as shared reference by governance rule

If quantity is non-numeric:
status = INCOMPLETE
failure_code = NON_NUMERIC_QUANTITY

If quantity <= 0:
status = FAIL
failure_code = ZERO_OR_NEGATIVE_QUANTITY

If source_line_id duplicates:
status = FAIL
failure_code = DUPLICATE_SOURCE_LINE

## Aggregation Preconditions

DOC 38 may aggregate only if:
- each DOC 37 node output has status = PASS
- each line has item_id
- each line has quantity
- each line has unit
- each line has source_node_id
- each line has registry_source
- each line has traceability_ref

If any node output is not PASS:
status = INCOMPLETE
failure_code = NODE_OUTPUT_NOT_PASS

If any line lacks traceability:
status = INCOMPLETE
failure_code = TRACEABILITY_MISSING

## Aggregation Rule

Lines may be aggregated only when all aggregation identity keys match.

Required aggregation identity keys:
- item_id
- item_type
- unit
- registry_source
- registry_version
- issue_context if present

For material lines, also require:
- selected_material_catalog_id

For fastener lines, also require:
- fastener_registry_version
- washer_package_rule_registry_version if washer package is involved
- joint_stack_rule_registry_version if line depends on stack rule

No silent merge is allowed if any identity field differs.

If same item_id has different units:
failure_code = MIXED_UNIT_CONFLICT

If same item_id has different registry_source:
failure_code = MIXED_REGISTRY_SOURCE_CONFLICT

If same item_id has different registry_version:
failure_code = REGISTRY_VERSION_MISMATCH

If material line lacks selected_material_catalog_id:
failure_code = SELECTED_MATERIAL_CATALOG_ID_MISSING

Quantities are summed.

Traceability must not be lost.
Aggregated line must include:
- total_quantity
- source_line_ids
- source_node_ids
- source_groups
- registry_versions

## Source Line Duplication Rule

DOC 38 must not aggregate the same source line twice in one aggregation request.

Required:
- every source_line_id must be unique

If duplicate source_line_id is detected:
status = FAIL
failure_code = DUPLICATE_SOURCE_LINE

If traceability_ref duplicates without explicit allowed shared-reference rule:
status = ENGINEERING_REQUIRED
failure_code = DUPLICATE_TRACEABILITY_REF

Rationale:
Prevents accidental double counting of the same local node output.

## Traceability Summarization Rule

DOC 38 must preserve traceability, but large aggregations may summarize references safely.

Allowed:
- source_node_ids list
- source_line_count
- traceability_ref_count
- traceability_refs_sample
- full_traceability_available = true

Rules:
- Full traceability must remain available in source_lines or external trace map.
- Aggregated line must never lose ability to trace back to original source lines.
- If traceability cannot be preserved:
  - status = INCOMPLETE
  - failure_code = TRACEABILITY_MISSING

For MVP:
- direct source_lines / traceability_refs arrays are allowed.
- summarization may be used only if full traceability is preserved elsewhere.

## Local Node Output vs Kit Issue

DOC 37:
local node output

DOC 38:
kit issue aggregation

DOC 38 output is still NOT:
- final procurement list
- final ERP BOM
- warehouse stock movement
- purchase request

DOC 38 output may become input to future modules:
- production issue
- warehouse reservation
- supply planning
- procurement planning

But those are outside DOC 38 MVP.

DOC 38 kit_issue_lines are not final ERP BOM lines.
They are production-preparation aggregation output only.

Forbidden in DOC 38:
- stock reservation
- warehouse write-off
- purchase request
- price calculation
- supplier selection
- ERP/1C posting
- production order release

If any downstream integration consumes DOC 38 output, it must pass through a separate module contract.

## Output Contract

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

For fastener kit issue lines:
- fastener_registry_version
- washer_package_rule_registry_version if applicable
- joint_stack_rule_registry_version if applicable

Rule:
notes must include conflict details when aggregation is blocked by version/source/unit mismatch.

Example output:

{
  "status": "PASS",
  "aggregation_scope": "DEMO_MVP",
  "product_type": "KZO",
  "product_id": "KZO_DEMO_CELL_001",
  "calculation_id": "CALC_DEMO_001",
  "source_node_count": 2,
  "source_nodes": [
    "KZO_NODE_MAIN_TO_BREAKER_A",
    "KZO_NODE_MAIN_TO_BREAKER_B"
  ],
  "kit_issue_lines": [
    {
      "item_id": "BOLT_FROM_FASTENER_REGISTRY_A",
      "item_type": "BOLT",
      "total_quantity": 6,
      "unit": "pcs",
      "registry_source": "fastener_registry_v1",
      "registry_version": "v1",
      "issue_context": "NODE_FASTENER_ISSUE",
      "source_node_ids": [
        "KZO_NODE_MAIN_TO_BREAKER_A",
        "KZO_NODE_MAIN_TO_BREAKER_B"
      ],
      "source_groups": [
        "BUSBAR_SIDE_CONNECTIONS"
      ],
      "source_line_ids": [
        "line_ref_001",
        "line_ref_002"
      ],
      "traceability_refs": [
        "trace_ref_001",
        "trace_ref_002"
      ],
      "source_line_count": 2,
      "traceability_ref_count": 2,
      "fastener_registry_version": "v1",
      "washer_package_rule_registry_version": "v1",
      "joint_stack_rule_registry_version": "v1"
    }
  ],
  "registry_versions": {
    "global_material_catalog_version": "string",
    "kzo_usage_registry_version": "string",
    "busbar_node_matrix_version": "string",
    "equipment_interface_registry_version": "string",
    "fastener_registry_version": "string",
    "joint_stack_rule_registry_version": "string",
    "washer_package_rule_registry_version": "string"
  },
  "failure_code": null,
  "notes": []
}

## Failure Codes

Required:
- NODE_OUTPUT_NOT_PASS
- TRACEABILITY_MISSING
- ITEM_ID_MISSING
- ITEM_TYPE_MISSING
- QUANTITY_MISSING
- SOURCE_LINE_ID_MISSING
- TRACEABILITY_REF_MISSING
- TRACEABILITY_REF_DUPLICATE
- UNIT_MISSING
- REGISTRY_SOURCE_MISSING
- AGGREGATION_SCOPE_MISSING
- SOURCE_NODE_ID_MISSING
- DUPLICATE_SOURCE_LINE
- DUPLICATE_TRACEABILITY_REF
- NON_NUMERIC_QUANTITY
- ZERO_OR_NEGATIVE_QUANTITY
- MIXED_UNIT_CONFLICT
- MIXED_REGISTRY_SOURCE_CONFLICT
- ISSUE_CONTEXT_MISMATCH
- REGISTRY_VERSION_MISMATCH
- SELECTED_MATERIAL_CATALOG_ID_MISSING
- KIT_ISSUE_AGGREGATION_INCOMPLETE
- UNSUPPORTED_AGGREGATION_SCOPE

## Status Rules

DOC 38 may return:
- PASS
- INCOMPLETE
- ENGINEERING_REQUIRED
- SELECTION_REQUIRED
- FAIL

PASS allowed only if:
- all source DOC 37 node outputs are PASS
- all lines are valid
- aggregation_scope is supported
- no mixed unit conflict exists
- traceability is preserved
- registry versions are present and consistent

If any source node is not PASS:
status = INCOMPLETE
failure_code = NODE_OUTPUT_NOT_PASS

If line units differ for same item_id:
status = INCOMPLETE
failure_code = MIXED_UNIT_CONFLICT

If registry source differs for same item_id:
status = INCOMPLETE
failure_code = MIXED_REGISTRY_SOURCE_CONFLICT

If registry versions conflict across source lines that would otherwise aggregate:
status = ENGINEERING_REQUIRED
failure_code = REGISTRY_VERSION_MISMATCH

If issue_context differs for lines that would otherwise aggregate:
status = ENGINEERING_REQUIRED
failure_code = ISSUE_CONTEXT_MISMATCH

## Registry Version Rule

DOC 38 must preserve registry versions from all source nodes.

If registry versions conflict across source lines that would otherwise be aggregated:
- do not silently merge
- return ENGINEERING_REQUIRED
- failure_code = REGISTRY_VERSION_MISMATCH
- notes must list:
  - item_id
  - conflicting registry_source
  - conflicting registry_versions
  - affected source_line_ids

## Traceability Rule

Every aggregated line must keep references to all source lines.

DOC 38 must never collapse quantity without source traceability.

If traceability cannot be preserved:
status = INCOMPLETE
failure_code = TRACEABILITY_MISSING

## MVP Boundary

DOC 38 does NOT:
- create final ERP BOM
- write to warehouse
- reserve stock
- create purchase requests
- perform pricing
- perform CAD validation
- perform procurement
- integrate with API/GAS/DB
- create admin panel
- modify DOC 36 or DOC 37 engines

DOC 38 may only define aggregation doctrine for verified local node package outputs.

## Governance

DOC 38 is doctrine only.
Implementation requires:
- separate planning task
- Gemini planning audit
- separate implementation task
- implementation audit

Any attempt to treat DOC 38 kit_issue_lines as final ERP BOM is a governance breach.

## Gemini Re-Audit Status

- Final verdict: **PASS**.
- DOC 38 is approved as aggregation doctrine standard.
- No implementation performed in this closeout.
- Next allowed step: **DOC 38 Slice 01 Basic Aggregation — PLANNING ONLY**.
- Implementation remains blocked until separate planning + audit + implementation task.
- Safety note:
  - if registry/source/traceability conflicts exist, aggregation must block rather than silently merge.

Slice 01 planning note:
DOC 38 Slice 01 planning is limited to basic aggregation of verified DOC 37 local node outputs.
It does not release final ERP BOM and does not integrate with warehouse/procurement systems.
