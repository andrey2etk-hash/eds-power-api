# KZO WELDED BUSBAR NODE MATRIX CONTRACT

## Status
MVP / PROTOTYPE / DOC-FIRST

## Purpose
Define how KZO cell types activate busbar semantic nodes and how each active node provides rules for busbar selection and length estimation.

## Core Formula
CELL_TYPE x BUSBAR_NODE
-> LENGTH_RULE + CURRENT_SOURCE + FORM_FACTOR_CONSTRAINTS

## Rule: Docs Before JSON
This document is the source of truth for busbar node matrix rules.
JSON registry must follow this contract.

## Busbar Semantic Node Concept
Busbar node = meaningful location where busbar may exist.

## Required Fields Per Matrix Entry
- cell_type
- busbar_node_id
- node_active
- length_rule_type
- length_mm_mvp
- current_source
- min_width_mm
- min_thickness_mm
- strip_count_policy
- form_factor_reason
- usage_context
- notes
- status

## Current Source Rules
Allowed current_source values:
- GLOBAL_BUSBAR_CURRENT
- CELL_RATED_CURRENT
- BRIDGE_RATED_CURRENT
- INTERFACE_RATED_CURRENT
- EXTERNAL_REFERENCE

## Length Rule Types
Allowed:
- FIXED_MVP
- CELL_WIDTH_BASED
- BRIDGE_LENGTH_BASED
- INTERFACE_SPLIT
- DEFERRED

## Form-Factor Constraint Rule
Busbar candidate must pass:
1. current requirement
2. form-factor requirement
3. product usage context requirement

Current pass alone is not enough.

Busbar node constraints may originate from:

- node matrix
- product usage registry
- equipment interface registry

Node matrix defines where.
Equipment interface defines apparatus compatibility.

## Example Rule
If node requires min_width_mm = 60,
then busbar candidates with section_width_mm < 60 must fail,
even if rated_current_a is sufficient.

## MVP Boundary
- No pricing
- No final BOM
- No exact constructive guarantee
- No final thermal/dynamic engineering
- Rough technical specification only

## Future Expansion
- dynamic short-circuit checks
- support spacing
- exact bending geometry
- metiz package mapping
- price layer
