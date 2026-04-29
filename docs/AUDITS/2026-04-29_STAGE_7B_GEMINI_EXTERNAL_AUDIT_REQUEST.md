# GEMINI STAGE 7B — Snapshot Contract Freeze (External Audit Request)

**Purpose.** Prompt for **external auditor Gemini** (independent critic). Gemini **does not** patch the repository, design Supabase DDL, SQL, migrations, or **Stage 8A** persistence — Gemini **reviews** whether **Stage 7B — KZO MVP Snapshot Contract Freeze** is **sound** as the **mandatory governance gate** before persistence.

**Strict:** Analysis only — **contract + governance**. Verdict is advisory to the human owner.

---

## Closure context (recorded)

| Layer | State |
| --- | --- |
| Snapshot contract | **`KZO_MVP_SNAPSHOT_V1`** documented in **`11_KZO_MVP_SNAPSHOT_V1_CONTRACT.md`** |
| Audit dossier | **`2026-04-29_STAGE_7B_KZO_MVP_SNAPSHOT_CONTRACT_FREEZE.md`** (**freeze before persistence**) |
| Prerequisite stages | **IDEA-0015** `IMPLEMENTED` (Stage **7A** unified MVP run operator-verified) |
| **IDEA-0016** | Master table **Status** = **`IMPLEMENTED`** |
| Forbidden in 7B | No Supabase tables, SQL, deployment, **new MVP engineering fields** in the **required V1 envelope** |

**Governance intent:** Anything **not** in **`KZO_MVP_SNAPSHOT_V1`** must **not** be treated as mandatory persisted schema until a **new snapshot version + IDEA**.

---

## Files for review (repository paths)

| Path | Why |
| --- | --- |
| `docs/00-02_CALC_CONFIGURATOR/09_KZO/11_KZO_MVP_SNAPSHOT_V1_CONTRACT.md` | Canonical JSON shape — required keys, versioning, SUCCESS/FAILED, explicit exclusions |
| `docs/AUDITS/2026-04-29_STAGE_7B_KZO_MVP_SNAPSHOT_CONTRACT_FREEZE.md` | Stage 7B scope — freeze-before-persistence gate |
| `docs/00_SYSTEM/12_IDEA_MASTER_LOG.md` | **IDEA-0016** row + Idea Notes vs **IDEA-0015** |
| `docs/CHANGELOG.md` | Stage 7B chronology |
| `docs/NOW.md` | Posture — Stage 8A gated after 7B |
| `docs/00-02_CALC_CONFIGURATOR/09_KZO/08_STATUS.md` | KZO-local gates / **Stage 8A** wording |
| `docs/00-02_CALC_CONFIGURATOR/09_STATUS.md` | Module status rollup |
| `docs/AUDITS/00_AUDIT_INDEX.md` | Audit navigation |
| **`main.py`** | **`prepare_calculation`** success **`data`** / **`metadata`** / error shapes (**contract alignment**) |

---

## Audit questions (Gemini must answer)

1. Does **`KZO_MVP_SNAPSHOT_V1`** **accurately reflect** real **verified MVP outputs** (structural footprint through burden — Stage 5A–7A stack)?
2. Is there **any contract drift** between the snapshot doc and **`prepare_calculation`** **actual** JSON (field names, nesting, omission of **`basic_result_summary`** / **`validation_status`**, etc.)?
3. Are there **missing critical fields** for **future** persistence (given V1 excludes BOM/pricing/DB IDs — flag only legitimate gaps)?
4. Is there **premature DB / schema inflation** embedded in prose (implicit columns, unnamed required indexes, speculative Supabase)?
5. Are **SUCCESS / FAILED** envelopes **governance-safe** (no fake partial engineering on failure; failure shape honest vs API)?
6. Is **Stage 7B** a **safe baseline** to authorize planning **Stage 8A** (persistence TASK) — not implementation?
7. Is the snapshot freeze **disciplined enough** to **prevent schema chaos** (“if not in V1…”) — list residual risks?

---

## Required Gemini response format

Gemini must respond with **exactly** this title and **these** markdown `##` sections (in order):

```markdown
# GEMINI STAGE 7B SNAPSHOT CONTRACT AUDIT

## PASS ITEMS

## RISKS

## DOC FIXES REQUIRED

## GOVERNANCE STATUS

## PERSISTENCE READINESS

## FINAL VERDICT
```

**FINAL VERDICT** must be **one line** after the heading:

`PASS` **or** `PASS WITH DOC FIXES` **or** `FAIL`

### Verdict semantics

- **PASS** — V1 aligns with **`prepare_calculation`** MVP truth; no hidden persistence inflation; FAILURE envelope safe; **IDEA-0016** closure defensible; **Stage 8A** may proceed as **governance-planned TASK** only.
- **PASS WITH DOC FIXES** — architecture OK; **explicit** naming / cross-reference / omission notes (e.g. **`basic_result_summary`**) recommended under **DOC FIXES REQUIRED**.
- **FAIL** — material mismatch with API **`data`**, contradictory governance, implicit schema mandate, or unsafety declaring freeze — **must** resolve before treating **Stage 7B** as closed for persistence planning.

---

## Auditor constraints

- Do **not** require **implementation** — no Supabase projects, migrations, RPC, or DDL.
- Do **not** invent new **IDEA Status Values** outside existing **`Status Values`** vocabulary.
- Do **not** treat this audit as **Stage 8A** specification — at most whether **freeze** authorizes **a future persistence TASK**.

_End of Gemini external audit request._
