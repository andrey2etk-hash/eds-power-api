# 1. Stage title

**Stage 8B.2A — Idempotency / duplicate-request governance doctrine**

| Field | Value |
| --- | --- |
| **Normative slice** | **`STAGE_8B_2A_IDEMPOTENCY_DUPLICATE_GOVERNANCE`** |
| **Parent TASK** | **`TASK-2026-08B-013`** (**`ACTIVE`**) · **IDEA-0023** |
| **Decomposition** | **`docs/AUDITS/2026-04-30_STAGE_8B_2_GOVERNANCE_SUBSTAGES_DECOMPOSITION.md`** (slice **`2A`**) |
| **Pre-gate** | **`docs/AUDITS/2026-04-30_STAGE_8B_2_PRE_GATE_SCOPE.md`** |
| **Primary canon rule** | Full doctrine text for **`2A`** lives here under **`docs/AUDITS/`** — **not** yet distilled into **`00_SYSTEM/`** (see §14). |
| **Label** | **`STAGE_8B_2A_DOCTRINE_PUBLISHED`** · focused Gemini **`STAGE_8B_2A_GEMINI_FOCUSED_AUDIT_PASS`** — **`docs/AUDITS/2026-04-30_GEMINI_STAGE_8B_2A_FOCUSED_AUDIT.md`** |

---

# 2. Purpose

Establish **bounded governance language** so the platform may later implement **repeat-safe persistence** **without**:

- collapsing **replay** vs **distinct submission** semantics,
- letting any client silently “decide” **duplicate vs new** outside **API authority**,
- multiplying persisted rows where the **intent** was **one logical save** (**double-commit / UX contradiction**),

while **deferring**: wire formats, schemas, transports, **`error_code` maps**, prepare/save edge matrices — **2B** onward.

---

# 3. Core risk blocked

| Risk | What **2A** prevents at doctrine level |
| --- | --- |
| **Semantic split-brain** | Same operator story interpreted as either “retry” or “new job” **without documented rules**. |
| **Client-side duplicate arbitration** | Any client asserting **truth of persistence** (**insert / reject / unify**) independently of orchestrated API response. |
| **Repeat-unsafe narration** | **Transport retry**, **replay**, **re-submit** confused with **fresh calculation path** — unbounded duplication or false **SUCCESS** ambiguity. |
| **Premature constitutional lock-in** | Pushing half-baked idioms into **`00_SYSTEM`** before **focused external critique** (**§15**). |

---

# 4. Definitions

Governance meanings only; **physical identity** (**headers, columns, uniqueness keys**) **deferred** to implementation tasks.

| Term | Definition |
| --- | --- |
| **`request_id`** | **Logical correlation handle** for an **end-to-end persistence attempt** in the canonical narrative **`prepare_calculation` → `KZO_MVP_SNAPSHOT_V1` → `save_snapshot`**. **Grounding** for “same stewardship thread” vs “new thread” **appeals to fields already normative** in **`11_KZO_MVP_SNAPSHOT_V1_CONTRACT`** and prepare response metadata — **no new wire mandate in this dossier**. |
| **Duplicate request** | A submission whose **governance predicate** **D** holds (see duplicate matrix **D-01–D-04**, §14): the platform **may** treat it as **continuation of one logical operation** rather than a **distinct** new persistence obligation — **subject to API authority** and later machine-readable signaling (**2C**). |
| **Replay** | Client or operator asserts **continuation** of a **prior logical submission** (**same stewardship intent**): not automatically a **new** business persistence event. Distinguished from **intentionally new payload** (**distinct attempt**) and from **neutral transport retry** of the **same** submission envelope where **intent** unchanged. |
| **Idempotent-safe** (**governance**) | Repeated or parallel attempts that **would** **not**, under accepted doctrine and future implementation, yield **incorrect extra durable facts** (**second row meaning “new calculation”**) when **predicate D** applies — i.e. **repeat-safety as an outcome posture**, not yet a claimed implementation property. |

---

# 5. Allowed governance

- **Doctrine text** under **`docs/AUDITS/`** (**this dossier**) as **primary canon for slice `2A`** until amended under **`TASK-013` / CHANGELOG** after Gemini cycle.
- **Request-identity doctrine** (§4): logical operation anchored to **bounded MVP snapshot semantics**.
- **Duplicate definition** via **predicate matrix** (**§14**) — extend **only versioned** inside **`TASK-013`**.
- **Replay boundary language** (§4 · §14) at **high level**; orphan / prepare-vs-save granularity → **2B**.
- **Acceptance vs failure doctrine** (**§§7–8**) using **classes** (**not** `error_code`).
- References to **`13_CLIENT_AGNOSTIC_PERSISTENCE_CONTRACT_V1`** and **`11_KZO_MVP_SNAPSHOT_V1_CONTRACT`** as **existing anchors** — **without** patching those files in **`2A`**.

---

# 6. Forbidden

- **`main.py`**, **`gas/`**, **routes**, **DB** / DDL / migrations · **retry workers** · **queues** — under **`2A` lane**.
- **Mandating** specific transports (**e.g.** named duplicate-key headers), **unique constraints**, or **retry engine semantics** — **implementation**, not **`2A`**.
- **`prepare_calculation ↔ save_snapshot` outcome grids** (**split outcome contract**) — **2B**.
- **`error_code` / machine-readable taxonomy** — **2C**.
- **Second authoritative `2A` dossier** — **exactly one** canon file pattern **`…STAGE_8B_2A_*`** for this slice.
- **Semantic abuse:** issuing a **fresh** logical identity **only** to bypass duplicate/replay doctrine (**governance outlaw** narrative).

