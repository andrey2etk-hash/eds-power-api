# MODULE 01 API AUTH ENDPOINT DATA CONTRACT PLAN

## Status
DOC ONLY / DATA CONTRACT PLANNING / NO IMPLEMENTATION

## Purpose
Define request/response JSON contracts and headers for Module 01 authorization endpoints.

## Source Principles
- corporate email is primary identity
- Google Session email is not auth proof
- admin-provisioned users only
- password required
- terminal_id / spreadsheet_id required
- API is sole authorization authority
- roles are additive
- API returns roles[], permissions[], menu_schema
- GAS renders only menu_schema
- session model is stateful opaque session token

## Common Headers

### Login Request Headers
Required:
- X-EDS-Client-Type: GAS
- X-EDS-Request-ID: optional but recommended

Not required before login:
- Authorization

### Authenticated Request Headers
Required:
- Authorization: Bearer <session_token>
- X-EDS-Terminal-ID: <spreadsheet_id>
- X-EDS-Client-Type: GAS
- X-EDS-Request-ID: optional but recommended

Forbidden:
- password in headers
- password in URL
- session token in URL
- Google Session email as auth header

## Common Response Envelope

Use consistent envelope:

```json
{
  "status": "SUCCESS",
  "data": {},
  "error": null,
  "metadata": {
    "request_id": "...",
    "api_version": "v1",
    "client_type": "GAS"
  }
}
```

or

```json
{
  "status": "FAILED",
  "data": null,
  "error": {
    "error_code": "...",
    "message": "...",
    "source_field": "..."
  },
  "metadata": {
    "request_id": "...",
    "api_version": "v1",
    "client_type": "GAS"
  }
}
```

No response may include:
- password
- password_hash
- reset_token_hash
- raw reset token except in future controlled reset flow if explicitly approved
- service keys
- Supabase secrets

## Endpoint 1: POST /api/v1/auth/login

### Purpose
Authenticate corporate user and create opaque session.

### Request Headers
Required:
- X-EDS-Client-Type: GAS

Optional:
- X-EDS-Request-ID

### Request Body

```json
{
  "email": "user@eds-ukraine.com",
  "password": "plaintext-password-entered-by-user",
  "terminal": {
    "spreadsheet_id": "google-sheet-id"
  }
}
```

Rules:
- email is manually entered by user
- password is sent only over HTTPS
- spreadsheet_id is required
- Google Session email must not be used as identity

### Success Response

```json
{
  "status": "SUCCESS",
  "data": {
    "auth_status": "AUTHENTICATED",
    "session": {
      "session_token": "<opaque-token>",
      "expires_at": "2026-05-05T12:00:00Z"
    },
    "user": {
      "user_id": "<uuid>",
      "email": "user@eds-ukraine.com",
      "display_name": "User Name",
      "status": "ACTIVE"
    },
    "terminal": {
      "terminal_id": "<uuid>",
      "spreadsheet_id": "google-sheet-id",
      "status": "ACTIVE"
    },
    "roles": [
      "CALCULATION_ENGINEER"
    ],
    "permissions": [
      "CALCULATION_CREATE",
      "CALCULATION_VIEW_OWN"
    ],
    "menu_schema": [
      {
        "menu_group_id": "calculations",
        "label": "Модуль розрахунків",
        "items": [
          {
            "action_id": "calculation.create",
            "label": "Створити новий розрахунок",
            "enabled": true,
            "order": 10,
            "required_permission": "CALCULATION_CREATE"
          }
        ]
      }
    ],
    "must_change_password": false
  },
  "error": null,
  "metadata": {
    "request_id": "...",
    "api_version": "v1",
    "client_type": "GAS"
  }
}
```

### Success With Required Password Change

If `must_change_password = true`:

```json
{
  "status": "SUCCESS",
  "data": {
    "auth_status": "PASSWORD_CHANGE_REQUIRED",
    "session": {
      "session_token": "<opaque-token>",
      "expires_at": "..."
    },
    "allowed_actions": [
      "auth.change_password",
      "auth.logout"
    ],
    "menu_schema": [
      {
        "menu_group_id": "profile",
        "label": "Профіль",
        "items": [
          {
            "action_id": "auth.change_password",
            "label": "Змінити пароль",
            "enabled": true,
            "order": 10,
            "required_permission": "PASSWORD_CHANGE_REQUIRED"
          }
        ]
      }
    ]
  },
  "error": null,
  "metadata": {
    "request_id": "...",
    "api_version": "v1",
    "client_type": "GAS"
  }
}
```

### Failure Response Examples

Invalid password:

```json
{
  "status": "FAILED",
  "data": null,
  "error": {
    "error_code": "AUTH_INVALID_CREDENTIALS",
    "message": "Невірна пошта або пароль.",
    "source_field": "credentials"
  },
  "metadata": {
    "request_id": "...",
    "api_version": "v1",
    "client_type": "GAS"
  }
}
```

Important:
Do not expose `AUTH_EMAIL_NOT_FOUND` to user-facing response.
Internal audit may record exact cause.

Terminal missing:

