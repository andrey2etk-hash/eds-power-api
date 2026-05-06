# MODULE 01 AUTH IMPLEMENTATION PLAN — API FIRST

## 1. Objective
Define API-first implementation plan for Module 01 authorization after successful test user provisioning, without code implementation in this step.

## 2. Current State
- Module 01 test user provisioning is closed as PASS.
- Verified records exist: user, auth row, `TEST_OPERATOR` role, user-role link, terminal binding.
- Manual DB Bridge is active for DB operations during MVP stage.
- Auth implementation code is not started.

## 3. API-first Architecture Rule
- Backend owns all auth logic and authorization decisions.
- GAS is a thin transport and rendering client only.
- Session representation is neutral at this stage: `session_token` / `session_handle`.
- Token format decision is pending and must be approved in a dedicated decision step.

## 4. Proposed endpoint
`POST /api/module01/auth/login`

## 5. Request contract
Request JSON:
- `email` (string, required, normalized to lower-case on backend)
- `password` (string, required)
- `spreadsheet_id` (string, required)

## 6. Success response contract
Response shape (draft):
- `ok`: `true`
- `session`: object
  - `session_token` or `session_handle` (exact field stays neutral until session strategy decision)
  - `expires_at` (ISO timestamp)
- `user`: object
  - `user_id`
  - `email`
  - `display_name`
- `authorization`: object
  - `roles[]`
  - `permissions[]`
  - `menu_schema`
- `request_id` (server-generated trace id)

## 7. Error response contract
Response shape (draft):
- `ok`: `false`
- `error`: object
  - `code` (stable machine code)
  - `message` (safe user-facing message)
  - `retryable` (boolean)
- `request_id`

Error classes to support:
- validation failure (`INVALID_REQUEST`)
- invalid credentials (`INVALID_CREDENTIALS`)
- account inactive/locked (`ACCOUNT_INACTIVE`, `ACCOUNT_LOCKED`)
- missing role/permission (`AUTHZ_DENIED`)
- terminal binding mismatch (`TERMINAL_NOT_ALLOWED`)
- temporary backend failure (`AUTH_SERVICE_ERROR`)

## 8. Backend check order
1. request validation
2. user lookup
3. user active check
4. auth row lookup
5. Argon2id password verification
6. failed_login_attempts / locked_until policy
7. role check
8. terminal binding check
9. session/token creation

## 9. Session strategy options
Decision update:
- Session strategy selected: DB Session (MVP)
- HMAC signed token: deferred
- JWT: deferred
- Implementation remains blocked pending session table schema plan

Candidate options (history):

- Option A: HMAC signed token
  - stateless verification on backend
  - requires strict secret lifecycle and rotation policy
- Option B: DB session table
  - stateful session handle with server-side lookup/revocation
  - aligns well with existing `module01_user_sessions` groundwork
- Option C: JWT
  - standardized format, but introduces signing/validation policy complexity
  - not assumed and not pre-approved
- Option D: other approved format
  - allowed only after explicit architecture/security review

Decision gate required before implementation:
- pick one session strategy
- define TTL, rotation, revocation, and logout invalidation behavior
- define hashing/signature policy and audit events

## 10. Security rules
- Never store plaintext password.
- Verify password hash using approved Argon2id flow.
- Never expose password hash in responses, logs, or repo docs.
- Fail closed on missing auth/session configuration.
- Apply lockout policy (`failed_login_attempts`, `locked_until`) with auditable updates.
- Return generic credential errors to prevent account enumeration.
- Ensure all auth attempts are auditable with request trace context.

Account enumeration rule:
- External login failure response: `AUTH_FAILED`
- Internal audit may store detailed reason (`EMAIL_NOT_FOUND`, `PASSWORD_INVALID`, `USER_INACTIVE`, `ACCOUNT_LOCKED`, `TERMINAL_NOT_BOUND`)
- Detailed credential failure reason must not be exposed to client.

## 11. GAS boundary
GAS must NOT:
- verify password
- check role
- check terminal binding
- create session
- access Supabase directly

GAS responsibilities:
- collect login payload
- call backend endpoint
- store returned session artifact per approved policy
- render backend-provided menu/authorization state

Terminal binding note:
- MVP accepts spreadsheet_id-only terminal binding.
- `terminal_secret` / terminal fingerprint are deferred as future hardening enhancements.

## 12. Implementation blockers
- Session table schema plan is not created yet (required for selected DB Session strategy).
- Session table SQL migration/provisioning plan is not audited yet.
- Final API response schema fields need lock-in after session decision.
- Lockout thresholds and retry policy values are not yet fixed.
- Audit event minimal set for login failure/success must be finalized for implementation.
- Runtime secret/config readiness must be confirmed before coding (without exposing values).
- Implementation slicing order must be re-confirmed against current `main.py` structure.
- Terminal binding hardening is pending (`terminal_secret` / fingerprint); MVP accepts spreadsheet_id-only binding.

## 13. Out of scope
- implementing endpoint code
- modifying `main.py`
- creating auth module/package
- GAS implementation changes
- SQL execution or DB writes
- Render environment configuration
- password reset/change-password implementation

## 14. Verdict
AUTH_IMPLEMENTATION_PLAN_PREPARED / PENDING_GEMINI_AUDIT
