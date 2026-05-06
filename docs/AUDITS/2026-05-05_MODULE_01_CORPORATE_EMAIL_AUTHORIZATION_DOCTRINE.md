# MODULE 01 CORPORATE EMAIL AUTHORIZATION DOCTRINE

## Status
DOC ONLY / AUTHORIZATION DOCTRINE / NO IMPLEMENTATION

## Purpose
Define the first authorization doctrine for Sakura / Module 01 personal Google Sheet terminals.

## Core Decision
Use corporate employee email as the primary user identity.

Preferred model:
- corporate email + password
- roles resolved from Supabase
- admin-provisioned access only

Rejected as primary model:
- open self-registration
- role binding only by Google account
- local Sheet-based role storage
- GAS-side access decisions

## User Identity Doctrine

Primary identity:
- corporate employee email

Examples:
- `user@eds-ukraine.com`

Corporate email is used to:
- find user in Supabase
- resolve user status
- resolve assigned roles
- determine available menu/functions

Google account may be used only as secondary technical context if needed later, but not as the primary role source.

## Google Session Identity Separation

Corporate email stored in Supabase is the Sakura identity.

Google account identity is not the Sakura authorization source.

GAS must not use:
- `Session.getActiveUser().getEmail()`
- `Session.getEffectiveUser().getEmail()`

as automatic authorization proof, login bypass, or role source.

Allowed future use:
- optional display hint only
- optional diagnostic context only
- optional secondary signal only if separately audited

Login Modal must require explicit corporate email entry unless a future audited SSO doctrine replaces this rule.

Google Session email must never override:
- corporate email entered by user
- Supabase user registry
- Supabase role assignments
- API authorization decision

## Registration Doctrine

Self-registration is forbidden.

Only admin can:
- create user
- assign corporate email
- assign role/roles
- issue initial password
- activate/deactivate user
- reset password
- assign or replace personal Google Sheet terminal

User cannot create their own account.

## Password Doctrine

Each user must have a password.

Initial password:
- issued by admin
- may be temporary
- user may be required to change it on first login

User must be able to:
- change password
- request password reset through corporate email

Admin must be able to:
- reset user password
- issue temporary password
- force password change on next login
- disable user access

Important security rule:
Passwords must never be stored as plain text.

Future data model should support fields such as:
- `password_hash`
- `password_updated_at`
- `must_change_password`
- `reset_token_hash`
- `reset_token_expires_at`
- `failed_login_attempts`
- `locked_until`

Do not implement these fields yet in this task. Record doctrine only.

## First Login Flow

When user opens personal Google Sheet terminal for the first time:

Custom menu shows only:

EDS Power
- Авторизуватись

No other functional menu items are visible before authorization.

User clicks:
Авторизуватись

Modal window asks:
- corporate email
- password

User must manually enter corporate email and password.

GAS sends request to API over HTTPS:
- entered corporate email
- password
- spreadsheet_id
- client_type = GAS
- module/mode context if needed

GAS does not auto-fill or silently authorize using Google account email.
GAS does not decide access locally.

API checks Supabase:
- user exists
- user status is ACTIVE
- password is valid
- user has active role/roles
- terminal is allowed / assigned if terminal binding is active

API returns:
- authorization status
- user display name
- role/roles
- allowed menu items / permissions

GAS then renders role-aware EDS Power menu.

## Failed Login Flow

If corporate email is not found:
Show message:
Користувача з такою корпоративною поштою не зареєстровано. Зверніться до адміністратора.

If password is incorrect:
Show message:
Невірний пароль.

If user is disabled:
Show message:
Доступ заблоковано. Зверніться до адміністратора.

If terminal is not assigned:
Show message:
Цей термінал не прив'язаний до вашого користувача. Зверніться до адміністратора.

## Role-Aware Menu Doctrine

Menu is generated according to roles returned by API.

Example before authorization:

EDS Power
- Авторизуватись

Example after authorization for calculation engineer:

EDS Power
- Модуль розрахунків
  - Створити новий розрахунок
  - Переглянути існуючий розрахунок
- Профіль
  - Змінити пароль
  - Вийти

