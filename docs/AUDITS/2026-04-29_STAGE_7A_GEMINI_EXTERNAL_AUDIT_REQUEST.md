# GEMINI STAGE 7A — Final Closure (External Audit Request)

**Purpose.** Prompt for **external auditor Gemini** (independent critic). Gemini **does not** patch the repository, rewrite governance corpora, or scope **Stage 7B** / **Stage 8+** implementation — Gemini **reviews** whether **Stage 7A — KZO End-to-End MVP Stabilization** is **coherently closure-ready** after unified **`runKzoMvpFlow()`** + operator verification PASS + doc-pass.

**Strict:** Analysis only. Verdict is advisory to the human owner.

---

## Closure context (recorded)

| Layer | State |
| --- | --- |
| Unified run | **`runKzoMvpFlow()`** — one **`prepare_calculation`** POST, then orchestrated writeback (**5A** + **5C** + unified **Stage 6 band**) |
| Operator verification | **PASS** — API **`status`** = **`success`**, **HTTP 200**, **`mvp_run_outcome`** = **`MVP_RUN_SUCCESS`** (manual Apps Script execution) |
| Sheet | **`Stage4A_MVP`**: **`E4:F19`** + **`E20:F20`**, **`E21:F26`**, **`E27:F40`** populated per verification |
| **`data` summaries present** | **`structural_composition_summary`**, **`physical_summary`**, **`physical_topology_summary`**, **`engineering_class_summary`**, **`engineering_burden_summary`** |
| GAS scope | Thin orchestration/writeback reuse of existing writers (**`writeStage5AOutputIntegration_`**, **`writeStage5CSheetOutputIntegration_`**, **`writeStage7AUnifiedStage6Band_`**); telemetry **`stage=7a-kzo-mvp-flow`**, **`mvp_run_outcome`** |
| Engineering logic | Owner claim: **no new engineering logic** added in Stage 7A — cohesion/orchestration only |
| **IDEA-0015** | Master table **Status** = **`IMPLEMENTED`** (post operator PASS doc-sync) |

**Forbidden for Stage 7A verification:** Treating this audit as mandate to implement **Supabase**, **BOM**, **pricing**, **`E41:F54`**, or new **`prepare_calculation`** math layers.

---

## Files for review (repository paths)

| Path | Why |
| --- | --- |
| `gas/Stage3D_KZO_Handshake.gs` | **`runKzoMvpFlow()`**, **`writeStage7AUnifiedStage6Band_()`**, orchestration boundaries vs discrete Stage runners |
| `docs/AUDITS/2026-04-29_STAGE_7A_KZO_END_TO_END_MVP_STABILIZATION.md` | MVP cohesion audit + operator PASS record |
| `docs/00_SYSTEM/12_IDEA_MASTER_LOG.md` | **IDEA-0015** row + Idea Notes closure |
| `docs/NOW.md` | Current posture vs Stage 7A |
| `docs/CHANGELOG.md` | Stage 7A chronology |
| `docs/AUDITS/00_AUDIT_INDEX.md` | Audit navigation pointer |
| `docs/00-02_CALC_CONFIGURATOR/09_KZO/08_STATUS.md` | KZO-local gate / Stage 7A line |
| `docs/00-02_CALC_CONFIGURATOR/09_STATUS.md` | Module status rollup |

Cross-check (recommended, not exhaustive): **`docs/00-02_CALC_CONFIGURATOR/09_KZO/10_OPERATOR_LAYOUT.md`** — Shell zones and **Stage 5B** API-only footprint vs Sheet governance.

---

## Audit questions (Gemini must answer)

1. Did Stage 7A **correctly unify** existing **validated layers** (**5A-output**, **5C topology**, **6B/6C engineering bands**) **without adding new engineering logic** in GAS?
2. Did **GAS** remain **thin** — orchestration + writeback/display only (no heuristic recomputation, no surrogate “smart” summaries in Scripts)?
3. Are **Sheet zones** (**`E4:F20`**, **`E21:F26`**, **`E27:F40`**) **consistent**, **fixed**, and **non-overlapping** relative to **`E41:F54`** reserve?
4. Is **`physical_summary`** (**Stage 5B**) correctly reflected as **API / Execution log telemetry** without **hidden Sheet drift** or an undeclared footprint block conflicting with **`IDEA-0009`** / layout governance?
5. Is **IDEA-0015** **properly closed** as **`IMPLEMENTED`** in the master table and notes (**no invented lifecycle**, defensible after operator PASS)?
6. From a **governance standpoint**, is **Stage 7A safe to treat as fully closed** — i.e., **cohesion gate satisfied** — before expanding depth?
7. **Forward planning only (pick one directional recommendation):** What is **safest next stage** narrative — **`7B` snapshot/contract freeze** governance step **or** **`8A` Supabase persistence** — and **why**? (Recommendation only; **no** implementation scope.)

---

## Required Gemini response format

Gemini must respond with **exactly** this title and **these** markdown `##` sections (in order):

```markdown
# GEMINI STAGE 7A FINAL CLOSURE AUDIT

## PASS ITEMS

## RISKS

## DOC FIXES REQUIRED

## GOVERNANCE STATUS

## NEXT STAGE RECOMMENDATION

## FINAL VERDICT
```

**FINAL VERDICT** must be **one line** after the heading:

`PASS` **or** `PASS WITH DOC FIXES` **or** `FAIL`

### Verdict semantics

- **PASS** — unified flow holds boundaries; thin GAS; Sheet governance intact; **`physical_summary`** treatment honest; **IDEA-0015** closure sound; acceptable to treat Stage **7A** as closed for governance.
- **PASS WITH DOC FIXES** — core OK; explicit doc alignment/naming/registry fixes recommended (list under **DOC FIXES REQUIRED**).
- **FAIL** — material scope breach, contract contradiction, drift into forbidden layers (e.g. undeclared Sheet expansion, engineering logic in GAS), or governance unsafety — **must** be resolved before declaring Stage **7A** governance-closed.

---

## Auditor constraints

- Do **not** require **implementation** of **Supabase**, **DB**, **BOM**, or **pricing** as a condition of **PASS**.
- Do **not** invent new **IDEA Status Values** in the master table as a fix.
- Do **not** specify full **Stage 7B** or **8A** product design — **at most** directional **next-stage** preference with rationale.

_End of Gemini external audit request._
