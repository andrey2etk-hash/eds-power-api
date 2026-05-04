# MODULE 01 REMOTE SUPABASE AUTH FIX PLAN

## Status
DOC ONLY / AUTH FIX PLANNING / NO EXECUTION

## Purpose

Plan a safe fix for the failed remote Supabase migration attempt caused by remote database authentication / permission issue.

## Failure Summary

Remote migration attempt status:
FAIL / BLOCKED

Observed issue:
- permission denied / authentication failure
- Supabase CLI indicates missing or required remote DB password handling
- `SUPABASE_DB_PASSWORD` may need to be set for the PowerShell session

Confirmed safe behavior:
- migration was not applied remotely
- no remote module01_ tables were created
- no manual DB patching occurred
- existing legacy tables remain safe
- no API/GAS code changed

## Root Cause Hypothesis

Likely cause:
Supabase CLI could not authenticate to remote Postgres because remote DB password was not available in the current PowerShell session.

Supabase docs note:
- remote database commands may require linked project
- remote DB password may be supplied through `SUPABASE_DB_PASSWORD`
- do not store secrets in repository or documentation

## Fix Scope

Allowed:
- set `SUPABASE_DB_PASSWORD` only in current PowerShell session
- verify Supabase CLI is linked to intended project
- verify remote connection with a harmless read-only query if supported by project convention
- re-attempt remote migration only after separate approval

Forbidden:
- storing password in repo
- storing password in docs
- writing password to .env committed to git
- running remote migration in this planning task
- manual DB patching
- editing migration file
- API/GAS code changes

## PowerShell Secret Handling Plan

Recommended method:
Use a current-session environment variable only.

Example placeholder:
`$env:SUPABASE_DB_PASSWORD = "<REMOTE_DB_PASSWORD_FROM_SUPABASE_DASHBOARD>"`

Rules:
- password must be entered manually by operator
- never paste actual password into docs or chat logs
- do not commit `.env`
- clear terminal history if needed according to local security practice
- after task, remove session variable if desired:
`Remove-Item Env:\SUPABASE_DB_PASSWORD`

## Remote Project Identity Verification

Before any retry:
- confirm linked Supabase project ref
- confirm project name / environment
- confirm this is the intended remote target
- if target unclear, stop

## Safe Connection Verification Plan

Before migration retry, perform a harmless connection verification.

Preferred:
- use a project-approved Supabase CLI command or read-only query

Examples to verify according to project convention:
- Supabase CLI project status / link inspection
- read-only `SELECT 1` if safely supported
- migration list/status command if available

Rules:
- no DDL
- no table creation
- no writes
- no manual patching

## Retry Boundary

This fix plan does not authorize retry.

After this plan:
1. Gemini audit of auth fix plan
2. if PASS, apply auth fix and perform preflight as separate narrow task
3. only then re-attempt remote migration if explicitly approved

## Failure Handling

If authentication still fails:
- stop immediately
- capture exact error
- do not retry blindly
- do not patch DB manually
- do not edit migration file
- create updated failure report

## Governance Boundary

This plan does not authorize:
- remote migration execution
- DDL execution
- table creation
- DB writes
- API/GAS changes
- migration edits
- production deployment
- RLS/triggers/functions
- procurement/warehouse/ERP
- pricing/CAD

## Next Allowed Step

Gemini audit of Remote Supabase Auth Fix Plan.

If PASS:
Remote Supabase Auth Fix Application / Preflight Only as separate task.

## Gemini Audit Status

- final verdict: PASS
- plan status: CLOSED / APPROVED
- required fixes: none
- next allowed step: Remote Supabase Auth Fix Application / Preflight Only
- remote migration retry not authorized in this closeout
- no secrets stored
- no DB writes performed
