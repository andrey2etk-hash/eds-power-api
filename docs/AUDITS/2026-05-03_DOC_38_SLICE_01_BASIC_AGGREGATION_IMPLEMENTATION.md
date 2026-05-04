# DOC 38 Slice 01 Basic Aggregation Implementation

## Scope

Implemented only:
- source DOC 37 node output PASS validation
- aggregation context validation for allowed scope values
- extraction of local node lines (`node_material_lines`, `node_fastener_lines`)
- pre-aggregation source line validation
- duplicate `source_line_id` and duplicate `traceability_ref` blocking
- quantity numeric and positive-value guards
- strict aggregation identity grouping
- quantity summation
- traceability-preserving local `kit_issue_lines` output

Excluded:
- final ERP BOM release
- warehouse reservation/write-off
- procurement outputs
- supplier selection
- pricing
- CAD
- API/GAS/DB integration
- registry data creation
- DOC 36 Slice 02
- DOC 38 Slice 02

## Files Changed

- `src/engines/kzo_welded/bom_aggregation_engine.py`
- `tests/test_bom_aggregation_slice01.py`
- `docs/AUDITS/2026-05-03_DOC_38_SLICE_01_BASIC_AGGREGATION_IMPLEMENTATION.md`
- `docs/CHANGELOG.md`
- `docs/NOW.md`

## Function Added

- `aggregate_kzo_node_package_lines(evaluation_input)`

Function properties:
- pure deterministic function
- no side effects
- no DB/API/GAS access
- no registry loading
- no procurement/warehouse behavior

## Tests Added

Test module:
- `tests/test_bom_aggregation_slice01.py`

Covered:
1. PASS aggregation with two nodes and same bolt item
2. Node output non-PASS block
3. Missing `source_line_id`
4. Duplicate `source_line_id`
5. Missing `traceability_ref`
6. Duplicate `traceability_ref`
7. Non-numeric quantity
8. Zero quantity
9. Negative quantity
10. Mixed unit conflict
11. Mixed registry source conflict
12. Registry version mismatch conflict
13. Missing `selected_material_catalog_id` for material line
14. Material aggregation identity includes `selected_material_catalog_id`
15. Unsupported aggregation scope
16. Output not final ERP BOM
17. No API/GAS/DB access in module

Execution:
- `python -m unittest tests.test_bom_aggregation_slice01` -> `OK (17 tests)`
- `python -m unittest tests.test_busbar_evaluation_engine_slice01 tests.test_busbar_node_package_slice01 tests.test_busbar_node_fastener_selection_slice02 tests.test_bom_aggregation_slice01` -> `OK (47 tests)`

## Gemini Planning Audit Guardrails Applied

1. Strict identity:
- `selected_material_catalog_id` is required for material lines and included in material aggregation identity.

2. Strict duplication block:
- duplicate `source_line_id` returns `FAIL / DUPLICATE_SOURCE_LINE`.

3. Specific failure codes:
- `NON_NUMERIC_QUANTITY` and `SELECTED_MATERIAL_CATALOG_ID_MISSING` are explicitly mapped and tested.

## Forbidden Scope Confirmation

- `kit_issue_lines` are production-preparation output only
- no final ERP BOM behavior
- no warehouse/procurement behavior
- no pricing/CAD behavior
- no API/GAS/DB behavior
- no registry data creation
- DOC 36 Slice 02 not started
- DOC 38 Slice 02 not started

## Gemini Implementation Audit

- Final verdict: **PASS**.
- Slice 01 is officially **CLOSED / VERIFIED**.
- No critical fixes required.
- Aggregation safety check: **SAFE**.
- Traceability check: **PRESERVED**.
- Kit issue / BOM drift check: **CLEAN**.
- File placement: **SAFE** (`src/engines/kzo_welded/bom_aggregation_engine.py`).
- Next allowed step:
  - DOC 38 Slice 02 planning only, OR
  - Module 01 local logic closeout (doc-only).
- DOC 38 Slice 02 implementation remains blocked until separate planning + audit + task approval.
- External integration remains blocked.
