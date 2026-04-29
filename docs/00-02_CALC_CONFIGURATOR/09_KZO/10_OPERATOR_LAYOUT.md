# KZO Operator Layout Governance (Stage 5D)

## Purpose

Define the **governance shell** for the KZO Google Sheets operator surface: fixed stage blocks, reserved future rows, and anti-overlap rules. This is **not** a UI redesign — it is continuity and readability architecture so Stage 6+ does not fragment the sheet.

**Formula (product line):** Structure → Scale → Topology → **Shell Governance** → Engineering expansion.

## Architecture roles (unchanged)

| Layer | Role |
| --- | --- |
| **API** | Engineering truth (calculations, summaries) |
| **GAS** | Transport only — read/write assigned ranges, no topology or layout logic |
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

**Stage 5B (`physical_summary`):** verified on **Render**; no separate operator Sheet block is defined in this MVP governance slice — scale remains API-visible unless a future TASK allocates a dedicated range.

## Reserved future zones (do not use until tasked)

Planning labels only — **no GAS/API writes** until a normalized TASK extends Stage 6/7.

| Label | Range | Intended use |
| --- | --- | --- |
| **STAGE_6_ENGINEERING** | **E27:F40** | Next engineering-expansion slice (blocked until Stage 5D governance accepted). |
| **STAGE_7_COMMERCIAL** | **E41:F54** | Later commercial/readout slice (blocked until tasked). |

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

Required fields for that future payload: **`layout_version`**, **`shell_structure_type`**, **`active_stage_zones`**, **`reserved_future_zones`**, **`block_growth_direction`**, **`anti_overlap_rules`**, **`interpretation_scope`**.

## API placement rule

The API must **never** dictate cell placement; placement is governance + GAS writeback contracts only.

## References

- KZO status: `docs/00-02_CALC_CONFIGURATOR/09_KZO/08_STATUS.md`
- IDEA: `IDEA-0011` in `docs/00_SYSTEM/12_IDEA_MASTER_LOG.md`
- Audit: `docs/AUDITS/2026-04-29_STAGE_5D_OPERATOR_LAYOUT_GOVERNANCE.md`
