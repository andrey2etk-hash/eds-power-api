# EDS Power DB-Driven Menu Backend Integration Plan

## 1. Purpose

Define how the FastAPI backend will read menu, module, and action visibility from the new `eds_power_*` registry tables in Supabase after **EDS_POWER_SQL_REGISTRY_S01** manual apply. This document is **planning only**: no Python, no SQL execution, no endpoint implementation.

## 2. Current Registry State

**Confirmed tables (operator-verified after manual apply):**

- `public.eds_power_modules`
- `public.eds_power_module_actions`
- `public.eds_power_role_module_access`

**Confirmed seed rows (conceptual handles; data lives in Supabase):**

- Modules: **SYSTEM_SHELL**, **MODULE_01**
- Actions: **REFRESH_MENU**, **SESSION_STATUS**, **LOGOUT**, **MODULE_01_PLACEHOLDER**

**Baseline counts (operator-reported):**

- `modules_count` = 2  
- `actions_count` = 4  
- `role_bindings_count` = 40  
- `updated_at` triggers = 3  

**Registry migration dependency:** **`EDS_POWER_SQL_REGISTRY_S01_APPLY_SUCCESS`** (see `docs/AUDITS/2026-05-07_EDS_POWER_SQL_REGISTRY_S01_MANUAL_APPLY_REPORT.md`).

Related contracts:

- `docs/ARCHITECTURE/EDS_POWER_DB_DRIVEN_DYNAMIC_MENU_REGISTRY_CONTRACT.md`
- `docs/ARCHITECTURE/EDS_POWER_DYNAMIC_MENU_PAYLOAD_CONTRACT.md`

## 3. Architecture Principle

**Backend decides.** The backend owns permission resolution, environment scoping, and menu shape.

**GAS** only:

- requests the menu payload over HTTPS (authenticated),
- renders the returned structure.

**GAS must NOT:**

- query Supabase directly,
- decide which modules or actions the user may see,
- filter by DEV / ADMIN_TEST / TEMPLATE (or similar) client-side,
- build the menu from hardcoded role logic that duplicates registry truth.

## 4. Proposed Service Layer

**Planned service name:** `MenuRegistryService` (or equivalent module-local name consistent with existing FastAPI layout).

**Responsibilities (design only):**

- Accept **authenticated user context** (session / identity already validated by existing auth flow).
- Resolve **`role_id`** / **`role_code`** for that user from the **authoritative source** used by Module 01 (to be confirmed in implementation readiness; see §13).
- Query the registry tables using **server-side** Supabase access (service role).
- Filter rows by **`environment_scope`** matching the **current backend environment** (see §6).
- Restrict to **active** modules and **enabled** actions per §5.
- Assemble and return a **normalized menu payload** aligned with §8 and the Dynamic Menu Payload Contract (no raw `eds_power_role_module_access` rows sent to the client).

**No implementation** is authorized by this document.

## 5. Required Query Logic

**Planning only.** The backend should resolve allowed menu items by joining registry data with the roles table used in Module 01.

**Logical join path:**

`public.eds_power_role_module_access` **acc**  
→ `public.eds_power_modules` **m** (on `acc.module_id = m.id`)  
→ `public.eds_power_module_actions` **a** (on `acc.action_id = a.id`)  
→ `public.module01_roles` **r** (on `acc.role_id = r.id`, for role integrity and optional metadata)

**Planned filters:**

- `acc.role_id` = authenticated user’s current role (same UUID / mapping as session).
- `acc.visible` = **true**
- `acc.enabled` = **true**
- `m.is_active` = **true**
- `a.enabled` = **true**
- `acc.environment_scope` = **current backend environment scope** (single value per deployment; see §13).
- **`m.module_status` allowed for current environment:** production deployments must not expose modules whose status is inappropriate for production (e.g. treat **DEV-only** or **ADMIN_TEST-only** visibility via binding `environment_scope` and/or status rules — exact matrix to be finalized at implementation and audit).

**Ordering:** plan to order modules by `m.sort_order`, actions by `a.sort_order` within each module.

## 6. Environment Scope Rules

Registry column **`environment_scope`** (per migration): `PRODUCTION`, `ADMIN_TEST`, `DEV`, `TEMPLATE`.

**Production backend** must return bindings scoped to **PRODUCTION** only (unless a **separate, audited** environment policy explicitly documents additional scopes for a non-production deployment).

