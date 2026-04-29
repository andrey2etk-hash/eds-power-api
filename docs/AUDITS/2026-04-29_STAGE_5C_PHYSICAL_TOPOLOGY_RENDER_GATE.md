# Stage 5C Physical Topology — Render Verification Gate

## Objective

Verify **`data.physical_topology_summary`** on **live Render** for the approved KZO MVP scenario, without changing API logic, GAS, or Sheet.

## Status

`VERIFIED_RENDER_PENDING_OPERATOR_VISIBLE_INTEGRATION`

Operator-visible Sheet integration of `physical_topology_summary` is **out of scope** for this gate (same pattern as Stage 5B).

## Governance (strict)

- No GAS changes in this gate
- No Sheet layout / range changes in this gate
- No topology rule expansion in this gate
- No BOM / pricing / CAD / weight / DB / Supabase

## Deployment path

GitHub `main` receives commit containing Stage 5C implementation; Render deploys GitHub-based revision — allow deployment lag before live fields appear.

**Deploy-containing commit (this session):** `f8065a3`

Endpoint:

`POST https://eds-power-api.onrender.com/api/calc/prepare_calculation`

## Canonical request vector (approved MVP scenario)

```json
{
  "meta": { "request_id": "stage5c-render-gate" },
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

## Live verification checklist

For `status: success`:

- [x] `data.physical_topology_summary` present (object)
- [x] `topology_version` = `KZO_STAGE_5C_TOPOLOGY_MVP_V1`
- [x] `topology_type` = `TOPOLOGY_BALANCED_SPLIT`
- [x] `total_sections` = `2`
- [x] `section_cell_counts` = `[11, 11]`
- [x] `interpretation_scope` present (non-empty)
- [x] `basis` present (non-empty)

Regression parity (additive contract):

- [x] `data.structural_composition_summary` present
- [x] `data.physical_summary` present

## Live probe record

Programmatic probes after push of `f8065a3`:

- Attempts 1–2: **`physical_topology_summary` not yet present** on responding instance (Render deployment lag).
- Attempt 3 (after ~80s cumulative delay): **`physical_topology_summary` present**; checklist matched; Stage 5A / 5B fields present.

Representative **`data.physical_topology_summary`** (live):

```json
{
  "topology_version": "KZO_STAGE_5C_TOPOLOGY_MVP_V1",
  "total_sections": 2,
  "topology_type": "TOPOLOGY_BALANCED_SPLIT",
  "section_distribution": [
    { "section_id": "A", "cell_count": 11 },
    { "section_id": "B", "cell_count": 11 }
  ],
  "section_cell_counts": [11, 11],
  "interpretation_scope": "PHYSICAL_TOPOLOGY_MVP_ONLY",
  "basis": "distribution from lineup_summary.total_cells and lineup_summary.sections (Stage 5A structural composition); scale context from Stage 5B physical footprint MVP (same request)"
}
```

## Result

Manual gate: **`PASS`** (live Render verification only).
