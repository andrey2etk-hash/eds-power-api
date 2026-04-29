# Stage 6C Engineering Burden — Render Verification Gate

## Objective

Verify `data.engineering_burden_summary` for KZO MVP on **live Render** (`POST /api/calc/prepare_calculation`) before declaring **Stage 6C** Render API verification complete. Operator-visible Sheet verification remains **out of scope** for this gate (see **IDEA-0014** status).

## IDEA-0014 status (after live PASS)

**`RENDER_VERIFIED_PENDING_OPERATOR_TEST`**

## Live verification recorded

**Result: PASS**

- **Deploy commit pushed to `main`:** `35ac23a` (Stage 6C `engineering_burden_summary` implementation + governance docs bundle).
- **Probe attempts:** Attempts **1–2** — **`engineering_burden_summary`** not yet visible on running instance (**deployment lag**, same pattern as Stage 5B Render gate).
- **Attempt 3 (~93s cumulative wait)** — **`engineering_burden_summary`** present; checklist fields **PASS**.
- Endpoint: **`POST https://eds-power-api.onrender.com/api/calc/prepare_calculation`**
- Probe `meta.request_id`: **`stage6c-render-gate`**

Representative excerpt — live `data.engineering_burden_summary`:

```json
{
  "burden_version": "KZO_STAGE_6C_ENGINEERING_BURDEN_MVP_V1",
  "structural_burden_class": "BURDEN_HEAVY",
  "assembly_burden_class": "ASSEMBLY_COMPLEX",
  "estimated_mass_class": "MASS_EXTENDED",
  "complexity_basis": "COMPLEXITY_HEAVY",
  "topology_basis": "TOPOLOGY_BALANCED_SPLIT",
  "footprint_basis": "SCALE_LARGE",
  "interpretation_scope": "ENGINEERING_BURDEN_ONLY_MVP"
}
```

(Values derive from heuristic mapping for the canonical 22-cell vector below; tiers are planning-grade only.)

## Preconditions still present (`status: success`, `data` present)

- `structural_composition_summary`
- `physical_summary`
- `physical_topology_summary`
- `engineering_class_summary`

All verified present alongside **`engineering_burden_summary`** on live PASS probe.

## Governance (unchanged for this gate)

- No **`main.py`** change for verification-only closure
- No GAS / Sheet edits for Render gate artifact
- No kg / BOM / pricing / procurement / Stage 7 expansion

## Reference request (canonical KZO MVP test vector)

Aligned with **`docs/AUDITS/2026-04-29_STAGE_5B_PHYSICAL_FOOTPRINT_RENDER_GATE.md`** (CFG_SINGLE_BUS_SECTION, 22 cells):

```json
{
  "meta": { "request_id": "stage6c-render-gate" },
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

## Live checklist (all PASS on Attempt 3)

| Check | PASS |
| --- | --- |
| `engineering_burden_summary` present | yes |
| `burden_version` = `KZO_STAGE_6C_ENGINEERING_BURDEN_MVP_V1` | yes |
| `structural_burden_class`, `assembly_burden_class`, `estimated_mass_class` present | yes |
| `complexity_basis`, `topology_basis`, `footprint_basis` present | yes |
| `interpretation_scope` = `ENGINEERING_BURDEN_ONLY_MVP` | yes |
| Prior layers preserved (listed above) | yes |

## References

- **`IDEA-0014`** — `docs/00_SYSTEM/12_IDEA_MASTER_LOG.md`
- Stage 6C foundation audit — `docs/AUDITS/2026-04-29_STAGE_6C_ENGINEERING_BURDEN_FOUNDATION.md`
