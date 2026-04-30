# EDS Power — Supabase root governance

## Purpose

Supabase is the **central memory layer for EDS Power**, not a database owned by one product line. Calculation modules (for example **`00-02_CALC_CONFIGURATOR` / KZO**) are **consumers** that write governed snapshots through APIs; schema must remain **explainable across products** (`product_type`, domain boundaries).

This aligns with **`00_SYSTEM`**: persistence follows **stable contracts** (**Execution → Freeze → Persist**). Stage **8A** = trusted storage — storage design must remain **architecture-first**, **KZO-second**.

---

## Folder layout

| Path | Role |
| --- | --- |
| **`migrations/`** | Sequential SQL migrations (Supabase/Postgres). Governed entries are registered in **`schema_registry/`** before adoption. |
| **`schema_registry/`** | Indexes of approved tables, owning domain, versioning, and IDEA linkage. **No “secret” DDL.** |
| **`domains/`** | Logical bounded contexts (auth, products, snapshots, …). Stub **README** per domain until an approved IDEA allocates concrete tables. |

---

## Governance rules (normative)

0. **`TABLE = SYSTEM`, `ROW = PRODUCT`.** Root-level table names MUST NOT encode a product line (**no** `kzo_*` owning tables for shared domains). Product identity is carried on rows (**`product_type`**, **`snapshot_version`**, JSON envelopes). Stage **8A.0.1** encodes this for **`calculation_snapshots`.**

1. **Central memory.** Supabase = system-wide persistence; module docs describe behavior, **`supabase/`** describes **what may exist as rows**.
2. **KZO = first validated consumer.** KZO MVP snapshot persistence is **one approved use-case**, not the **naming root** for the whole DB (see discriminators below).
3. **No KZO-generic global names.** Names like `equipment` sitting only for KZO without `product_type` / domain cues are discouraged for **shared** projections. Prefer domain-scoped or neutral names + **`product_type`** when the row is product-specific (see **`domains/README.md`**).
4. **Product-specific payloads** MUST be discriminated (e.g. **`product_type`**, **`snapshot_version`**, **`domain`** in JSON/registry metadata) unless a dedicated approved IDEA declares a purely single-product MVP table with freeze documentation.
5. **First persisted snapshot remains `KZO_MVP_SNAPSHOT_V1`.** Calculation truth is frozen upstream; inserts store **frozen JSON** without ERP decomposition (see **`domains/snapshots/README.md`**).
6. **Stage 8A.0** (this governance pack) introduces **folders + docs only**: **no new migration** authored under 8A.0 purely for governance; **no SQL execution obligation** inside this IDEA.
7. **No DDL without an approved IDEA** that touches registry + changelog/stakeholders as required by project norms.
8. **No premature ERP.** No BOM hubs, costing ledgers, full MRP, or unconstrained **`analytics`** fact tables unless a separate IDEA freezes scope.

---

## Stage gates

