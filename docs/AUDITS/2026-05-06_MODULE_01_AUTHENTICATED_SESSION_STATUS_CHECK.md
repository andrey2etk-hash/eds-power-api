# MODULE 01 AUTHENTICATED SESSION STATUS CHECK

## Objective
Implement and verify the first secure authenticated backend action after `FIRST_LIVE_SAKURA_LOGIN_PASS`.

## Scope
Bounded auth-only implementation:
- backend session status endpoint
- GAS test function to call endpoint with `Authorization: Bearer <session_token>`
- no calculation logic
- no KZO/KTP/BMZ logic
- no DB schema changes

## Implementation summary
- Added backend endpoint: `GET /api/module01/auth/session/status`.
- Added backend token validation path:
  - token presence
  - token hash lookup in session table
  - revoked/expired checks
  - user and terminal checks
  - role presence check
- Added GAS operator test function:
  - `runModule01AuthenticatedSessionStatusCheck()`
  - reads session token from `UserProperties`
  - sends Bearer header
  - shows safe result summary (no token output)

## Backend endpoint
- Route: `GET /api/module01/auth/session/status`
- Success response:
  - `status = success`
  - `authenticated = true`
  - `user_id`, `email`, `role`, `terminal_id`, `expires_at`, `remaining_seconds`
- Error envelope:
  - `status = auth_error`
  - machine-readable `error_code`
  - `source_field = Authorization`
  - `module = MODULE_01_AUTH`
  - `action = session_status`

## GAS test function
- Function: `runModule01AuthenticatedSessionStatusCheck()`
- Behavior:
  - uses stored session token from `UserProperties`
  - calls backend session status endpoint
  - displays safe status/error fields to operator
- Security:
  - does not log or display token
  - does not decode token

## Security boundaries
- raw session token is never written to docs/repo
- token hash is never returned by endpoint
- password/password hash are never returned
- no direct Supabase access from GAS
- no backend secret values exposed

## What was tested
Automated tests (`python -m unittest`):
- valid token -> success envelope (`authenticated = true`)
- missing token -> `AUTH_MISSING_TOKEN`
- invalid token -> `AUTH_INVALID_TOKEN`
- existing login endpoint regression suite remains PASS

## What was NOT tested
- live expired token scenario (manual/operator follow-up)
- live revoked token scenario (manual/operator follow-up)
- terminal mismatch live scenario (manual/operator follow-up)
- multi-user concurrency behavior in same Sheet

## Result
First secure authenticated action implemented and test-covered without entering calculation scope.

## Verdict
AUTHENTICATED_SESSION_STATUS_CHECK_IMPLEMENTED / PENDING_GEMINI_AUDIT
