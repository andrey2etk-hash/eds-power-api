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
| IDEA-0007 | 2026-04-29 | Stage 5A First Practical KZO Logic | `RIGHT_NOW` | `P1` | `TASK` | Stage 5A | Only after Stage 4C `VERIFIED_OPERATOR_SHELL` | Inject first narrow practical KZO logic only after the operator shell is stable | `UNLOCKED_NEXT_PRIMARY` |

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
- not parallel with Stage 4C

Trigger condition:

- only after Stage 4C `VERIFIED_OPERATOR_SHELL`

Required scope:

- first narrow KZO logic only
- use stabilized operator shell only

Forbidden scope:

- pricing
- commercial layer
- BOM explosion
- CAD
- technical department overbuild
- multi-product
- DB foundation shift

Reason:

- Stage 5A is strategically immediate but must not run before shell maturity.
- This protects architecture from premature coupling.
- Correct sequence is `4B -> 4C -> 5A`, not `4B -> (4C + 5A)`.

Key governance principle:

- First stable operator shell, then practical product logic.

Scope guard:

- 5A remains parked until Stage 4C is verified as operator shell.
