# KZO Welded Incoming Cell DNA

## 1. Purpose

Define canonical incoming-cell DNA for `KZO_WELDED` using inheritance from the welded LINE cell DNA plus incoming-specific delta attributes.

## 2. Scope: KZO_WELDED / INCOMING_CELL

This document applies only to:

- family: `KZO_WELDED`
- cell type: `INCOMING_CELL`

Out of scope:

- other families
- other cell types
- implementation/API/GAS/DB changes

## 3. Inheritance model

`INCOMING_CELL = LINE_CELL_BASE + INCOMING_DELTA`

## 4. Inherited attributes

Inherited baseline is defined by:

- `docs/00-02_CALC_CONFIGURATOR/09_KZO/19_KZO_WELDED_LINE_CELL_FULL_DNA.md`

This document does not duplicate full inherited attribute text.

## 5. Incoming delta attributes

- `auxiliary_transformer_presence`: `YES` / `NO` / `PREPARED`
- `auxiliary_transformer_manufacturer`
- `auxiliary_transformer_type`
- `auxiliary_transformer_power`
- `auxiliary_transformer_protection_fuse_presence`
- `auxiliary_transformer_protection_fuse_type`
- `auxiliary_transformer_protection_fuse_current`

## 6. PREPARED canon

`PREPARED` means:

- reserved place
- mounting prepared
- busbar preparation completed
- partial wiring prepared

## 7. PREPARED validation

For `auxiliary_transformer_presence = PREPARED`:

- `auxiliary_transformer_manufacturer` = nullable
- `auxiliary_transformer_type` = nullable or project-defined placeholder
- `auxiliary_transformer_power` / frame-size-defining value = REQUIRED

Reason:

- bracket and volume compatibility depend on transformer size.

## 8. Incoming current logic

Incoming cell main apparatus rating must be checked against `busbar_rated_current` from global configuration,
or explicitly marked as future override if final incoming rating policy is not finalized for project specifics.

## 9. Downstream impact map

- auxiliary transformer presence -> relay compartment layout, bracket, bus preparation, wiring, BOM, passport
- auxiliary transformer power -> mounting dimensions / volume compatibility
- protection fuse -> purchasing / schematic / BOM
- incoming current logic -> main apparatus selection / validation

## 10. Unknowns requiring user confirmation

- exact protection fuse variants
- volume/height compatibility rules
- whether incoming main apparatus rating always equals `busbar_rated_current` or can differ by project

---

This artifact is documentation-only and implementation-ready for user confirmation.
