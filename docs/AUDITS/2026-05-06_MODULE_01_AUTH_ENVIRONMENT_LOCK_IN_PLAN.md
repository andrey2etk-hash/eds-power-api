# MODULE 01 AUTH ENVIRONMENT LOCK-IN PLAN

## Objective
Define required environment readiness before Module 01 auth login implementation.

## Required Environment Variables

### SUPABASE_URL
Purpose:
Connect backend to Supabase.

Required:
YES

Validation:
Presence only. Do not print value.

### SUPABASE_SERVICE_ROLE_KEY
Purpose:
Backend privileged access to auth-related tables.

Required:
YES

Validation:
Presence only. Do not print value.

Security:
Must exist only in Render/local secure env.
Never in repo.
Never in GAS.
Never in client.

### AUTH_SESSION_TTL_HOURS
Purpose:
Defines DB session expiration TTL.

Required:
YES

MVP expected:
12

Validation:
Presence and parseable positive integer.

### EDS_SESSION_HMAC_SECRET
Status:
DEFERRED / NOT REQUIRED FOR DB SESSION MVP
unless signed-token/HMAC strategy is selected later.

Reason:
DB session MVP stores session_token_hash and validates by lookup.
Raw token is random; DB stores hash only.

## Safe Verification Method

Allowed future check:
- code may verify env variable presence
- logs may report variable_present: true/false
- logs must NOT print values

Example safe status:
```json
{
  "SUPABASE_URL": "present",
  "SUPABASE_SERVICE_ROLE_KEY": "present",
  "AUTH_SESSION_TTL_HOURS": "present_valid"
}
```

Forbidden:
- printing secrets
- committing .env
- storing secret values in docs
- sending service role key to GAS/client

## Fail Closed Rule

If required env is missing:
API must return controlled internal startup/config error.
Login endpoint must not operate.

## Render Boundary

Render env changes require separate operator action.
Cursor must not set Render env.
Cursor must not request secrets in chat.

## Local Dev Boundary

Local .env may exist only outside repo commit.
.env must remain ignored.
No secrets in documentation.

## Implementation Gate

Before coding:
- env lock-in plan audited PASS
- Cursor may implement presence checks without printing values
- actual Render env confirmation may be manual/operator-provided

## Verdict
ENV_LOCK_IN_PLAN_PREPARED / PENDING_GEMINI_AUDIT
