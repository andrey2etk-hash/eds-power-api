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

Operative **sub-state** strings (such as **`PENDING_SUPABASE_VERIFICATION`**) appear only in Idea Notes until a live gate PASS; they are **not** additional master **`Status`** column tokens unless formally added here.

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
| IDEA-0011 | 2026-04-29 | Stage 5D KZO Operator Layout Governance MVP: fixed stage shell zones and vertical expansion before Stage 6 | `RIGHT_NOW` | `P1` | `TASK` | Stage 5D | After Stage 5C operator Sheet topology writeback verified | Governed operator shell — one stage block — additive downward growth — no redesign | `IMPLEMENTED` |
| IDEA-0012 | 2026-04-29 | Stage 6A KZO Reserved Operator Block Activation: activate E27:F40 as governed shell infra before Stage 6 engineering | `RIGHT_NOW` | `P1` | `TASK` | Stage 6A | After Stage 5D shell governance MVP implemented | Activate reserved shell block only — no engineering formulas,BOM,Business logic — not API topology | `IMPLEMENTED` |
| IDEA-0013 | 2026-04-29 | Stage 6B KZO Engineering Classification MVP: lineup scale/complexity classification from structure and topology | `RIGHT_NOW` | `P1` | `TASK` | Stage 6B | After Stage 6A operator shell block verified | Planning-grade engineering class only — no mass, BOM, price, CAD | `IMPLEMENTED` |
| IDEA-0014 | 2026-04-29 | Stage 6C KZO Engineering Burden Foundation MVP: planning-grade production burden from classification + topology (not kg/BOM/price) | `RIGHT_NOW` | `P1` | `TASK` | Stage 6C | After Stage 6B closed with Gemini SAFE TO PROCEED TO STAGE 6C | Planning burden before precision — burden tiers only — no BOM/CAD procurement | `IMPLEMENTED` |
| IDEA-0015 | 2026-04-29 | Stage 7A KZO end-to-end MVP stabilization: unified operator-grade flow (single API call + orchestrated Sheet writeback) | `IMMEDIATE_CRITICAL` | `P0` | `URGENT_TASK` | Stage 7A | After Stage 6C operator-visible **`IMPLEMENTED`** closes layered stack | **Stabilize before deepen** — one scenario (5A+5C+6B/6C layers) — no BOM/DB/pricing/new API math until MVP cohesion validated | `IMPLEMENTED` |
| IDEA-0016 | 2026-04-29 | Stage 7B KZO MVP snapshot contract freeze: canonical `KZO_MVP_SNAPSHOT_V1` before persistence | `IMMEDIATE_CRITICAL` | `P0` | `URGENT_TASK` | Stage 7B | After **IDEA-0015** `IMPLEMENTED` (7A operational PASS) | **Freeze before persistence** — one trusted object for Stage 8A — no Supabase/SQL in 7B | `IMPLEMENTED` |
| IDEA-0017 | 2026-04-29 | Stage 8A Supabase first persistence MVP: insert-only `calculation_snapshots` (`product_type` KZO), `POST /api/kzo/save_snapshot` | `RIGHT_NOW` | `P1` | `TASK` | Stage 8A | After **IDEA-0016** `IMPLEMENTED`; **IDEA-0018**/**IDEA-0019**/`IDEA-0020`/`IDEA-0022` **`IMPLEMENTED`**; **live** gate **PASS** recorded | **Persist frozen truth** — one row per snapshot; **`STAGE_8A_COMPLETE`** | `IMPLEMENTED` |
| IDEA-0018 | 2026-04-29 | Stage 8A.0 EDS Power Supabase root governance foundation — central DB memory, not KZO-root architecture | `IMMEDIATE_CRITICAL` | `P0` | `URGENT_TASK` | Stage 8A.0 | Before expanding live persistence footprint beyond ad-hoc module naming | Folder + naming + migration registry rules — **docs only** — no ERP/BOM/analytics DDL | `IMPLEMENTED` |
| IDEA-0019 | 2026-04-29 | Stage 8A.0.1 Root migration naming correction — `calculation_snapshots` replaces KZO-biased table name (`TABLE=SYSTEM`, `ROW=PRODUCT`) | `IMMEDIATE_CRITICAL` | `P0` | `URGENT_TASK` | Stage 8A.0.1 | After **IDEA-0018** (**8A.0**); **before** first live push using root governance | Canonical migration + archive superseded DDL; **`KZO_MVP_SNAPSHOT_V1`** unchanged | `IMPLEMENTED` |
| IDEA-0020 | 2026-04-29 | Stage 8A.0.2 Supabase remote baseline alignment — legacy remote `public` (`legacy_baseline`); **`calculation_snapshots` DDL** ordered after baseline import | `IMMEDIATE_CRITICAL` | `P0` | `URGENT_TASK` | Stage 8A.0.2 | Declared non-empty **`public`** (objects, bom_links, ncr, production_status, **`v_*`**) | **`LEGACY_REMOTE_BASELINE.md`** + **`_pending_after_remote_baseline/`** hold pattern — zero destructive DB action in TASK | `IMPLEMENTED` |
| IDEA-0021 | 2026-04-29 | Role-adaptive operational shell doctrine (“self-checkout principle”): guided role-specific UI above, system truth / ERP / DB underneath | `NORMAL_LONG_TERM` | `P3` | `FUTURE` | Post–core platform architecture / multi-module UX doctrine | After stable CALC + persistence + first operational modules | One truth layer below; many governed operational shells above — users do not operate core accounting/ERP unless role requires it | `FUTURE` |
| IDEA-0022 | 2026-04-29 | Stage 8A.0.3 Supabase remote baseline capture — authoritative migration slot ordering before `calculation_snapshots`; schema-only DDL from remote (no prod `db push`) | `IMMEDIATE_CRITICAL` | `P0` | `URGENT_TASK` | Stage 8A.0.3 → **8A.1** | After **IDEA-0020** **`IMPLEMENTED`**; local replay + promotion per **8A.0.8** / **8A.1** | **`20260429110000`** \< **`20260429120000_calculation_snapshots_v1`**; verified **`supabase db reset`** non-prod | `IMPLEMENTED` |
| IDEA-0023 | 2026-04-30 | Stage 8B Client-Agnostic Persistence Flow — platform persistence architecture (not GAS orchestration) | `RIGHT_NOW` | `P1` | `TASK` | Stage 8B | After **`IDEA-0017`** **`IMPLEMENTED`** / **`STAGE_8A_COMPLETE`**; **before** web/mobile/portals/multi-client UX expansion without this freeze | **Client ≠ core; API = orchestrator; Supabase = memory** — identical persistence path from any adapter | `ACTIVE` |

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