```json
{
  "status": "FAILED",
  "data": null,
  "error": {
    "error_code": "AUTH_TERMINAL_REQUIRED",
    "message": "Не передано ідентифікатор термінала.",
    "source_field": "terminal.spreadsheet_id"
  },
  "metadata": {
    "request_id": "...",
    "api_version": "v1",
    "client_type": "GAS"
  }
}
```

Terminal not assigned:

```json
{
  "status": "FAILED",
  "data": null,
  "error": {
    "error_code": "AUTH_TERMINAL_NOT_ASSIGNED",
    "message": "Цей термінал не прив'язаний до вашого користувача. Зверніться до адміністратора.",
    "source_field": "terminal.spreadsheet_id"
  },
  "metadata": {
    "request_id": "...",
    "api_version": "v1",
    "client_type": "GAS"
  }
}
```

## Endpoint 2: POST /api/v1/auth/refresh_menu

### Purpose
Validate existing opaque session and return current roles, permissions, and menu_schema.

### Request Headers
Required:
- Authorization: Bearer <session_token>
- X-EDS-Terminal-ID: <spreadsheet_id>
- X-EDS-Client-Type: GAS

### Request Body

```json
{
  "request_context": {
    "reason": "onOpen"
  }
}
```

Allowed `reason` values:
- `onOpen`
- `manual_refresh`

Slice 01 rule:
- `refresh_menu` on every `onOpen` is mandatory.

### Success Response

```json
{
  "status": "SUCCESS",
  "data": {
    "auth_status": "AUTHENTICATED",
    "user": {
      "user_id": "<uuid>",
      "email": "user@eds-ukraine.com",
      "display_name": "User Name"
    },
    "terminal": {
      "terminal_id": "<uuid>",
      "spreadsheet_id": "google-sheet-id",
      "status": "ACTIVE"
    },
    "roles": [],
    "permissions": [],
    "menu_schema": [],
    "menu_schema_version": "v1",
    "session": {
      "expires_at": "..."
    }
  },
  "error": null,
  "metadata": {
    "request_id": "...",
    "api_version": "v1",
    "client_type": "GAS"
  }
}
```

### Failure Response

If token expired/revoked:

```json
{
  "status": "FAILED",
  "data": null,
  "error": {
    "error_code": "AUTH_SESSION_INVALID",
    "message": "Сесію завершено. Авторизуйтесь повторно.",
    "source_field": "Authorization"
  },
  "metadata": {
    "request_id": "...",
    "api_version": "v1",
    "client_type": "GAS"
  }
}
```

GAS behavior:
- delete local `session_token`
- show only `Авторизуватись` menu

## Endpoint 3: POST /api/v1/auth/logout

### Purpose
Revoke current session and instruct GAS to clear local token/menu state.

### Headers
Required:
- Authorization: Bearer <session_token>
- X-EDS-Terminal-ID: <spreadsheet_id>
- X-EDS-Client-Type: GAS

### Request Body

```json
{
  "reason": "user_logout"
}
```

### Success Response

```json
{
  "status": "SUCCESS",
  "data": {
    "revoked": true,
    "local_clear_required": true
  },
  "error": null,
  "metadata": {
    "request_id": "...",
    "api_version": "v1",
    "client_type": "GAS"
  }
}
```

GAS behavior:
- delete local `session_token` from `UserProperties`
- show only `Авторизуватись` menu

## Endpoint 4: POST /api/v1/auth/change_password

### Purpose
Allow authenticated user to change password.

### Headers
Required:
- Authorization: Bearer <session_token>
- X-EDS-Terminal-ID: <spreadsheet_id>
- X-EDS-Client-Type: GAS

### Request Body

```json
{
  "current_password": "old-password",
  "new_password": "new-password",
  "confirm_password": "new-password"
}
```

### Success Response

```json
{
  "status": "SUCCESS",
  "data": {
    "password_changed": true,
    "must_change_password": false
  },
  "error": null,
  "metadata": {
    "request_id": "...",
    "api_version": "v1",
    "client_type": "GAS"
  }
}
```

Rules:
- `current_password` required unless future admin reset flow allows reset token
- new password must meet policy
- password values never logged

## Endpoint 5: POST /api/v1/auth/request_password_reset

### Purpose
Request password reset through corporate email.

### Headers
Required:
- X-EDS-Client-Type: GAS

### Request Body

```json
{
  "email": "user@eds-ukraine.com"
}
```

### Response
Always neutral:

```json
{
  "status": "SUCCESS",
  "data": {
    "message": "Якщо акаунт існує, інструкції буде надіслано на корпоративну пошту."
  },
  "error": null,
  "metadata": {
    "request_id": "...",
    "api_version": "v1",
    "client_type": "GAS"
  }
}
```

Rules:
- do not reveal if email exists
- store only `reset_token_hash`
- never log raw token
- email service not implemented in this task

## Endpoint 6: POST /api/v1/auth/admin_reset_password

### Purpose
Allow admin to reset password or force password change.

### Headers
Required:
- Authorization: Bearer <session_token>
- X-EDS-Terminal-ID: <spreadsheet_id>
- X-EDS-Client-Type: GAS

### Request Body

