# 1. Stage title

**Stage 8B.2B — Prepare / Save split outcome governance doctrine**

| Field | Value |
| --- | --- |
| **Normative slice** | **`STAGE_8B_2B_PREPARE_SAVE_SPLIT_OUTCOME_GOVERNANCE`** |
| **Parent TASK** | **`TASK-2026-08B-013`** (**`ACTIVE`**) · **IDEA-0023** |
| **Upstream slice** | **`STAGE_8B_2A_IDEMPOTENCY_DUPLICATE_GOVERNANCE`** — closed **by reference only** (**§5**) · **`docs/AUDITS/2026-04-30_STAGE_8B_2A_IDEMPOTENCY_DUPLICATE_GOVERNANCE.md`** |
| **Decomposition** | **`docs/AUDITS/2026-04-30_STAGE_8B_2_GOVERNANCE_SUBSTAGES_DECOMPOSITION.md`** (slice **`2B`**) |
| **Pre-gate** | **`docs/AUDITS/2026-04-30_STAGE_8B_2_PRE_GATE_SCOPE.md`** |
| **Primary canon (`2B` segment)** | This file under **`docs/AUDITS/`** — **not** distilled into **`00_SYSTEM/`** (same discipline as **`2A`**) unless **explicit TASK** after acceptance |
| **Label** | **`STAGE_8B_2B_DOCTRINE_PUBLISHED`** (authored dossier · **awaits focused Gemini audit** · §15) |

---

# 2. Purpose

Establish **governance-safe** language for **split execution** across:

**`prepare_calculation`** (**phase `P`**) · **`save_snapshot`** (**phase `S`**)

so that **later implementation** may preserve **persistence trust** under **phased orchestration**:

- phased success/failure meanings are **articulated**, not implied,
- **orphan narratives** (prepare looks “usable” while persistence lineage is ambiguous) are **bounded**,
- **replay after partial outcomes** aligns with **duplicate/replay doctrine** (**`2A`**) **without this slice redefining** identity.

**Not in scope:** how responses are coded (**`2C`**), integrity rule catalog (**`2D`**), or any runnable path.

---

# 3. Core risk blocked

| Risk | What **`2B`** blocks at doctrine level |
| --- | --- |
| **Orphan ambiguity** | “Something succeeded somewhere” → clients or Sheets **silently invent** persisted truth. |
| **Phase conflation** | Treating **`P` outcome alone** as equivalent to **compound persistence completion**. |
| **Retry without stewardship** | Re-entering **`S`** or **`P`** **without** documented phase-eligibility vs **`2A`** (**§§9–10**). |
| **`2C`/`2D` bleed** | Machine error tables (**`2C`**) or integrity redesign (**`2D`**) disguised as split-outcome clarification. |

---

# 4. Definitions (**governance**)

Governance meanings only · **Wire field lists, HTTP semantics, DDL** deferred to **implementation TASKs**.

| Term | Definition |
| --- | --- |
| **Phase `P`** | **`prepare_calculation`** bounded API step that yields **calculated artifact + metadata** usable (when governance-success applies) **as input narrative** for **`save_snapshot`** — **does not imply** persisted row existence. |
| **Phase `S`** | **`save_snapshot`** bounded API step that authorizes (**when governance-success applies** under future implementation) durable snapshot persistence **through API** (**`docs/00_SYSTEM/13_CLIENT_AGNOSTIC_PERSISTENCE_CONTRACT_V1.md`** lineage). |
| **Compound persistence story** | **Both** **`P` governance-success** **and** **`S` governance-success** inside **one orchestrated stewardship thread** — doctrinal anchor for **full persistence success** (**no DB wording** here). |
| **Partial phased success** | **`P`** governance-success **plus** **`S` governance-non-success** (**or unattributable / uncertain `S` outcome for that thread**) — persistence story **must not** collapse to **compound completion**. |
| **Governance orphan** | Stewardship posture where partial phased outcomes meet **ambiguous authority** (“did persistence land for this thread?”). Doctrine: **steady ambiguity is unacceptable**; reconciliation obligation surfaces via API truth (**thin client**) — **`2C`** binds **surface shape** later. |
| **Phase authority** | **API response per phase** is authoritative for whether **that phase’s governance outcome applies** · clients **do not infer** **`S`** completion from **`P`** alone. |