### IDEA-0011 — Stage 5D KZO Operator Layout Governance MVP

Classification / priority / decision:

- `RIGHT_NOW` / `P1` / `TASK`

Stage target:

- Stage 5D

Trigger condition:

- After Stage 5C API and operator-visible Sheet topology thin writeback verified.

Key thesis:

- Sheet = governed operator shell; GAS = transport only; API = engineering truth. Fix stage blocks and reserved rows before Stage 6 to protect operational readability.

Governance record:

- `docs/00-02_CALC_CONFIGURATOR/09_KZO/10_OPERATOR_LAYOUT.md`
- Audit: `docs/AUDITS/2026-04-29_STAGE_5D_OPERATOR_LAYOUT_GOVERNANCE.md`
- MVP shell: `SHELL_VERTICAL_EXPANSION` — active `E4:F20` (5A structure band), `E21:F26` (5C topology); reserved `E27:F40` (Stage 6), `E41:F54` (Stage 7)
- This MVP wave: **documentation only** — no API payload, no new GAS surfaces (reference JSON for future `operator_layout_governance_summary` when tasked)
- **Accepted:** Stage 5D Operator Layout Governance MVP after **PASS WITH DOC FIXES** (governance verification gate + `basis` field alignment in `10_OPERATOR_LAYOUT.md`; doc-pass 29.04.2026)

### IDEA-0012 — Stage 6A KZO Reserved Operator Block Activation MVP

Classification / priority / decision:

- `RIGHT_NOW` / `P1` / `TASK`

Stage target:

- Stage 6A

Trigger condition:

- After Stage 5D operator shell governance documentation MVP (**IDEA-0011** `IMPLEMENTED`).

Key thesis:

- **Reserved ≠ operational** until shell activation: GAS-only constants, placeholder writeback to **`E27:F40`**, reset for block only, telemetry — **no** API `stage6_operator_shell_summary`, **no** engineering layer (Stage 6B+ only after verification).

Implementation record:

