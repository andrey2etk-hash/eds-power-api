# Stage 6B — Engineering classification MVP

## Date

2026-04-29

## Principle

**Classification before precision.** Planning-grade labels only — no mass, BOM, price, thermal, procurement, or CAD.

## API

- Response field: **`data.engineering_class_summary`** (built in `main.py` alongside structural / topology summaries).
- Envelope: **`classification_version`**, **`lineup_complexity_class`**, **`lineup_scale_class`**, **`section_complexity_profile`**, **`total_cells_basis`**, **`topology_basis`**, **`interpretation_scope`** = `ENGINEERING_CLASSIFICATION_ONLY_MVP`.

## Classification domains

- **Complexity tier:** `LIGHT` | `STANDARD` | `HEAVY` | `EXTENDED` (overall lineup heuristic from topology unevenness, section count, structural flags).
- **Scale tier:** `COMPACT` (≤8 cells) | `STANDARD` (9–16) | `LARGE` (17–26) | `EXTENDED` (27+).
- **Section profile:** per-section `LIGHT`/`STANDARD`/`HEAVY` from section cell counts.

## GAS

- **`runStage6BEngineeringClassificationFlow()`** — thin writeback **`E27:F40`** only; no recomputation of classes in Sheets.
- Reuses Stage 6 shell band (**overwrites** Stage 6A placeholder rows when Stage 6B flow runs).

## Forbidden

Mass, BOM, pricing, CAD, DB, Sidebar, formulas in GAS beyond mapping.

## Verdict

**PASS** — first engineering-intelligence bridge without violating KZO MVP governance chain.

## References

- `docs/00-02_CALC_CONFIGURATOR/09_KZO/10_OPERATOR_LAYOUT.md`
- **`IDEA-0013`** — `docs/00_SYSTEM/12_IDEA_MASTER_LOG.md`
