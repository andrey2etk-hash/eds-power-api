# KZO Layered Node Prototype MVP — Live Failure Diagnosis

Date: 2026-05-01  
Mode: diagnosis only (no changes performed)

## Root Cause

**Deployment stale for prototype slice.**  
`layered_node_summary` logic exists only in local uncommitted `main.py` changes, so live Render runtime does not contain this code path yet.

## Evidence

1. **Deployed commit coverage check**
   - `git rev-parse HEAD` = `515c82ada1c4f22122d87a52a0b2d1b1aeb16a3b`
   - `git rev-parse origin/main` = `515c82ada1c4f22122d87a52a0b2d1b1aeb16a3b`
   - `git status --short` shows `main.py` modified locally (not committed/pushed).
   - Conclusion: Render deploy (from `origin/main`) cannot include local prototype edits.

2. **Live main.py tuple logic presence (indirect verification)**
   - Local `main.py` diff contains:
     - constants:
       - `KZO_PROTOTYPE_CONSTRUCTIVE_FAMILY = "KZO_WELDED"`
       - `KZO_PROTOTYPE_CELL_ROLE = "VACUUM_BREAKER"`
       - `KZO_PROTOTYPE_CELL_POSITION = "LEFT_END"`
       - `KZO_PROTOTYPE_NODE = "INSULATOR_SYSTEM"`
     - function `_build_kzo_layered_node_summary(payload)`
     - insertion point before response return:
       - `layered_node_summary = _build_kzo_layered_node_summary(payload)`
       - conditional add to `data`
   - This confirms intended logic exists locally only.

3. **Payload exactness/casing check**
   - Live request used exact tuple and field names:
     - `constructive_family: KZO_WELDED`
     - `cell_role: VACUUM_BREAKER`
     - `cell_position: LEFT_END`
     - `node: INSULATOR_SYSTEM`
   - Casing and key names match local implementation exactly.

4. **Path evaluation and reachability**
   - Local diagnostic call to `prepare_calculation` with selected tuple:
     - `LOCAL_HAS_LAYERED True`
   - Live call with same tuple:
     - `HAS_LAYERED False`
   - Baseline live layers still present (`structural_composition_summary`, `physical_summary`, `physical_topology_summary`), proving route works but prototype branch absent in deployed runtime.

## Check Mapping

- deployment stale -> **YES (root cause)**
- payload mismatch -> **NO**
- field naming/casing mismatch -> **NO**
- tuple condition mismatch -> **NO**
- code path unreachable by design -> **NO (reachable locally; absent live)**

## Exact Minimal Fix Path

1. Commit only prototype API slice files:
   - `main.py`
   - `tests/test_prepare_calculation_layered_node_prototype.py`
2. Push to `origin/main` and wait for Render rollout.
3. Re-run live selected/non-selected verification gate.

## No Changes Performed

Diagnosis executed only. No code, DB, GAS, Sheet, or architecture changes performed in this step.
