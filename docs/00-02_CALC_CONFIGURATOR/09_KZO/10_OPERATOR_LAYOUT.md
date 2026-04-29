# KZO Operator Layout Governance (Stage 5D) — Stages 6A–6C shell & engineering layers

## Purpose

Define the **governance shell** for the KZO Google Sheets operator surface: fixed stage blocks, reserved future rows, and anti-overlap rules. This is **not** a UI redesign — it is continuity and readability architecture so Stage 6+ does not fragment the sheet.

**Formula (product line):** Structure → Scale → Topology → **Shell Governance** → **Shell activation (Stage 6A)** → **Classification (Stage 6B)** → **Burden foundation (Stage 6C)** → Later precision.

## Architecture roles (unchanged)

| Layer | Role |
| --- | --- |
| **API** | Engineering truth — **`engineering_class_summary`** (**Stage 6B**) derives from Stage 5A/5C summaries only; **`engineering_burden_summary`** (**Stage 6C**) derives from 6B + topology + structural flags — **no** kg/BOM/pricing |
| **GAS** | Transport / writeback to assigned ranges — Stage **6A** shell placeholder (**no** API engineering field); Stage **6B** maps API **`engineering_class_summary`** to **`E27:F40`** only; Stage **6C** maps **`engineering_burden_summary`** to **`E27:F40`** only — **no** burden math in GAS |
| **Sheet** | Governed operator shell — one approved block per stage |

## Shell model (MVP): `SHELL_VERTICAL_EXPANSION`

- **Growth direction:** downward only (`DOWNWARD_VERTICAL`).
- **Rule:** **one stage = one shell block** — fixed row boundaries, additive expansion into **reserved** zones only.
- **Not in scope for MVP:** hybrid shell, horizontal branching, dynamic repositioning, auto-collapse UI, adaptive dashboards.

## Active stage zones (`Stage4A_MVP`)

These ranges are **approved** for current operator writeback. GAS must write **only** inside the block assigned to that stage’s integration (see existing GAS constants).

| Logical block | A1 range | Notes |
| --- | --- | --- |
| **STAGE_5A_STRUCTURE** | **E4:F20** | Structural / output integration: implementation uses `E4:F19` plus row **`E20:F20`** for flags — together they occupy rows **4–20** (one governance block). |
| **STAGE_5C_TOPOLOGY** | **E21:F26** | Topology thin writeback (`physical_topology_summary`). |
| **STAGE_6A_RESERVED_SHELL** | **E27:F40** | **Stage 6A** — shell infrastructure placeholder (`stage6_*` logs / optional placeholder rows before 6B). |
| **STAGE_6B_ENGINEERING_CLASS** | **E27:F40** | **Stage 6B** — **`engineering_class_summary`** (**`runStage6BEngineeringClassificationFlow()`**). |
| **STAGE_6C_ENGINEERING_BURDEN** | **E27:F40** | **Stage 6C** — **`engineering_burden_summary`** (**`runStage6CEngineeringBurdenFlow()`**). Running **6B** or **6C** overwrites the **same** governed band (`E41:F54` remains untouched). |

**Stage 5B (`physical_summary`):** verified on **Render**; no separate operator Sheet block is defined in this MVP governance slice — scale remains API-visible unless a future TASK allocates a dedicated range.

## Reserved future zones

| Label | Range | Status |
| --- | --- | --- |
| **STAGE_6_ENGINEERING** (6B classification / 6C burden — same band, alternate writebacks) | **E27:F40** | **Stage 6B / 6C:** API emits **`engineering_class_summary`** / **`engineering_burden_summary`**; **Stage 6A** prerequisite for shell semantics. |
| **STAGE_7_COMMERCIAL** | **E41:F54** | Reserved — **no** GAS writes until tasked. |

## Stage 6A — GAS-only shell summary (not an API field in 6A)

Target shape for **logs / contract reference** (built in GAS as `buildStage6OperatorShellSummary_()`; **not** added to `prepare_calculation` response in Stage 6A):

```json
{
  "stage6_operator_shell_summary": {
    "shell_block_version": "KZO_STAGE_6A_OPERATOR_SHELL_V1",
    "reserved_range": "E27:F40",
    "shell_status": "ACTIVE_RESERVED_BLOCK",
    "shell_activation_date": "YYYY-MM-DD",
    "shell_type": "SHELL_VERTICAL_EXPANSION",
    "interpretation_scope": "SHELL_ONLY_NO_ENGINEERING"
  }
}
```

**Shell status states (normative):** `RESERVED_DOC_ONLY` → `ACTIVE_RESERVED_BLOCK` (Stage 6A target) → `STAGE_6_ENGINE_ENABLED` (future; not used in 6A).

**GAS entry points:** `runStage6AActivateReservedOperatorBlockFlow()` (placeholder writeback + telemetry), `runStage6AResetReservedOperatorBlockOnly()` (clears **E27:F40** only).

## Stage 6B — `engineering_class_summary` (API + thin GAS)

API returns **`data.engineering_class_summary`** on success (see `main.py` `_build_kzo_engineering_class_summary`). Interpretation **`ENGINEERING_CLASSIFICATION_ONLY_MVP`** — no BOM, kg, thermal, CAD, pricing.