**Production backend** must **NOT** return menu items whose effective scope is **DEV**, **ADMIN_TEST**, or **TEMPLATE** unless such a policy is explicitly approved and documented (fail closed by default).

Non-production backends (staging, local) may use different scope constants; those must be **configuration-driven**, not client-chosen query parameters.

## 7. Endpoint Planning

**Target endpoint concept:**

`GET /api/module01/auth/menu`

**Purpose:** Return an authenticated, **DB-driven** menu payload derived from the registry for the current user and environment.

**Current state:** Any **mock** or **hardcoded** menu path used today **remains** until a separate **implementation task** is approved after plan audit. This plan does **not** replace the mock.

**Auth:** Must require a valid Module 01 session / identity; anonymous access must not leak registry-backed menu.

## 8. Dynamic Menu Payload Contract

**Conceptual output shape** (align with `EDS_POWER_DYNAMIC_MENU_PAYLOAD_CONTRACT`; field names may be normalized to match that contract at implementation):

```json
{
  "status": "success",
  "data": {
    "modules": [
      {
        "module_code": "...",
        "module_name": "...",
        "module_status": "...",
        "actions": [
          {
            "action_key": "...",
            "action_type": "...",
            "menu_label": "...",
            "enabled": true,
            "metadata": {}
          }
        ]
      }
    ]
  },
  "error": null,
  "metadata": {
    "request_id": "...",
    "api_version": "...",
    "logic_version": null,
    "execution_time_ms": 0
  }
}
```

The actual envelope (`status`, `data`, `error`, `metadata`) must follow the **global API response envelope** and existing dynamic menu contract; `metadata` on each action may map from `public.eds_power_module_actions.metadata` where safe.

## 9. Error Contract

**Planned stable error codes** (exact strings subject to Gemini audit and alignment with `04_DATA_CONTRACTS`):

- `MENU_REGISTRY_UNAVAILABLE` — registry tables missing, migration not applied, or dependency failure.
- `MENU_ROLE_NOT_FOUND` — authenticated user has no resolvable role for registry lookup.
- `MENU_NO_ALLOWED_ACTIONS` — role valid but no rows pass filters (optional: may still return 200 with empty modules per product decision — **to be decided at implementation**).
- `MENU_ENVIRONMENT_SCOPE_INVALID` — backend environment not configured or cannot map to a valid scope.
- `MENU_REGISTRY_QUERY_FAILED` — database or Supabase client error after retries/logging.

All errors use the **global response envelope** with `status` ≠ success, structured `error`, and safe `metadata` (request id, no secrets).

## 10. Security Boundary

- Backend uses **service-role** (or equivalent server-only) access to Supabase for registry reads.
- **GAS** never receives raw `eds_power_role_module_access` rows or internal UUID graphs beyond what is required for UI (prefer opaque action keys and labels only).
- **GAS** receives only the **safe menu payload** defined by contract.
- **No secrets** in responses or logs; no direct client DB access.

## 11. Migration Dependency

This plan depends on:

- **`EDS_POWER_SQL_REGISTRY_S01_APPLY_SUCCESS`**

If registry tables are missing or unreadable, the menu reader must **fail closed** (error response, no guessed menu from registry).

## 12. Out of Scope

- Backend implementation code
- GAS menu rendering changes beyond what future tasks specify
- New SQL migrations or registry schema changes
- Role admin UI
- Advanced RBAC or per-button engines beyond registry rows
- Web/mobile rollout outside current GAS/Sheets context
- Calculation or Module 01 engineering logic

## 13. Implementation Readiness Checklist

Before any code task:

- [ ] Confirm **endpoint route** convention with existing Module 01 auth routes.
- [ ] Confirm **user role resolution** source (session claim, join table, etc.).
- [ ] Confirm **backend environment variable / constant** for `environment_scope` (e.g. `PRODUCTION` only on Render prod).
- [ ] Confirm **payload contract** alignment with `EDS_POWER_DYNAMIC_MENU_PAYLOAD_CONTRACT.md`.
- [ ] Confirm **fail-closed** behavior when registry is empty or query fails.
- [ ] **Gemini audit** of this plan (`DB_DRIVEN_MENU_BACKEND_PLAN_READY_FOR_AUDIT` → audited verdict).

## 14. Verdict

**`DB_DRIVEN_MENU_BACKEND_PLAN_READY_FOR_AUDIT`**
