# KZO WELDED SR CELL DNA

## Status
PRE-CONSTRUCTIVE / CONCEPTUAL CALCULATION ONLY

## Scope Boundary
This document governs calculation doctrine only.
It does NOT define final cabinet construction.
Future cabinet-level constructive stages may introduce substantially more divergence.

## Core Formula
SR = LINE_CELL_BASE + SECTION_DISCONNECTOR_DELTA + SV/SR_INTERFACE

## Core Principle
SR mirrors much of SV paired logic,
but must avoid redundant duplication when paired with SV.

## Mandatory Pair Rule
SR cannot be VALID independently if configured as SV/SR pair member.

Required:

- pairing_id
- paired_sv_cell_id
- sv_sr_connection_type
- interface_master_cell

## Vacuum Pair Exception
IF paired SV includes vacuum breaker:
REMOVE from SR:

- vacuum breaker
- current transformers

## Safe Base

- LINE_CELL_BASE may be used as conceptual baseline
- SR may inherit broad line-cell logic where valid
- Interface logic remains paired with SV

## Risks

- Duplicate breaker allocation
- Duplicate CT allocation
- Conflicting interface ownership
- Incorrect standalone SR normalization
- Topology drift
- Future constructive divergence mistaken as current calculation doctrine

## Missing Inputs

- pairing_id
- paired_sv_cell_id
- sv_sr_connection_type
- interface_master_cell
- sr_role_type
- inter_cell_distance
- orientation
- busbar_bridge_owner
- cross_cell_interlock_logic

## Governance Warning
Current doctrine is CALCULATION ONLY.
Construction-stage SR cabinet differences are intentionally deferred.

## Implementation Blockers
SR implementation blocked until:

- SV_SR_PAIR_DNA approved
- interface ownership defined
- paired vacuum logic approved
- topology clarified