- `gas/Stage3D_KZO_Handshake.gs`: `STAGE_6A_RESERVED_OPERATOR_BLOCK_RANGE_A1` = `E27:F40`, `STAGE_6A_BLOCK_NAME`, `STAGE_6A_SHELL_BLOCK_VERSION`, `runStage6AActivateReservedOperatorBlockFlow()`, `runStage6AResetReservedOperatorBlockOnly()`, `buildStage6OperatorShellSummary_()` (logged shape matches target JSON; not an API field in 6A)
- Audit: `docs/AUDITS/2026-04-29_STAGE_6A_RESERVED_BLOCK_ACTIVATION.md`
- Operator verification **PASS 29.04.2026** — **`E27:F40`** activation and reset behavior verified; **`shell_block_version`** **`KZO_STAGE_6A_OPERATOR_SHELL_V1`**; **`shell_status`** activation **`ACTIVE_RESERVED_BLOCK`** / reset log **`RESERVED_DOC_ONLY`**; telemetry includes **`stage6_operator_shell_summary`**. (**`ACTIVE_RESERVED_BLOCK`** / **`RESERVED_DOC_ONLY`** are shell block states, not IDEA **Status Values**.)

### IDEA-0013 — Stage 6B KZO Engineering Classification MVP

Classification / priority / decision:

- `RIGHT_NOW` / `P1` / `TASK`

Stage target:

- Stage 6B

Trigger condition:

- After Stage 6A reserved operator shell block operator-verified.

Key thesis:

- **Classification before precision**: API derives **`engineering_class_summary`** from structural + topology summaries only — planning labels (scale / complexity tier / per-section profile), **no** kg, BOM, thermal, CAD, procurement.

Implementation record:

- `main.py`: `_build_kzo_engineering_class_summary()` → `data.engineering_class_summary` on success
- `gas/Stage3D_KZO_Handshake.gs`: `runStage6BEngineeringClassificationFlow()`, writeback **`E27:F40`** only (Stage 6 band; overwrites Stage 6A placeholder when Stage 6B flow runs — thin transport, no classification math in GAS)
- Audit: `docs/AUDITS/2026-04-29_STAGE_6B_ENGINEERING_CLASSIFICATION.md`
- **Operator verification PASS** — API **`http_code` 200**, **`engineering_class_summary_present`**, GAS **`writeback_completed`** on **`E27:F40`** (14-row block; no **`request_or_writeback_failed`**); thin client preserved; no BOM/pricing/mass/DB/Supabase. Closure: Stage 6B = **`IMPLEMENTED`** + **operator-verified** (**`IMPLEMENTED`** stays the only IDEA **Status** token in master table).
- **Stage 6B Engineering Classification MVP closed** after **external Gemini PASS** (**`SAFE TO PROCEED TO STAGE 6C`**) + **operator verification PASS** **29.04.2026** — doc-pass + governance sync only; **Stage 6C** (**IDEA-0014**) delivered afterward; cohesion gate **Stage 7A** (**IDEA-0015**) tracks unified MVP operator flow (no new **Status Values** for closure-only notes).

### IDEA-0014 — Stage 6C KZO Engineering Burden Foundation MVP

Classification / priority / decision:

- `RIGHT_NOW` / `P1` / `TASK`

Stage target:

- Stage 6C

Trigger condition:

- After Stage 6B closure and **`SAFE TO PROCEED TO STAGE 6C`** governance gate.

Key thesis:

- **Planning burden before precision burden** — **`engineering_burden_summary`** from 6B + topology + structural flags only; **`estimated_mass_class`** = burden tier, **not** kg.

Implementation record:

- `main.py`: `_build_kzo_engineering_burden_summary()` → `data.engineering_burden_summary` on success
- `gas/Stage3D_KZO_Handshake.gs`: `runStage6CEngineeringBurdenFlow()`, writeback **`E27:F40`** only (thin transport; overwrites Stage 6 band when 6C runs)
- Audit MVP: `docs/AUDITS/2026-04-29_STAGE_6C_ENGINEERING_BURDEN_FOUNDATION.md`
- **Live Render PASS** (**29.04.2026**) — deploy **`35ac23a`**; probe **`POST`** `prepare_calculation`; attempts **1–2** через deployment lag — **attempt 3**: **`engineering_burden_summary`** присутній (`docs/AUDITS/2026-04-29_STAGE_6C_ENGINEERING_BURDEN_RENDER_GATE.md`)
- **Operator Sheet verification PASS** (**29.04.2026**) — **`runStage6CEngineeringBurdenFlow()`**, **`Stage4A_MVP`**, **`http_code` 200**, **`engineering_burden_summary_present`**, **`writeback_completed`** → **`E27:F40`**; thin GAS; scope preserved (нема kg/BOM/pricing як у gate)
- Master table **Status**: **`IMPLEMENTED`** (interim label **`RENDER_VERIFIED_PENDING_OPERATOR_TEST`** знято док-пасом після operator-visible PASS)

### IDEA-0015 — Stage 7A KZO end-to-end MVP stabilization

