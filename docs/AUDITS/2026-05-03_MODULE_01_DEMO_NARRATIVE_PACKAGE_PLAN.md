# MODULE 01 DEMO NARRATIVE PACKAGE PLAN

## Status

PLANNING ONLY / NO PRESENTATION FILE / NO IMPLEMENTATION

## Purpose

Define the director-facing story for the Module 01 local KZO engineering demo.

The narrative must explain:

- what problem the system solves
- how the local engineering chain works
- why registry truth matters
- how the system prevents engineering mistakes
- how traceability works
- why `kit_issue_lines` are useful for production preparation
- what is still outside MVP scope

## Audience

Primary:

- director / management

Secondary:

- production leadership
- engineering leadership
- technical department
- future implementation stakeholders

## Core Message

Use this core message:

"Система не просто рахує. Вона аргументує кожне інженерне рішення через реєстри, блокує неповні дані і зберігає простежуваність від комплекту видачі назад до конкретного вузла."

## Demo Story Structure

### 1. Problem

Explain current pain points:

- manual engineering decisions are hard to trace
- bolt length / washer package mistakes cause production delays
- local node calculations are often disconnected from kit issue preparation
- final lists may lose connection to source nodes
- engineers spend time checking repeated logic manually

### 2. What We Built

Explain Module 01 local engineering logic:

DOC 36:
safe busbar evaluation

DOC 37 Slice 01:
node geometry and joint stack

DOC 37 Slice 02:
local fastener selection

DOC 38 Slice 01:
basic aggregation into `kit_issue_lines`

### 3. Demo Input

Explain the demo uses:

- two demo KZO nodes
- immutable fixture data
- no live DB
- no API
- no manual editing during run

Node A:

- total length = `1290 mm`

Node B:

- total length = `1200 mm`

Both:

- busbar-side joint stack = `30 mm`
- equipment-side joint stack = `18 mm`

### 4. Engineering Decision Example

Explain bolt selection:

BUSBAR_SIDE:

- required bolt length = `48.5 mm`
- `M12x45` is too short
- `M12x55` is selected

EQUIPMENT_SIDE:

- required bolt length = `36.5 mm`
- `M12x45` is valid
- `M12x45` is selected

Message:
The system does not guess or choose manually.
It compares physical stack requirements against registry-backed fastener data.

### 5. Aggregation Result

Explain DOC 38 output:

Aggregated `kit_issue_lines`:

- `M12x55` bolt = `6 pcs`
- `M12x45` bolt = `6 pcs`
- `M12` nut = `12 pcs`
- `M12` flat washer = `24 pcs`
- `M12` disc spring washer = `12 pcs`

Explain:
These are production-preparation `kit_issue_lines`, not final procurement or warehouse documents.

### 6. Traceability Proof

Explain that every aggregated line keeps:

- `source_node_ids`
- `source_line_ids`
- `traceability_refs`
- `registry_versions`

Director-friendly wording:
"Ми можемо побачити, з якого саме вузла прийшла кожна позиція в комплекті."

### 7. Safety Proof

Explain:

- incomplete data is blocked
- optional backup fixture exists but is not part of main demo
- if phase length is missing, system returns `INCOMPLETE / PHASE_LENGTH_MISSING`

This is a backup talking point only, not the main demo flow.

### 8. What This Is Not

Explicitly state:
This is not:

- final ERP BOM
- warehouse write-off
- purchase request
- supplier selection
- pricing
- CAD validation
- production order release
- API/GAS/DB integration

This is:

- verified local engineering logic
- production-preparation `kit_issue_lines` logic
- proof of deterministic calculation chain

### 9. Business Value

Explain benefits:

- fewer repeated manual checks
- fewer errors in fastener length and quantity
- better preparation for production
- traceability from kit issue to engineering node
- safer future integration with database / ERP / production workflows
- clear separation between engineering logic and external systems

### 10. Next Step Proposal

Recommend next stage after demo:

Option A:
prepare MVP registry data expansion

Option B:
plan API/GAS integration for controlled demo UI

Option C:
plan DOC 38 Slice 02 / production issue extension

Recommended:
Start with Demo UI / API-GAS planning only after management approves the local logic value.

## Demo Script Outline

Create a simple 5-10 minute sequence:

1. Show problem.
2. Show two nodes.
3. Run local demo.
4. Show bolt decision.
5. Show `kit_issue_lines`.
6. Show traceability.
7. Explain boundaries.
8. Ask for next-stage approval.

## Required Demo Artifacts To Prepare Later

This plan may reference future artifacts, but must not create them now:

- one-page executive summary
- demo output screenshot / JSON view
- short slide deck
- management glossary
- Q&A list
- "what this is not" boundary slide

## Data Ownership Note

Registry Truth means approved engineering reference data.

For MVP:

- registry data ownership belongs to responsible engineering authority
- recommended owner: Chief Designer / Engineering Department / Technology Owner
- registry changes must be controlled and reviewed
- engineering values must not be changed through hidden code logic
- registry changes must be traceable through versioning and changelog

Director-facing wording:

"Система не вигадує інженерні значення. Вона використовує затверджені довідники. Відповідальність за актуальність цих довідників має бути закріплена за відповідальним інженерним власником — наприклад, головним конструктором, технічним відділом або призначеним власником реєстру."

## Gemini Audit Status

- Final verdict: `PASS`.
- Required Data Ownership Note: added.
- Narrative plan approved for next-stage presentation artifact preparation.
- No implementation performed.
- No slides created.
- No API/GAS/DB/procurement/warehouse/ERP/pricing/CAD actions.

## Governance Boundary

This planning document does not authorize:

- creating slides
- changing code
- changing fixtures
- changing tests
- API/GAS/DB integration
- ERP/procurement/warehouse integration
- production use
- final BOM release

Future narrative artifacts require separate task.
