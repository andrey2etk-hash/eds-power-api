# Stage 8B.3A — Live Failure Diagnosis

Date: 2026-05-01  
Mode: diagnosis only (no code/DB/GAS changes performed)

## Root Cause

**Primary root cause: deployment is stale relative to local `8B.3A` code.**

`8B.3A` duplicate-protection changes exist only in local uncommitted working tree (`main.py`, `kzo_snapshot_persist.py`) and therefore are not present in deployed Render runtime.

## Evidence

1. **Deployed commit check**
   - `git rev-parse HEAD` = `09b1db94123b63b267359272ab1abcc1bc9f1c2c`
   - `git rev-parse origin/main` = `09b1db94123b63b267359272ab1abcc1bc9f1c2c`
   - `git status --short` shows local modified files including:
     - `main.py`
     - `kzo_snapshot_persist.py`
   - Conclusion: `8B.3A` code is not committed/pushed, so Render cannot run it.

2. **Live behavior check (already executed gate)**
   - First request with `request_id A` -> `STORED`
   - Second request with same `request_id A` -> `STORED` (expected `DUPLICATE_REJECTED`)
   - Third request with `request_id B` -> `STORED`
   - Conclusion: live route behavior matches pre-`8B.3A` logic.

3. **Request metadata shape expectation**
   - Local validator requires `request_metadata.request_id` for SUCCESS snapshots.
   - Persistence schema defines `request_metadata JSONB` in `public.calculation_snapshots`.
   - This confirms intended JSON path is valid (`request_metadata.request_id`) and not the primary blocker.

4. **Duplicate check ordering (local code)**
   - Local `save_snapshot` executes duplicate check (`find_snapshot_by_request_id`) **before** insert call.
   - Therefore, logic order is correct in local implementation.

5. **find_snapshot_by_request_id / Supabase shape compatibility**
   - Local query targets JSONB containment on `request_metadata` with `{"request_id": <rid>}` and filters by `product_type='KZO'`.
   - With `request_metadata JSONB`, query shape is plausible.
   - No live runtime evidence indicates this query executes yet, because stale deploy prevents path activation.

## Minimal Fix Recommendation

1. Promote current local `8B.3A` changes to deployed runtime (commit + deploy).
2. Re-run exact 3-step live gate:
   - first A -> `STORED`
   - replay A -> `DUPLICATE_REJECTED`
   - first B -> `STORED`
3. If replay A still stores after fresh deploy, then run focused DB-level check on `request_metadata` JSON content and containment filter behavior.

## Files Likely Needed (if fix execution is authorized)

- `main.py`
- `kzo_snapshot_persist.py`
- `tests/test_save_snapshot_duplicate_protection.py`
- `docs/AUDITS/2026-05-01_STAGE_8B_3A_LIVE_VERIFICATION.md` (update after re-gate)

## No Changes Performed

Diagnosis completed without implementation updates, DB actions, or GAS changes.