Classification / priority / decision:

- `IMMEDIATE_CRITICAL` / `P0` / `URGENT_TASK`

Stage target:

- Stage 7A

Trigger condition:

- After **IDEA-0014** `IMPLEMENTED` (**Stage 6C** layered output proven); before **Stage 7B+** depth expansion — **architecture stabilization gate** (“MVP cohesion before expansion”).

Key thesis:

- **Validated layers → unified flow → operational MVP.** One operator entry (**`runKzoMvpFlow()`**): single **`prepare_calculation`** POST → writeback orchestration only — Structure (**5A**), Physical scale (**`data.physical_summary`** telemetry / API-only block), Topology (**5C**), Classification + Burden (**unified `E27:F40`** — stacked 6B+6C fields in **one** `setValues`, no duplicate per-stage reruns).

Implementation record:

- `gas/Stage3D_KZO_Handshake.gs`: **`runKzoMvpFlow()`**, **`writeStage7AUnifiedStage6Band_()`** — reuses **`writeStage5AOutputIntegration_`**, **`writeStage5CSheetOutputIntegration_`**; telemetry **`mvp_run_outcome`**: **`MVP_RUN_SUCCESS`** / **`MVP_RUN_FAILED`**; **`telemetry_tag`**: **`stage=7a-kzo-mvp-flow`**
- Forbidden: new parameters/calcs, BOM, pricing, DB, Supabase; no new **`E41:F54`** writes
- Audit (cohesion): `docs/AUDITS/2026-04-29_STAGE_7A_KZO_END_TO_END_MVP_STABILIZATION.md`
- **Operator verification PASS** (manual Apps Script) — API **`success`**, **`http_code`** **200**, **`mvp_run_outcome`** **`MVP_RUN_SUCCESS`**; **`Stage4A_MVP`** zones **`E4:F19`** / **`E20:F20`**, **`E21:F26`**, **`E27:F40`**; **`structural_composition_summary`**, **`physical_summary`**, **`physical_topology_summary`**, **`engineering_class_summary`**, **`engineering_burden_summary`** present in **`data`**; thin GAS transport/orchestration only (**doc-pass**).
- Master table **Status**: **`IMPLEMENTED`** (unchanged **`Status Values`**).

### IDEA-0016 — Stage 7B KZO MVP snapshot contract freeze

Classification / priority / decision:

- `IMMEDIATE_CRITICAL` / `P0` / `URGENT_TASK`

Stage target:

- Stage 7B

Trigger condition:

- After **IDEA-0015** `IMPLEMENTED` (**Stage 7A** unified run operator-verified); **before** **Stage 8A** Supabase (or any DB) persistence.

Key thesis:

- **Working MVP → persistable system object.** Single canonical **`KZO_MVP_SNAPSHOT_V1`**: **`snapshot_version`**, **`run_status`**, **`timestamp_basis`**, **`logic_version`**, **`request_metadata`**, **`normalized_input`**, plus **all** current validated output layers (**`structural_composition_summary`**, **`physical_summary`**, **`physical_topology_summary`**, **`engineering_class_summary`**, **`engineering_burden_summary`**) — API key names preserved (no alias drift).

Implementation record:

- Normative contract: `docs/00-02_CALC_CONFIGURATOR/09_KZO/11_KZO_MVP_SNAPSHOT_V1_CONTRACT.md` — versioning policy; **`SUCCESS`** / **`FAILED`** envelope; explicit **non-inclusion** of BOM/pricing/DB IDs in V1
- Audit: `docs/AUDITS/2026-04-29_STAGE_7B_KZO_MVP_SNAPSHOT_CONTRACT_FREEZE.md` (**freeze before persistence**)
- Forbidden in Stage 7B: Supabase tables, SQL, DB deployment, new engineering fields beyond validated MVP layers
- Master table **Status**: **`IMPLEMENTED`** (documentation contract only; **Stage 8A** references this object as persistence source)
- **Formal closure (Gemini doc-pass):** Stage **7B** **CLOSED** after external Gemini **`SAFE TO PROCEED TO STAGE 8A`** — **`KZO_MVP_SNAPSHOT_V1`** remains **frozen** as sole persistence-shape baseline (**no V1 contract edits** outside a new snapshot version + IDEA). Controlled persistence implementation tracked as **IDEA-0017**.

### IDEA-0017 — Stage 8A Supabase first persistence MVP

Classification / priority / decision:

- `RIGHT_NOW` / `P1` / `TASK`

Stage target:

- Stage **8A** (first persistence under root DB governance) — **`STAGE_8A_COMPLETE`**

