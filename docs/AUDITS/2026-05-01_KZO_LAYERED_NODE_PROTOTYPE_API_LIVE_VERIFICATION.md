# KZO Layered Node Prototype MVP — API Live Verification

Date: 2026-05-01  
Mode: verification only (no implementation changes)

## Objective

Verify live API behavior for bounded prototype tuple:

- `constructive_family = KZO_WELDED`
- `cell_role = VACUUM_BREAKER`
- `cell_position = LEFT_END`
- `node = INSULATOR_SYSTEM`

## Environment

- Host: `https://eds-power-api.onrender.com`
- Endpoint: `POST /api/calc/prepare_calculation`

## Checks and Results

1. Selected tuple returns `layered_node_summary`  
   **Result:** PASS  
   **Evidence:** rollout polling attempt 6 returned `LAYERED True` for selected tuple.

2. Non-selected tuple does not return `layered_node_summary`  
   **Result:** PASS  
   **Evidence:** non-selected tuple returned `LAYERED False`.

3. Existing response layers remain present (`structural_composition_summary`, `physical_summary`, `physical_topology_summary`)  
   **Result:** PASS  
   **Evidence:** both selected/non-selected responses returned all three baseline layers.

## Gate Verdict

`PASS`

## Deployment/Rollout Note

Render rollout required polling after push. PASS behavior appeared on attempt 6.

## Live Evidence Snapshot

- Selected RID: `live-layered-f2274f3411b1-sel`
- Non-selected RID: `live-layered-f2274f3411b1-non`
- Selected summary tuple:
  - `constructive_family = KZO_WELDED`
  - `cell_role = VACUUM_BREAKER`
  - `cell_position = LEFT_END`
  - `node = INSULATOR_SYSTEM`
- Selected summary keys present:
  - `placement_points`
  - `presence_rules_result`
  - `primary_components`
  - `dependent_hardware`
  - `aggregate_bom`
  - plus identity/meta fields (`constructive_family`, `cell_role`, `cell_position`, `node`, `prototype_version`, `interpretation_scope`)

## Scope Compliance

- no code changes
- no DB changes
- no GAS changes
- no Sheet changes
- no scope expansion
