# Stage 8B.3A — Bounded Implementation Plan

Scope: implementation planning only for API duplicate snapshot protection MVP.  
Execution mode: bounded, safe, minimal mutation.

## 1. Exact implementation objective

Implement the smallest API-side protection at `POST /api/kzo/save_snapshot` so repeated/replayed requests do not create duplicate persistence truth while preserving existing V1 contract behavior and thin-client architecture.

## 2. Allowed files only

- `main.py` (save_snapshot route boundary and response mapping only)
- `kzo_snapshot_persist.py` (duplicate detection and bounded idempotency checks only)
- `docs/AUDITS/` artifacts for execution and verification logs
- `docs/TASKS.md`, `docs/NOW.md`, `docs/CHANGELOG.md`, `docs/AUDITS/00_AUDIT_INDEX.md` for registry updates

## 3. Forbidden files

- `gas/` (no GAS flow changes)
- `supabase/migrations/` (no redesign migrations)
- `docs/00-02_CALC_CONFIGURATOR/` product-flow docs outside status sync needs
- Any new module files or new service layers

## 4. Minimum code boundary

- Route boundary: `save_snapshot` only
- Input leverage: existing `request_id` and current snapshot envelope fields only
- Decision scope: duplicate/replay classification + response shaping only
- No expansion into `prepare_calculation`, product logic, async, or orchestration redesign

## 5. Duplicate detection strategy

- Build bounded idempotency fingerprint from existing stable save envelope primitives
- Detect replay/duplicate before new write is accepted
- If exact duplicate is detected, return governance-safe duplicate outcome instead of silent second truth write
- Keep API as sole authority (no client-side duplicate logic)

## 6. Expected response states

- `SUCCESS_STORED` — first valid write persisted
- `DUPLICATE_BLOCKED` (or canonical duplicate-safe equivalent aligned with 8B.2C) — repeated/replayed equivalent write safely blocked
- `SUCCESS_DISTINCT_STORED` — new distinct valid write persisted
- Failure responses remain machine-readable and phase-aligned with 8B.2C doctrine

## 7. Test cases

1. First valid save request -> success + stored state.
2. Immediate identical replay (same identity envelope) -> duplicate-safe blocked state.
3. Distinct valid payload save -> success + stored state.
4. Duplicate response machine-readability conforms to 8B.2C envelope doctrine.
5. No changes in GAS behavior (thin client unchanged).
6. No regression in baseline `save_snapshot` validation for non-duplicate valid/invalid paths.

## 8. Rollback plan

- Roll back to pre-8B.3A API behavior if duplicate protection destabilizes save flow.
- Use latest verified baseline behavior from post-8B.1B / 8B.2 closeout state.
- Re-open planning, tighten boundary, and re-author bounded patch scope before next attempt.

## 9. Failure risks

- Overreach into persistence redesign beyond duplicate protection
- Contract drift in response fields breaking existing thin-client expectations
- False-positive duplicate blocking for distinct valid saves
- Hidden spread into unrelated modules or async architecture

## 10. Success condition

`8B.3A` is implementation-ready when one small, auditable plan exists to add duplicate/replay protection in `save_snapshot` only, with strict boundary controls, deterministic tests, and zero platform redesign.

---

Final rule: this artifact authorizes bounded implementation execution planning, not implementation itself.
