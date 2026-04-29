# Idea Master Log

This file is the single source of truth for all normalized ideas in EDS Power.

## Status Values

- `NEW`
- `ACTIVE`
- `BACKLOG`
- `FUTURE`
- `PARKED`
- `IMPLEMENTED`
- `REJECTED`
- `RENORMALIZED`

## Master Table

| Idea_ID | Date | Raw Idea | Classification | Priority | Decision | Stage Target | Trigger Condition | Key Thesis | Status |
|---|---|---|---|---|---|---|---|---|---|
| IDEA-0001 | 2026-04-29 | Create Idea Normalizer | `IMMEDIATE_CRITICAL` | `P0` | `URGENT_TASK` | System governance | Anti-drift protection required before future idea intake | Create an idea intake firewall before raw ideas can influence implementation | `IMPLEMENTED` |
| IDEA-0002 | 2026-04-29 | Develop Google Sheets Sidebar UI as an interface layer for EDS Power navigation, module access, quick actions, logic, and scenarios without changing core architecture | `NORMAL_BUT_LATER` | `P2` | `BACKLOG` | Post-Google Sheets Core Structure Draft | After stable sheet architecture, module map, and user role logic | Develop Google Sheets Sidebar UI as structured operational control panel for EDS Power modules after core logic is defined | `BACKLOG` |
| IDEA_20260426_001 | 2026-04-29 | Run Stage 3E manual `testKzoPrepareCalculation()` execution to verify GAS -> API handshake on Render | `RIGHT_NOW` | `P1` | `TASK` | Stage 3E | Stage 3D handshake baseline exists and manual log verification is the active gate before any UI expansion | Verify the data pipeline between Google and Render without adding a UI layer | `ACTIVE` |
| IDEA-0003 | 2026-04-29 | Stage 3F Sheet Writeback MVP: Google Sheet -> GAS -> Render API -> basic_result_summary -> fixed test range writeback | `RIGHT_NOW` | `P1` | `TASK` | Stage 3F | Immediately after validated Stage 3E manual API handshake success | Implement minimal visible writeback loop from Render API response into Google Sheets test range | `ACTIVE` |
| IDEA-0004 | 2026-04-29 | Stage 4A Google Sheet Core Template Protection and Structured Input Layer | `RIGHT_NOW` | `P1` | `TASK` | Stage 4A | Immediately after Stage 3F governance sync with VERIFIED_MVP_ONLY / verified writeback baseline | Transform Stage 3F test loop into protected Google Sheet MVP configurator shell with deterministic structure | `IMPLEMENTED` |
| IDEA-0005 | 2026-04-29 | Stage 4B Input Normalization Layer for Google Sheet MVP Shell | `RIGHT_NOW` | `P1` | `TASK` | Stage 4B | After Stage 4A protected shell verified | Convert protected template shell into resilient human-operable MVP shell through deterministic GAS normalization | `IMPLEMENTED` |
| IDEA-0006 | 2026-04-29 | Stage 4C KZO Usable Input Form | `RIGHT_NOW` | `P1` | `TASK` | Stage 4C | Immediately after Stage 4B `VERIFIED_STRUCTURAL_PREFLIGHT` | Stabilize the KZO operator-grade input shell before practical product logic | `IMPLEMENTED` |
| IDEA-0007 | 2026-04-29 | Stage 5A First Practical KZO Logic: Structural Composition and Lineup Meaning Layer | `RIGHT_NOW` | `P1` | `TASK` | Stage 5A | Immediately after Stage 4C `VERIFIED_OPERATOR_SHELL` with frozen input contract | Introduce first structural engineering meaning without crossing into design, BOM, or commercial layers | `IMPLEMENTED` |
| IDEA-0008 | 2026-04-29 | Stage 5A-Output-Integration: Operator-visible structural summary | `RIGHT_NOW` | `P1` | `TASK` | Stage 5A-Output-Integration | After Stage 5A API structural summary verified | Expose existing Stage 5A structural engineering output to operator shell without expanding GAS logic | `IMPLEMENTED` |
| IDEA-0009 | 2026-04-29 | Stage 5B KZO Physical Footprint MVP: API-side lineup scale estimate from structural composition | `RIGHT_NOW` | `P1` | `TASK` | Stage 5B | After Stage 5A structural meaning + operator-visible output integration verified | Rough physical footprint scale from validated structure without CAD/BOM/weight/detail design | `VERIFIED_RENDER_PENDING_OPERATOR_VISIBLE_INTEGRATION` |
| IDEA-0010 | 2026-04-29 | Stage 5C KZO Physical Topology MVP: section distribution and topology type from structural/footprint layers | `RIGHT_NOW` | `P1` | `TASK` | Stage 5C | After Stage 5A structural composition and Stage 5B physical footprint are Render-verified | MVP physical arrangement semantics only — no busbar/cable/detailed engineering | `IMPLEMENTED` |