```json
{
  "target_user_id": "<uuid>",
  "mode": "TEMPORARY_PASSWORD",
  "force_change": true
}
```

Allowed `mode` values:
- `TEMPORARY_PASSWORD`
- `RESET_LINK`

### Success Response

```json
{
  "status": "SUCCESS",
  "data": {
    "admin_reset_completed": true,
    "target_user_id": "<uuid>",
    "must_change_password": true
  },
  "error": null,
  "metadata": {
    "request_id": "...",
    "api_version": "v1",
    "client_type": "GAS"
  }
}
```

Rules:
- requires `ADMIN` or `OWNER` permission
- action must be audited
- never return temporary password in response

## Session Storage Contract

### GAS Side
GAS may store:
- session_token
- session_expires_at
- user display label if needed
- menu_schema cache if needed

GAS must not store:
- password
- password_hash
- reset token
- reset_token_hash
- Supabase keys
- service_role key

Storage:
- `PropertiesService.getUserProperties()`

### API Side
API stores:
- session_token_hash
- user_id
- terminal_id
- expires_at
- revoked_at
- last_seen_at
- client_type

Future table likely:
- `module01_user_sessions`

No SQL in this task.

## Terminal-Session Binding Rule

For every authenticated request:
- API must load session by `session_token_hash`.
- API must compare request header `X-EDS-Terminal-ID` with session `terminal_id` / `spreadsheet_id` binding.
- If `X-EDS-Terminal-ID` does not match the session-bound terminal:
  - revoke the session immediately
  - return `AUTH_SESSION_INVALID`
  - audit `SESSION_TERMINAL_MISMATCH` or equivalent session failure event
  - never process the requested action
- GAS must clear local `session_token` and return UI to only `Авторизуватись`.

## Session Token Entropy Rule

`session_token` must be:
- opaque
- generated by cryptographically secure random generator
- high entropy
- not derived from `user_id` / email / `terminal_id` / time
- stored by API only as `session_token_hash`
- returned to GAS only once during login response

Recommended MVP token:
- 32-byte random token encoded as hex/base64url

Do not store raw token in database or logs.

## Error Code Registry

Include planned error codes:
- AUTH_INVALID_CREDENTIALS
- AUTH_USER_DISABLED
- AUTH_USER_LOCKED
- AUTH_PASSWORD_CHANGE_REQUIRED
- AUTH_TERMINAL_REQUIRED
- AUTH_TERMINAL_NOT_FOUND
- AUTH_TERMINAL_NOT_ASSIGNED
- AUTH_NO_ACTIVE_ROLES
- AUTH_SESSION_INVALID
- AUTH_SESSION_EXPIRED
- AUTH_SESSION_REVOKED
- AUTH_PASSWORD_POLICY_FAILED
- AUTH_PASSWORD_MISMATCH
- AUTH_RESET_REQUEST_ACCEPTED
- AUTH_ADMIN_PERMISSION_REQUIRED
- AUTH_INTERNAL_ERROR

## Audit Events

Planned audit events:
- LOGIN_SUCCESS
- LOGIN_FAILED
- LOGOUT
- SESSION_REFRESHED
- PASSWORD_CHANGED
- PASSWORD_RESET_REQUESTED
- PASSWORD_RESET_COMPLETED
- ADMIN_PASSWORD_RESET
- USER_LOCKED
- USER_UNLOCKED

Audit must never contain:
- password
- password_hash
- raw session token
- raw reset token
- reset_token_hash

## Boundary

This plan does not authorize:
- API implementation
- GAS implementation
- Python code
- SQL migration
- DB writes
- session table creation
- password hashing implementation
- email sending implementation
- production deployment

## Open Questions For Gemini

1. Is opaque token session model correctly represented in request/response contracts?
2. Should login response expose `session_token` directly to GAS, or wrap it in a nested `session` object as shown?
3. Should `AUTH_INVALID_CREDENTIALS` replace separate `AUTH_EMAIL_NOT_FOUND` / `AUTH_INVALID_PASSWORD` in user-facing errors?
4. Should `refresh_menu` be mandatory on every `onOpen`?
5. Should `permissions[]` be returned in addition to `menu_schema`?
6. Should `admin_reset_password` ever return a temporary password, or should it only trigger reset link/force-change flow?
7. Is `UserProperties` acceptable for storing `session_token` in GAS for MVP?

## Recommended Next Step

Gemini audit of this Data Contract Plan.

If PASS:
Create API Auth Endpoint Implementation Slice Plan.

## Gemini Audit Status

- final verdict: PASS
- plan status: CLOSED / APPROVED
- required fixes applied:
  - terminal-session binding enforcement
  - high-entropy opaque token rule
- opaque token model accepted
- `session_token` wrapped in `session` object accepted
- `AUTH_INVALID_CREDENTIALS` should replace separate public email/password failure codes
- `refresh_menu` on `onOpen` is mandatory for Slice 01
- return both `permissions[]` and `menu_schema`
- `admin_reset_password` must never return temporary password in response
- `UserProperties` accepted for GAS token storage in MVP
- next allowed step: API Auth Endpoint Implementation Slice Plan
