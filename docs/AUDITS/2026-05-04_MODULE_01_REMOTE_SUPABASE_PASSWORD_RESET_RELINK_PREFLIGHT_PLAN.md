# MODULE 01 REMOTE SUPABASE PASSWORD RESET + RELINK PREFLIGHT PLAN

## Status
DOC ONLY / PREFLIGHT PLANNING / NO EXECUTION

## Purpose
Plan a safe reset/relink/read-only validation flow for resolving remote Supabase CLI auth-context mismatch before any remote migration retry.

## Confirmed Safe State
- remote migration not applied
- no module01_ tables created remotely
- no DDL succeeded
- no DB writes
- no API/GAS/Python changes
- no migration edits
- no secrets stored
- legacy tables unaffected

## Root Cause Working Theory
Likely auth-context mismatch between:
- direct query path
- linked migration-management path
- pooler path

Path A is approved:
Password Reset + Relink + Linked Read-only Migration Status.

## Dashboard Password Reset Plan

Operator action:
- open Supabase Dashboard
- go to EDSPower Database
- project ref: mvcxtwoxhopumxcryxlc
- Project Settings / Database
- reset DB password

Rules:
- do not paste password into chat
- do not paste password into docs
- do not commit password
- do not store password in `.env`
- record only that password reset was performed

Risk note:
Any service using the old DB password may require update.
Current known Render/API environment uses `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY`, not necessarily DB password, but confirm before changing production-facing services.

## PowerShell Session Password Handling

After reset:
Set new DB password only in current PowerShell session.

Example placeholder:
`$env:SUPABASE_DB_PASSWORD = "<NEW_REMOTE_DB_PASSWORD>"`

Rules:
- never print password
- only check presence:
  `if ($env:SUPABASE_DB_PASSWORD) { "SUPABASE_DB_PASSWORD_SET" } else { "MISSING" }`

After preflight:
`Remove-Item Env:\SUPABASE_DB_PASSWORD`

## Relink Plan

Run:
`supabase link --project-ref mvcxtwoxhopumxcryxlc`

Requirements:
- must complete without error
- report only success/failure
- do not log password

Record:
- linked project ref
- link command status PASS / FAIL

## Read-only Validation Plan

After relink:

1. Confirm project identity:
- EDSPower Database
- mvcxtwoxhopumxcryxlc

2. Run:
`supabase db query --linked "SELECT 1 as auth_test;"`

Expected:
`auth_test = 1`

3. Run:
`supabase migration list`

or if project convention requires:
`supabase migration list --linked`

Expected:
command completes without `SQLSTATE 28P01`

Important:
This is the gate for future `db push`.
If migration list/status fails, `db push` remains forbidden.

## Forbidden During This Preflight

Do NOT run:
- `supabase db push`
- migration execution
- DDL
- table creation
- DB writes
- manual DB patching
- migration repair
- SQL Editor migration execution

Do NOT modify:
- API code
- GAS code
- Python code
- migration file

Do NOT store:
- password
- full DB URL with password
- tokens
- service role key
- connection string with password

## Success Criteria

PASS only if:
- password reset completed by operator
- `SUPABASE_DB_PASSWORD` set in session
- `supabase link` completed successfully
- linked `SELECT 1` passes
- migration list/status passes without `28P01`
- no `db push` executed
- no DB writes performed
- no secrets stored

## Failure Handling

If any step fails:
- stop immediately
- capture exact error
- do not retry blindly
- do not `db push`
- do not patch DB manually
- create failure report
- return to fix planning

## Next Allowed Step

After this plan:
- Gemini audit of Password Reset + Relink Preflight Plan
- if PASS: execute Password Reset + Relink Preflight as separate narrow task
- `db push` remains forbidden until preflight result is audited and migration list/status passes

## Governance Boundary

This plan does not authorize:
- password reset execution
- relink execution
- `db push`
- DDL
- table creation
- DB writes
- API/GAS implementation
- migration edits
- production deployment
- procurement/warehouse/ERP
- pricing/CAD

## Gemini Audit Status

- final verdict: PASS
- plan status: CLOSED / APPROVED
- no required blocking fixes
- reset before relink accepted
- migration list/status gate accepted
- Dashboard database status check recommended after reset
- next allowed step: Execute Password Reset + Relink Preflight
- db push remains forbidden
