# KZO WELDED SHMR DELTA

## Status
PRE-CONSTRUCTIVE / CONCEPTUAL CALCULATION ONLY

## Classification
SHM derivative only.
Not separate base family.

## Core Formula
SHMR = SHM_BASE + DISCONNECTOR_DELTA

## SHM Base Reference
Use:

- `docs/00-02_CALC_CONFIGURATOR/09_KZO/27_KZO_WELDED_SHM_DNA.md`

## Additional Mandatory Input
- shmr_disconnector_type

## Dependency Rules
IF `bridge_type = SHMR`:

- `shmr_disconnector_type` = REQUIRED

## Downstream Impact
- purchasing
- switching package
- disconnector procurement
- topology + isolation governance

## Risks
- SHMR mistaken for standalone topology
- missing disconnector definition
- duplicate SHM logic
- premature interlock assumptions

## Missing Inputs
- disconnector catalog
- compatibility matrix
- switching constraints
- constructive mounting doctrine

## Governance Warning
SHMR is SHM derivative only.
Detailed disconnector mechanics deferred.

## Implementation Blockers
No implementation until:

- SHM approved
- SHMR delta approved
- disconnector governance defined
