# MODULE 01 GAS AUTH INTEGRATION PLAN

## Objective
Define safe GAS integration architecture for Module 01 auth system.

## GAS Boundary

GAS responsibilities:
- transport only
- session token storage
- UI/menu interaction
- forwarding authenticated API requests

Forbidden:
- password verification
- Supabase access
- role calculation
- session creation
- token hashing

## Planned GAS Components

Suggested modules:
- AuthMenu.gs
- AuthTransport.gs
- AuthSession.gs
- AuthUi.gs

Document purpose only.
Do NOT implement.

## Login Transport Plan

Use:
`UrlFetchApp.fetch()`

Method:
`POST`

Headers:
`Content-Type: application/json`

Body:
```json
{
  "email": "<user email>",
  "password": "<user password>",
  "spreadsheet_id": "<spreadsheet id>"
}
```

Transport:
HTTPS only.

## Session Token Storage Plan

Use:
`PropertiesService`

Preferred:
`UserProperties`

Fallback:
`DocumentProperties` only if governance requires shared session behavior.

Store:
- session_token
- expires_at
- user_email
- optional role_codes cache

Never store:
- password
- password hash
- Supabase keys

## Session Validation Strategy

Before API calls:
- check token exists
- optional local expires_at precheck
- otherwise backend validates session

Backend remains source of truth.

## Planned Auth Menu Flow

Before login:
Menu:
- Авторизуватись

After login:
Menu:
- Оновити меню
- Вийти
- доступні actions later

## Failure Handling

Network/API failures:
- friendly UI message
- no raw stack trace to user

AUTH_FAILED:
- generic login failure message

Missing token:
- require re-login

Expired session:
- require re-login

## Security Rules

Never:
- log password
- log session token
- expose token in spreadsheet cells
- expose token in alerts/toasts
- send token to third-party services

Only backend validates auth.

## Session Usage Rule

Future API requests:
`Authorization: Bearer <session_token>`

No Supabase direct calls from GAS.

## Open Questions

- UserProperties vs DocumentProperties
- session refresh strategy
- logout cleanup behavior
- session expiration UX
- multi-user same-sheet behavior
- token rotation later

## Recommended MVP Decisions

For MVP:
- UserProperties preferred
- manual re-login after expiration
- no refresh endpoint yet
- explicit logout clears token
- one user session per spreadsheet user

## Manual Testing Plan

Planned tests:
1. successful login
2. wrong password
3. invalid spreadsheet_id
4. expired session
5. logout cleanup
6. no token state

## Implementation Gate

Before GAS code:
- Gemini audit PASS
- decide UserProperties vs DocumentProperties
- confirm menu lifecycle
- confirm logout behavior

## Boundary Confirmation

Confirm:
- no GAS code created
- no API changes
- no SQL
- no DB writes
- no secrets stored

## Verdict
GAS_AUTH_INTEGRATION_PLAN_PREPARED / PENDING_GEMINI_AUDIT