**`2A` terms** (**replay**, **duplicate**, **predicate D**, **idempotent-safe**): normative glossary **outside** **`2B`** (**§5**).

---

# 5. Relationship to **8B.2A** (**reference-only**)

- **`request_id`**, **duplicate predicate D**, **replay**, **`CLASS_*`** outcomes (**acceptance lineage**): **normative meanings** · **`docs/AUDITS/2026-04-30_STAGE_8B_2A_IDEMPOTENCY_DUPLICATE_GOVERNANCE.md`**.
- **`2B`** **assigns**: **phase outcome composition**, **replay eligibility after partial phased outcomes**, **orphan-prevention posture** — **assuming** **`2A`** unchanged.
- **`2B`** **does not amend** **`2A`** matrix rows or glossary **except** through **explicit** **`TASK` / dossier amendment** outside this file.

---

# 6. Allowed governance (**`2B` only**)

- **Phase-state doctrine** (**§8**) — compound vs partial **governance tags** (**no** **`error_code`** here — **`2C`**).
- **Persistence phase definitions** (**§4**).
- **Retry governance boundaries** at **`P`/`S` boundary** (**§§9–10**) — narratives only.
- **Orphan doctrine** (**§10**).
- **Client-neutral phased rules** (**§11**).

---

# 7. Forbidden (**`2B` lane** · hard stop)

| Category | Forbidden |
| --- | --- |
| **Implementation** | **`main.py`**, **`gas/`**, **`kzo_snapshot_persist.py`**, routes, SQL/DDL |
| **API redesign** | New mandatory parameters, contract shape bifurcation |
| **`2C` intrusion** | Stable **`error_code`** maps, machine taxonomy tables, normative **`failure`** JSON appendix |
| **`2D` intrusion** | **`KZO_MVP_SNAPSHOT_V1`** layer inflation, integrity catalog as **rewrite** herein |
| **Infra disguise** | **Async**, **queues**, failed-persistence subsystem |
| **Second competing `2B` dossier** | **Exactly one** canonical pattern **`…STAGE_8B_2B_*`** for slice **`2B`** |

---

# 8. Phase outcome taxonomy (**split outcomes**)

**Governance tags** (below) are **labels only** · **implementation** maps them · **`2C`** binds **machine-readable** shape.

| Tag | Narrative shorthand | Stewardship gist |
| --- | --- | --- |
| **`COMPOUND_OK`** | **`P` ok · `S` ok** | **Trusted compound persistence completion** · **`snapshot_id` / timestamps** surfaced **only** per **authenticated API success story** (**thin client**). |
| **`PARTIAL_PS`** | **`P` ok · `S` attempted · `S` not governance-success OR uncertain attribution** | **Explicit partial** — **must not pretend **`COMPOUND_OK`**. |
| **`BLOCKED_S`** | **`P` governance-fail** | **`save_snapshot` blocked** along that thread (**do not pretend** same artifact can **`S`**-complete **without fresh sanctioned `P`** path). Narrative constraint **only**. |
| **`NOT_ATTEMPTED_S`** | **`P` lineage never reached sanctioned `S` attempt boundary** | **Neutral** "`S` not legitimately underway" — **not** hidden **`PARTIAL_PS`**. |

### Quadrant anchors (**explicit tie to IDEA brief**)

