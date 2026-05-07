# Terminal spreadsheet match — internal diagnostics (2026-05-07)

## Objective

When login fails at **`SPREADSHEET_ID_MISMATCH`** despite operators believing the Sheet id matches, stdout diagnostics must show **why** the normalized compare disagrees — **without** logging full `spreadsheet_id` strings, passwords, hashes, or tokens.

## Where emitted

- **`SPREADSHEET_ID_MISMATCH`** — full digest block (failure path).
- **`TERMINAL_FOUND`** — same digest block (success path past spreadsheet compare); confirms request vs stored alignment in logs.

## Fields (stdout `EDS_POWER_AUTH_LOGIN_DIAG`)

| Key | Meaning |
|-----|---------|
| `request_spreadsheet_len` | Character length of request value as received by login (after `_auth_validate_request_shape` strip). |
| `stored_spreadsheet_len` | Character length of raw DB/API value (stringified if non-string). |
| `request_spreadsheet_suffix_12` | Last up to 12 characters of raw request (partial fingerprint). |
| `stored_spreadsheet_suffix_12` | Last up to 12 characters of raw stored. |
| `request_spreadsheet_md5` | `md5(utf-8)` hex of **raw** request string. |
| `stored_spreadsheet_md5` | `md5(utf-8)` hex of **raw** stored string. |
| `request_spreadsheet_normalized_len` | Length after `_auth_normalize_login_spreadsheet_id`. |
| `stored_spreadsheet_normalized_len` | Same for stored. |
| `request_spreadsheet_normalized_md5` | `md5(utf-8)` of normalized request. |
| `stored_spreadsheet_normalized_md5` | `md5(utf-8)` of normalized stored. |
| `terminal_spreadsheet_match` | Boolean per same rule as auth gate (`bool(norm_stored) and norm_request == norm_stored`). |

## Security

- No full `spreadsheet_id` in diagnostic JSON (suffix + hash only).
- No passwords, `password_hash`, session tokens, or service keys.

## Code

- `main.py`: `_auth_login_spreadsheet_id_diag`, merged into `_auth_emit_login_diagnostic` payloads for the stages above; keys whitelisted in `_AUTH_LOGIN_DIAG_ALLOWED_KEYS`.

## Operator use

After deploy, grep **`EDS_POWER_AUTH_LOGIN_DIAG`** for the failing **`request_id`**. If **`SPREADSHEET_ID_MISMATCH`**: compare **lengths**, **suffix_12**, and **md5** pairs — mismatches isolate invisible/extra characters or entirely different ids without pasting full values into tickets.