Trigger condition:

- After **IDEA-0016** `IMPLEMENTED` (**`KZO_MVP_SNAPSHOT_V1`** frozen).
- After **IDEA-0018** **`IMPLEMENTED`** (Supabase central-memory governance — **non-KZO-root** naming and registry discipline).
- After **IDEA-0022** **`IMPLEMENTED`** (repo migration **`110000`** → **`120000`** verified non-prod — **8A.1**).

Key thesis:

- **Persist frozen truth.** System table **`calculation_snapshots`**, **`product_type`** **`KZO`** at insert, insert-only, JSONB contract columns; **`prepare_calculation`** unchanged; **`POST /api/kzo/save_snapshot`** validates V1 + INSERT only.

Implementation record:

- `kzo_snapshot_persist.py` — **`validate_kzo_mvp_snapshot_v1`**, **`insert_snapshot_row`** (Supabase REST; env **`SUPABASE_URL`**, **`SUPABASE_SERVICE_ROLE_KEY`**)
- `main.py` — **`POST /api/kzo/save_snapshot`**
- `supabase/migrations/20260429120000_calculation_snapshots_v1.sql` — **active** (**Stage 8A.1** promotion; audit **`docs/AUDITS/2026-04-30_STAGE_8A_1_CALCULATION_SNAPSHOTS_PROMOTION_TEST.md`** — **`FIRST_PERSISTENCE_READY_NON_PROD`**); **`_pending_after_remote_baseline/`** reserved for future holds — registered **`schema_registry/REGISTRY_INDEX.md`** (**IDEA-0019** naming); superseded DDL **`migrations/_archive_pre_8a0_1_kzo_tables/`**
- Root DB topology (not KZO-as-root): **`supabase/README.md`**, **`schema_registry/`**, **`domains/`**
- Mapping: `docs/00-02_CALC_CONFIGURATOR/09_KZO/13_KZO_MVP_SNAPSHOT_V1_SQL_MAPPING.md`
- Governance: `docs/00-02_CALC_CONFIGURATOR/09_KZO/14_CALC_TRUTH_VS_PERSISTENCE_STAGE_8A.md`
- Audit: `docs/AUDITS/2026-04-29_STAGE_8A_SUPABASE_FIRST_PERSISTENCE_MVP.md`
- Live verification gate: `docs/AUDITS/2026-04-29_STAGE_8A_SUPABASE_LIVE_VERIFICATION_GATE.md` — **LIVE PASS** (**2026-04-30**); closeout dossier **`docs/AUDITS/2026-04-30_STAGE_8A_2_1_LIVE_DEPLOY_CALCULATION_SNAPSHOTS.md`** (**`STAGE_8A_COMPLETE`**)
- Forbidden: BOM, pricing, retrieval APIs, dashboards, **`prepare_calculation`** mutations, contract field inflation without V2
- Thin GAS **`saveKzoSnapshotV1()`** — transport only
- Master table **Status**: **`IMPLEMENTED`** (**2026-04-30**)

**Recommended next operational slice (post–IDEA-0017, under IDEA-0023):** **`TASK-2026-08B-012`** (**Stage 8B.1A**) — canonical **`save_snapshot`** contract hardening on the **API** first; then **`TASK-2026-08B-011`** (**Stage 8B.1B**) — thin **GAS** transport (**`prepare_calculation`** → **`KZO_MVP_SNAPSHOT_V1`** envelope → **`saveKzoSnapshotV1()`** / **`save_snapshot`**), **without** retrieval/history/analytics expansion. Gemini preflight (**`docs/AUDITS/2026-04-30_STAGE_8B_1_GEMINI_PREFLIGHT_REQUEST.md`**) reinforces **API-first** order — **no** “GAS as orchestrator” wording.

### IDEA-0018 — Stage 8A.0 EDS Power Supabase root governance foundation

Classification / priority / decision:

- `IMMEDIATE_CRITICAL` / `P0` / `URGENT_TASK`

Stage target:

- Stage **8A.0**

Trigger condition:

- Required **before** assuming Supabase DDL is scoped only to **KZO**; aligns **`00_SYSTEM`** principle that DB is **system memory**, gated by maturity and frozen contracts (**7B** freeze precedes persistence).

Key thesis:

- **Prevent KZO-centric database architecture.** Supabase = central memory; **KZO** = first validated **consumer** of **`snapshots`**; general tables eschew product-coded names without **`product_type`** / domain rules.

Implementation record (documentation + folder scaffolding **only** — **no new migration** authored under **8A.0** for governance):

