# KZO WELDED SV CELL DNA

## Status
PRE-CONSTRUCTIVE / DOC ONLY

## Governance Verdict
SAFE WITH STRUCTURAL FIXES
IMPLEMENTATION BLOCKED — TOPOLOGY INCOMPLETE

## Core Formula
SV = LINE_CELL_BASE + SECTION_BREAKER_DELTA + SV/SR_INTERFACE

## Mandatory Pair Doctrine
SV cannot reach VALID state if SR cell is missing from same configuration session.

Required parameters:

- pairing_id
- interface_master_cell

Rule:

- SV = interface master
- SR = interface slave for interface BOM/spec allocation

## Safe Base

- LINE_CELL_BASE inheritance is allowed as baseline
- Vacuum SV removes line disconnector and related drive/interlock/limit switch elements
- Interface allocation is required to prevent duplication

## Risks

- SV and SR may receive conflicting interface choices
- DIRECT_BACK_TO_BACK may invalidate LINE_CELL_BASE assumptions
- Primary circuit is busbar-to-busbar, not busbar-to-line
- Busbar bridge ownership is unresolved
- RVZ-10/630(1000) III TOP_POLES_TO_BUSBAR may require separate doctrine

## Missing Inputs

- sv_sr_connection_type
- pairing_id
- interface_master_cell
- inter_cell_distance
- cross_cell_interlock_logic
- phase_alignment / phase_swap_required
- busbar_bridge_owner
- rvz_section_disconnector_layout

## SV/SR Interface Rules

Record current draft rules:

- CABLE: cable + terminations allocated only to SV
- SIDE_BUSBAR_TO_ADJACENT_SR: busbar + insulators split between SV/SR; 3 pass-through insulators only in SV
- BUSBAR_BRIDGE_FACE_TO_FACE: topology incomplete; side enclosure/box may belong to bridge
- DIRECT_BACK_TO_BACK: topology incomplete; 3 pass-through insulators only in SV

## Layered Node Compatibility

SIDE_BUSBAR is one virtual node split across two physical cells.
Future BOM aggregation must support Virtual Node Split.

## Implementation Status

Cursor must NOT implement SV logic until:

- SV_SR_PAIR_DNA is defined
- pairing_id rule is defined
- interface ownership is defined
- connection topology is clarified
- busbar bridge ownership is clarified
