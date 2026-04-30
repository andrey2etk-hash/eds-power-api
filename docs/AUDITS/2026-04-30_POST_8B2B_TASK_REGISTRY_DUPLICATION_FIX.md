# POST–8B.2B TASK registry duplication fix

**Classification:** Documentation hygiene (**registry clarity only**).  
**Date:** 2026-04-30.  
**Not:** Stage **8B.2C** execution · governance expansion · implementation.

## Duplication source

After **8B.2B** closeout labeling, **`TASK-2026-08B-013`** (**Stage **8B.2****) was repeated almost verbatim across **`NOW.md`**, **`12_IDEA_MASTER_LOG.md`**, **`09_STATUS.md`**, **`09_KZO/08_STATUS.md`**, and parts of **`00_AUDIT_INDEX.md`**. Each repetition restated parent-gate **`ACTIVE`** and sub-slice status with the **same** canonical meaning, which invited **silent drift** (e.g. one file still saying Gemini **8B.2B** pending while another treated **8B.2B** **CLOSED**).

## Corrections (**single TASK truth**)

Canonical parent-gate narration and audit paths reside in **`docs/TASKS.md`** **`§ TASK-2026-08B-013`**. Peripheral registries now **point** to that section instead of cloning the full rollup.

**Confirmed canonical posture (patch target):**

- **`TASK-2026-08B-013`** **`ACTIVE`** (**Stage **8B.2****)
- **`8B.2A`** **CLOSED**
- **`8B.2B`** **CLOSED** (doctrine **`STAGE_8B_2B_DOCTRINE_PUBLISHED`**; Gemini gate **`STAGE_8B_2B_GEMINI_FOCUSED_AUDIT_PASS`** — lodging path **`docs/AUDITS/YYYY-MM-DD_GEMINI_STAGE_8B_2B_FOCUSED_AUDIT.md`** per **`docs/AUDITS/2026-04-30_GEMINI_STAGE_8B_2B_FOCUSED_AUDIT_REQUEST.md`**; repo tip may omit the dated lodged file until the operator adds it)
- **`8B.2C`** **NEXT**: **`NOT_STARTED` / NON-CANONICAL / AWAITING IDEA NORMALIZER** — **no premature activation** · no canonical **`2C`** dossier until normalization

**Files touched:**

- **`docs/TASKS.md`** — merged duplicate sub-slice table rows into one **`Slice progression`** row; consolidated Gemini gate bullets (**no** duplicate **`### Stage 8B.2A`** heading); **`8B.2B`** delivery line aligned with **`CLOSED`**
- **`docs/NOW.md`** — collapsed redundant **`TASK-013`** / **8B.2** lines; **`Slice status`** shortened to **`TASKS`** pointer
- **`docs/00_SYSTEM/12_IDEA_MASTER_LOG.md`** — **`TASK-013`** rollup shortened to **`TASKS`** **`§ TASK-013`** pointers where full paths duplicated
- **`docs/00-02_CALC_CONFIGURATOR/09_STATUS.md`** — headline status → **`TASKS`** canon
- **`docs/00-02_CALC_CONFIGURATOR/09_KZO/08_STATUS.md`** — fast-read + operator registry bullets → rollup pointer
- **`docs/CHANGELOG.md`** — this hygiene entry (**top**)
- **`docs/AUDITS/00_AUDIT_INDEX.md`** — **Latest** + **Post–Stage **8A**** **8B.2** line + **Stage audits** listing

Historically authored audit bodies (**e.g.** **`docs/AUDITS/2026-04-30_STAGE_8B_2B_PREPARE_SAVE_SPLIT_OUTCOME_GOVERNANCE.md`**, **`CHANGELOG`** entries dated **2026-04-30**) were **not** rewritten retroactively beyond this reconciliation note where needed conceptually (**no** fabricated closeout text).

## No governance drift

Stage ordering, **`FORBIDDEN`** lanes, **`TASK`** IDs (including **`012`** **≠** **8B.2**), and **`COMPLETE`** (**only** after **2A–2E** + synthesis) are unchanged in meaning. **`8B.2C`** remains **explicitly non-active** until **Idea Normalizer** normalization.

## No implementation drift

**No** edits to **`main.py`**, **`gas/`**, **API** routes, migrations, **Supabase**, or runtime config.

## 8B.2C path

Repository registries now support a **clean handoff** to **Stage **8B.2C** normalization**: next action is **`TASK`/normalizer-aligned** dossier authoring for **`8B.2C`**, **not** code or widening **Stage **8B.2**** scope beyond **`TASK`** text.
