# KZO Validation

## 1. Required Fields

Required fields for KZO validation:

- object_number
- product_type
- voltage_class
- busbar_current
- configuration_type
- quantity_total
- cell_distribution
- breaker_type (if applicable)

Rules:

- `object_number` may be missing in DRAFT
- `object_number` is required before VALIDATED / final / production transition
- structurally invalid payloads are blocked in all statuses

## 2. Allowed Value Matrix

### voltage_class:

- 6kV
- 10kV
- 20kV
- 35kV

### configuration_type:

- SINGLE_BUS
- SINGLE_BUS_SECTION
- DOUBLE_BUS (deferred unless MVP approved)

### cell_type:

- INCOMER
- OUTGOING
- PT
- BUS_SECTION
- RISER
- SHM
- SHMR

### quantity rules:

- quantity_total > 0
- sum(cell_distribution) == quantity_total

## 3. Draft vs Validated Rules

Missing `breaker_type`:

- allowed in DRAFT
- blocked in VALIDATED if required by selected cell type

Missing `voltage_class`:

- allowed in DRAFT
- blocked in VALIDATED

Broken JSON schema:

- blocked always

## 4. Error Codes

- KZO_REQUIRED_FIELD_MISSING
- KZO_INVALID_VOLTAGE_CLASS
- KZO_CELL_QUANTITY_MISMATCH
- KZO_UNSUPPORTED_CONFIGURATION

## Stage 2E boundaries

This file defines validation foundation only.

It does not define:

- KTP logic
- Powerline logic
- BOM
- CAD
- production routes
- supplier logic
- commercial logic
- API code
