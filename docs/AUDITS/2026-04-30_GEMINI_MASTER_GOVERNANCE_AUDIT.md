# GEMINI MASTER GOVERNANCE AUDIT — EDS POWER

**Audience:** Maintainer / Idea Normalizer / Future implementers  
**Mode:** External critical auditor (governance & architecture stress test) — **documentation-only evidence**  
**Evidence cut:** Repo docs listed below; **no** runtime probing, **no** code churn in this dossier  
**Method:** Contradiction hunting against stated chain Stage 1 foundations → **8B.2** decomposition  

**Review packet (anchors):**

- `docs/00_SYSTEM/00_SYSTEM_OVERVIEW.md`, `02_GLOBAL_RULES.md`, `04_DATA_CONTRACTS.md`, `06_OBJECT_STATUSES.md`, `08_AI_AGENT_RULES.md`, `12_IDEA_MASTER_LOG.md`, `13_CLIENT_AGNOSTIC_PERSISTENCE_CONTRACT_V1.md`
- `docs/00-02_CALC_CONFIGURATOR/00_MODULE_OVERVIEW.md`, `09_STATUS.md`, `09_KZO/*` (indirect via status + audits)
- `docs/AUDITS/00_AUDIT_INDEX.md`, `2026-04-30_STAGE_8B_1B_GAS_THIN_CLIENT_ADAPTER.md`, `2026-04-30_STAGE_8B_2_PRE_GATE_SCOPE.md`, `2026-04-30_STAGE_8B_2_GOVERNANCE_SUBSTAGES_DECOMPOSITION.md`
- `docs/NOW.md`, `docs/TASKS.md`, `docs/CHANGELOG.md`

---

## EXECUTIVE VERDICT

**SAFE WITH FIXES**

The persistence governance spine (**API orchestrates**, **Supabase memory**, **`KZO_MVP_SNAPSHOT_V1` freeze**, **`8B.1` split + operator closeouts**) is **directionally coherent** and unusually mature for an MVP-phase repo.

You are **not** clean: there are **document-level contradictions**, **TASK-ID hygiene hazards**, **naming coupling** (**KZO in URL**) sold next to **client-agnostic** rhetoric, and at least **one catastrophic global rule sentence** if read literally (**docs-before-code unconditionally**).

None of those yet prove the architecture is rotten — they prove **governance debt is migrating from “ideas” into “policy surface area.”** Treat **doc fixes + registry discipline** as **blocking before** widening **implementation** beyond **8B.2 governance**.

---

## WHAT IS STRONG

**Freeze these principles; do not “refactor ethos” casually.**

1. **Thin client stance** codified repeatedly (`02_GLOBAL_RULES.md` §6, `13_CLIENT_AGNOSTIC_PERSISTENCE_CONTRACT_V1.md`, **8B.1B** closeout dossier): GAS constrained to HTTP transport + bounded pre-flight hygiene.
2. **Single persistence pathway narrative** frozen in contract V1 (`prepare_calculation → snapshot envelope → POST /api/kzo/save_snapshot → Supabase`).
3. **Stage split discipline**: **8B.1A** (API correctness / envelope) precedes **8B.1B** (thin adapter operator proof) — sane execution ordering; reduced coupling hallucinations.
4. **ID collision handling is explicit**: **8B.2 canonicalized to `TASK-2026-08B-013`** with **written rejection** of reusing **`012`** for normalization drafts — boring, necessary, mature.
5. **8B.2 decomposition (`2A–2E`)** mitigates “harden everything in one Cursor prompt” — **overlap rules**, ordering rationale, explicit anti-implementation fences.

---

## GOVERNANCE DRIFT

### MANDATORY GOVERNANCE Q&A

1. **Coherent Stage 1 → 8B.2?** **Mostly yes** — skeleton → MVP layers → frozen snapshot → persistence → adapter → governance gate. Weak spots below.
2. **Duplicate numbering / task continuity?** **`TASK-2026-08B-001`** umbrellas Stage **8B** while operative slices are **`011/012/013`**. Gap **`002–010`** is **unexplained in TASKS**. That vacuum invites **Normalizer `012` mis-assignment forever**.
3. **Idea Normalizer discipline?** **Improved retroactively** (handles + dossiers + decomposition). **Risk**: **handles multiply faster than master table clarity** (**many `STAGE_*` labels**) — readability rot.
4. **Governance bloat?** **Yes.** Overlapping dossiers (**pre-gate**, **normalized gate**, **decomposition**, Gemini preflights). **Indexing helps** (`00_AUDIT_INDEX`) but **CHANGELOG + NOW + IDEA log** duplicate facts.
5. **Audit history noise?** **Operational risk.** Long tail is acceptable **only** while **`00_AUDIT_INDEX` stays the spine**; unindexed fossils become lore.