Example future roles:
- OWNER
- ADMIN
- DIRECTOR
- SALES_MANAGER
- CALCULATION_ENGINEER
- CONSTRUCTOR
- TECHNOLOGIST
- PRODUCTION
- KITTING

The exact menu matrix is not implemented in this task.
This doctrine only defines the principle.

## Permission Set / Menu Schema Doctrine

API response must include an explicit permission set or menu schema.

GAS renders menu from API response.

GAS must not contain authoritative hardcoded role-to-menu access logic.

GAS may contain only display/rendering logic, for example:
- draw menu item labels
- call menu actions allowed by API
- refresh displayed menu after authorization

Authorization truth remains:
Supabase -> API -> permission/menu schema -> GAS render

## Session Revalidation Doctrine

Because roles may change while a Google Sheet session is open, local menu state is temporary.

Required future behavior:
- `onOpen` must revalidate authorization with API
- "Оновити меню" / "Refresh Menu" command should be available after login
- logout must clear local authorization/session state
- API response should include permission/menu schema version or timestamp if needed later

GAS menu display must be treated as a cached UI surface, not a source of truth.

## Personal Terminal Doctrine

One user may have a personal Google Sheet terminal.

Personal terminal:
- is only a UI surface
- does not store authoritative roles
- does not store passwords
- does not store business truth
- receives allowed actions from API

Supabase remains Source of Truth.

GAS remains thin client:
- modal UI
- transport
- display
- no business logic
- no authorization logic
- no password storage

## Forgot Password / Password Reset Doctrine

User may request password reset from login modal:

Забув пароль

Flow:
1. User enters corporate email.
2. API checks if active user exists.
3. System sends reset link or reset code to corporate email.
4. User sets new password.
5. Reset token/code expires after limited time.

Important:
The system should reset password, not "remind" the old password.
Old password must not be recoverable.

No email sending implementation in this task.
Record doctrine only.

## Admin Password Reset Doctrine

Admin must be able to:
- reset password for user
- generate temporary password
- force password change on next login
- disable user account

Admin reset should be audited in future:
- actor admin user
- target user
- timestamp
- request_id if available
- source client

No admin UI implementation in this task.

## Security Guardrails

Forbidden:
- store password in Google Sheet cells
- store password in GAS PropertiesService
- write password to logs
- store plain-text password in Supabase
- send password in URL/query parameters
- make GAS decide authorization locally
- allow self-registration
- expose role management to non-admin users
- use Google Session email as login bypass
- use Google Session email as role source
- hardcode role-to-menu authorization in GAS
- keep stale role/menu state without revalidation path

Required future principles:
- HTTPS only
- password hash only
- reset tokens hashed
- audit password reset actions
- admin-only provisioning
- API-side permission enforcement
- role/menu decisions returned from API

## Relation To Existing Module 01 Schema

Current Module 01 Slice 01 already has:
- `module01_users`
- `module01_roles`
- `module01_user_roles`
- `module01_user_terminals`

This doctrine may require future schema expansion for authentication fields, for example:
- `password_hash`
- `must_change_password`
- `reset_token_hash`
- `reset_token_expires_at`

Do not modify schema in this task.
Do not create migration in this task.

## Boundary

This document does not authorize:
- SQL migration
- schema changes
- API implementation
- GAS implementation
- modal UI implementation
- password reset service
- email service
- production deployment

## Next Allowed Step

Authorization Data Model Extension Plan.

Follow-up planning sequence after this step:
1. authorization data model extension
2. login modal UI plan
3. API auth endpoint plan
4. role-aware menu plan

## Gemini Audit Status

- verdict: PASS WITH DOC FIXES
- required fixes:
  - Google Session identity separation
  - API-provided permission/menu schema
  - session/menu revalidation doctrine
- fixes applied: YES
- status after fixes: READY FOR GEMINI RE-AUDIT
- no implementation performed

## Gemini Re-Audit Status

- final verdict: PASS
- doctrine status: CLOSED / APPROVED
- no required blocking fixes
- carry-forward note: API Auth Endpoint Plan must require GAS to send `terminal_id` / `spreadsheet_id` during login so `module01_user_terminals` enforcement is possible
- next allowed step: Authorization Data Model Extension Plan
