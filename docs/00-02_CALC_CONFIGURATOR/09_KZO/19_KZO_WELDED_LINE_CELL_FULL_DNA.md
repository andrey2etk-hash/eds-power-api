# KZO Welded Line Cell Full DNA

## 1. Purpose

Capture the canonical full engineering attribute set for `KZO_WELDED` line cell configuration in MVP documentation form, before implementation.

## 2. Scope: KZO_WELDED / LINE_CELL only

This artifact applies only to:

- product family: `KZO_WELDED`
- cell type: `LINE_CELL`

Out of scope:

- other KZO cell types
- non-welded families
- implementation/API/GAS/DB changes

## 3. Attribute list

All attributes below are treated as core MVP attributes (no core/secondary split):

1. cell number by schematic
2. outgoing line name
3. switching device type
4. fuse rated current (if switching device is `LBS_FUSE` / `ВНАП`)
5. bus disconnector type/current (if vacuum breaker)
6. line disconnector type/current (if vacuum breaker)
7. drive type
8. electromagnetic locks
9. current transformer presence
10. CT secondary winding count
11. CT accuracy class
12. CT ratio
13. cable count
14. cable type (`single-core` / `three-core`)
15. cable cross-section
16. meter presence (`yes` / `no` / `prepared`)
17. zero-sequence CT presence
18. zero-sequence CT type
19. surge arrester on cable
20. voltage indicators on cable
21. main/earthing knife position feedback
22. line ammeter presence/type
23. network analyzer presence/type

## 4. Dependency rules

Global dependency law: each downstream attribute unlocks only after required upstream context is valid.

MVP dependency examples for LINE_CELL:

- `switching_device_type = VACUUM_BREAKER` unlocks:
  - bus disconnector type/current
  - line disconnector type/current
- `switching_device_type = LBS_FUSE / ВНАП` requires:
  - fuse rated current
- `current_transformer_presence = YES` unlocks:
  - CT secondary winding count
  - CT accuracy class
  - CT ratio
- `zero-sequence_CT_presence = YES` unlocks:
  - zero-sequence CT type
- `meter_presence` state influences whether:
  - line ammeter presence/type
  - network analyzer presence/type
  are required or optional in final passport set.

## 5. Downstream impact map

- `line_name` -> passport + dispatcher metal marking
- `ammeter_type` -> front door punching / facade BOM
- `network_analyzer_type` -> front door punching / wiring / purchasing
- `cable_count` + `cable_cross_section` -> cable support / cable compartment layout
- `zero_sequence_CT_type` -> mounting bracket / cable path
- `CT winding/class/ratio` -> purchasing + schematic/passport data
- `switching_device_type` -> primary circuit construct
- `fuse_rated_current` (for `LBS_FUSE` / `ВНАП`) -> purchasing + protection selection + schematic + passport + BOM

## 6. Passport / marking impact

The following fields directly shape passport/marking output:

- cell number by schematic
- outgoing line name
- switching device type
- CT ratio/class/winding metadata
- meter/ammeter/network analyzer presence and type
- knife position feedback declaration

Dispatcher/metal marking uses canonical `outgoing line name` + schematic numbering.

## 7. Purchasing impact

Purchasing-impacting fields in this DNA:

- switching device type
- fuse rated current (for `LBS_FUSE` / `ВНАП`)
- bus disconnector type/current (if vacuum breaker)
- line disconnector type/current (if vacuum breaker)
- CT presence + winding count + accuracy class + ratio
- zero-sequence CT presence/type
- meter/ammeter/network analyzer presence/type
- surge arrester on cable
- voltage indicators on cable

## 8. Constructive impact

Constructive/layout-impacting fields in this DNA:

- cable count
- cable type (`single-core` / `three-core`)
- cable cross-section
- zero-sequence CT type
- knife position feedback hardware expectations
- selected measuring equipment mounting requirements

These fields define constructive constraints for line cell enclosure zones and front-door interfaces.

## 9. Validation notes

- No downstream attribute may be finalized if its upstream dependency is unresolved.
- Conditional attributes remain blocked when prerequisite conditions are false.
- `meter_presence` values are constrained to: `yes`, `no`, `prepared`.
- Cable attributes (`count`, `type`, `cross-section`) are validated as a coherent set, not independently.
- CT fields are valid only when CT presence is confirmed.
- `fuse_rated_current` is required when `switching_device_type = LBS_FUSE / ВНАП`.

## 10. Unknowns requiring user confirmation

The following require explicit user confirmation before implementation logic:

- full allowed catalog values for each manufacturer-bound field
- exact requirement matrix between `meter_presence` and analyzer/ammeter combinations
- final rule for `prepared` state effects in passport/purchasing outputs
- edge-case handling for multi-cable mixes under one line cell
- exact serialization format for knife position feedback in passport schema

## KGU Line Specialization Reference

For `KGU_LINE` use:

- `docs/00-02_CALC_CONFIGURATOR/09_KZO/26_KZO_WELDED_KGU_LINE_DELTA.md`

Rule:

- `KGU_LINE` inherits LINE base
- `KGU_LINE` requires cable-side TN synchronization delta
- `KGU_LINE` is a LINE specialization, not a separate base DNA

---

This document is planning/documentation only and is implementation-ready for user review.