| Gate | Meaning |
| --- | --- |
| **8A.0** | **Supabase root governance foundation** — this structure + rules; **documentation only** until closed. |
| **8A.0.1** | **Root migration naming correction** — **`calculation_snapshots`** + **`product_type`**, supersedes **`kzo_mvp_snapshots_v1`** draft DDL (archived). **Before** first live push when possible. |
| **8A.0.2** | **Remote baseline alignment (governance + hold)** — live **`public`** not empty (**`legacy_baseline`** tables/views). **Do not** **`db push`** until baseline migration authored; **`calculation_snapshots`** DDL **held** in **`migrations/_pending_after_remote_baseline/`**. See **`schema_registry/LEGACY_REMOTE_BASELINE.md`** + audit **8A.0.2**. (**IDEA-0020**.) |
| **8A.0.3** | **Remote baseline capture (repo slot + operator DDL paste)** — **`20260429110000_remote_legacy_baseline.sql`** in **`migrations/`** root (scaffold **\<** snapshot hold). **No prod `db push`** in task; **Dashboard DDL freeze** during capture. Status: **`BASELINE_CAPTURED_PENDING_REPLAY_TEST`**. Audit **`2026-04-29_STAGE_8A_0_3_REMOTE_BASELINE_CAPTURE.md`**. (**IDEA-0022**.) |
| **8A.0.4** | **Local replay / staging verification** — paste factual schema-only DDL, then **`supabase db reset`** (or disposable migrate) **only** locally / staging — **never prod `db push` in this TASK**. **2026-04-29 attempt:** **`BLOCKED_BY_LOCAL_TOOLING`** — audit **`2026-04-29_STAGE_8A_0_4_BASELINE_REPLAY_TEST.md`**. On success status becomes **`BASELINE_REPLAY_VERIFIED`**. |
| **8A.0.5** | **Local tooling precheck** — operator install plan for **`pg_dump`** / Supabase CLI / optional Docker. Audit **`2026-04-29_STAGE_8A_0_5_LOCAL_TOOLING_PRECHECK.md`**. Status: **`READY_FOR_OPERATOR_TOOLING_INSTALL`**. |
| **8A.0.6** | **Import captured `remote_schema.sql`** into **`20260429110000_remote_legacy_baseline.sql`** (**sanitized**, schema-only). Status: **`REAL_BASELINE_CAPTURED_PENDING_REPLAY`**. Audit **`2026-04-29_STAGE_8A_0_6_ACTUAL_REMOTE_BASELINE_CAPTURE.md`**. |
| **8A.0.7** | **Baseline local replay verification** — **`supabase db reset`** (or disposable DB). **2026-04-29:** **`BLOCKED_BY_DOCKER`** (no Docker/CLI on agent PATH); **`BASELINE_REPLAY_VERIFIED`** pending operator. Audit **`2026-04-29_STAGE_8A_0_7_BASELINE_REPLAY_VERIFICATION.md`**. Next: **8A.0.8** snapshot DDL promotion test. |
| **8A.1** | **First snapshot persistence aligned with root model** — migration + API + verification under registry (consumer: KZO via row **`product_type`**, contract **`KZO_MVP_SNAPSHOT_V1`**). (**IDEA-0017** + live gate.) |

---

## Remote legacy baseline (non-empty Supabase)

**Status:** **`REAL_BASELINE_CAPTURED_PENDING_REPLAY`** (**8A.0.6**) + **`BLOCKED_BY_DOCKER`** (**8A.0.7** replay not run — **`BASELINE_REPLAY_VERIFIED`** pending). Prior **`LEGACY_REMOTE_SCHEMA_DETECTED`** (**8A.0.2**).

If the linked Supabase project already contains **`public.objects`**, **`bom_links`**, **`ncr`**, **`production_status`**, **`v_*`** views — treat as **`legacy_baseline`** (see **`schema_registry/LEGACY_REMOTE_BASELINE.md`**). Rules:

- **Preserve** until separately audited (**no** drops/renames from snapshot MVP workstreams).
- **New EDS Power persistence is additive only** — **`calculation_snapshots`** does not justify destructive cleanup of unrelated legacy objects.
- **Repo migrations MUST NOT casually trail behind remote** — baseline SQL must be imported into **`supabase/migrations/`** ahead of **`calculation_snapshots`** restore from **`_pending_after_remote_baseline/`** (after **`BASELINE_REPLAY_VERIFIED`** per **8A.0.7**).

---

## Forbidden in root governance phases

- DB connection strings or secrets in this repo (**use host env**, see **`.env.example`**).
- **`supabase`** used as synonym for “KZO database”.
- Building full **auth**/roles**/production**/analytics** schemas proactively without IDEA approval.

---

## References

- **`docs/00_SYSTEM/04_DATA_CONTRACTS.md`** — if present, system data contracts  
- **`docs/00_SYSTEM/03_ARCHITECTURE.md`** — system modules  
- **`docs/00-02_CALC_CONFIGURATOR/09_KZO/14_CALC_TRUTH_VS_PERSISTENCE_STAGE_8A.md`** — calculation truth vs persistence  
- **`schema_registry/README.md`**, **`schema_registry/LEGACY_REMOTE_BASELINE.md`**, **`domains/README.md`**
