# MODULE 01 LOGIN MODAL UI PLAN

## Status
DOC ONLY / UI PLANNING / NO IMPLEMENTATION

## Purpose
Define the planned Google Sheets login modal for Module 01 authorization.

## Source Principles
- corporate email is primary identity
- password required
- self-registration forbidden
- Google Session email is not auth proof
- API is sole authorization authority
- GAS is thin client
- terminal_id/spreadsheet_id must be sent to API
- opaque session token returned by API
- GAS stores only session_token in UserProperties

## Initial Menu State

Before authorization, custom menu shows only:

EDS Power
- Авторизуватись

No other functional menu items are visible before authorization.

## Login Modal Fields

Modal must contain:
- title: Авторизація EDS Power
- corporate email input
- password input
- Увійти button
- Забув пароль link/button
- optional status/error message area

Fields:
- email manually entered by user
- password manually entered by user
- no auto-login from Google Session email

Forbidden:
- using Session.getActiveUser().getEmail() as login bypass
- storing password in cells
- storing password in PropertiesService
- logging password

## Login Button Behavior

When user clicks Увійти:

GAS collects:
- email
- password
- spreadsheet_id from active spreadsheet
- client_type = GAS
- request_id if available

GAS sends request to:
POST /api/v1/auth/login

GAS receives:
- session_token
- expires_at
- user
- terminal
- roles[]
- permissions[]
- menu_schema
- must_change_password

If success:
- store session_token in UserProperties
- store expires_at if needed
- render menu_schema
- close modal or show success message

If must_change_password:
- show restricted menu / change password flow only

If failure:
- show user-friendly error
- do not store password
- do not store failed password
- do not expose internal technical details

## Error Display

User-facing messages:
- Невірна пошта або пароль.
- Доступ заблоковано. Зверніться до адміністратора.
- Цей термінал не прив'язаний до вашого користувача. Зверніться до адміністратора.
- Сесію завершено. Авторизуйтесь повторно.

Do not show:
- raw API stack traces
- password validation internals
- whether email exists, if security policy requires generic error

## Forgot Password UI

Modal includes:
- Забув пароль

Click behavior:
- user enters corporate email
- GAS calls password reset request endpoint later
- response message is neutral:
  Якщо акаунт існує, інструкції буде надіслано на корпоративну пошту.

No email implementation in this task.

## Session Storage UI Doctrine

GAS may store:
- session_token
- session_expires_at
- optional menu_schema cache

GAS must not store:
- password
- password_hash
- reset token
- reset_token_hash
- service_role key
- Supabase keys

Storage location:
- PropertiesService.getUserProperties()

## onOpen Behavior

On sheet open:
1. GAS checks if session_token exists in UserProperties.
2. If no token:
   show only Авторизуватись menu.
3. If token exists:
   call refresh_menu endpoint.
4. If refresh success:
   render returned menu_schema.
5. If refresh failed:
   delete local token
   show only Авторизуватись menu.

## Logout Behavior

Menu should support future logout:
- call /api/v1/auth/logout
- delete local session_token
- clear local menu cache
- show only Авторизуватись menu

## Visual Design Notes

Modal should be simple:
- clean white card
- EDS Power / Sakura title
- corporate email field
- password field
- primary Увійти button
- secondary Забув пароль action
- concise error area

No heavy UI implementation in this task.

## Boundary

This plan does not authorize:
- GAS implementation
- HTML modal creation
- API implementation
- SQL
- DB writes
- password handling implementation
- session handling implementation
- production deployment

## Dependency Note

Functional login implementation requires:
- API Auth Endpoint Implementation Slice Plan
- GAS Login Modal Implementation Plan
- API/GAS contract already approved

## Next Allowed Step

Gemini audit of Login Modal UI Plan.

If PASS:
Create API Auth Endpoint Implementation Slice Plan or GAS Login Modal Implementation Plan.

Recommended:
API Auth Endpoint Implementation Slice Plan before GAS implementation.

## Gemini Audit Status

- final verdict: PASS
- plan status: CLOSED / APPROVED
- onOpen `refresh_menu` behavior accepted
- token storage in `UserProperties` accepted
- carry-forward: timeout/fallback required for `refresh_menu`/`onOpen` implementation
- next allowed step: API Auth Endpoint Implementation Slice Plan
