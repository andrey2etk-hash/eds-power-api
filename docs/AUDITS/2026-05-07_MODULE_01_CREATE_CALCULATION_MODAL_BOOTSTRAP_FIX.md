# Module 01 — Create Calculation Modal Bootstrap Fix

## Objective

Fix the Create Calculation modal stuck on **«Зачекайте…»** with **Створити** permanently disabled because bootstrap never completed from HTML.

## Root cause

`Module01CreateCalculationModalHtml.html` called **`google.script.run.module01CreateCalculationBootstrap_()`**. In Apps Script, **trailing-underscore** functions are treated as private / not reliably exposed to `google.script.run` and often **do not appear** in the runnable function list. The success handler never ran, so loading state never cleared and submit stayed disabled.

## Fix

1. **`gas/Module01CreateCalculationModal.gs`** — public wrapper:
   - **`module01CreateCalculationBootstrap()`** → delegates to **`module01CreateCalculationBootstrap_()`** (unchanged internal logic).
2. **`gas/Module01CreateCalculationModalHtml.html`** — on load calls **`module01CreateCalculationBootstrap`** (no trailing underscore).

## Files changed

| File | Change |
|------|--------|
| `gas/Module01CreateCalculationModal.gs` | Public `module01CreateCalculationBootstrap` |
| `gas/Module01CreateCalculationModalHtml.html` | `google.script.run` target updated |

## Behavior after fix

- On load: bootstrap runs; **«Зачекайте…»** hides on success or error.
- On success: **`btn-submit`** enables (same as prior intended design).
- On bootstrap failure: **err-box** shows server/session message or generic bootstrap error; submit stays disabled.

## Scope confirmation

- **No** backend, **no** DB/SQL/migrations, **no** registry, **no** product/calculation/KZO logic.

## Verdict

**`MODULE_01_CREATE_CALCULATION_MODAL_BOOTSTRAP_FIX_IMPLEMENTED`** — operator: re-sync GAS and re-test modal open + submit.
