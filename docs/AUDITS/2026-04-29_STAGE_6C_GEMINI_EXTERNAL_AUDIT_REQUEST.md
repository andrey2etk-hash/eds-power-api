# GEMINI STAGE 6C — Full Closure (External Audit Request)

**Purpose.** Prompt for **external auditor Gemini** (independent critic). Gemini **does not** patch the repository, rewrite governance corpora, or scope **Stage 6D** / precision implementation — Gemini **reviews** whether **Stage 6C — KZO Engineering Burden Foundation MVP** is **coherently closed** after API + Render + operator Sheet + doc-pass.

**Strict:** Analysis only. Verdict is advisory to the human owner.

---

## Closure context (recorded)

| Layer | State |
| --- | --- |
| API | **`data.engineering_burden_summary`** via **`_build_kzo_engineering_burden_summary()`** — **`interpretation_scope`** = **`ENGINEERING_BURDEN_ONLY_MVP`** |
| Live Render | **PASS** — `docs/AUDITS/2026-04-29_STAGE_6C_ENGINEERING_BURDEN_RENDER_GATE.md` (deploy lag noted; checklist on canonical KZO vector) |
| GAS | **Thin** — `runStage6CEngineeringBurdenFlow()`, writeback **`E27:F40`** only; telemetry **`6C_ENGINEERING_BURDEN`** |
| Operator Sheet | **PASS** — **PASS** logged in same Render gate dossier (Apps Script execution excerpts, **`Stage4A_MVP`** / **`E27:F40`**) |
| **IDEA-0014** | Master table **Status** = **`IMPLEMENTED`** (post-Render interim **`RENDER_VERIFIED_PENDING_OPERATOR_TEST`** superseded by doc-sync) |
| Forbidden for 6C | No exact **kg**, BOM, pricing, procurement mass economics, DB/Supabase precision layers in this stage |

---

## Files for review (repository paths)

| Path | Why |
| --- | --- |
| `main.py` | `_build_kzo_engineering_burden_summary()`, `prepare_calculation` response wiring; inputs from 6B + topology + structural flags only |
| `gas/Stage3D_KZO_Handshake.gs` | Stage 6C flows, **`STAGE_6C_ENGINEERING_BURDEN_RANGE_A1`**, 14-row **`setValues`** alignment with **`E27:F40`** |
| `docs/AUDITS/2026-04-29_STAGE_6C_ENGINEERING_BURDEN_FOUNDATION.md` | Stage 6C principle, forbidden list, verdict |
| `docs/AUDITS/2026-04-29_STAGE_6C_ENGINEERING_BURDEN_RENDER_GATE.md` | Render PASS + operator Sheet PASS, checklists |
| `docs/00_SYSTEM/12_IDEA_MASTER_LOG.md` | **IDEA-0014** row + notes |
| `docs/00-02_CALC_CONFIGURATOR/09_KZO/08_STATUS.md` | KZO-local status / gate narrative |
| `docs/00-02_CALC_CONFIGURATOR/09_STATUS.md` | Module status |
| `docs/CHANGELOG.md` | Chronology of Stage 6C + closures |
| `docs/NOW.md` | Current posture |
| `docs/AUDITS/00_AUDIT_INDEX.md` | Audit navigation |
| `docs/00-02_CALC_CONFIGURATOR/09_KZO/10_OPERATOR_LAYOUT.md` | Stage 6 band, 6B vs 6C overwrite semantics |

Optional helper (not part of product contract): `scripts/ping_prepare_calculation_live.py` — local smoke to live API.

---

## Audit questions (Gemini must answer)

1. Did Stage 6C preserve **“planning burden only”** boundaries — in particular is **`estimated_mass_class`** clearly **not** kilograms / not procurement truth?
2. Any **false precision drift** toward exact mass, BOM, pricing, or CAD in reviewed **API / GAS / docs** paths?
3. Did **GAS** remain a **thin client** (transport + display of API fields, no burden heuristic recomputation in Sheets)?
4. Is **`E27:F40`** **Stage 6 governed block** integrity preserved (same band as 6A/6B; 6C overwrite semantics documented; no drift into **`E41:F54`**)?
5. Any **contract drift** across pipeline **5A → 5B → 5C → 6B → 6C** (field naming, interpretation scopes, forbidden layers)?
6. Is the **burden layer** architecturally **valid** as the next bridge after **classification (6B)** and before any **precision / commercial** TASKs (not asking to design 6D — only whether 6C closes that gap honestly)?
7. Is **IDEA-0014** **closure** in master log + audits **consistent** (no invented lifecycle tokens; **IMPLEMENTED** defensible after Render + Sheet PASS)?
8. Is the system **safe to plan or proceed** toward a **future** stage (**e.g. Stage 6D** or later precision gates) **from a governance perspective** — or are there **blockers**? (No **Stage 6D** implementation assumed or required in this audit.)

---

## Required Gemini response format

Gemini must respond with **exactly** these top-level sections and headings (markdown `##`):

- `# GEMINI STAGE 6C FULL CLOSURE AUDIT`
- `## PASS ITEMS`
- `## RISKS`
- `## DOC FIXES REQUIRED`
- `## GOVERNANCE STATUS`
- `## ARCHITECTURAL MATURITY`
- `## FINAL VERDICT` — **one line**: `PASS` **or** `PASS WITH DOC FIXES` **or** `FAIL`

### Verdict semantics

- **PASS** — boundaries hold; thin GAS; contracts aligned; **IDEA-0014** closure sound; forward planning acceptable with only **cosmetic** doc nits.
- **PASS WITH DOC FIXES** — core architecture OK; **explicit** doc or naming alignment recommended (list under **DOC FIXES REQUIRED**).
- **FAIL** — material scope breach, governance contradiction, or architectural unsafety that must be **resolved** before treating **Stage 6C** as governance-closed.

---

## Auditor constraints

- Do **not** require **kg**, BOM, CAD, DB, or pricing in **Stage 6C** as a condition of PASS.
- Do **not** invent new **IDEA Status Values** in the master table as a fix.
- Do **not** implement or specify **Stage 6D** scope — at most **whether** planning may continue under existing governance.

_End of Gemini external audit request._
