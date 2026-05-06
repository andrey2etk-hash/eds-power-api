# MODULE 01 REMOTE SUPABASE AUTH FIX PATH DECISION

## Status
DOC ONLY / FIX PATH DECISION / NO EXECUTION

## Purpose
Decide the next safe path for resolving Supabase remote auth-context mismatch before any remote migration retry.

## Confirmed Safe State
- remote migration not applied
- no module01_ tables created remotely
- no DDL succeeded
- no DB writes
- no API/GAS/Python changes
- no migration edits
- no secrets stored

## Connection History Summary

PASS path:
- `--linked`
- session `SUPABASE_DB_PASSWORD`
- read-only `select 1` returned PASS

FAIL paths:
- `supabase db push --linked`
- later `supabase migration list`
- explicit transaction pooler URI query/list
- all failed with `SQLSTATE 28P01`

## Interpretation
The issue is not generic inability to connect.
The issue is likely auth-context mismatch between Supabase CLI command paths.

Possible factors:
- password reset/propagation timing
- stale link context
- direct vs pooler mode
- username format mismatch
- password URI encoding issue
- CLI command-specific auth path
- session variable/order issue not fully ruled out

## Candidate Fix Paths

### Path A — Password Reset + Relink + Linked Read-only Migration Status
Steps:
1. User resets DB password in Supabase Dashboard.
2. User sets new password only in current PowerShell session.
3. Run `supabase link --project-ref mvcxtwoxhopumxcryxlc`.
4. Run linked read-only `SELECT 1`.
5. Run linked migration list/status read-only.
6. Only if both pass, plan remote `db push` retry.

Pros:
- resets credential uncertainty
- refreshes CLI link state
- avoids explicit pooler URI password encoding complexity

Cons:
- password reset may affect other tools using DB password
- requires careful secret hygiene

### Path B — Session Pooler Diagnostic
Test Session Pooler connection mode separately from Transaction Pooler.

Pros:
- may match migration-management requirements better

Cons:
- still requires URI handling and password encoding

### Path C — Direct IPv6 Strategy
Use direct host/port if network supports IPv6.

Pros:
- avoids pooler username mismatch

Cons:
- may not work on current network / Free plan direct IPv4 limitations

### Path D — SQL Editor Manual Migration
Run SQL manually in Supabase Dashboard SQL Editor.

Pros:
- bypasses CLI auth issue

Cons:
- emergency fallback only
- risks bypassing normal migration tracking
- requires separate plan/audit
- not recommended as next step

## Recommended Path
Path A:
Password Reset + Relink + Linked Read-only Migration Status.

Reason:
It is the cleanest way to remove credential/link-state uncertainty before any new `db push` attempt.

## Required Guardrails For Path A
- no password in docs/chat/repo
- password typed only in Dashboard/PowerShell
- no `db push` during fix application
- no DDL
- no table creation
- no DB writes
- read-only checks only
- after success, Gemini audit result before retry
- reset DB password only with user awareness that DB-password-dependent integrations may need update

## Next Allowed Step
Gemini audit of this Fix Path Decision.

If PASS:
Remote Supabase Password Reset + Relink Preflight Planning.

Not execution yet.

## Governance Boundary
This decision does not authorize:
- password reset execution
- relink execution
- `db push`
- DDL
- table creation
- DB writes
- API/GAS implementation
- migration edits
- SQL Editor manual migration