- `supabase/README.md` — global rules; **8A.0** vs **8A.1** gates
- `supabase/migrations/README.md` — migration discipline; cites existing DDL
- `supabase/schema_registry/README.md`, `supabase/schema_registry/LEGACY_REMOTE_BASELINE.md`, `supabase/schema_registry/REGISTRY_INDEX.md` — **`calculation_snapshots`** (**8A.0.1**); **`LEGACY_REMOTE_SCHEMA_DETECTED`** (**8A.0.2**); superseded **`kzo_mvp_snapshots_v1`** draft documented in **`migrations/_archive_pre_8a0_1_kzo_tables/`**
- `supabase/domains/README.md` — domain map + **`product_type`** discriminator
- Stub domains: `auth/`, `users/`, `roles/`, `products/`, `calculations/`, `snapshots/`, `production/`, `supply/`, `employee_skills/`, `analytics/` — placeholders only
- Forbidden in **8A.0**: live migration execution mandate, ERP schema, BOM/pricing/analytics DDL, auth expansion

Master table **Status**: **`IMPLEMENTED`**

### IDEA-0019 — Stage 8A.0.1 Root migration governance correction

Classification / priority / decision:

- `IMMEDIATE_CRITICAL` / `P0` / `URGENT_TASK`

Stage target:

- Stage **8A.0.1**

Key thesis:

- **`TABLE = SYSTEM`**, **`ROW = PRODUCT`**. Replace KZO-biased root name with **`public.calculation_snapshots`** and **`product_type = 'KZO'`**. **`KZO_MVP_SNAPSHOT_V1`** remains the contract id (Stage **7B**).

Implementation record:

- `supabase/migrations/_pending_after_remote_baseline/20260429120000_calculation_snapshots_v1.sql`
- `supabase/migrations/_archive_pre_8a0_1_kzo_tables/` — superseded draft DDL
- `docs/AUDITS/2026-04-29_STAGE_8A_0_1_ROOT_MIGRATION_GOVERNANCE_CORRECTION.md`
- `kzo_snapshot_persist.py` — **`product_type`** on INSERT

Master table **Status**: **`IMPLEMENTED`**

### IDEA-0020 — Stage 8A.0.2 Supabase remote baseline alignment

Classification / priority / decision:

- `IMMEDIATE_CRITICAL` / `P0` / `URGENT_TASK`

Stage target:

- Stage **8A.0.2**

Key thesis:

- Non-empty **`public`** on Supabase (**`LEGACY_REMOTE_SCHEMA_DETECTED`**). **`calculation_snapshots`** DDL **held** (**`_pending_after_remote_baseline/`**) until authoritative **baseline** migrations precede **`db push`**. No destructive DDL in this IDEA.

Implementation record (**docs + hold**; **no** live DB / **no **`db push`**):

- **`supabase/schema_registry/LEGACY_REMOTE_BASELINE.md`**
- **`supabase/migrations/_pending_after_remote_baseline/`** + root **`migrations/README.md`** update
- **`docs/AUDITS/2026-04-29_STAGE_8A_0_2_SUPABASE_REMOTE_BASELINE_ALIGNMENT.md`**

Master table **Status**: **`IMPLEMENTED`**

### IDEA-0022 — Stage **8A.0.3** Remote baseline capture (ordering + operator DDL paste)

Stage target:

- Stage **8A.0.3** (**capture-only**)

Key thesis:

- Repo migration ordering must **trail** authoritative remote legacy **`public`**: **`20260429110000_remote_legacy_baseline.sql`** strictly **before** **`20260429120000_calculation_snapshots_v1.sql`** (canonical DDL; **promoted** in **8A.1**).

Strict:

- **No** **`db push`** / apply to prod inside baseline capture TASK framing; local/disposable **`supabase db reset`** for verification.
- Factual DDL is committed from **`remote_schema.sql`** only — **never** fabricated in repo.

Freeze:

- **`LEGACY_REMOTE_BASELINE.md`** — no Dashboard DDL on listed legacy **`public`** during capture window.

Closure:

- **8A.0.6:** **`REAL_BASELINE_CAPTURED_PENDING_REPLAY`** — merged **`remote_schema.sql`** → **`20260429110000_remote_legacy_baseline.sql`**
- **8A.0.7:** **`BLOCKED_BY_DOCKER`** in agent session (**2026-04-29** audit) — superseded once operator tooling enabled
- **8A.0.8 (**`2026-04-30`**):** **`CURSOR_LOCAL_STACK_VERIFIED`**
- **8A.1 (**`2026-04-30`**):** **`FIRST_PERSISTENCE_READY_NON_PROD`** — DDL under **`supabase/migrations/`** + **`supabase db reset`** PASS

