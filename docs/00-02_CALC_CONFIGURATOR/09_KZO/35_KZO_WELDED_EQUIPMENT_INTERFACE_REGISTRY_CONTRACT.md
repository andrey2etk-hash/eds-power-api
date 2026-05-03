# KZO WELDED EQUIPMENT INTERFACE REGISTRY CONTRACT

## Status
MVP / PROTOTYPE / DOC-FIRST

## Purpose
Define how equipment-specific constructive constraints affect semantic nodes and engineering candidate selection.

## Core Formula
CELL DNA
-> Active Semantic Node
-> Equipment Interface Constraint
-> Candidate Filter
-> Registry Selection

## Docs Before JSON Rule
This document is source of truth.
JSON registry must follow this contract.

## Equipment Interface Concept
Equipment does not directly define full busbar.
Equipment defines:
- minimum physical compatibility
- terminal geometry constraints
- allowable materials
- node-specific interface restrictions

## Required Fields Per Equipment Entry
- equipment_id
- equipment_family
- equipment_type
- interface_node
- terminal_min_width_mm
- terminal_min_thickness_mm
- compatible_busbar_materials
- strip_count_constraints
- topology_constraints
- interface_reason
- source_basis
- notes
- status

## Equipment Family Examples
- VACUUM_BREAKER
- DISCONNECTOR
- LOAD_BREAK_SWITCH
- VT_BRANCH
- BRIDGE_INTERFACE

## Constraint Rule
A candidate may pass current,
but FAIL equipment interface.

Example:
If breaker terminal width = 60 mm,
busbar width < 60 mm = FAIL.

## MVP Boundary
- rough interface constraints only
- no full CAD geometry
- no bolt pattern
- no final mounting package
- no final apparatus dimensional certification

## Future Expansion
- exact drilling templates
- bolt package mapping
- dynamic apparatus variants
- manufacturer-specific dimensional packs