| Operator story (**plain**) | Primary tag |
| --- | --- |
| Prepare success · Save success | **`COMPOUND_OK`** |
| Prepare success · Save fail | **`PARTIAL_PS`** |
| Prepare fail · Save blocked | **`BLOCKED_S`** |
| Replay after partial (**§9**) | **Eligible only under **`2A`** + stewardship narrative** (**never** implicit **`COMPOUND_OK`**) |

---

# 9. Replay after partial success (**boundary with **`2A`**)

1. **`COMPOUND_OK`:** **`S`** leg satisfied — **`2A`** governs duplicates/replays (**`CLASS_*`**) · **`2B` does not re-decide**.
2. **`PARTIAL_PS`:** **`S`** incomplete or failed-attributability — **`2A`** distinguishes **same-intent retry of phase `S`** vs **`CLASS_REJECT_CLIENT_AMBIGUITY`** vs **distinct new **`P`** thread** · **`2B`** forbids silently upgrading to **`COMPOUND_OK`**.
3. **`BLOCKED_S`** / **`NOT_ATTEMPTED_S`:** **`S`** is **not legitimised** by **`P` alone`; **replay** ⇒ **normally** new sanctioned **`P`** first (**salvage** narratives ⇒ **implementation** / **`2C`** only).

---

# 10. Orphan prevention boundaries

| Rule | Doctrine |
| --- | --- |
| **Authority** | Surfaces (**Sheet/UI**) **reflect API phase authority**, not synthesized persistence. |
| **Forbidden UX doctrine** | **No “happy persistence” anchored only on `P`** when **`PARTIAL_PS`** / **`BLOCKED_S`**. |
| **Ambiguity** | Thread ambiguity aligns with **`CLASS_REJECT_CLIENT_AMBIGUITY`** (**`2A`**) · **`2C`** supplies **parsable manifestation** (**deferred**) |

---

# 11. Client-neutral phased contract

- **`P`/`S` semantics attach to generic client adapters** (**GAS** is first exemplar · **no GAS-exclusive phase authority**).
- Transport quirks (**timeouts, quotas**) ⇒ **implementation TASK** · **`2B`** cites **`13_CLIENT_AGNOSTIC_PERSISTENCE_CONTRACT_V1.md`** by **intent alignment** only.

---

# 12. Deferred (**owner**)

| Item | Owner |
| --- | --- |
| **`error_code`**, machine **`failure`** shape | **`2C`** |
| Integrity rules (**blocking `P` vs `S`**) | **`2D`** |
| Backoff counts, keyed idempotency transport | Post-governance **implementation TASK** |

---

# 13. Success condition (**`2B`**)

- This dossier (**§§1–15**) lodged as **single **`2B`** canon** (**`TASK-013`**, **`CHANGELOG`**).
- Focused Gemini **`2B`** audit → **`STAGE_8B_2B_GEMINI_FOCUSED_AUDIT_PASS`** (or DOC FIX **only** herein).

---

# 14. Failure condition (**`2B`**)

| Failure | Result |
| --- | --- |
| Open **`2C`** dossier **without** **`2B`** Gemini closeout (**§13**) | **blocked** |
| Redefining **`2A`** identity/matrix **within this file** (outside **§5** pointer) | **blocked** |
| Embedding **`error_code`** / **`2D`** integrity catalog herein | **blocked** |

---

# 15. Stage boundary (**`2B`**) · next (**`2C`**)

**`2B` ends with:**

- §§**8–11** frozen · overlap guard (**§§5, 14**) · Gemini disposition (**§13**).

**Mandatory sequencing:**

1. **Focused Gemini 8B.2B** audit — **`docs/AUDITS/2026-04-30_GEMINI_STAGE_8B_2B_FOCUSED_AUDIT_REQUEST.md`**
2. **`STAGE_8B_2C_MACHINE_READABLE_PERSISTENCE_ERROR_DOCTRINE`** — **separate dossier**.

---

_Amend post-Gemini **PASS**: explicit **`CHANGELOG`/`TASK`** note for edits to **§§5–11, §8**._

_End._