## Idea Notes

### IDEA-0002 — Google Sheets Sidebar UI

Review stage:

- Re-evaluate after first usable operational spreadsheet framework.

Possible future sidebar blocks:

- Dashboard
- Objects
- Configurator
- Production Transfer
- Kitting
- Supply
- Analytics
- Admin / Rules

Scope guard:

- allowed now: collect UX ideas
- allowed now: mockup/design concepts
- forbidden now: build full production UI architecture
- forbidden now: shift focus away from core system logic

### IDEA_20260426_001 — Stage 3E Manual GAS Execution

Critic audit notes:

- Render free tier may cold-start; first manual request may exceed the normal response window.
- Stage 3E must verify the endpoint path `/api/calc/prepare_calculation`.
- Stage 3E must verify clean execution logs with `logic_version` before any Stage 3F cell-writing work.

Builder scope guard:

- allowed now: manual Apps Script execution of `testKzoPrepareCalculation()`
- allowed now: collect Execution Log output for verification
- forbidden now: create table buttons
- forbidden now: change Google Sheets structure
- forbidden now: add UI, sidebar, or cell-writing behavior

### IDEA-0003 — Stage 3F Sheet Writeback MVP

Review stage:

- Re-evaluate after first successful Sheet writeback.

Minimum output fields:

- `validation_status`
- `object_number`
- `product_type`
- `voltage_class`
- `busbar_current`

Allowed scope:

- reuse existing GAS request
- parse `basic_result_summary`
- write fixed key fields into test cells
- use test sheet only
- preserve logging

Blocked scope:

- Sidebar
- UI polish
- buttons
- Supabase
- AUTH
- BOM
- costing
- production transfer
- multi-sheet architecture

Governance rule:

- no business logic in GAS
- GAS = request / response / writeback only

Success definition:

- user can visibly confirm input -> API -> normalized response -> sheet cells

### IDEA-0004 — Stage 4A Google Sheet Core Template Protection

Review stage:

- After protected template and structured input shell are validated.

Required MVP scope:

- define fixed input zone
- define fixed output zone
- lock cell map
- protect structure cells
- protect formulas/system zones
- allow user edits only in approved input cells
- add dropdown enums where possible
- preserve MVP-safe validation

Input zone candidates:

- `object_number`
- `product_type`
- `logic_version`
- `voltage_class`
- `busbar_current`
- `breaker_type` if MVP-approved

Output zone candidates:

- `validation_status`
- normalized outputs
- `http_code`
- `stage`

Cell map examples:

- `B2` = `object_number`
- `B3` = `product_type`
- `D2` = `validation_status`

GAS rule:

- GAS remains a thin client only
- read fixed cells
- build request
- send API request
- parse response
- write fixed outputs

Forbidden scope:

- Sidebar
- buttons beyond minimal if not essential
- batch
- DB
- Supabase
- multi-product
- advanced UI
- architecture expansion

Required documentation candidates:

- `Stage_4A_Template_Map.md`
- `MVP_Cell_Map.md`
- `Input_Output_Zone_Governance.md`

Success definition:

- protected Sheet exists
- user enters approved KZO inputs
- GAS executes
- API validates
- outputs return safely
- structure remains intact

Scope guard:

- Stage 4A = shell hardening only
- not platform expansion

### IDEA-0005 — Stage 4B Input Normalization Layer

Review stage:

- After stable manual-input resilience is confirmed.

Required MVP scope:

- empty normalization
- required field gate before API call
- enum verification against allowed maps
- safe numeric parsing
- explicit local output errors
- preserve final API validation as source of truth

Empty normalization:

- blank -> `null`
- `N/A` -> `null`
- whitespace trim
- explicit optional vs required distinction

Required field gate:

- missing required fields block local request
- no API call when required fields are missing
- write explicit output zone error

Enum verification:

- Sheet value must match allowed enum map
- mismatch writes local error

Safe numeric parsing:

- trim
- parse integer / float deterministically
- reject malformed values
- no silent coercion

Required local output error codes:

- `INPUT_ERROR_MISSING_REQUIRED`
- `INPUT_ERROR_BAD_ENUM`
- `INPUT_ERROR_BAD_NUMBER`

Required output zone additions:

- `local_input_status`
- `error_code`
- `error_field`

Thin client law:

- allowed: sanitize
- allowed: format
- allowed: structure validate
- allowed: transport
- forbidden: business calculations
- forbidden: engineering logic
- forbidden: product intelligence
- forbidden: hidden rule engine

API law:

- final validation remains API
- GAS = pre-flight safety only

Forbidden scope:

- Sidebar
- Advanced UI
- Batch
- DB
- Supabase
- Product expansion
- Rule creep

Required documentation candidates:

- `Stage_4B_Input_Normalization.md`
- `GAS_Preflight_Governance.md`
- `MVP_Input_Error_Codes.md`

Success definition:

- user enters imperfect manual data
- GAS safely normalizes
- obvious mistakes are blocked locally
- valid payload is sent
- API validates
- stable output is returned

Scope guard:

- Stage 4B = resilience layer only
- not business logic migration

### IDEA-0006 — Stage 4C KZO Usable Input Form

Sequencing role:

- sole current execution gate after Stage 4B

Trigger condition:

- immediately after Stage 4B `VERIFIED_STRUCTURAL_PREFLIGHT`

Required scope:

- KZO only
- operator shell only
- input ergonomics only
- shell maturity gate before product logic

Forbidden scope:

- practical product calculations
- pricing
- BOM
- technical output sheet
- DB
- sidebar
- batch
- architecture expansion

Reason:

- Stage 4B made the shell structurally stable.
- Stage 4C must prove the shell is operator-grade before logic is built on top.
- This prevents input redesign, logic remapping, rework, and shell/logic coupling.

Success definition:

- Stage 4C = `VERIFIED_OPERATOR_SHELL`
- KZO operator shell is stable enough for first practical KZO logic to depend on it

Implementation record:

- `setupStage4COperatorShell()` prepared
- `runStage4CKzoOperatorShellFlow()` prepared
- grouped operator input sections prepared
- protected zone map prepared
- telemetry tag `stage=4C` prepared
- manual setup verification passed at 14:30
- operator flow verification passed at 14:32
- warm run verification passed at 14:34 without cold-start blocker
- final status = `VERIFIED_OPERATOR_SHELL`

Scope guard:

- no practical product logic before shell usability stabilizes

### IDEA-0007 — Stage 5A First Practical KZO Logic

Sequencing role:

- `NEXT_PRIMARY / IMMEDIATE_POST_4C`
- active only after Stage 4C `VERIFIED_OPERATOR_SHELL`

Trigger condition:

- immediately after Stage 4C `VERIFIED_OPERATOR_SHELL` with frozen input contract

Required scope:

- KZO only
- API-side only
- structural engineering normalization only
- lineup structural summary
- cell-type composition summary
- first practical technical meaning
- normalized output expansion only
- deterministic rules only

Narrow execution candidate:

- Configured KZO Structural Composition Summary

Input interpretation:

- total lineup
- voltage class
- busbar current
- cell types and quantities

Allowed first outputs:

- total lineup structure
- cell category breakdown
- functional lineup composition
- first structural flags

Example safe output:

