# MODULE 01 REMOTE SUPABASE POOLER CONNECTION FIX PLAN

## Status
DOC ONLY / CONNECTION FIX PLANNING / NO EXECUTION

## Problem Summary
Remote migration commands fail even though read-only query can pass.

Observed failure:
`SQLSTATE 28P01 password authentication failed`.

Dashboard evidence shows:
- Direct connection is not IPv4 compatible.
- Transaction pooler is IPv4 compatible.
- Transaction pooler uses username format:
  `postgres.<project_ref>`

## Confirmed Safe State
- migration not applied remotely
- no module01_ tables created remotely
- no DB writes
- no API/GAS/Python changes
- no secrets stored

## Connection Modes Observed

Direct connection:
- host: `db.mvcxtwoxhopumxcryxlc.supabase.co`
- port: `5432`
- user: `postgres`
- IPv4 compatibility: no

Transaction pooler:
- host: `aws-1-eu-central-1.pooler.supabase.com`
- port: `6543`
- user: `postgres.mvcxtwoxhopumxcryxlc`
- IPv4 compatibility: yes

## Root Cause Hypothesis
Remote migration path is using pooler-style connection but not using the pooler-required username or updated connection context.

Potential issue:
- stale Supabase CLI link config
- wrong username for pooler
- direct connection unavailable over IPv4
- migration commands requiring direct connection but CLI falls back to pooler
- password correct but for different connection username/path

## Allowed Future Diagnostic/Fix Actions
After audit only:
- inspect safe Supabase CLI config without secrets
- inspect linked project ref
- relink with correct project
- test explicit pooler connection string without exposing password
- test direct connection only if IPv6/direct path is available
- consider using `DATABASE_URL`/PG connection string only in session if supported
- no DB writes until read-only validation passes

## Forbidden Actions
- no `db push` in this planning task
- no DDL
- no table creation
- no manual DB patching
- no migration edits
- no API/GAS code changes
- no secrets in docs/repo

## Candidate Fix Paths

### Path A — Pooler URI Strategy
Use transaction pooler connection details:
- host: `aws-1-eu-central-1.pooler.supabase.com`
- port: `6543`
- user: `postgres.mvcxtwoxhopumxcryxlc`

Test read-only query using explicit connection string or environment variable without exposing password.

If read-only explicit pooler query passes, plan remote migration command using approved Supabase CLI/connection method.

### Path B — Direct Connection Strategy
Use direct connection:
- host: `db.mvcxtwoxhopumxcryxlc.supabase.co`
- port: `5432`
- user: `postgres`

Only viable if IPv6/direct access works or environment supports it.

### Path C — Remote SQL Editor Manual Migration
Emergency fallback only:
Run migration SQL manually in Supabase SQL Editor.
Requires separate plan and audit.
Not recommended unless CLI path is blocked.

## Recommended Path
Path A first: Pooler URI Strategy.

Reason:
Dashboard marks transaction pooler as IPv4 compatible and provides username format required for pooler.

## Security Handling
- password typed only in terminal/session variable
- no password in docs/chat/repo
- if password was exposed earlier, reset before final successful remote push
- remove session variable after diagnostic

## Next Allowed Step
Gemini audit of this fix plan.

If PASS:
Remote Pooler Connection Diagnostic Execution — read-only / no db push.

## Gemini Audit Status

- final verdict: PASS
- plan status: CLOSED / APPROVED
- no required blocking fixes
- accepted Path A: explicit pooler URI strategy
- accepted Path B: direct strategy only if IPv6/direct access works
- SQL Editor remains emergency fallback only
- required infrastructure/service status check before diagnostic
- next allowed step: Remote Pooler Connection Diagnostic Execution — read-only / no db push
- db push remains forbidden
