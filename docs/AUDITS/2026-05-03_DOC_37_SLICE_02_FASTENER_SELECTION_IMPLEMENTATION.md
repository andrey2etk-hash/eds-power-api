# DOC 37 Slice 02 Fastener Selection Implementation

## Scope

Implemented only:
- Slice 01 PASS dependency gate
- required connection group presence checks
- prepared registry truth consumption per connection group:
  - Joint Stack Rule
  - Washer Package Rule
  - Fastener Registry items
  - Equipment Interface constraints (when provided)
- strict required-data checks with explicit failure mapping
- required bolt length calculation
- strict active bolt matcher (`item_type=BOLT`, `is_active=true`, diameter match, `length_mm >= required_bolt_length_mm`)
- local `node_fastener_lines` generation only

Excluded:
- final BOM aggregation
- cross-node aggregation
- procurement outputs
- pricing
- CAD validation
- thermal/short-circuit certification
- API/GAS/DB integration
- registry data creation

## Files Changed

- `src/engines/kzo_welded/busbar_node_fastener_selection_engine.py`
- `tests/test_busbar_node_fastener_selection_slice02.py`
- `docs/AUDITS/2026-05-03_DOC_37_SLICE_02_FASTENER_SELECTION_IMPLEMENTATION.md`
- `docs/CHANGELOG.md`
- `docs/NOW.md`

## Function Added

- `evaluate_busbar_node_fastener_selection(evaluation_input)`

Function properties:
- pure deterministic function
- no side effects
- no DB/API/GAS access
- no admin panel access
- consumes prepared registry truth only

## Tests Added

Test module:
- `tests/test_busbar_node_fastener_selection_slice02.py`

Covered:
1. Slice 01 non-PASS blocks Slice 02
2. Missing required connection group
3. Missing washer package rule
4. Missing `hardware_stack_sum_mm`
5. Missing `thread_pitch_mm`
6. Missing `safety_margin_mm`
7. No active bolts
8. Tight-fit bolt accepted (`length_mm == required_bolt_length_mm`)
9. No downward rounding (`40.1` does not accept bolt `40`)
10. Multiple valid bolts without selection policy -> `SELECTION_REQUIRED`
11. One valid bolt creates local `node_fastener_lines`
12. Missing nut data
13. Missing washer data
14. Equipment interface conflict
15. No API/GAS/DB access indicators in module

Execution:
- `python -m unittest tests.test_busbar_node_fastener_selection_slice02` -> `OK (15 tests)`
- `python -m unittest tests.test_busbar_evaluation_engine_slice01 tests.test_busbar_node_package_slice01 tests.test_busbar_node_fastener_selection_slice02` -> `OK (30 tests)`

## Gemini Planning Audit Guardrails Applied

1. Interface Authority:
- equipment interface constraints conflict with joint stack defaults -> explicit non-PASS with `INTERFACE_FASTENER_CONFLICT`.

2. No downward rounding:
- bolt matcher requires `length_mm >= required_bolt_length_mm`; down-rounding is not allowed.

3. Strict Bolt Matcher:
- matcher enforces `item_type=BOLT`, `is_active=true`, exact diameter match, and minimum length condition.

4. Registry Error Mapping:
- missing washer/nut/thread/hardware/safety data mapped to specific failure codes.

## Forbidden Scope Confirmation

- No final BOM generation
- No cross-node aggregation
- No procurement output
- No pricing logic
- No CAD logic
- No API/GAS/DB changes
- No registry data creation
- DOC 36 Slice 02 not started
- DOC 38 not started

## Gemini Implementation Audit

- Final verdict: **PASS**.
- Slice 02 is officially **CLOSED / VERIFIED**.
- No critical fixes required.
- Fastener selection check: **SAFE**.
- Interface authority check: **STRICTLY ENFORCED**.
- Local output / BOM drift check: **CLEAN**.
- File placement: **SAFE** (`src/engines/kzo_welded/busbar_node_fastener_selection_engine.py`).
- Next allowed step:
  - DOC 38 doctrine/planning only.
- BOM/API/GAS/DB/procurement implementation remains blocked until separate doctrine + planning + audit + task approval.
