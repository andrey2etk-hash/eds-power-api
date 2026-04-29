# KZO Outputs

## Stage 3A MVP Outputs

This file defines only MVP outputs for KZO Calculation Object V1.

It does not define advanced calculations, BOM, CAD, production routes, supplier logic, commercial logic, or API implementation.

All outputs must align with:

- `docs/00-02_CALC_CONFIGURATOR/09_KZO/07_VALIDATION.md`
- `docs/00_SYSTEM/04_DATA_CONTRACTS.md`
- `docs/00_SYSTEM/06_OBJECT_STATUSES.md`

## validation_status

Validation status is returned inside `data.validation_status`.

It describes whether the KZO Calculation Object V1 passed flat MVP validation.

Allowed MVP values:

- `VALIDATED`
- `ERROR`

Rules:

- `VALIDATED` means all required MVP fields are present, allowed, and quantity rules pass
- `ERROR` means validation failed and an error object must be returned

## normalized_payload

Normalized payload is returned inside `data.normalized_payload`.

It is the validated KZO Calculation Object V1 after field normalization.

Success response envelope:

```json
{
  "status": "success",
  "data": {
    "validation_status": "VALIDATED",
    "normalized_payload": {
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
      "status": "VALIDATED",
      "breaker_type": null,
      "notes": null
    },
    "basic_result_summary": {
      "summary_version": "KZO_MVP_V1",
      "product_type": "KZO",
      "logic_version": "KZO_MVP_V1",
      "voltage_class": "VC_10",
      "busbar_current": 1250,
      "configuration_type": "CFG_SINGLE_BUS_SECTION",
      "quantity_total": 22,
      "cell_type_summary": {
        "CELL_BUS_SECTION": 2,
        "CELL_INCOMER": 2,
        "CELL_OUTGOING": 16,
        "CELL_PT": 2
      },
      "validation_status": "VALIDATED"
    }
  },
  "error": null,
  "metadata": {
    "request_id": "uuid",
    "api_version": "0.1.0",
    "logic_version": "KZO_MVP_V1",
    "execution_time_ms": 0
  }
}
```

## basic_result_summary

`basic_result_summary` is the first normalized KZO structural summary.

It is returned inside `data.basic_result_summary`.

Required fields:

- product_type
- logic_version
- voltage_class
- busbar_current
- configuration_type
- quantity_total
- cell_type_summary
- validation_status

Rules:

- normalized echo + validated structure only
- no engineering assumptions
- no price calculation
- no BOM calculation
- no CAD output
- no production route
- no commercial offer generation
- no dimensions
- no weight

## structural_composition_summary

`structural_composition_summary` is the Stage 5A first practical KZO structural meaning layer.

It is returned inside `data.structural_composition_summary`.

Required fields:

- summary_version
- product_type
- lineup_summary
- cell_composition
- functional_lineup_composition
- structural_flags
- interpretation_scope

Rules:

- API-side only
- deterministic structural interpretation only
- no design recommendations
- no breaker selection
- no PT truck selection
- no busbar sizing
- no price calculation
- no BOM calculation
- no CAD output
- no production route
- no commercial offer generation

Example:

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

## physical_summary

`physical_summary` is the Stage 5B MVP **rough physical scale** estimate for the KZO lineup. It is derived only from the Stage 5A `structural_composition_summary.lineup_summary` (validated cell count and configuration sections). It is returned inside `data.physical_summary`.

Rules:

- API-side only
- estimate only — not detailed engineering, not CAD
- deterministic MVP assumptions (documented constant `mvp_standard_cell_width_mm`)
- no BOM, no pricing, no weight
- no GAS computation (GAS unchanged)

Example:

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

## physical_topology_summary

`physical_topology_summary` is the Stage 5C MVP **physical arrangement** interpretation: how total cells are grouped into named sections for the configured section count. It is additive; returned inside `data.physical_topology_summary`. It is derived from Stage 5A `lineup_summary.total_cells` and `lineup_summary.sections`; it does **not** perform bus sizing, routing, CAD, BOM, pricing, or weight.

Rules:

- API-side only — no GAS, no Sheet
- deterministic split: one section ⇒ all cells in `A`; two sections ⇒ uneven split assigns the odd cell to section `A` (`TOPOLOGY_UNEVEN_SPLIT`), balanced counts ⇒ `TOPOLOGY_BALANCED_SPLIT`
- not detailed plant layout — topology labels are MVP placeholders only

Example (two sections, 22 cells, balanced):

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

## error object

Errors must follow the Global Error Contract in `docs/00_SYSTEM/04_DATA_CONTRACTS.md`.

Error response envelope:

```json
{
  "status": "validation_error",
  "data": null,
  "error": {
    "error_code": "KZO_CELL_QUANTITY_MISMATCH",
    "message": "Cell distribution sum must match quantity_total",
    "source_field": "cell_distribution",
    "module": "CALC_CONFIGURATOR",
    "action": "prepare_calculation"
  },
  "metadata": {
    "request_id": "uuid",
    "api_version": "0.1.0",
    "logic_version": "KZO_MVP_V1",
    "execution_time_ms": 0
  }
}
```
