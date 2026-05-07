# Module 01 login — terminal lookup fix (2026-05-07)

## Evidence

Render diagnostics showed **`PASSWORD_VERIFY`** success then **`SPREADSHEET_ID_MISMATCH`** with **`supabase_query_terminal_found: false`**, while Supabase UI showed an **ACTIVE** terminal for the same user with the expected **`spreadsheet_id`**.

## Root cause

Login used a **single Supabase query** on `module01_user_terminals` with **both** `user_id` **and** `spreadsheet_id` in **`.eq()`** filters (PostgREST exact match on `spreadsheet_id`).

That fails in production when the stored `spreadsheet_id` **does not byte-equal** the client value — for example **leading/trailing spaces**, **BOM** (`\ufeff`), or other invisible characters introduced via manual SQL / copy-paste — even though the operator-visible value matches the Sheet file id.

A secondary fragility: any subtle mismatch on the **compound** filter yields an empty result set, which previously collapsed into the same diagnostic bucket as a true “wrong sheet” case.

## Fix (backend only)

1. **Fetch terminal by `user_id` only** — schema enforces **`unique (user_id)`** on `module01_user_terminals`, so at most one row per user.
2. **Normalize** request and stored ids with **`_auth_normalize_login_spreadsheet_id`** (strip + remove common invisible characters).
3. **Enforce binding in Python**:
   - if no row → **`TERMINAL_LOOKUP_FAILED`** (generic client still `AUTH_FAILED`);
   - if normalized ids differ → **`SPREADSHEET_ID_MISMATCH`**;
   - if `status != ACTIVE` → **`TERMINAL_INACTIVE`** (unchanged);
   - else proceed to session creation.

**Security:** Wrong spreadsheet still fails; inactive terminal still fails; no bypass.

## Tests

- `tests/test_module01_auth_login_endpoint.py` — happy path with `user_id` filter; wrong sheet with terminal row present; no row; inactive terminal; BOM/whitespace normalization success.

## Verdict

**`PASS`** — aligns DB “looks correct” rows with client ids under real-world formatting noise without weakening terminal binding.
