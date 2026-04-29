# Stage 5A Structural Composition Task

## Objective

Introduce the first narrow API-side practical KZO engineering value layer after Stage 4C `VERIFIED_OPERATOR_SHELL`.

Stage 5A must transform:

```text
validated payload -> structural interpretation -> practical KZO structure meaning
```

It must not transform the system into a design engine, BOM engine, costing engine, or commercial module.

## Status

`COMPLETE_API_RENDER_AND_OPERATOR_VISIBLE_SHEET`

Operator-visible integration artifact:

`docs/AUDITS/2026-04-29_STAGE_5A_OUTPUT_INTEGRATION.md`

## Trigger Condition

Stage 5A is allowed only because Stage 4C is now:

`VERIFIED_OPERATOR_SHELL`

The Stage 4C input contract is considered frozen enough for first narrow API-side structural interpretation.

## Core Thesis

Stage 5A introduces first structural engineering meaning without crossing into design, BOM, or commercial layers.

Anti-drift law:

```text
Interpret structure.
Do not engineer solutions yet.
```

## Allowed Scope

- KZO only
- API-side only
- structural engineering normalization only
- lineup structural summary
- cell-type composition summary
- first practical technical meaning
- normalized output expansion only
- deterministic rules only

## Forbidden Scope

- pricing
- BOM
- costing
- CAD
- DB
- Supabase
- Sidebar
- GAS logic expansion
- Sheet redesign
- commercial logic
- technical documentation packs
- procurement logic
- multi-product
- production transfer

## Narrowest Safe Practical Logic

Name:

`Configured KZO Structural Composition Summary`

Input:

- total lineup
- voltage class
- busbar current
- cell types and quantities

Output:

- total lineup structure
- cell category breakdown
- functional lineup composition
- first structural flags

## Safe First Rule Types

- cell count validation
- cell type grouping
- lineup composition logic
- section count
- functional role summary

## Example Safe Output Shape

```json
{
  "validation_status": "VALIDATED",
  "product_type": "KZO",
  "lineup_summary": {
    "total_cells": 22,
    "sections": 1,
    "primary_voltage_class": "10kV",
    "busbar_current": "630A"
  },
  "cell_composition": {
    "incoming": 2,
    "outgoing": 16,
    "pt": 2,
    "sectionalizer": 1,
    "bus_riser": 1
  },
  "structural_flags": [
    "dual_incoming",
    "high_outgoing_density",
    "pt_present"
  ]
}
```

## Explicitly Forbidden Outputs

Stage 5A must not answer:

- use this breaker
- use this PT truck
- busbar size = X
- price = Y

## Success Condition

Before Stage 5A:

```text
Payload valid.
```

After Stage 5A:

```text
KZO = 22-cell lineup, dual incoming, 16 outgoing, PT-equipped, 10kV / 630A structure.
```

## Architecture Boundary

Stage 5A creates this bridge:

```text
Validation -> Structural Understanding -> Later Technical Logic
```

Future Stage 5B+ may add deeper technical depth only through separate normalized tasks.

## Implementation Guard

Implementation must be API-side only.

GAS remains a thin client:

- no new GAS logic expansion
- no Sheet redesign
- no operator shell changes

API remains responsible for:

- deterministic structural interpretation
- normalized output expansion
- final validation boundaries

## Next Required Action

Verify Stage 5A through Render/API execution after deployment.

## Implementation Result

Implemented in:

- `main.py`

Added API-side constants:

- `KZO_CELL_COMPOSITION_FIELDS`
- `KZO_VOLTAGE_CLASS_LABELS`
- `KZO_CONFIGURATION_SECTION_COUNTS`

Added API-side helper:

- `_build_kzo_structural_composition_summary(normalized_payload)`

Response expansion:

- `data.structural_composition_summary`

No endpoint name, request envelope, validation error envelope, GAS code, or Sheet structure was changed.

## Implemented Output Fields

`structural_composition_summary` contains:

- `summary_version`
- `product_type`
- `lineup_summary`
- `cell_composition`
- `functional_lineup_composition`
- `structural_flags`
- `interpretation_scope`

Implemented summary version:

```text
KZO_STAGE_5A_STRUCTURAL_COMPOSITION_V1
```

Implemented interpretation scope:

```text
STRUCTURAL_COMPOSITION_ONLY
```

## Local Smoke Verification

Input:

