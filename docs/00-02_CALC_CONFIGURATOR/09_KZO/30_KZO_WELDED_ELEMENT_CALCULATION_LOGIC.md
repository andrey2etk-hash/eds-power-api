# KZO WELDED ELEMENT CALCULATION LOGIC

## Status
MVP / PROTOTYPE

## Purpose
Transform DNA selections into rough engineering calculation outputs for live prototype.

## Scope
MVP only:

- Busbar logic
- Insulator logic
- Primary equipment package logic
- Simplified accessory package logic

## Section 1 — Busbar Logic
Input:

- busbar_rated_current

Output:

- rough busbar section class

Example:

1000A -> Cu 60x10 (placeholder until refined)

## Section 2 — Insulator Logic
Input:

- short_circuit_current
- busbar_length

Output:

- insulator spacing step
- rough insulator count

Example:

20kA -> 600mm step

## Section 3 — Primary Equipment Package
Input:

- cell type
- switching type

Output:

- rough primary package

## Section 4 — Simplified Accessory Package
Input:

- cell role

Output:

- rough mounting/accessory kit

## Governance Warning
This document is MVP approximation only.
Not final BOM.
Not final engineering.
Designed for live calculator demonstration.

## Refinement Rule
All future refinements:

[PROTOTYPE_REFINEMENT]
