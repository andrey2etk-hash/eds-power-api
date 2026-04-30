# Calculation truth vs persistence layer (Stage 8A)

## Calculation truth (`prepare_calculation`)

- **Single governed entry:** `POST /api/calc/prepare_calculation`
- **Produces:** validated `data` including `normalized_payload` and all engineering summaries.
- **Purpose:** Compute **KZO MVP engineering meaning** from input — **source of truth** for MVP calculation output.

## Persistence layer (`save_snapshot`)

- **Single governed entry:** `POST /api/kzo/save_snapshot`
- **Accepts:** already-frozen **`KZO_MVP_SNAPSHOT_V1`** JSON (built per Stage 7B contract from a validated run).
- **Stores:** one append-only row in **`calculation_snapshots`** (`product_type` = **`KZO`** for MVP) — JSONB columns mirror the contract; **no recomputation**, **no reinterpretation** of engineering layers.
- **Purpose:** Give EDS Power **durable memory** without turning this route into BOM/ERP/commercial logic.

## Anti-drift

- Fields **not** in **`KZO_MVP_SNAPSHOT_V1`** **must not** become mandatory persisted structure without **`KZO_MVP_SNAPSHOT_V2`**, **IDEA**, and audit (Stage **7B** law).
- Stage **8A** excludes: pricing, BOM, procurement systems, dashboards, retrieval APIs beyond insert response — unless separately tasked.

## Sequence

```
prepare_calculation → (client/assembler builds `KZO_MVP_SNAPSHOT_V1`) → save_snapshot → one INSERT only
```