GAS **`runStage6BEngineeringClassificationFlow()`** maps fields to **`E27:F40`** (same Stage 6 band as 6A; 6B run overwrites placeholder when used).

Illustrative shape:

```json
{
  "engineering_class_summary": {
    "classification_version": "KZO_STAGE_6B_ENGINEERING_CLASS_MVP_V1",
    "lineup_complexity_class": "STANDARD",
    "lineup_scale_class": "LARGE",
    "section_complexity_profile": ["STANDARD", "STANDARD"],
    "total_cells_basis": 22,
    "topology_basis": "TOPOLOGY_BALANCED_SPLIT",
    "interpretation_scope": "ENGINEERING_CLASSIFICATION_ONLY_MVP"
  }
}
```

## Stage 6C — `engineering_burden_summary` (API + thin GAS)

API returns **`data.engineering_burden_summary`** on success (`_build_kzo_engineering_burden_summary`). Interpretation **`ENGINEERING_BURDEN_ONLY_MVP`** — **`estimated_mass_class`** is burden-tier semantics only (**not kg**).

GAS **`runStage6CEngineeringBurdenFlow()`** maps fields to **`E27:F40`** (overwrites sheet content in this band — rerun 6B if classification rows must appear on-sheet).

Illustrative shape:

```json
{
  "engineering_burden_summary": {
    "burden_version": "KZO_STAGE_6C_ENGINEERING_BURDEN_MVP_V1",
    "structural_burden_class": "BURDEN_STANDARD",
    "assembly_burden_class": "ASSEMBLY_STANDARD",
    "estimated_mass_class": "MASS_HEAVY",
    "complexity_basis": "COMPLEXITY_STANDARD",
    "topology_basis": "TOPOLOGY_BALANCED_SPLIT",
    "footprint_basis": "SCALE_LARGE",
    "interpretation_scope": "ENGINEERING_BURDEN_ONLY_MVP"
  }
}
```

## Minimum governance rules

1. **Fixed zone per approved stage** — boundary strings are immutable without a TASK and audit.
2. **Reserved zones before use** — future stages consume only predefined rows.
3. **No overwrite upward** — a later stage must not relocate or overwrite an earlier approved block.
4. **No block drift** — expansion is **additive**; no retroactive shell fragmentation.
5. **Growth = additive only** — new content moves **down** into reserved bands.

## Anti-overlap rules (normative text)

- No stage may overwrite a prior approved zone.
- Each stage receives a fixed row boundary.
- Expansion only into **reserved** zone rows.
- No retroactive shell fragmentation.

## Target payload (future API contract reference)

**Strict (this stage):** no API implementation — documentation only.

When a future TASK emits **`operator_layout_governance_summary`**, shape should align with:

```json
{
  "operator_layout_governance_summary": {
    "layout_version": "kzo_operator_shell_mvp_v0.1",
    "shell_structure_type": "SHELL_VERTICAL_EXPANSION",
    "active_stage_zones": {
      "STAGE_5A_STRUCTURE": "E4:F20",
      "STAGE_5C_TOPOLOGY": "E21:F26"
    },
    "reserved_future_zones": {
      "STAGE_6_ENGINEERING": "E27:F40",
      "STAGE_7_COMMERCIAL": "E41:F54"
    },
    "block_growth_direction": "DOWNWARD_VERTICAL",
    "anti_overlap_rules": [
      "No stage may overwrite prior approved zone",
      "Each stage receives fixed row boundary",
      "Expansion only into reserved zone",
      "No retroactive shell fragmentation"
    ],
    "interpretation_scope": "Operator sheet shell governance only",
    "basis": "KZO MVP operator continuity"
  }
}
```

Required fields for that future payload: **`layout_version`**, **`shell_structure_type`**, **`active_stage_zones`**, **`reserved_future_zones`**, **`block_growth_direction`**, **`anti_overlap_rules`**, **`interpretation_scope`**, **`basis`**.

## API placement rule

The API must **never** dictate cell placement; placement is governance + GAS writeback contracts only.

## References

- KZO status: `docs/00-02_CALC_CONFIGURATOR/09_KZO/08_STATUS.md`
- IDEA: **`IDEA-0011`** (Stage 5D), **`IDEA-0012`** (Stage 6A), **`IDEA-0013`** (Stage 6B), **`IDEA-0014`** (Stage 6C) in `docs/00_SYSTEM/12_IDEA_MASTER_LOG.md`
- Audits: `docs/AUDITS/2026-04-29_STAGE_5D_OPERATOR_LAYOUT_GOVERNANCE.md`; verification closure: `docs/AUDITS/2026-04-29_STAGE_5D_GOVERNANCE_VERIFICATION_GATE.md`; Stage 6A: `docs/AUDITS/2026-04-29_STAGE_6A_RESERVED_BLOCK_ACTIVATION.md`; Stage 6B: `docs/AUDITS/2026-04-29_STAGE_6B_ENGINEERING_CLASSIFICATION.md`; Stage 6C: `docs/AUDITS/2026-04-29_STAGE_6C_ENGINEERING_BURDEN_FOUNDATION.md`