### Hard contradictions (non-negotiable attention)

**A — Documentation before code (literal poison)**  

`docs/00_SYSTEM/02_GLOBAL_RULES.md` states that if **code contradicts documentation**, documentation is fixed **first**, then code. Taken literally this **inverts engineering reality** for security, correctness bugs, regulatory truth, persistence invariants — **documents must follow reality** when reality is objectively wrong.

**Governance implication:** Either **qualify** that rule (**exception classes**) or you’ve embedded a **known-false axiom** into the constitution.

**B — “Client agnostic” vs KZO-branded API surface**

`13_CLIENT_AGNOSTIC_PERSISTENCE_CONTRACT_V1.md` frames **platform persistence**, but the canonical save route is **`POST /api/kzo/save_snapshot`**. **Product coupling at the transport seam** is acceptable for MVP — **honesty required**: agnosticism is **path discipline**, not **URL cosmetics**.

**C — Module status header lag**

`docs/00-02_CALC_CONFIGURATOR/09_STATUS.md` opens with **Stage 4C** while enumerating **through 8A complete** in body — **stale narrative at fold one** → trust erosion for external readers.

**D — Data contracts debt call**

`TASK-2026-08B-001` expects **`04_DATA_CONTRACTS.md`** patch for persistence envelopes “when API is final” — **split-brain risk** versus **`13_CLIENT_AGNOSTIC_PERSISTENCE_CONTRACT_V1.md`** unless closed explicitly.

**E — Placeholder audit still referenced**

`TASK-2026-08B-001` lists `docs/AUDITS/YYYY-MM-DD_STAGE_8B_PLATFORM_PERSISTENCE_NOT_GAS_PERSISTENCE.md` — **unresolved template** while umbrella governance claims completeness. Micro-scale **registry dishonesty**.

---

## ARCHITECTURE DRIFT

### MANDATORY ARCHITECTURE Q&A

6. **Thin client law intact?** **On paper: yes. On repo mass: unverified line-by-line here.** **8B.1B** dossier is tight. A very large `gas/Stage3D_KZO_Handshake.gs` (**thousands of lines** in working tree) is **prima facie fatigue risk** — not proof of violation, but **cognitive coupling** unless mechanically enforced (**splitting**, policy checks).

7. **Hidden GAS privilege drift?** Primary vector is **convenience** (“just this once in the script”). Governance warns — **runtime defense is thin** absent automation.

8. **API overload?** Pressures: (a) **KZO-named route**; (b) **response envelope richness** (**failure** + legacy mirrors). Neither fatal today — watch **field creep**.

9. **Persistence modular?** **Reasonably** — validation + insert pathway described in TASKS. **Semantic coupling** to **V1 snapshot** dominates.

10. **KZO ↔ persistence dangerous coupling?** **Strategic**, not DDL: MVP snapshot is **KZO-shaped**. Survivable **if** “table = system, row = product” holds (**IDEA-0019** line). Failure: **-field creep disguised as stabilization** — pre-gate **FORBIDDEN** blocks it; enforcement is the job.

---

## OVERENGINEERING

1. **Label / stage-tag explosion** — traceability ↑, parsing cost ↑.
2. **Dual error channels** (`failure` + `error_code` mirror) — migration pragmatism; **needs sunset doctrine** or rots client coherence.
3. **Audit-heavy culture** — healthy if compressed; risky if substitutes for **small executable invariants** (outside current **8B.2 governance-only** pledge).

---

## UNDERENGINEERING

1. **`02_GLOBAL_RULES.md` truth ordering** — **must be fixed / qualified**.
2. **`TASK-2026-08B-*` numbering narrative** — **fill gaps or formally reserve**.
3. **`04_DATA_CONTRACTS.md`** vs **`save_snapshot` reality** — **align or defer with rationale**.
4. **Mechanical thin-GAS enforcement** — governance text ≠ linter.
5. **Idempotency / duplicate semantics** — **deliberately missing until 2A**; that is sequencing **correctness** plus **risk concentration**.

---

## STAGE 8B.2 DECOMPOSITION REVIEW

### Mandatory execution questions

11. **Decomposition correctness?** **Good.** Slices align with ambiguity clusters: replay/identity (**2A**), phased outcomes (**2B**), failure machine-readability (**2C**), integrity stance vs frozen **V1** (**2D**), neutrality verification (**2E**).

12. **Gaps?** **`request_id` / correlation vs DB uniqueness** deferred — OK **only** if **2A** anchors identifiers used across phases. Observability doctrine still light.