- `quantity_total` = `22`
- `voltage_class` = `VC_10`
- `busbar_current` = `1250`
- `configuration_type` = `CFG_SINGLE_BUS_SECTION`
- `CELL_INCOMER` = `2`
- `CELL_OUTGOING` = `16`
- `CELL_PT` = `2`
- `CELL_BUS_SECTION` = `2`

Observed result:

```json
{
  "summary_version": "KZO_STAGE_5A_STRUCTURAL_COMPOSITION_V1",
  "product_type": "KZO",
  "lineup_summary": {
    "total_cells": 22,
    "sections": 2,
    "primary_voltage_class": "10kV",
    "busbar_current": "1250A",
    "configuration_type": "CFG_SINGLE_BUS_SECTION"
  },
  "cell_composition": {
    "incoming": 2,
    "outgoing": 16,
    "pt": 2,
    "sectionalizer": 2
  },
  "functional_lineup_composition": {
    "incoming_cells": 2,
    "outgoing_cells": 16,
    "voltage_transformer_cells": 2,
    "sectionalizer_cells": 2
  },
  "structural_flags": [
    "dual_incoming",
    "high_outgoing_density",
    "pt_present",
    "sectionalized_lineup"
  ],
  "interpretation_scope": "STRUCTURAL_COMPOSITION_ONLY"
}
```

Local result:

- direct API function smoke test passed
- status = `success`
- `structural_composition_summary` returned as expected

## Remaining Verification

Pending:

- operator-visible integration if the Stage 4C shell later needs to expose the new field

Not required in Stage 5A:

- GAS logic expansion
- Sheet output redesign

## Deployment Candidate Gate

Local smoke passed:

- Stage 5A API direct function smoke test passed
- `data.structural_composition_summary` is present locally
- `lineup_summary` is present locally
- `cell_composition` is present locally
- `functional_lineup_composition` is present locally
- `structural_flags` is present locally

Live Render pre-deploy check:

- live Render API still returns Stage 3C / Stage 4B fields only
- `structural_composition_summary` is not present yet
- returned `data` keys:
  - `validation_status`
  - `logic_version`
  - `status`
  - `normalized_payload`
  - `basic_result_summary`

Reason:

- Render deployment is GitHub-based in the current repository setup.
- No `render` CLI, deploy hook, Render token, or `render.yaml` deployment path is available locally.
- Therefore Stage 5A must be committed and pushed as a deployment candidate before live Render verification can pass.

Candidate rule:

- this commit is a deployment candidate
- this is not a verified release
- Stage 5A must not be marked `VERIFIED` until deployed Render API returns `structural_composition_summary`

Required live Render fields after deploy:

- `structural_composition_summary`
- `lineup_summary`
- `cell_composition`
- `functional_lineup_composition`
- `structural_flags`

## Live Render Verification Result

Deployment candidate commit:

- `483a556` — `Add Stage 5A KZO structural composition summary`

Live Render verification:

- first checks after push still returned Stage 3C / Stage 4B fields only
- after Render deployment completed, live API returned Stage 5A fields

Confirmed live response fields:

- `structural_composition_summary` = present
- `lineup_summary` = present
- `cell_composition` = present
- `functional_lineup_composition` = present
- `structural_flags` = present

Confirmed live summary:

```json
{
  "summary_version": "KZO_STAGE_5A_STRUCTURAL_COMPOSITION_V1",
  "product_type": "KZO",
  "lineup_summary": {
    "total_cells": 22,
    "sections": 2,
    "primary_voltage_class": "10kV",
    "busbar_current": "1250A",
    "configuration_type": "CFG_SINGLE_BUS_SECTION"
  },
  "cell_composition": {
    "incoming": 2,
    "outgoing": 16,
    "pt": 2,
    "sectionalizer": 2
  },
  "functional_lineup_composition": {
    "incoming_cells": 2,
    "outgoing_cells": 16,
    "voltage_transformer_cells": 2,
    "sectionalizer_cells": 2
  },
  "structural_flags": [
    "dual_incoming",
    "high_outgoing_density",
    "pt_present",
    "sectionalized_lineup"
  ],
  "interpretation_scope": "STRUCTURAL_COMPOSITION_ONLY"
}
```

Gate result:

- Stage 5A = `VERIFIED_RENDER_PENDING_OPERATOR_VISIBLE_INTEGRATION`
- no GAS layout changes were made
- no Sheet writeback redesign was made
- no Stage 5B scope was started
