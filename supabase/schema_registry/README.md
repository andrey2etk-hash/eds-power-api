# Schema registry rules

## Role

Every **new** Postgres object that survives past an MVP gate should be **registered** here **before or with** its first migration merge (same PR ideally). The registry is **documentation-first**; Postgres remains source of DDL in **`../migrations/`**.

## Entries (per table or cohesive object)

Recommended fields:

- **Resource name** (Postgres: `schema.table`).
- **Domain** (see **`../domains/README.md`**).
- **Owning IDEA** ID.
- **Consumer product(s)** (`KZO`, `*` future, …).
- **Freeze / version key** (e.g. **`KZO_MVP_SNAPSHOT_V1`** for snapshot JSON shape).
- **Mutation policy**: append-only, insert-only API, …

## File naming

- Use stable ids: **`REG_<IDEA>_YYYYMMDD_<slug>.md`** or a single **`REGISTRY_INDEX.md`** that lists all rows until volume grows.

## Drift prevention

- If migration renames/drops/changes semantics → **update registry in the same PR** or mark **DEPRECATED** with replacement pointer.
- Snapshot contract changes require **new **`snapshot_version`** + IDEA**, not silent column inflation.

## Legacy remote baseline

Operational doc: **`LEGACY_REMOTE_BASELINE.md`** (Stage **8A.0.2**) — coexistence rules with non-empty **`public`**.

Legacy migrations may precede formal registry rows. **`REGISTRY_INDEX.md`** may list them retrospectively (**backfill**) as part of **8A.1**.
