# Stage 5B Physical Footprint — Render Verification Gate

## Objective

Verify `data.physical_summary` for KZO MVP on **live Render** (`POST /api/calc/prepare_calculation`) before declaring Stage 5B API-complete beyond local implementation.

## Status

`VERIFIED_RENDER_PENDING_OPERATOR_VISIBLE_INTEGRATION`

Operator-visible integration of `physical_summary` remains a **separate** optional task — this closure is **live Render API** verification only.

## Live verification recorded

UTC/local not recorded precisely in automation; programmatic probe after GitHub deploy (`main` containing Stage 5B):

- Deployment candidate commit on `main`: `8df5c3d`

- Attempts 1–2: `physical_summary` not yet present on running instance (deployment lag).
- Attempt 3: `physical_summary` present; exact field match against checklist: **PASS**

Observed live `data.physical_summary` (Representative excerpt — full object returned by API):

```json
{
  "summary_version": "KZO_STAGE_5B_PHYSICAL_FOOTPRINT_MVP_V1",
  "estimated_total_width_mm": 17600,
  "section_count": 2,
  "footprint_class": "large_lineup",
  "basis": "total_cells x standard_cell_width_mvp",
  "mvp_standard_cell_width_mm": 800,
  "interpretation_scope": "PHYSICAL_SCALE_ESTIMATE_MVP_ONLY"
}
```

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

Reference vector: canonical JSON in “Reference request”; **Result: all items verified on deployed Render**.

For `status: success` and present `data`:

- [x] `data.physical_summary` object present (not null / not omitted)
- [x] `data.physical_summary.summary_version` = `KZO_STAGE_5B_PHYSICAL_FOOTPRINT_MVP_V1`
- [x] `data.physical_summary.estimated_total_width_mm` = `17600`
- [x] `data.physical_summary.section_count` = `2`
- [x] `data.physical_summary.footprint_class` = `large_lineup`
- [x] `data.physical_summary.mvp_standard_cell_width_mm` = `800`
- [x] `data.physical_summary.interpretation_scope` = `PHYSICAL_SCALE_ESTIMATE_MVP_ONLY` (MVP / footprint estimate only)
- [x] `data.physical_summary.basis` present (string includes MVP basis, e.g. `total_cells x standard_cell_width_mvp`)

## Historical baseline (before Stage 5B deploy)

Before the GitHub revision containing Stage 5B was deployed to Render, live `data.physical_summary` could be absent even when `status` was `success`. A probe before the deploying commit logged `physical_summary` as **not present** — consistent with pre-Stage-5B revision.
