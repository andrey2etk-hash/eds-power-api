# MODULE 01 DEMO SCENARIO PLAN

## Status
PLANNING ONLY / NO IMPLEMENTATION

## Purpose

Define a demonstration scenario for Module 01 local KZO engineering logic.

The demo must show:

Input prepared engineering data
-> DOC 36 busbar evaluation safety
-> DOC 37 node geometry and joint stack
-> DOC 37 fastener selection
-> DOC 38 kit issue aggregation

## Demo Audit Decisions

Accepted:
- registry version visibility
- immutable demo fixtures
- management glossary
- audit trail sample
- BOM vs Kit Issue clarification

Partially accepted:
- negative scenario only as backup, not main flow

Rejected for main demo:
- failed Node C inside primary demo path

## Main Demo Flow

The main demo uses only successful verified nodes:

- Node A = PASS
- Node B = PASS
- Aggregation = PASS
- kit_issue_lines = generated

Purpose:
Show useful engineering output and traceability.

## Optional Backup Safety Fixture

A separate optional fixture may demonstrate INCOMPLETE behavior.

Rules:
- not part of primary demo
- not shown unless asked
- used only to prove guardrails
- must not distract from main value demo

## Demo Scope

Included:
- one KZO demo product / cell / node group
- prepared registry-like input objects
- selected busbar candidate status flow
- node geometry calculation
- fastener selection result
- aggregation into kit_issue_lines
- JSON-style demo output
- explanation for management / director

Excluded:
- live API
- GAS
- Supabase
- Google Sheets
- admin panel
- real warehouse
- procurement
- ERP / 1C
- final BOM release
- pricing
- CAD

## Demo Scenario Candidate

Use a small controlled example:

Product:
KZO demo cell or demo node group

Nodes:
At least 2 busbar nodes, for example:
- KZO_NODE_MAIN_TO_BREAKER_A
- KZO_NODE_MAIN_TO_BREAKER_B

Each node should produce:
- local material line or prepared material line
- local fastener lines
- traceability references

DOC 38 should aggregate repeated fastener lines into kit_issue_lines.

## Required Demo Inputs

Prepared input only.

No DB loading.
No API.
No registry generation.

Input groups:
1. DOC 36 prepared result
2. DOC 37 Slice 01 prepared geometry input
3. DOC 37 Slice 02 prepared fastener registry truth
4. DOC 38 prepared node outputs

## Registry Version Visibility

Demo output must show registry versions used for:
- busbar catalog
- KZO usage registry
- busbar node matrix
- equipment interface registry
- fastener registry
- joint stack rule registry
- washer package rule registry

## Immutable Demo Fixtures

Demo input fixtures are fixed during the run.
No live editing.
No hidden mutation.
No DB/API dependency.

## Expected Demo Output

Demo should be able to show:

1. Status flow:
- DOC 36 = PASS
- DOC 37 Slice 01 = PASS
- DOC 37 Slice 02 = PASS
- DOC 38 Slice 01 = PASS

2. Engineering result:
- busbar node geometry
- joint stack thickness
- selected local fasteners
- aggregated kit_issue_lines

3. Traceability:
Every kit_issue_line must show:
- source_node_ids
- source_line_ids
- traceability_refs

Audit trail sample requirement:
- at least one PASS node must include a compact step-by-step audit trail sample across DOC 36 -> DOC 37 Slice 01 -> DOC 37 Slice 02.

## Demo Explanation For Director

Prepare short explanation:

"System does not guess.
It reads engineering registry truth, validates every step, blocks incomplete data, and only then aggregates verified node lines into a production-preparation kit issue list."

## Management Glossary

- Joint Stack = товщина пакету з’єднання
- Kit Issue = комплект видачі на виробництво
- Registry Truth = затверджений довідник інженерних даних
- Traceability = можливість побачити, з якого вузла прийшла позиція
- Not Final BOM = ще не закупівля і не складське списання

## BOM vs Kit Issue Clarification

DOC 38 output is production-preparation kit issue.
It is not:
- final ERP BOM
- procurement request
- warehouse write-off
- purchase order
- pricing document

## Governance Boundary

This demo is not production deployment.

The demo does NOT authorize:
- final ERP BOM
- warehouse issue
- procurement
- pricing
- API/GAS/DB integration
- admin panel
- broad product expansion

## Success Criteria

Demo is successful if it can show:

1. local engineering logic works end-to-end
2. incomplete or inconsistent data is blocked
3. kit_issue_lines are traceable
4. no final BOM / procurement / warehouse drift exists

## Next After Demo Planning

Allowed next steps after this plan:
- Gemini audit of demo scenario plan
- demo data preparation planning
- demo JSON fixture preparation
- presentation narrative planning

Implementation still requires separate approved task.
