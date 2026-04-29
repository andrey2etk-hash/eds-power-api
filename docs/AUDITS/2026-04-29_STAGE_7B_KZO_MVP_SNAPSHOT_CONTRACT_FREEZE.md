# Stage 7B — KZO MVP snapshot contract freeze (audit)

## Purpose

Architecture gate **“freeze before persistence.”** **`Stage 7A`** proves **execution** (**one successful run yields one cohesive operator-visible surface**). **`Stage 7B`** answers: **what exact object is canonical** for **trust and audit** before **Stage 8A** (Supabase or any DB) **materializes** rows.

**Verdict framing:** Without a frozen snapshot contract, persistence risks **schema drift**, **retroactive migrations**, and **API/GAS/document inconsistency**.

---

## Scope (Stage 7B)

| Delivered | Description |
| --- | --- |
| Canonical contract | **`KZO_MVP_SNAPSHOT_V1`** — see **`docs/00-02_CALC_CONFIGURATOR/09_KZO/11_KZO_MVP_SNAPSHOT_V1_CONTRACT.md`** |
| Required field list | Locked in contract table + JSON scaffold |
| Versioning policy | **`snapshot_version`** vs product **`logic_version`** — orthogonal, monotonic snapshot labels |
| Success / failure envelopes | **`run_status`** **`SUCCESS`** / **`FAILED`** with minimum **`FAILED`** shape |
| Stage 8A hand-off | Explicit: V1 blob is source object for persistence design — **no** Stage 8A implementation in Stage 7B |

---

## Forbidden (explicit)

- Supabase tables, SQL, migrations, deployment  
- New **`prepare_calculation`** parameters or engineering maths  
- Required inclusion of BOM, pricing, procurement, DB IDs, revision graph in **`KZO_MVP_SNAPSHOT_V1`**

---

## Governance status

**Anti-drift rule:** Anything **not** in **`KZO_MVP_SNAPSHOT_V1`** does **not** belong as a **mandatory persisted field** in **Stage 8A** unless a **new snapshot version** and **IDEA** introduce it.

**Sequence:**

1. **7A** — Operational unified MVP flow (**trusted run**).
2. **7B** — **Canonical snapshot contract freeze** (**trusted object**).
3. **8A** — Persistence MVP (**trusted storage**) — **only after 7B**.

---

## Success condition

One **successful** KZO MVP run maps to **one** **`KZO_MVP_SNAPSHOT_V1`** object with **`run_status: "SUCCESS"`** and all required layers populated from validated **`prepare_calculation`** **`data`**.

---

## References

- **`docs/00-02_CALC_CONFIGURATOR/09_KZO/11_KZO_MVP_SNAPSHOT_V1_CONTRACT.md`**
- **`docs/00_SYSTEM/12_IDEA_MASTER_LOG.md`** — **IDEA-0016**

---

## External Gemini audit — **PASS**

Independent auditor (Gemini) review of snapshot contract alignment with **`prepare_calculation`** MVP outputs and governance boundaries (see **`docs/AUDITS/2026-04-29_STAGE_7B_GEMINI_EXTERNAL_AUDIT_REQUEST.md`** for prompt context).

**Recorded verdict:** **`SAFE TO PROCEED TO STAGE 8A`** — persistence planning / implementation may proceed **only** under a **separate normalized IDEA + TASK** that **persists `KZO_MVP_SNAPSHOT_V1` as frozen** (no contract redesign in Stage 8A scope).

---

## Formal closure (Stage 7B — doc-pass)

**Stage 7B — KZO MVP Snapshot Contract Freeze** is **governance-closed**:

- **`KZO_MVP_SNAPSHOT_V1`** normative text is **frozen** (`11_KZO_MVP_SNAPSHOT_V1_CONTRACT.md`); **no field changes** via hotfix — only a **future** **`KZO_MVP_SNAPSHOT_V2`** (or later) plus **IDEA** may extend the contract.
- Verified MVP output layers in V1: **`structural_composition_summary`**, **`physical_summary`**, **`physical_topology_summary`**, **`engineering_class_summary`**, **`engineering_burden_summary`**, plus envelope fields (**`snapshot_version`**, **`run_status`**, **`timestamp_basis`**, **`logic_version`**, **`request_metadata`**, **`normalized_input`**) and **SUCCESS** / **FAILED** shapes.
- **`IDEA-0016`** master **Status** remains **`IMPLEMENTED`** (canonical; **no new Status Values**).

**Strategic rule:** **Stage 7B = CLOSED.** **Stage 8A = NOT STARTED** until a **separate** normalized **IDEA + TASK**. Stage **8A** must **implement persistence of frozen V1 only** — not redesign or expand the MVP contract inside persistence work.
