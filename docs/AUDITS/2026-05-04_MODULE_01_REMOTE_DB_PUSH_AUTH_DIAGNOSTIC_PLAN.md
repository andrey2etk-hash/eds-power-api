# MODULE 01 REMOTE DB PUSH AUTH DIAGNOSTIC PLAN

## Status
DOC ONLY / DIAGNOSTIC PLANNING / NO EXECUTION

## Problem Summary

Remote auth preflight partially succeeds:
- read-only query returns `auth_test = 1`

But remote migration push fails:
- `supabase db push --linked`
- SQLSTATE 28P01 password authentication failed for user `postgres`

## Confirmed Safe State

- migration not applied remotely
- no remote module01_ tables created
- no DDL succeeded
- no DB writes
- no API/GAS/Python changes
- no secrets stored
- legacy tables unaffected

## Known Environment

- project ref: mvcxtwoxhopumxcryxlc
- project name: EDSPower Database
- Supabase CLI installed: v2.95.4
- Supabase CLI available update: v2.98.1

## Diagnostic Goals

Determine why `db query --linked` succeeds while `db push --linked` fails.

Potential causes:
1. stale Supabase project link / cached password state
2. db push using different connection flow than db query
3. password variable not available to subprocess context during push
4. CLI version bug or behavior fixed in newer release
5. project password reset not fully propagated
6. command requires relink with current password

## Allowed Diagnostic Actions In Future Task

Allowed only after this plan is audited:
- inspect Supabase CLI version
- inspect linked project ref
- inspect safe non-secret config files
- verify session variable presence without printing value
- rerun read-only query
- run migration list/status commands if read-only
- consider updating Supabase CLI as separate approved task
- consider relinking project as separate approved task:
  `supabase link --project-ref mvcxtwoxhopumxcryxlc`
  using password prompt/session password
- do not print secrets

## Forbidden Actions

Do NOT:
- run `supabase db push`
- execute migration
- run DDL
- create tables
- manually patch remote DB
- edit migration file
- store password in docs/repo
- commit `.env`
- modify API/GAS/Python code

## Proposed Diagnostic Sequence

### Step 1 — Close Failed Push Attempt
Record current FAIL / BLOCKED as safe failure.

### Step 2 — Verify CLI/Link State
Check:
- `supabase --version`
- linked project ref
- safe project status
- no secrets printed

### Step 3 — Re-run Read-only Auth Check
Run:
`supabase db query --linked "SELECT 1 as auth_test;"`

Expected:
auth_test = 1

### Step 4 — Check Migration Status Read-only
Use project-approved read-only migration status/list command if available.
Do not run push.

### Step 5 — Decide Fix Path

Possible fix paths:
A. Relink remote project with current password
B. Update Supabase CLI
C. Reset DB password again and relink
D. Use explicit DB URL execution strategy only if separately planned and audited

Recommended first fix:
Relink project with current password, then read-only preflight.

## Security Notes

- password must be typed only in terminal prompt or session env var
- no secret in docs/chat/repo
- if password was exposed in chat earlier, reset it before final successful remote push
- after use, remove session env var:
  `Remove-Item Env:\SUPABASE_DB_PASSWORD`

## Next Allowed Step

Gemini audit of this diagnostic plan.

If PASS:
Remote DB Push Auth Diagnostic Execution — read-only / no push.

## Gemini Audit Status

- final verdict: PASS
- plan status: CLOSED / APPROVED
- required fixes: none (no blocking fixes)
- added diagnostic concern: direct vs pooled connection / connection pooling
- CLI update recommended before relink
- next allowed step: Remote DB Push Auth Diagnostic Execution — read-only / no push
- db push remains forbidden