Operative (**cleared**):

- ~~**`PENDING_STAGING_REPLAY_804`**~~ — satisfied by verified local **`db reset`** + **8A.1** dossier.

Artifacts:

- **`supabase/migrations/20260429110000_remote_legacy_baseline.sql`**
- **`supabase/migrations/20260429120000_calculation_snapshots_v1.sql`**
- **`docs/AUDITS/2026-04-29_STAGE_8A_0_3_REMOTE_BASELINE_CAPTURE.md`**
- **`docs/AUDITS/2026-04-29_STAGE_8A_0_4_BASELINE_REPLAY_TEST.md`**
- **`docs/AUDITS/2026-04-29_STAGE_8A_0_5_LOCAL_TOOLING_PRECHECK.md`**
- **`docs/AUDITS/2026-04-29_STAGE_8A_0_6_ACTUAL_REMOTE_BASELINE_CAPTURE.md`**
- **`docs/AUDITS/2026-04-29_STAGE_8A_0_7_BASELINE_REPLAY_VERIFICATION.md`**
- **`docs/AUDITS/2026-04-30_STAGE_8A_0_8_CURSOR_LOCAL_CONNECTIVITY.md`**
- **`docs/AUDITS/2026-04-30_STAGE_8A_1_CALCULATION_SNAPSHOTS_PROMOTION_TEST.md`**

Master table **Status**: **`IMPLEMENTED`** (**2026-04-30** — non-prod promotion test closes ordering + replay chain)

### IDEA-0023 — Stage **8B** Client-Agnostic Persistence Flow Governance

**ID note:** Draft text suggested **`IDEA-0022`** — conflicts with **`IDEA-0022`** (baseline capture). Assigned **`IDEA-0023`**.

**One-line strategy:** Persistence is **saved by platform architecture**, not by “GAS persistence”.

**Core law:**

- **Client ≠ system core.**
- **API = orchestrator** (calc truth, snapshot validation, envelope, persistence calls).
- **Supabase = memory** (immutable rows; no orchestration engineering).

---

#### CURSOR TASK: **STAGE 8B** — CLIENT-AGNOSTIC PERSISTENCE FLOW GOVERNANCE
→ Tracked as **`TASK-2026-08B-001`** in **`docs/TASKS.md`**.

##### STEP 1 — Canonical persistence flow

```text
Any Client
  → POST /api/calc/prepare_calculation (calculation truth)
  → verified snapshot object (e.g. KZO_MVP_SNAPSHOT_V1 envelope)
  → POST /api/kzo/save_snapshot
  → snapshot_id + persistence response
```

No alternative “write path” for production snapshot rows.

##### STEP 2 — Client role (GAS / Web / Mobile / Agents / future)

**Allowed**

- Call API only.
- Send normalized payloads; display API + persistence outcomes.
- Surface **`snapshot_id`**, **`persistence_status`**, **`failure`** / error codes.

**Forbidden**

- Direct Supabase / DB writes from clients.
- Client-owned persistence semantics (“saved in Sheet” as system truth).
- Client-side business or engineering logic (beyond pre-flight **form** checks per **`02_GLOBAL_RULES`**).
- Mutating **`KZO_MVP_SNAPSHOT_V1`** outside API-owned versioning policy.
- **GAS-only** orchestration dependency (GAS **must not** become the implicit system brain).
- Sheet-first architecture bias (Sheet displays; API decides).

##### STEP 3 — API role (owns)

- Calculation truth (**`prepare_calculation`** lineage).
- Snapshot validation (**`validate_kzo_mvp_snapshot_v1`**).
- Persistence contract (**`save_snapshot`**).
- Unified response envelopes.
- Sole Supabase **`calculation_snapshots`** interaction for MVP path.

##### STEP 4 — Supabase role

- Storage of snapshot rows **only** (immutable insert policy as per Stage 8A).
- No client logic; no recomputation / BOM / pricing orchestration.

##### STEP 5 — Canonical **`save_snapshot` response** (CLIENT_AGNOSTIC_PERSISTENCE_CONTRACT_V1)

Required fields (**document + converge implementation**): **`status`**, **`snapshot_id`**, **`persistence_status`**, **`snapshot_version`**, **`created_at`**, **`failure`** (or equivalent structured error on reject path).
Current API may require additive fields in a sub-TASK — contract is **normative target**.

##### STEP 6 — Document