13. **Wrong sequencing?** **`2A→2B→2C→2D→2E` default stands.** Parallel **2D+2C** invites taxonomy thrash unless **failure classes** stabilize first.

14. **Oversized slices?** **2B** is the heavyweight scenario fan-out — mitigate by forbidding taxonomy sprawl inside **2B** (already intended; enforce).

15. **Cursor corridor safe?** **More safe after decomposition.** **Unsafe** if “governance sprint” stealth-includes API edits. **`PLANNED` must remain a hard latch.**

---

## RISK

### Mandatory risk questions

16. **Systemic blockers before 8B.2A “implementation thinking” spills into code**

    1. **Unwritten idempotency / duplicate doctrine** — largest operational trapdoor.
    2. **Literal doc-vs-code rule** — can mis-train autonomous agents catastrophically.
    3. **TASK-ID vacuum (`002–010`)** — repeated Normalizer collisions.
    4. **`/api/kzo/...` vs platform rhetoric** — manage expectations openly.
    5. **Data contracts vs live shapes** — split-brain for integrators.

17. **Biggest governance lie (harsh)**

    **Unqualified “documentation first when code contradicts docs.”**

18. **Most likely future architectural collapse vector**

    **Thickened GAS** + **second persistence shortcut** (**Sheet-as-truth**, **direct Supabase tooling**) justified as ops.

19. **Overengineering zones**

    Tag sprawl, permanent dual-error surfaces without sunset, uncompressed audit archaeology.

20. **Underdefined critical zones**

    **Replay matrices**, **duplicate acceptance criteria**, **client obligations after partial success**, **minimum machine-readable persistence error set**.

---

## TOP 10 CRITICAL FIXES

*(Governance / documentation / registry — **not product features**)*

1. **Rewrite / qualify** `02_GLOBAL_RULES.md` **doc-vs-code precedence** (**exceptions for objective wrongness / security / persistence invariants**).
2. **`TASK-2026-08B-*` map** — explain **001 vs 011** or **explicit ID reservation policy**.
3. **Fix lead paragraph** in `docs/00-02_CALC_CONFIGURATOR/09_STATUS.md` (**truth at first scroll**).
4. **Resolve `YYYY-MM-DD` placeholder audit** under **`TASK-2026-08B-001`** (real file or **explicit CANCELLED**).
5. **`04_DATA_CONTRACTS.md`** — persistence envelope subsection ** or **labeled DEFERRED** + pointer.
6. **Sunset doctrine** for mirrored error fields (**acceptance criteria**).
7. **Normalizer → TASK-ID checklist** (**diff against `docs/TASKS.md` before registry merge**).
8. **`13_CLIENT_AGNOSTIC_PERSISTENCE_CONTRACT_V1.md`**: one honest paragraph on **`/api/kzo/…` seam** (**MVP** vs posture).
9. **Label budget policy** (**primary canonical tag per milestone** optional rule).
10. **`8B.2A` output template** (mandatory headings: decisions, rejects, identifiers) — block essay drift.

---

## TOP 10 FALSE PROBLEMS

1. **“Too many audits”** — indexing + staleness control matters; counts don’t.
2. **“GAS exists ⇒ violation”** — wrong target; thickness is.
3. **“Must shard GAS file now”** — engineering hygiene unless violations proven.
4. **“Neutral web/mobile proof required for 8B.2 honesty”** — explicitly **off-lane**; don’t inflate scope.
5. **“Immediately mint TASK-014–018 for slices”** — often bureaucracy **unless parallelism demands**.
6. **“Rename endpoints before doctrine”** — theatre over substance for replay safety.
7. **“Gemini dossiers supersede TASKS”** — false hierarchy.
8. **“Bilingual changelog noise”** — operational annoyance architecture.
9. **“Supabase morally wrong because KZO-first”** — wrong; structure matters, not jealousy order.
10. **“Decomposition is wasted ceremony”** — false; prevents Cursor blast radius explosions.

---

## FINAL STAGE READINESS

**Can Stage 8B.2A begin safely?**

**YES — as pure governance authoring**, **provided**:

- **No silent TASK status escalation** (“small code fix”).
- **`02_GLOBAL_RULES.md` contradiction** patched **before** scaling agent autonomy.
- **Accept** that **2A** is the downstream trust anchor — weak **2A** makes **2B–2E** theatre.

**NO — as blended governance + patch** — that path collapses **8B.2** intent.

---

**CLOSURE.** **SAFE WITH FIXES.** The repo exhibits **surprising maturity** paired with **a few constitution-grade footguns.** Remove the footguns — **still without shipping new product scope.**

---

_End — GEMINI MASTER GOVERNANCE AUDIT (documentary critique; **no implementation**)._  
