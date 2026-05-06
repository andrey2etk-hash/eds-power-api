# MODULE 01 AUTHENTICATED API CALL PLAN

## Objective
Define how authenticated Sakura sessions will authorize future Module 01 API calls.

## Current Verified State
- FIRST_LIVE_SAKURA_LOGIN_PASS
- GAS -> Render -> Supabase auth flow verified
- Session row exists
- Authenticated menu state confirmed

## Planned Authenticated Request Flow
1. User logs in through Google Sheet terminal.
2. GAS stores session token only in UserProperties.
3. Future API request adds:
   Authorization: Bearer <session_token>
4. Backend validates session token.
5. Backend checks:
   - token hash exists
   - session is not revoked
   - expires_at is still valid
   - user exists
   - terminal is valid
   - role is allowed for requested action
6. Only then backend runs allowed Module 01 action.
7. Response returns through standard envelope.

## Target Future Endpoint Classes
Document conceptually only:
- authenticated calculation preview
- authenticated calculation prepare
- authenticated snapshot save
- authenticated user/session status check

Do NOT define final endpoint implementation yet unless already canonical.

## Required Backend Validation Rules
- missing Authorization header -> AUTH_MISSING_TOKEN
- invalid token -> AUTH_INVALID_TOKEN
- expired session -> AUTH_SESSION_EXPIRED
- revoked session -> AUTH_SESSION_REVOKED
- terminal mismatch -> AUTH_TERMINAL_MISMATCH
- insufficient role -> AUTH_FORBIDDEN_ROLE

## Response Envelope Requirement
All authenticated API responses must preserve existing contract:
```json
{
  "status": "...",
  "data": "...",
  "error": "...",
  "metadata": "..."
}
```

## Thin GAS Rule
GAS may:
- attach Authorization header
- call API
- display response
- show error message

GAS must NOT:
- validate token cryptographically
- decode token
- decide role permissions
- calculate engineering logic
- write directly to Supabase
- store token in repo/docs/chat

## Security Boundary
- Token value must never be written to docs.
- Password must never be written to docs.
- Token hash must never be written to docs.
- Backend owns token validation.
- Supabase stores session records.
- GAS is only authenticated client adapter.

## Out of Scope
- calculation implementation
- KZO/KTP/BMZ logic
- new DB migrations
- Render env changes
- role matrix expansion
- admin panel
- token refresh flow
- multi-client rollout

## Stage Gate
This plan must be reviewed before any authenticated calculation implementation begins.

## Verdict
AUTHENTICATED_API_CALL_PLAN_READY_FOR_REVIEW
