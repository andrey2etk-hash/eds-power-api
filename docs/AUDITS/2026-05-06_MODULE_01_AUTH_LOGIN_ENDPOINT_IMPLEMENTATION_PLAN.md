# MODULE 01 AUTH LOGIN ENDPOINT IMPLEMENTATION PLAN

## Objective
Prepare bounded implementation plan for first backend auth endpoint after Module 01 data layer preparation is complete.

## Source and Current State
- Source verdict: `SESSION_TABLE_CREATED_VERIFIED_PASS`
- Test user provisioning: `CLOSED / PASS`
- `public.module01_user_sessions`: created and verified
- Session strategy: DB Session selected
- API-first auth plan: prepared and aligned
- This task: planning only, no code changes

## Target Endpoint
`POST /api/module01/auth/login`

## Request Contract
Required request fields:
- `email`
- `password`
- `spreadsheet_id`

## Success Behavior
On valid login, backend must:
- validate credentials
- verify terminal binding
- verify active `TEST_OPERATOR` role assignment
- create raw session token
- store only `session_token_hash` in `public.module01_user_sessions`
- return raw session token once to caller
- return user profile and `allowed_actions`

## External Failure Rule
- External failure response for credential/user/terminal login failure must return `AUTH_FAILED`
- No account enumeration details may be exposed to client
- Internal audit/log may record detailed reason

## Implementation Scope (Bounded)
Allowed future code files:
- `main.py` OR backend auth router if existing architecture supports it
- small helper module only if already consistent with repo style

Allowed logic:
- request schema
- email lookup
- user status check
- password hash verification via `argon2-cffi`
- active role assignment check
- terminal binding check by `spreadsheet_id`
- session token generation
- `session_token_hash` generation
- insert session row
- success/error response contract

## Session Token Rule
Raw session token:
- generated with cryptographically safe randomness
- returned only once in successful login response
- never stored in DB
- never logged

Stored value:
- `session_token_hash` only

TTL:
- `AUTH_SESSION_TTL_HOURS`
- default 12 if env configured according to existing governance
- fail closed if required env missing, if this is already approved by env doctrine

## Response Contract

Success:

```json
{
  "status": "success",
  "data": {
    "user": {
      "user_id": "...",
      "email": "...",
      "display_name": "...",
      "role_codes": ["TEST_OPERATOR"]
    },
    "session": {
      "session_token": "...",
      "expires_at": "..."
    },
    "allowed_actions": ["auth.login", "auth.refresh_menu"]
  },
  "error": null,
  "metadata": {
    "request_id": "...",
    "module": "MODULE_01_AUTH"
  }
}
```

Failure:

```json
{
  "status": "auth_failed",
  "data": null,
  "error": {
    "error_code": "AUTH_FAILED",
    "message": "Authentication failed"
  },
  "metadata": {
    "request_id": "...",
    "module": "MODULE_01_AUTH"
  }
}
```

## Strict Out of Scope
Do NOT include:
- GAS UI
- refresh endpoint
- logout endpoint
- password reset
- admin role management
- registration
- OAuth
- JWT
- HMAC token
- full RBAC expansion
- lockout writeback unless explicitly approved
- failed login audit table
- Render deployment
- schema changes

## Implementation Blockers to Confirm Before Coding
Before coding, confirm:
- exact Supabase client pattern already used in repo
- env variable availability:
  - `SUPABASE_URL`
  - `SUPABASE_SERVICE_ROLE_KEY`
  - `AUTH_SESSION_TTL_HOURS`
- whether `EDS_SESSION_HMAC_SECRET` is needed for DB session token hashing or not
- exact hashing method for `session_token_hash`
- exact response envelope style already used by `main.py`
- no conflict with existing API routes

## Planning Verdict
AUTH_LOGIN_ENDPOINT_PLAN_PREPARED / PENDING_GEMINI_AUDIT

## Boundary Confirmation
Confirm:
- no API implementation
- no auth logic code changes
- no GAS code changes
- no DB writes
- no SQL execution
- no Render env changes
- no secret values stored