- **`docs/00_SYSTEM/13_CLIENT_AGNOSTIC_PERSISTENCE_CONTRACT_V1.md`** — normative contract.

##### STEP 7 — GAS rule

- **Thin Client Adapter V1** only: transport + display; **no** orchestration core.

##### STEP 8 — Audit

- **`docs/AUDITS/YYYY-MM-DD_STAGE_8B_PLATFORM_PERSISTENCE_NOT_GAS_PERSISTENCE.md`** — “Platform persistence, not GAS persistence”.

##### Sequencing (Stage **8B.1** split — **`STAGE_8B_DOC_STATE_ALIGNED`**)

1. **`TASK-2026-08B-012`** — **8B.1A** **`save_snapshot`** API contract hardening (validation / response / anti-orchestration leak) — plan **`docs/AUDITS/2026-04-30_STAGE_8B_1A_API_SAVE_CONTRACT_GOVERNANCE_PLAN.md`**.
2. **`TASK-2026-08B-011`** — **8B.1B** Thin GAS adapter (**blocked** until **8B.1A** implementation exit).

Gemini critic preflight (**`docs/AUDITS/2026-04-30_STAGE_8B_1_GEMINI_PREFLIGHT_REQUEST.md`**) audits the **thin-GAS plan** **before** coding and aligns stakeholders on **API-first** reinforcement.

##### FORBIDDEN (Stage 8B scope guard)

- GAS as orchestration core; Sheet as permanent truth; direct DB from clients; web/mobile divergence in persistence path; BOM; pricing; production transfer; analytics; auth overexpansion.

##### SUCCESS

After **8B**: Google Sheets, Web, Mobile, Agents, and future clients use the **same** API persistence pathway end-to-end.

##### ANTI-DRIFT

No client may redefine system persistence without **IDEA → TASK** and contract version bump.

**Implementation record (when started):**

- TASK: **`docs/TASKS.md`** — **`TASK-2026-08B-001`** (master); **`TASK-2026-08B-012`** (**8B.1A**); **`TASK-2026-08B-011`** (**8B.1B**)
- Contract: **`docs/00_SYSTEM/13_CLIENT_AGNOSTIC_PERSISTENCE_CONTRACT_V1.md`**
- **8B.1** split + doc alignment: **`STAGE_8B_DOC_STATE_ALIGNED`** (**`CHANGELOG`**, **`NOW`**, **`12_IDEA_MASTER_LOG`**)

Master table **Status**: **`ACTIVE`** until **8B** governance + audit **PASS** — then **`IMPLEMENTED`**.

### IDEA-0021 — EDS Power role-adaptive operational shell doctrine (“self-checkout principle”)

**Strategic one-liner:** Industrial **self-checkout architecture** — **simple for each worker, deep underneath.**

Classification / priority / decision:

- `NORMAL_LONG_TERM` / `P3` / `FUTURE`

Stage target:

- Post–**core platform architecture** / multi-module **UX doctrine** (broader than KZO or Google Sheets alone)

Trigger condition:

- After **stable CALC + persistence + first operational modules** — reopen for product strategy review

Review stage:

- **Re-evaluate** when moving from MVP tooling to company-wide **operator ecosystem**

Core design law:

- **Complexity below.** **Operational simplicity above.**

Key thesis:

- **Users should not operate core accounting / ERP / DB directly** unless their role truly requires it.
- **EDS Power** should expose only the **minimal operational layer** each participant needs; **truth**, **rules**, **analytics**, **governance** remain **under** that layer.
- **1C / ERP / DB ≠ operator interface** — they may be the **truth layer**, while participants work through **governed adaptive shells**.

Self-checkout analogy:

- Cashier / shopper does **not** work in the bookkeeping DB; they see a **guided flow** and **next required action** — warehouse, postings, analytics run **underneath**.

EDS Power role sketch (illustrative — **not** execution scope now):

- Майстер — only their operation  
- Конструктор — only required engineering inputs  
- Менеджер — commercial flow  
- Комплектувальник — pick task  
- Керівник — analytics / bottlenecks  
- Бухгалтерія — accounting truth **when role requires exposure to it**

Possible future implications (**no** TASK until renormalized):

- Role dashboards; guided flows; kiosk / station / mobile task views; department shells; API-first orchestration; **1C integration as backend truth**, not mandatory front desk for every user.

Forbidden **now**:

- UI overbuild; app-ecosystem sprawl; auth redesign; ERP rewrite; premature dedicated mobile platform.

Anti-drift:

- **Doctrine only** — no automatic expansion of current build stages without a new **IDEA → TASK** chain.

Master table **Status**: **`FUTURE`**