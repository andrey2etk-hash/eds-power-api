# Stage 5B Physical Footprint — Render Verification Gate

## Objective

Verify `data.physical_summary` for KZO MVP on **live Render** (`POST /api/calc/prepare_calculation`) before declaring Stage 5B API-complete beyond local implementation.

## Status

`DEPLOYMENT_CANDIDATE_PENDING_RENDER_VERIFICATION`

Do **not** promote to `VERIFIED_RENDER_PENDING_OPERATOR_VISIBLE_INTEGRATION` until the live check below passes.

## Governance (unchanged)

- No GAS changes for this gate
- No Sheet changes for this gate
- No pricing, BOM, weight, CAD, DB, Supabase

## Deployment path

Render deploy is GitHub-based in the current setup. A commit that includes `main.py` Stage 5B `physical_summary` must be pushed; then wait for Render to deploy the new revision.

## Reference request (canonical test vector)

`POST /api/calc/prepare_calculation`

Example payload (matches structural + footprint expectations for `CFG_SINGLE_BUS_SECTION`, 22 cells):

```json
{
  "meta": { "request_id": "stage5b-render-gate" },
  "module": "CALC_CONFIGURATOR",
  "action": "prepare_calculation",
  "payload": {
    "object_number": "7445-B",
    "product_type": "KZO",
    "logic_version": "KZO_MVP_V1",
    "voltage_class": "VC_10",
    "busbar_current": 1250,
    "configuration_type": "CFG_SINGLE_BUS_SECTION",
    "quantity_total": 22,
    "cell_distribution": {
      "CELL_INCOMER": 2,
      "CELL_OUTGOING": 16,
      "CELL_PT": 2,
      "CELL_BUS_SECTION": 2
    },
    "status": "DRAFT"
  }
}
```

## Live verification checklist (must all pass)

For `status: success` and present `data`:

- [ ] `data.physical_summary` object present (not null / not omitted)
- [ ] `data.physical_summary.summary_version` = `KZO_STAGE_5B_PHYSICAL_FOOTPRINT_MVP_V1`
- [ ] `data.physical_summary.estimated_total_width_mm` = `17600`
- [ ] `data.physical_summary.section_count` = `2`
- [ ] `data.physical_summary.footprint_class` = `large_lineup`
- [ ] `data.physical_summary.mvp_standard_cell_width_mm` = `800`
- [ ] `data.physical_summary.interpretation_scope` = `PHYSICAL_SCALE_ESTIMATE_MVP_ONLY` (MVP / footprint estimate only)
- [ ] `data.physical_summary.basis` present (string includes MVP basis, e.g. `total_cells x standard_cell_width_mvp`)

## Pre-deploy observation (expected)

Before the GitHub revision containing Stage 5B is deployed to Render, live `data.physical_summary` may be absent even when `status` is `success`.

Recorded probe baseline (repository state before deploy commit in this gate task): live Render returned `physical_summary` as **not present** in `data` for the reference vector — consistent with **pre-Stage-5B deployment**.

## Pass transition

When the checklist above passes on live Render, update this document status to:

`VERIFIED_RENDER_PENDING_OPERATOR_VISIBLE_INTEGRATION`

(Operator-visible integration of `physical_summary` remains a separate optional task; this gate is **Render API truth** only.)
