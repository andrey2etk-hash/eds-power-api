# Stage 2 CALC Configurator Skeleton Audit Report

## Audit date

2026-04-26

## Audit trigger

User requested Stage 2 preparation for `00-02_CALC_CONFIGURATOR`, then provided Gemini audit fixes for the CALC skeleton.

## Last audit reference

`docs/AUDITS/2026-04-26_STAGE_1_GEMINI_AUDIT_FIX_PACK_V2.md`

## Files reviewed

- `docs/00_SYSTEM/04_DATA_CONTRACTS.md`
- `docs/00-02_CALC_CONFIGURATOR/00_MODULE_OVERVIEW.md`
- `docs/00-02_CALC_CONFIGURATOR/01_GOAL.md`
- `docs/00-02_CALC_CONFIGURATOR/02_INPUTS.md`
- `docs/00-02_CALC_CONFIGURATOR/03_PROCESS_FLOW.md`
- `docs/00-02_CALC_CONFIGURATOR/04_OUTPUTS.md`
- `docs/00-02_CALC_CONFIGURATOR/05_FUNCTIONS.md`
- `docs/00-02_CALC_CONFIGURATOR/06_DB_TABLES.md`
- `docs/00-02_CALC_CONFIGURATOR/07_MODULE_LINKS.md`
- `docs/00-02_CALC_CONFIGURATOR/08_UI_UX.md`
- `docs/00-02_CALC_CONFIGURATOR/09_STATUS.md`
- `docs/00-02_CALC_CONFIGURATOR/10_CONFIG.md`

## Gemini critique summary

Gemini audit identified that the CALC skeleton needed clearer boundaries before MVP preparation.

Required audit fixes:

- consolidate CALC API entry around one external action
- keep validation, normalization and calculation as internal API stages
- prevent GAS from calling internal stages separately
- update Base Calculation Object with version and timestamps
- allow `object_number` to be optional at draft stage
- define Calculation Object Lifecycle
- align inputs with auth/session requirements and global contracts
- add validation failure branch and error path
- avoid product-specific logic

## GPT interpretation

The critique is accepted as documentation refinement only.

The correct interpretation is:

- `prepare_calculation` is the only external CALC API entry point at this stage
- validation, normalization and calculation are internal API stages
- GAS remains a thin client and does not call internal stages
- Base Calculation Object may evolve in `04_DATA_CONTRACTS.md` because it is the shared contract source
- CALC skeleton must stay generic until Stage 2 MVP scope is approved through TASK

## Accepted items

- `prepare_calculation` fixed as the single external API entry point
- internal API stages documented as validation, normalization, calculation preparation and response formation
- GAS restriction added for internal stages
- Base Calculation Object updated with `version`
- Base Calculation Object updated with `created_at`
- Base Calculation Object updated with `updated_at`
- `object_number` allowed to be `null` at `draft`
- Calculation Object Lifecycle added:
  - draft
  - validated
  - error
  - calculated
  - locked
  - archived
- auth/session requirements added to CALC inputs
- validation failure branch added to process flow
- error path added to process flow
- product-specific examples removed from CALC skeleton

## Rejected items

- no product-specific logic
- no KSO-specific logic
- no architecture redesign
- no async implementation
- no AUTH expansion
- no API endpoint implementation
- no DB implementation
- no code implementation

## Deferred items

- first MVP product type selection
- product-specific parameter details
- calculation formulas
- API implementation
- database table design
- UI / GAS implementation
- integration with commercial offers
- integration with production transfer
- status move from `planned` to `draft_ready`

## Cursor actions performed

- Created missing CALC skeleton files
- Updated CALC skeleton documentation
- Updated only the Base Calculation Object section in `04_DATA_CONTRACTS.md`
- Added auth/session requirements to CALC inputs
- Added internal API stage boundaries
- Added Calculation Object Lifecycle
- Added validation failure branch and error path
- Removed product-specific example values from CALC skeleton
- Verified Markdown with `git diff --check`
- Verified absence of conflict markers
- Verified linter diagnostics for changed docs

## User final decision

User instructed Cursor to apply Stage 2 Gemini audit fixes to the CALC skeleton as documentation refinement only.

User also confirmed that an audit report is required by the audit rules after completing the changes.

## Key decisions locked

- `prepare_calculation` is the single external CALC API entry point
- GAS cannot call internal CALC stages separately
- Base Calculation Object includes version and timestamps
- `object_number` is optional at draft stage
- Calculation Object Lifecycle is standardized
- CALC remains product-agnostic until MVP TASK approval

## Next stage entry conditions

Before `00-02_CALC_CONFIGURATOR` moves to `draft_ready`:

- Full CALC skeleton verified
- System docs synchronized
- First MVP product type selected
- Product-specific parameter set approved
- First calculation scenario defined
- Stage 2 MVP TASK approved

## Status

✔ Closed — Stage 2 CALC Skeleton Fix Pack Approved
