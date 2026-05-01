# KZO Welded Global Configuration Flow MVP

## 1. PURPOSE

Define the first canonical top-level operator selection sequence for `KZO_WELDED` before any local cell-level decomposition.

## 2. MVP STATUS

Planning / architecture only.

No implementation is authorized by this artifact.

## 3. GLOBAL LOCKED PARAMETERS

The following global parameters are selected and locked at top-level:

- `rated_voltage`
- `busbar_rated_current`
- `short_circuit_current`
- `busbar_material`
- `row_layout`
- `double_row_orientation`
- `quantity_total`
- `row_1_cell_count`

## 4. GLOBAL CONDITIONAL PARAMETERS

Conditional parameters become available only after prerequisite global context is valid:

- `row_2_cell_count`
- `vacuum_breaker_manufacturer`
- `vacuum_breaker_type`
- `relay_manufacturer`
- `relay_type`
- `ct_manufacturer`
- `vt_manufacturer`
- `metering`
- `terminal_manufacturer`

## 5. FIELD SEQUENCE LAW

Each next field unlocks only after valid prior dependency.

Rule:

- invalid or unresolved upstream value keeps downstream state `BLOCKED`
- downstream option lists are always filtered by current validated upstream context
- `row_2_cell_count` is available only when `row_layout = DOUBLE_ROW`

## 6. DEPENDENCY EXAMPLES

Example canonical chain:

`short_circuit_current`  
-> `vacuum_breaker_manufacturer`  
-> `vacuum_breaker_type`

Additional dependency example:

`rated_voltage` + `busbar_rated_current`  
-> allowed `ct_manufacturer` / `vt_manufacturer` sets

Cell-count dependency rules:

- `SINGLE_ROW`: `row_1_cell_count = quantity_total`; `row_2_cell_count = NOT_APPLICABLE`
- `DOUBLE_ROW`: `row_1_cell_count + row_2_cell_count = quantity_total`

## 7. UI STATE MODEL

Canonical field state model:

- `NOT_SELECTED`
- `SELECTED`
- `BLOCKED`
- `NOT_PRESENT`

State law:

- `BLOCKED` means a valid dependency path is not yet satisfied
- `NOT_PRESENT` means field is not applicable under current global context

## 8. VALIDATION PRINCIPLES

- No invalid downstream options may be shown.
- Upstream change invalidates incompatible downstream selections.
- Incompatible configuration must not silently pass.
- If valid candidate set becomes empty for a required downstream field, system returns `HARD_BLOCK` with explicit reason and blocking field.

## 9. FUTURE LOCAL BOUNDARY

Global first, local later.

This flow governs only top-level global configuration for `KZO_WELDED` MVP.
Local node/cell logic is deferred to a separate bounded lane.

## 10. FORBIDDEN

- No local node logic
- No insulator logic
- No BOM
- No override complexity except future note
- No API redesign
- No DB/GAS/Sheet implementation

MVP override guard:

- Local override of global `busbar_material` at cell level is forbidden in this MVP flow.

## 11. SUCCESS CONDITION

A governed top-level RP selection architecture exists before cell-level decomposition, with deterministic dependency order, explicit blocking behavior (`HARD_BLOCK`), and filtered downstream compatibility.
