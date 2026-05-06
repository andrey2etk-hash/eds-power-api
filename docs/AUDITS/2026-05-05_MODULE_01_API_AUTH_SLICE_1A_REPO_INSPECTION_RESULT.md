# MODULE 01 API AUTH SLICE 1A REPO INSPECTION RESULT

## Status
AUDIT ONLY / NO CODE CHANGES

## Purpose
Inspect the current repository structure, dependencies, and backend patterns before Module 01 auth endpoint implementation (`login`, `refresh_menu`, `logout`).

## Repo Health
- Branch: `main`.
- Working tree is dirty: `44` changed/untracked paths total.
- Composition of dirty state:
  - docs: `42` paths
  - SQL migrations: `2` paths
- Current dirty state is mostly documentation, but includes migration files; implementation should start from a clean isolation boundary (new branch and focused commit scope) to avoid mixed diffs.

## FastAPI Structure
- Current app entry point is `main.py` with single `FastAPI()` instance.
- No `APIRouter` modules and no `include_router(...)` pattern detected.
- Existing endpoints are registered directly in `main.py`:
  - `/api/demo/module-01/kzo/run`
  - `/api/calc/prepare_calculation`
  - `/api/kzo/save_snapshot`
- `/api/v1/...` namespace is not currently used.
- Current KZO and persistence logic are concentrated in `main.py` + helper module `kzo_snapshot_persist.py`.

Recommended future file touch scope (for implementation phase, not now):
- keep `main.py` as app bootstrap
- add auth router module (for `/api/v1/auth/*`)
- add auth service/helper module(s)
- add dedicated permissions/menu constants module
- add targeted tests in `tests/`

## DB Access Pattern
- Current persistence path uses `supabase-py` client (`create_client`) in `kzo_snapshot_persist.py`.
- Connection pattern: server-side environment variables (`SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`) read via `os.environ`.
- Client object is cached in-process (`_client`) and used via table REST operations.
- Current endpoint functions are synchronous (`def`, not `async def`) and follow sync helper calls.

Feasibility for auth:
- Pattern can support auth reads/writes to Module 01 tables.
- Service-role based server-side access pattern is already established.

Risks:
- auth writes/audits in sync path may increase latency without careful error/timeout handling.
- no dedicated abstraction layer yet for auth/session/audit operations.

## Dependency Check
Dependency manifest found:
- `requirements.txt`:
  - `fastapi`
  - `uvicorn`
  - `supabase>=2.10.0`

Observed:
- `fastapi`: present
- `pydantic`: implicit via `fastapi`, not explicitly pinned
- `supabase`: present
- `argon2-cffi`: not declared
- `bcrypt`: not declared
- `passlib`: not declared
- JWT libs (`python-jose`/similar): not declared
- `python-dotenv`: not declared

Password hashing library readiness:
- ARGON2ID support in repo dependencies: missing
- BCRYPT support in repo dependencies: missing

Session hashing readiness:
- HMAC/SHA256 can be implemented via Python standard library (`hmac`/`hashlib`) without extra package installation.

## Environment Variable Requirements
Currently used in code:
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`

Present in `.env.example`:
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`

Not currently used in code (but needed for planned auth slice):
- `EDS_SESSION_HMAC_SECRET`
- `API_VERSION`
- `AUTH_SESSION_TTL_HOURS`

Notes:
- no secret values were inspected or printed
- only names/patterns were inspected

## Audit Event Contract Feasibility
`module01_audit_events` columns (from migration):
- `id`
- `entity_type`
- `entity_id`
- `event_type`
- `actor_user_id`
- `event_at`
- `request_id` (uuid)
- `source_client`
- `metadata` (jsonb)

Feasibility assessment:
- Auth events can be stored without schema change using existing columns + `metadata`.
- `terminal_id`, `target_user_id`, and extended audit context can be placed in `metadata`.
- `client_type` can map to `source_client`.

Caution:
- `request_id` is typed as `uuid`; if auth contract allows non-UUID request IDs, strict mapping rules are required.
- If strict field-level event contract is required beyond metadata mapping, a separate Audit Event Data Contract Plan is recommended.

## Permission/Menu Mapping Location
Current codebase has no auth/permissions constants module.

Recommended MVP location for static API-side mapping:
- create dedicated auth constants module (example direction: `src/auth/permissions_map.py` or equivalent router-local constants file), then consume it from auth service layer.

Reason:
- keeps role-menu logic out of GAS
- keeps mapping centralized and explicit for additive multi-role resolution

## Test Strategy Feasibility
- Existing test suite is present under `tests/`.
- Current tests use `unittest` pattern (no explicit `pytest` dependency declaration detected).
- Endpoint tests currently invoke endpoint functions directly and mock internals where needed.

Feasible minimal future tests:
- login validation failures (missing fields, invalid creds generic response)
- terminal-required and terminal-mismatch cases
- refresh with invalid/expired/revoked token
- logout invalid token

Successful login test status:
- blocked until test user provisioning path is planned (user + password_hash + terminal + active roles).

## Blockers
- Password hashing dependencies for auth verification are not declared (`argon2-cffi`/`bcrypt`/or equivalent support layer missing in manifest).
- Auth session secret env is not yet defined in code/config (`EDS_SESSION_HMAC_SECRET` pattern needed for HMAC path).
- Audit write contract details are only partially explicit (mapping strategy to `metadata` and UUID policy for `request_id` must be finalized).
- No test user provisioning path is defined for successful login path validation.
- Working tree is not clean (contains docs and migration changes); safe implementation needs isolated clean scope.

## Non-Blockers
- Docs-heavy dirty state by itself does not prevent inspection/planning.
- GAS UI implementation is not required for backend auth slice.
- Password reset and `change_password` are deferred by approved scope.
- Missing `/api/v1` today is structural debt, not a blocker (can be introduced in auth router slice).

## Recommended Next Step
**B. Create Audit Event Data Contract Plan**

Rationale:
- Audit schema is mostly usable, but auth event field mapping and `request_id` UUID policy should be locked before endpoint writes.
- This reduces implementation rework across `login`/`refresh_menu`/`logout` and keeps Slice 1B+ focused on code execution with clear contracts.

## Boundary Confirmation
- no code changes
- no SQL
- no DB writes
- no dependency installation
- no env secret changes
- no deployment
- no secrets printed

## Gemini Audit Status

- final verdict: PASS
- result status: CLOSED / APPROVED
- no required fixes
- key blockers accepted
- request_id UUID strictness carried forward
- next allowed step: Module 01 Audit Event Data Contract Plan
