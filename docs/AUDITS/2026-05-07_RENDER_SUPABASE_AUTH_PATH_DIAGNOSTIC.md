# Render → Supabase Module 01 login diagnostic logging

**Date:** 2026-05-07  
**Mode:** Backend **log-only** instrumentation (no auth decision changes, no client envelope changes).

## Objective

When `POST /api/module01/auth/login` returns generic **`AUTH_FAILED`** (HTTP 200), operators need **server-side** evidence of which gate failed (user lookup, auth row, lock, password verify, role, terminal / spreadsheet binding) without exposing secrets in API responses.

## Security

**Forbidden in logs:** plaintext password, `password_hash`, session tokens, Supabase service role key, other full secrets.

**Client contract unchanged:** responses remain generic **`AUTH_FAILED`** for denied login paths; **`AUTH_CONFIG_ERROR`** for configuration failures remains as before.

## Enable / disable

Emission is **`OFF` by default**. Set environment variable **`EDS_POWER_AUTH_DEBUG_LOGS`** to a truthy value (`1`, `true`, `yes`, `on`) **only** for short-lived triage. Unset or falsy in production.

## Log format

Search Render logs for prefix:

`EDS_POWER_AUTH_LOGIN_DIAG`

Each line is a single JSON object (sorted keys) after that prefix, written to **process stdout** via `print(..., flush=True)` **only when `EDS_POWER_AUTH_DEBUG_LOGS` is truthy**, so lines appear alongside Uvicorn access logs (Python’s default logging config often drops `logging.info` from app modules).

### Allowed fields

| Field | Description |
|--------|-------------|
| `request_id` | Correlates with response `metadata.request_id` on success; ties multiple diag lines for one attempt. |
| `auth_stage` | Current pipeline stage (see below). |
| `email_present` | Request shape: email present and non-empty string. |
| `email_domain` | Domain part of email only (no local-part). |
| `spreadsheet_id_present` | Request shape: spreadsheet id present. |
| `spreadsheet_id_suffix` | Last up to 6 characters of spreadsheet id (reduced fingerprint). |
| `supabase_query_user_found` | User row returned for email filter. |
| `user_status` | Raw `module01_users.status` when loaded. |
| `supabase_query_auth_row_found` | Row in `module01_user_auth` for `user_id`. |
| `password_algorithm` | Value from auth row (e.g. `ARGON2ID`); **not** the hash. |
| `password_hash_present` | Non-empty string hash present (boolean only). |
| `locked_until_present` | `locked_until` considered set for logging purposes. |
| `password_verify_result` | Set when password step completed: `false` mismatch, `true` if verifier accepted. |
| `supabase_query_terminal_found` | Terminal row returned for `user_id` + `spreadsheet_id` filter. |
| `terminal_status` | `module01_user_terminals.status` when row loaded. |
| `terminal_spreadsheet_match` | Stored `spreadsheet_id` on row equals request (when comparable). |
| `final_auth_result` | `AUTH_FAILED` on intermediate/failure lines; `LOGIN_SUCCESS` on success line. |

### `auth_stage` values (emitted)

- `LOGIN_REQUEST_RECEIVED` — malformed body or config failure before/upon entry (subset of fields).
- `USER_LOOKUP_STARTED`
- `USER_LOOKUP_FAILED` — no user, invalid `user_id`, or **unexpected exception** (coarse bucket).
- `USER_FOUND` — user active; also reused when **password verify succeeded** but **`TEST_OPERATOR`** role is missing (see below).
- `USER_INACTIVE`
- `AUTH_ROW_LOOKUP_STARTED`
- `AUTH_ROW_MISSING`
- `AUTH_ROW_FOUND`
- `USER_LOCKED` — `locked_until` in the future, or unparseable lock timestamp (same fail-closed behavior as before).
- `PASSWORD_VERIFY_STARTED`
- `PASSWORD_VERIFY_FAILED`
- `TERMINAL_LOOKUP_STARTED`
- `TERMINAL_FOUND`
- `TERMINAL_INACTIVE`
- `SPREADSHEET_ID_MISMATCH` — no terminal row for `(user_id, spreadsheet_id)` (equivalent to prior “terminal None” path).
- `TERMINAL_LOOKUP_FAILED` — terminal row present but **`id`** invalid (same as before).
- `LOGIN_SUCCESS`

### Interpretation notes

1. **Role gate:** There is no separate `auth_stage` for “role missing”. If **`password_verify_result` is `true`** and **`auth_stage` is `USER_FOUND`** with **`final_auth_result` `AUTH_FAILED`**, the failure is **after password verification** and **before terminal lookup** — i.e. **`TEST_OPERATOR`** not in resolved active role codes.
2. **Multiple lines per request:** Normal — stage transitions emit separate diagnostics; filter by **`request_id`**.
3. **Removal:** This telemetry is intended as **temporary** operations aid; remove or gate behind env when root cause is found.

## Code touchpoint

- `main.py`: `module01_auth_login`, helpers `_auth_emit_login_diagnostic`, `_auth_redact_email_domain`, `_auth_redact_spreadsheet_suffix`, `_auth_login_shape_flags`.

## Operator: Render verify

1. Deploy revision containing this logging.
2. Reproduce login from GAS (or curl) once.
3. In Render → **Logs**, grep **`EDS_POWER_AUTH_LOGIN_DIAG`** and the **`request_id`** from the JSON response metadata (if present) or time window.
4. Read the **last** `auth_stage` with **`AUTH_FAILED`** before success (if any) to locate the gate.
