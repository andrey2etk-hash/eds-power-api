# GEMINI STAGE 6B — Engineering Classification MVP (External Audit Request)

**Purpose.** Prompt for **external auditor Gemini**. Gemini does **not** implement logic, patch the repository, or rewrite project docs unless the human owner applies findings later — Gemini **reviews** the Stage 6B delivery **after** operator verification **PASS**.

**Strict:** Gemini **analyzes** the listed evidence and answers the questions below. Verdict applies to **whether it is safe to proceed toward Stage 6C** from a governance / thin-client / scope standpoint.

---

## Operator verification context (recorded facts)

Manual run on **`Stage4A_MVP`** after GAS **`setValues`** row-count alignment (**14 rows** ↔ **`E27:F40`**).

| Observation | Recorded |
| --- | --- |
| HTTP | **`http_code`** **200** |
| API payload | **`engineering_class_summary_present`** **true** (operator / log) |
| GAS | **`writeback_completed`**; telemetry **`stage`** = **`6B_ENGINEERING_CLASSIFICATION`** |
| Sheet | **`E27:F40`** (**14** rows); no row/range mismatch after fix |
| Failure path | **`request_or_writeback_failed`** **not** triggered for that successful writeback |
| Thin client | Mapping from API JSON to cells — **no** engineering-class math in GAS |
| Scope | **No** mass, BOM, pricing, DB, Supabase, CAD expansion in this stage |

**IDEA-0013:** Master table **Status** remains canonical **`IMPLEMENTED`**. **Operator-verified** / **operator verification PASS** are **prose closure** labels in audit notes (not a new **Status Values** token).

---

## Prerequisites (what Gemini should assume)

1. **`prepare_calculation`** success path returns **`data.engineering_class_summary`** built server-side from **`structural_composition_summary`** + **`physical_topology_summary`** only (planning labels; **`interpretation_scope`** = **`ENGINEERING_CLASSIFICATION_ONLY_MVP`**).
2. Stage 6B GAS reuses the **Stage 6 band** **`E27:F40`** (same constant as Stage 6A reserved block; Stage 6B **overwrites** placeholder content when the Stage 6B flow runs).
3. Operator verification **PASS** is already documented in **`docs/AUDITS/2026-04-29_STAGE_6B_ENGINEERING_CLASSIFICATION.md`** — this Gemini pass is **independent** confirmation, not a replacement for that log.

---

## Files for review (check these paths in repo)

| Path | Why |
| --- | --- |
| `main.py` | `_build_kzo_engineering_class_summary()` — inputs, outputs, **`interpretation_scope`**, no mass/BOM/price/CAD |
| `gas/Stage3D_KZO_Handshake.gs` | `STAGE_6B_ENGINEERING_CLASSIFICATION_RANGE_A1`, `runStage6BEngineeringClassificationFlow()`, `writeStage6BEngineeringClassification_()` — **14**-row `setValues`, thin mapping |
| `docs/AUDITS/2026-04-29_STAGE_6B_ENGINEERING_CLASSIFICATION.md` | Declared boundaries, operator **PASS** table, forbidden list |
| `docs/00_SYSTEM/12_IDEA_MASTER_LOG.md` | **IDEA-0013** — **Status** = **`IMPLEMENTED`**; operator closure in notes |

---

## Audit questions (Gemini must answer)

**A. API classification scope**

1. Does **`engineering_class_summary`** stay **planning-grade** (complexity / scale / section profile + basis fields) with **no** precision economics (mass, BOM, price) or external DB/Supabase?
2. Is the **only** declared interpretation scope **`ENGINEERING_CLASSIFICATION_ONLY_MVP`** consistent with the implementation (no hidden coupling to forbidden layers)?

**B. GAS thin client & writeback**

3. Does GAS **only** transport and display API truth (including **`JSON.stringify`** for the section profile list if used) **without** recomputing **`lineup_complexity_class`**, **`lineup_scale_class`**, or per-section labels?
4. Is writeback **confined** to **`E27:F40`** (14×2) with **14** rows supplied to `setValues` (aligned with the range — no off-by-one drift)?

**C. Stage 6 block usage**

5. Is reuse of the Stage 6A **reserved band** for Stage 6B **governable** (same operator column real estate; overwrite semantics documented) or does Gemini see a **layout / safety** conflict with earlier stages?

**D. Drift & governance**

6. Is there **evidence** in the reviewed paths of **scope creep** toward mass, BOM, pricing, DB, or Supabase for Stage 6B?
7. Is **IDEA-0013** handling (**`IMPLEMENTED`** + prose **operator-verified**) **consistent** with master **Status Values** discipline (no invented status token)?

**E. Stage 6C readiness (forward-looking, not design)**

8. Given the above, is the project **positioned** to plan Stage 6C **without** retroactive breach of “classification before precision,” or does Gemini see a **blocker** that must be fixed first?

---

## Required Gemini response format

Return the answer **with exactly** these section headings:

```markdown
# GEMINI STAGE 6B ENGINEERING CLASSIFICATION MVP — EXTERNAL AUDIT

## PASS ITEMS

## RISKS

## FIXES REQUIRED (IF ANY)

## GOVERNANCE NOTES (IDEA-0013 / STATUS VALUES)

## FINAL VERDICT

<one line: SAFE TO PROCEED TO STAGE 6C | SAFE WITH FIXES | BLOCKED>
```

### Verdict semantics

- **SAFE TO PROCEED TO STAGE 6C** — API scope and thin GAS writeback match governance; **IDEA-0013** handling acceptable; no material drift; any remaining items are **cosmetic** or **future-stage** only.
- **SAFE WITH FIXES** — Core delivery is sound, but **documentation**, **naming**, or **minor alignment** should be applied before or alongside Stage 6C planning (Gemini must **list** fixes).
- **BLOCKED** — Material scope breach, unsafe writeback / range behavior, or governance violation that must be **resolved** before treating Stage 6B as closed for forward motion.

---

## Auditor constraints (do not)

- Do **not** propose expanding Stage 6B into mass, BOM, pricing, or DB in this gate.
- Do **not** require new **Status Values** in the IDEA master table for operator closure.
- Do **not** redesign the Sheet layout beyond commenting on **E27:F40** reuse safety.

---

_End of Gemini external audit request._