```json
{
  "validation_status": "VALIDATED",
  "product_type": "KZO",
  "lineup_summary": {
    "total_cells": 22,
    "sections": 1,
    "primary_voltage_class": "10kV",
    "busbar_current": "630A"
  },
  "cell_composition": {
    "incoming": 2,
    "outgoing": 16,
    "pt": 2,
    "sectionalizer": 1,
    "bus_riser": 1
  },
  "structural_flags": [
    "dual_incoming",
    "high_outgoing_density",
    "pt_present"
  ]
}
```

Safe first rule types:

- cell count validation
- cell type grouping
- lineup composition logic
- section count
- functional role summary

Forbidden scope:

- pricing
- commercial layer
- BOM explosion
- CAD
- DB
- Supabase
- Sidebar
- GAS logic expansion
- Sheet redesign
- technical documentation packs
- procurement logic
- multi-product
- production transfer
- technical department overbuild
- DB foundation shift

Explicitly forbidden outputs:

- use this breaker
- use this PT truck
- busbar size = X
- price = Y

Reason:

- Stage 4C stabilized the operator shell and froze the input contract.
- Stage 5A can safely move from validation shell to practical structural interpretation.
- The system should answer what the KZO structurally is without entering design, BOM, costing, or commercial layers.

Key governance principle:

- Interpret structure.
- Do not engineer solutions yet.

Scope guard:

- Stage 5A = Structural Composition + Lineup Meaning Layer only.
- Not design logic.
- Not commercial logic.
- Not production logic.

Success condition:

- before Stage 5A: payload is valid
- after Stage 5A: KZO is explained structurally, for example:
  - 22-cell lineup
  - dual incoming
  - 16 outgoing
  - PT-equipped
  - 10kV / 630A structure

Strategic bridge:

- Validation
- Structural Understanding
- later technical logic in future Stage 5B+

Implementation record:

- API-side helper `_build_kzo_structural_composition_summary()` added
- response field `data.structural_composition_summary` added
- local smoke test passed
- live Render pre-deploy check still returns Stage 3C / Stage 4B fields only
- deployment candidate required because Render deploy is GitHub-based
- live Render verification passed after deployment
- no GAS logic expansion
- no Sheet redesign
- no pricing, BOM, DB, commercial, or production logic

### IDEA-0008 — Stage 5A-Output-Integration Operator-Visible Structural Summary

Review stage:

- Completed: operator-visible structural summary confirmed in Sheet (manual Apps Script verification).
Trigger condition:

- after Stage 5A API structural summary verified

Key thesis:

- Expose existing Stage 5A structural engineering output to operator shell without expanding GAS logic.

Reason:

- This is not a new logic layer.
- This is existing Stage 5A value exposure.
- API already performs the engineering logic.
- GAS must only transport and write visible results.
- Without this, Stage 5A remains partially hidden from the operator.

Allowed scope:

- read `structural_composition_summary` from API response
- minimal GAS field mapping
- write summary to defined output zone
- minimal output zone extension if structurally required
- preserve frozen shell architecture where possible
- logging

Forbidden scope:

- new calculations
- structural interpretation in GAS
- API logic duplication
- pricing
- BOM
- dimensions
- weights
- DB
- Supabase
- Sidebar
- layout redesign
- product logic migration

Safe implementation model:

- API returns:
  - `lineup_summary`
  - `cell_composition`
  - `structural_flags`
- GAS reads and writes only.
- Sheet displays:
  - `total_cells`
  - incoming count
  - outgoing count
  - PT count
  - structural flags

Critical governance rule:

- If GAS transforms engineering meaning beyond formatting/writeback, it is a governance breach.
- Allowed: display.
- Forbidden: interpret.

Success condition:

- operator moves from `Payload validated` to `I visibly see KZO structure in Sheet`

Anti-drift law:

- Output visibility does not equal logic expansion.

Narrowest safe execution:

- Stage 5A API output visibility only
- no new logic
- no shell drift
- no GAS breach

Implementation record:

- `runStage5AOutputIntegrationFlow()` verified
- `writeStage5AOutputIntegration_()` verified
- `writeStage5AOutputIntegrationError_()` verified
- output rows verified for:
  - `stage5a_summary_version`
  - `total_cells`
  - `incoming_count`
  - `outgoing_count`
  - `pt_count`
  - `structural_flags`
