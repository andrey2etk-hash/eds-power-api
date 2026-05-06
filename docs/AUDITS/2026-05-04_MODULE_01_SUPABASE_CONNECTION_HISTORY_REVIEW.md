# MODULE 01 SUPABASE CONNECTION HISTORY REVIEW

## Status
DIAGNOSTIC REVIEW ONLY / NO DB WRITES

## Summary
- Previously successful path was read-only `--linked` connectivity checks with session-scoped `SUPABASE_DB_PASSWORD`, including at least one recorded `supabase db query --linked "SELECT 1..."` PASS.
- Consistent failure path is migration-management/remote apply path with `SQLSTATE 28P01`, including `supabase db push --linked`, and later `supabase migration list` / explicit pooler `--db-url` checks.
- Most likely mismatch is not API/code related but auth-context related (credential + connection mode/username path), with unresolved uncertainty around secret freshness/encoding and pooler login expectations.

## Connection Command Matrix

| command | connection mode | result | error | notes |
|---|---|---|---|---|
| `supabase projects list` | linked metadata/API | PASS | none | identity repeatedly confirmed for `mvcxtwoxhopumxcryxlc` (`EDSPower Database`) |
| `supabase db query --linked "select 1 as connectivity_check;"` | linked read-only | PASS | none | recorded in auth preflight result |
| `supabase migration list` (auth preflight report) | linked migration read-only | PASS | none | same preflight report states migration history read succeeded |
| `supabase db query --linked "SELECT 1 as auth_test;"` | linked read-only | PASS | none | PASS after CLI update + relink in DB-push auth diagnostic |
| `supabase migration list` (DB push auth diagnostic) | linked migration read-only | FAIL | `SQLSTATE 28P01` | failure output references pooler host/user path |
| `supabase link --project-ref mvcxtwoxhopumxcryxlc -p "<session password>"` | relink operation | PASS | none | relink completed, but did not remove later migration-path auth failure |
| `supabase db push --linked` (retry/final execution docs) | linked migration apply | FAIL / BLOCKED | `SQLSTATE 28P01` | command executed in retry/final attempts; migration not applied |
| `supabase db query --db-url "<POOLER_URI>" "SELECT 1 as pooler_auth_test;"` | explicit pooler (`aws-1-eu-central-1.pooler.supabase.com:6543`, user `postgres.mvcxtwoxhopumxcryxlc`) | FAIL | `SQLSTATE 28P01` | explicit transaction pooler test did not authenticate |
| `supabase migration list --db-url "<POOLER_URI>"` | explicit pooler | FAIL | `SQLSTATE 28P01` | migration-list over explicit pooler also failed |
| `supabase db query --linked "select current_database() as db_name, current_user as db_user;"` + remote preflight sequence in first remote execution report | linked remote check path | FAIL / BLOCKED | login-role error (`permission denied to alter role "cli_login_postgres"`) | earlier failure mode before later stable `28P01` reproduction |

## Successful Connection Path
The documented successful method is:
- linked project selected as `mvcxtwoxhopumxcryxlc`
- session-only secret handling via `SUPABASE_DB_PASSWORD` (set in current shell session, removed after checks)
- read-only linked query command:
  - `supabase db query --linked "SELECT 1 as auth_test;"` (or equivalent `connectivity_check`)
- no DB writes, no migration apply.

This indicates remote read connectivity can work in linked/query flow under the recorded session setup.

## Failed Paths
- `supabase db push --linked` failed repeatedly with `SQLSTATE 28P01`; migration not applied.
- `supabase migration list` failed in later diagnostics with `SQLSTATE 28P01` and pooler reference in error output.
- explicit transaction pooler tests with `--db-url` failed for both query and migration-list with `SQLSTATE 28P01`.
- earlier remote attempt also showed a different blocked mode (`permission denied to alter role "cli_login_postgres"`), then later stabilized to password-auth failures.

No report indicates successful DB write or successful migration execution in remote environment.

## Pooler Diagnostic Review
Based on recorded execution notes, explicit pooler testing was likely executed in technically correct order:
- session password variable was set,
- pooler URI was built in-session,
- read-only commands were executed,
- session variable was removed.

Therefore, a missing "manual pre-paste before Cursor command" step is **not proven** as root cause from current evidence.

More likely unresolved causes:
- credential mismatch for pooler login context (username/path expectations),
- stale/incorrect password at time of pooler auth,
- connection-string encoding/path nuance not yet isolated (especially for password characters),
- possible distinction between linked management path and explicit pooler path auth handling.

## Recommended Next Step
Run one narrow, read-only task focused on controlled reproduction with manual session preparation:

- Manually set a session variable for password in PowerShell (no echo),
- Manually build a `$poolerUrl` variable in PowerShell (no echo),
- Run only:
  - `supabase db query --db-url $poolerUrl "SELECT 1 as pooler_auth_test;"`
  - `supabase migration list --db-url $poolerUrl`
- Optionally in same task, re-run `supabase db query --linked "SELECT 1 as linked_auth_test;"` for side-by-side contrast.

No `db push`, no migration apply.

## Guardrail Confirmation
- no db push
- no migration execution
- no DDL
- no table creation
- no DB writes
- no API/GAS/Python changes
- no migration edits
- no secrets stored
