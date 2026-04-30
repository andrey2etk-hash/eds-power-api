# Legacy remote baseline — non-empty Supabase (`public`)

## Status lineage

| Stage | Registry state |
| --- | --- |
| **8A.0.2** | **`LEGACY_REMOTE_SCHEMA_DETECTED`** — declared coexistence governance |
| **8A.0.3** | **`BASELINE_CAPTURED_PENDING_REPLAY_TEST`** — migration slot **`20260429110000_remote_legacy_baseline.sql`** present; factual DDL body **past** agent scaffold when operator runs capture (pending **replay** **`8A.0.4`**) |
| **8A.0.4** | **`BLOCKED_BY_LOCAL_TOOLING`** (2026-04-29 agent session) — **`pg_dump`** / Supabase CLI / Docker unavailable on PATH; noop body **retained** (no invented DDL). Re-run when operator can dump + **`supabase db reset`** locally. Audit: **`2026-04-29_STAGE_8A_0_4_BASELINE_REPLAY_TEST.md`**. |
| **8A.0.6** | **`REAL_BASELINE_CAPTURED_PENDING_REPLAY`** — **`remote_schema.sql`** merged into **`20260429110000_remote_legacy_baseline.sql`** (sanitized **`pg_dump`** markers; schema-only). **`calculation_snapshots`** still **held**. Audit: **`2026-04-29_STAGE_8A_0_6_ACTUAL_REMOTE_BASELINE_CAPTURE.md`**. |
| **8A.0.7** | **`BLOCKED_BY_DOCKER`** — local **`supabase db reset`** not executed (Docker + Supabase CLI **missing** on PATH this session); **`BASELINE_REPLAY_VERIFIED`** **not** claimed. Disposable replay path documented in audit **`2026-04-29_STAGE_8A_0_7_BASELINE_REPLAY_VERIFICATION.md`**. |

## Remote freeze (**8A.0.3 / 8A.0.4**)


**Until factual baseline DDL is committed and replay-tested on staging:** operators MUST **avoid manual Supabase Dashboard DDL** changes to listed **`public`** legacy objects (creates/alters/drops/views). Ordinary **data** operations are out of scope of this freeze unless they imply DDL.

---

## Existing tables (declared baseline)

Treat as **`legacy_baseline`** — registered for governance alignment only.

| Object | Classification |
| --- | --- |
| **`public.objects`** | legacy_baseline |
| **`public.bom_links`** | legacy_baseline |
| **`public.ncr`** | legacy_baseline |
| **`public.production_status`** | legacy_baseline |

## Existing views

| Pattern | Classification |
| --- | --- |
| **`public.v_*`** | legacy_baseline |

**After capture paste (8A.0.6 DONE):** Explicit view names are in baseline migration DDL (**23 × **`public.v_*`**). Legacy table list below remains the declared minimum.

---

## Baseline migration (repo)

**File:** **`supabase/migrations/20260429110000_remote_legacy_baseline.sql`**

Ordering is **before** **`20260429120000_calculation_snapshots_v1`** (currently only in **`_pending_after_remote_baseline/`**).

---

## Normative governance rules

1. **`LEGACY_REMOTE_SCHEMA_DETECTED`** — recognise that remote ≠ empty; repo migrations lacked baseline until **8A.0.3** slot.
2. **Preserve until separately audited.** No renaming, dropping, or destructive rewrite of **`legacy_baseline`** objects without **AUDIT → IDEA → migration** bundle.
3. **Additive EDS persistence.** **`calculation_snapshots`** introduces **additive** DDL only; no cascade affecting legacy artefacts.
4. **No careless `db push`** to prod — **replay on staging first** (**8A.0.7** / **`BASELINE_REPLAY_VERIFIED`**).
5. **No KZO rollback** of unrelated legacy artefacts for snapshot MVP scope.

---

## Related registry entries

- **`REGISTRY_INDEX.md`** — legacy rows + **`calculation_snapshots`** hold pointer
- **`../migrations/README.md`** — scaffold vs held DDL semantics

---

## Cross-reference audits

- **`docs/AUDITS/2026-04-29_STAGE_8A_0_2_SUPABASE_REMOTE_BASELINE_ALIGNMENT.md`**
- **`docs/AUDITS/2026-04-29_STAGE_8A_0_3_REMOTE_BASELINE_CAPTURE.md`**
- **`docs/AUDITS/2026-04-29_STAGE_8A_0_4_BASELINE_REPLAY_TEST.md`**
- **`docs/AUDITS/2026-04-29_STAGE_8A_0_5_LOCAL_TOOLING_PRECHECK.md`**
- **`docs/AUDITS/2026-04-29_STAGE_8A_0_6_ACTUAL_REMOTE_BASELINE_CAPTURE.md`**
- **`docs/AUDITS/2026-04-29_STAGE_8A_0_7_BASELINE_REPLAY_VERIFICATION.md`**