---

# 7. Acceptance states

Governance-only **categories** (**implementation maps later**, **2C**):

| Class | Meaning |
| --- | --- |
| **`CLASS_ACCEPT_DISTINCT`** | Platform accepts work as **genuinely new** logical persistence (**new durable fact** justified). |
| **`CLASS_TREATED_AS_DUPLICATE_INTENT`** | Platform treats submission as aligned with **already satisfied** logical operation (**repeat-safety posture** intended). |
| **`CLASS_REJECT_CLIENT_AMBIGUITY`** | Identity / payload story **insufficient or contradictory**; **no** silent merge into **SUCCESS** pretending a clean new row (**policy: reject ambiguity**). |

---

# 8. Failure states

Governance (**not** coded errors):

| State | Narrative |
| --- | --- |
| **Rejected — ambiguity** | Maps to **`CLASS_REJECT_CLIENT_AMBIGUITY`**; operator must reconcile (**thin client surfaces API truth only** — §10). |
| **Rejected — integrity breach** | Snapshot or contract contradiction (**detailed layering** ⇢ **2D** overlap; **`2A` only asserts** rejection is valid **policy surface** when doctrine cannot unify intent). |
| **Policy fork unresolved** | E.g. **D-02** default (**distinct**) vs alternate product stance — documented as **explicit sign-off deferred** (**§11**); **until closed**, default stands. |

---

# 9. Client-neutral rule

Any **present or future client** (**GAS**, web, mobile, agent) **consumes the same orchestrated semantics**: **duplicate / replay / idempotent-safe** distinctions are **resolved at API orchestration**, not via **adapter-specific persistence truth**. **`2A`** does **not** specify per-client quirks.

---

# 10. Thin client rule

Clients **transport** payloads and **surface** **`status`**, **`failure`**, ids, timestamps per existing contracts — **they do not** author final **duplicate vs accept** decisions **independent of** API responses. **Sheet / UI** remain **display truth**, not **system of record** for persistence arbitration.

---

# 11. Deferred

| Item | Owner slice / channel |
| --- | --- |
| **Prepare/save orphan semantics**, phase edges | **`2B`** |
| **`error_code` / response field binding** | **`2C`** |
| **Transport keys, HTTP headers, DB uniqueness** | Explicit **implementation TASK** (**post-governance**) |
| **Distilled constitutional excerpt in `00_SYSTEM/`** | **After** Gemini **PASS** · **explicit TASK** (**e.g.** **`04_DATA_CONTRACTS.md`** patch) |

---

# 12. Success condition

- **`TASK-013`** remains **`ACTIVE`**; slice **`8B.2A`** doctrinal text **complete** in **this file** (**§§1–15**).
- **Focused Gemini** audit executed per **`docs/AUDITS/2026-04-30_GEMINI_STAGE_8B_2A_FOCUSED_AUDIT_REQUEST.md`** with lodged closeout **`docs/AUDITS/2026-04-30_GEMINI_STAGE_8B_2A_FOCUSED_AUDIT.md`** (**`PASS WITH DOC FIXES`** applied **in dossier** **2026-04-30**) → registry label **`STAGE_8B_2A_GEMINI_FOCUSED_AUDIT_PASS`**.

---

# 13. Failure condition

- Proceeding to **`2B`** **without** Gemini closeout (**§12**) — **blocked**.
- Sneaking implementation (**code / DDL / transports**) under **`2A` banner — **blocked** (**§6**).

---

# 14. Stage boundary

- **`2A` ends with:** frozen governance text + **accepted** Gemini outcome (**DOC FIXES** allowed **within this dossier**).
- **`2A` does not** ship **constitutional `00_SYSTEM` migration** (**§11**).
- Duplicate matrix (**authoritative governance rows**, version inside **`TASK-013`**):

| ID | Scenario | Target classification | Note |
| --- | --- | --- | --- |
| **D-01** | Repeated **`request_id`** in applicable context | Duplicate / continuity | Align with **`request_id`** semantics in existing contracts |
| **D-02** | New **`request_id`**, snapshot body **materially identical** | **Distinct by default** (recommended) until explicit product exception | Update row only after **signed** governance change |
| **D-03** | Any snapshot layer differs | **Distinct** by default | |
| **D-04** | Transport retry (**same** submission intent) | Align with **initial** logical operation (**no** double “new success” lie) | |

---

# 15. Next dependency (**2B**)

1. Focused Gemini audit lodged — **`docs/AUDITS/2026-04-30_GEMINI_STAGE_8B_2A_FOCUSED_AUDIT.md`** (**`PASS WITH DOC FIXES`**; doc fixes applied **same date**) → **`STAGE_8B_2A_GEMINI_FOCUSED_AUDIT_PASS`**
2. **Then:** **`STAGE_8B_2B_PREPARE_SAVE_SPLIT_OUTCOME_GOVERNANCE`** — prepare/save **split outcome** doctrine (**separate dossier**).

---

_Amendment:_ **§§4–8, §14 matrix** after initial Gemini **PASS** — **explicit** repo edit + **`TASK-013` / `CHANGELOG` note** — **no silent drift._

_End._
