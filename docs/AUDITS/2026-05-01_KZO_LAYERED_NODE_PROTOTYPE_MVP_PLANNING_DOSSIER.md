# KZO Layered Node Prototype MVP — Demo Case Planning Dossier

Status: `PLANNING_ONLY`  
Execution class: prototype framing only  
Bounded selection:

- Constructive family: `KZO_WELDED`
- Demo cell: `VACUUM_BREAKER_LEFT_END`
- Demo node: `INSULATOR_SYSTEM`

## 1. Constructive Family Definition

`KZO_WELDED` is the single prototype family for this slice.

Planning attributes:

- welded frame baseline
- deterministic mounting zones
- bounded compatibility map (prototype-only)

Out of scope:

- other families
- cross-family comparative rollout

## 2. Cell Role Definition

`VACUUM_BREAKER_LEFT_END` is defined as one bounded demo role:

- breaker-centric terminal role
- left-end topology anchor role
- role carries node eligibility constraints for `INSULATOR_SYSTEM`

## 3. Cell Position Definition

Position context is fixed to left-end placement.

Planning implications:

- position contributes placement point priorities
- position constrains optional hardware presence
- position affects dependency fan-out only within this demo node

## 4. Placement Point Map

Prototype L1 placement points for selected role/node:

- `PP_FRAME_LEFT_PRIMARY`
- `PP_INSULATOR_SUPPORT_A`
- `PP_INSULATOR_SUPPORT_B`
- `PP_BREAKER_INTERFACE_LEFT`

Map is planning-grade and deterministic for this one case only.

## 5. Presence Rule Matrix

Prototype L2 matrix (bounded):

- If role = `VACUUM_BREAKER_LEFT_END`, `INSULATOR_SYSTEM` = `REQUIRED`
- If position = `LEFT_END`, left support pair = `REQUIRED`
- If family = `KZO_WELDED`, welded support bracket set = `REQUIRED`
- Any rule conflict in demo case = `PLAN_INVALID` (planning gate fail)

## 6. Primary Component Logic

Prototype L3 primary components for demo node:

- insulator base element
- left support bracket set
- primary fastening interface

Logic principle:

- components derived from family + role + position tuple
- no BOM explosion and no multi-node cascade in this slice

## 7. Dependent Hardware Logic

Prototype L4 dependent hardware:

- washers/bolts/nuts linked to primary component count
- dependent hardware derived by deterministic dependency table
- no procurement/pricing logic

Reusable doctrine:

- `deriveDependentHardware` consumes rule parameters, not duplicated function branches.

## 8. Aggregate BOM Output Model

Prototype L5 output model (planning shape only):

- `node_id`
- `node_type`
- `primary_components[]`
- `dependent_hardware[]`
- `aggregate_counts`
- `planning_confidence`
- `scope_guard_state`

This is a demo presentation model, not production BOM.

## 9. Admin Future UI Rule-Edit Path

Future admin rule-edit concept (deferred, no implementation now):

- family rule set table
- role/position matrix editor
- node dependency override panel
- preview-only recomputation sandbox

Rule:

- admin editing is future UX path only; current slice remains planning artifact.

## 10. Scope Guard

Hard boundaries for this dossier:

- one family only (`KZO_WELDED`)
- one cell only (`VACUUM_BREAKER_LEFT_END`)
- one node only (`INSULATOR_SYSTEM`)
- no code/API/DB/GAS changes
- no full BOM
- no all-family rollout

## 11. Demo Presentation Value

This dossier gives a presentation-capable proof frame that EDS Power can map:

`family + role + position -> layered node logic -> bounded aggregate BOM model`

without architectural drift or premature expansion.

---

Final rule: planning artifact only; implementation requires a separate explicit bounded execution task.
