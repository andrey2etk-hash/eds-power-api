# SV/SR PAIR DNA

## Status
REQUIRED BEFORE IMPLEMENTATION

## Purpose
Define paired-cell dependency between SV and SR.

## Rule of Paired Existence
SV cannot be VALID without paired SR.
SR cannot independently allocate interface elements already owned by SV.

## Required Parameters

- pairing_id
- sv_cell_id
- sr_cell_id
- interface_master_cell
- sv_sr_connection_type
- inter_cell_distance
- orientation
- busbar_bridge_owner
- cross_cell_interlock_logic

## Interface Master Rule
Default:

- SV = interface_master_cell
- SR = interface_slave_cell

## SR Reduction Rule (Vacuum SV Pair)
IF SV contains vacuum breaker:
SR must NOT duplicate:

- vacuum breaker
- current transformers

## Pair Calculation Principle
SV/SR pair is conceptual calculation group first,
not cabinet design doctrine.

## Governance Boundary
Current pair doctrine governs:

- equipment presence
- equipment removal
- interface ownership
- anti-duplication

Deferred:

- cabinet structural divergence
- roof/floor construction
- panel mechanics
- constructive frame differences

## Open Questions

- Who owns busbar bridge as product/node?
- Is side box part of bridge or cell?
- How to split busbar/insulator quantities between SV and SR?
- Which variants invalidate LINE_CELL_BASE?
- What exact topology rules apply to face-to-face and back-to-back?

## Blocker
IMPLEMENTATION BLOCKED UNTIL PAIR DOCTRINE IS APPROVED
