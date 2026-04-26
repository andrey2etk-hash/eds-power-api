# KZO Validation

## Governance status

APPROVED_WITH_FIXES

Stage 2E validation foundation was normalized after Gemini provisional review.

This file defines flat MVP validation only.

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

- `VC_06` = 6kV
- `VC_10` = 10kV
- `VC_20` = 20kV
- `VC_35` = 35kV

### configuration_type:

- `CFG_SINGLE_BUS` = Single bus
- `CFG_SINGLE_BUS_SECTION` = Single bus with section

### cell_type:

- `CELL_INCOMER` = Incomer
- `CELL_OUTGOING` = Outgoing
- `CELL_PT` = Voltage transformer cell
- `CELL_BUS_SECTION` = Bus section cell

### quantity rules:

- quantity_total > 0
- sum(cell_distribution) == quantity_total

## 3. Flat MVP Validation Rules

Validation checks only:

- field present?
- field allowed?
- quantity match?
- required by selected config?

No deep dependency trees are part of Stage 2E MVP validation.

## 4. Draft vs Validated Rules

Missing `breaker_type`:

- allowed in DRAFT
- blocked in VALIDATED if required by selected cell type

Missing `voltage_class`:

- allowed in DRAFT
- blocked in VALIDATED

Broken JSON schema:

- blocked always

## 5. Error Codes

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