- manual Sheet verification verified transport/writeback-only behavior

Manual verification record:

- Timestamp: 29.04.2026 15:51-15:52
- Function: `runStage5AOutputIntegrationFlow()`
- Log: HTTP `200`, `stage` = `5A_OUTPUT_INTEGRATION`, `telemetry_tag` = `stage=5A-output-integration`, `structural_summary_present` = `true`
- Writeback: `Stage4A_MVP!E4:F19`, flags `Stage4A_MVP!E20:F20`
- Sheet: `operator_shell_status` = `STAGE_5A_OUTPUT_VISIBLE`; counts visible; `structural_flags` visible

### IDEA-0009 — Stage 5B KZO Physical Footprint MVP

Classification / priority / decision:

- `RIGHT_NOW` / `P1` / `TASK`

Stage target:

- Stage 5B

Trigger condition:

- After Stage 5A structural meaning + operator-visible output integration verified.

Key thesis:

- API-side estimate of lineup physical scale from already validated structural composition (structure → rough physical scale).

Narrow execution candidate:

- `Lineup Physical Footprint Summary` — field `physical_summary` in `prepare_calculation` success payload.

Allowed:

- KZO-only
- API-side only
- estimated lineup width (`estimated_total_width_mm`)
- section count (`section_count`, aligned with structural `lineup_summary.sections`)
- rough footprint class (`footprint_class`, deterministic MVP buckets)
- normalized output with documented MVP assumptions (`basis`, `mvp_standard_cell_width_mm`)
- deterministic MVP assumptions only

Forbidden:

- pricing
- BOM
- weight
- CAD
- procurement
- DB / Supabase
- sidebar
- Sheet redesign
- GAS business logic
- detailed engineering dimensions

Example output shape:

```json
{
  "physical_summary": {
    "summary_version": "KZO_STAGE_5B_PHYSICAL_FOOTPRINT_MVP_V1",
    "estimated_total_width_mm": 17600,
    "section_count": 2,
    "footprint_class": "large_lineup",
    "basis": "total_cells x standard_cell_width_mvp",
    "mvp_standard_cell_width_mm": 800,
    "interpretation_scope": "PHYSICAL_SCALE_ESTIMATE_MVP_ONLY"
  }
}
```

Implementation record:

- `_build_kzo_physical_footprint_summary(structural_composition_summary)` added in `main.py`
- `data.physical_summary` returned on success (derived only from Stage 5A structural summary; no GAS changes)

Render gate:

- Audit record: `docs/AUDITS/2026-04-29_STAGE_5B_PHYSICAL_FOOTPRINT_RENDER_GATE.md`
- Live Render `POST /api/calc/prepare_calculation` checklist: **PASS** (see audit)
- Lifecycle status after live verification: `VERIFIED_RENDER_PENDING_OPERATOR_VISIBLE_INTEGRATION`

### IDEA-0010 — Stage 5C KZO Physical Topology MVP

Classification / priority / decision:

- `RIGHT_NOW` / `P1` / `TASK`

Stage target:

- Stage 5C

Trigger condition:

- After Stage 5A structural composition and Stage 5B physical footprint are Render-verified.

Narrow execution candidate:

- `physical_topology_summary` only — additive field in `prepare_calculation` success payload.

Implementation record:

- `_build_kzo_physical_topology_summary(structural_composition_summary)` in `main.py`
- `data.physical_topology_summary` on success; derived from `lineup_summary.total_cells` and `lineup_summary.sections` (Stage 5A structural); basis text references Stage 5B footprint context in API response only.

Sheet output integration:

- Operator Sheet verification PASS 29.04.2026

Render gate:

- Audit record: `docs/AUDITS/2026-04-29_STAGE_5C_PHYSICAL_TOPOLOGY_RENDER_GATE.md`
- Live Render `POST /api/calc/prepare_calculation` checklist: **PASS** (deploy commit `f8065a3`; attempts 1–2 deployment lag, attempt 3 matched)
- Lifecycle status after live verification: `VERIFIED_RENDER_PENDING_OPERATOR_VISIBLE_INTEGRATION`
