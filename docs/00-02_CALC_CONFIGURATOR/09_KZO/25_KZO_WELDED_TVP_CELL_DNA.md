# KZO WELDED TVP CELL DNA

## Status
PRE-CONSTRUCTIVE / CONCEPTUAL CALCULATION ONLY

## Scope Boundary
This doctrine governs TVP calculation logic only.
It does NOT define final cabinet construction, compartment mechanics, mounting geometry, or full BOM.

## Cell Classification
TVP is a distinct KZO cell type.

## Core Formula
TVP_CELL = TVP_PLACEMENT_MODE + PRIMARY_SWITCHING + FUSE_PROTECTION + TRANSFORMER_DATA

## TVP Placement Modes
- EXTERNAL_TVP_NEARBY_CABLE_FED
- INTERNAL_TVP_IN_CELL

## External TVP Mode
- LINE-like structural possibility
- External transformer
- Cable-fed nearby transformer
- Transformer not allocated inside cell
- Internal transformer-specific equipment fields may be blocked or informational only

## Internal TVP Mode
- Transformer inside cell
- Primary switching required
- Fuse protection required
- Transformer definition required

## Primary Switching
- DISCONNECTOR
- LOAD_BREAK_SWITCH_VNAP

## Mandatory Internal TVP Parameters
- fuse_rated_current
- transformer_type
- transformer_power
- transformer_manufacturer
- transformer_full_name

## Dependency Rules
If `tvp_placement_mode = EXTERNAL_TVP_NEARBY_CABLE_FED`:

- `transformer_type` = optional / external_reference
- `transformer_power` = optional / external_reference
- `transformer_manufacturer` = optional / external_reference
- `transformer_full_name` = optional / external_reference
- internal fuse logic may be blocked unless explicitly required by project

If `tvp_placement_mode = INTERNAL_TVP_IN_CELL`:

- `primary_switching_type` = required
- `fuses_required` = required
- `fuse_rated_current` = required
- `transformer_type` = required
- `transformer_power` = required
- `transformer_manufacturer` = required
- `transformer_full_name` = required

## Downstream Impact
- purchasing
- passport
- dispatcher naming
- fuse procurement
- transformer procurement
- constructive branch logic
- future compartment layout

## Risks
- TVP mistaken for LINE
- external/internal mode confusion
- missing fuse logic
- transformer under-definition
- premature constructive assumptions

## Missing Inputs
- allowed fuse current catalog
- transformer compatibility matrix
- manufacturer catalog
- dimensional constraints
- exact naming conventions

## Governance Warning
Conceptual calculation doctrine only.
Constructive cabinet divergence deferred.

## Implementation Blockers
No implementation until:

- TVP DNA approved
- external/internal mode clarified
- fuse doctrine approved
- transformer catalog governance defined
