# MVP DATABASE ACCESS POLICY (MANUAL DB BRIDGE)

## Status
ACTIVE (MVP STAGE ONLY)

## Problem Statement
During MVP stage, automated agents (Cursor) do not have direct access to Supabase database due to:

- missing DB credentials in runtime
- security constraints
- CLI permission limitations
- governance restriction: no secret exposure

## Decision
All database interaction during MVP is performed via **Manual DB Bridge**.

## Manual DB Bridge Definition

Manual DB Bridge = workflow where:

1. Cursor generates SQL (DOC ONLY)
2. Human operator executes SQL manually in Supabase SQL Editor
3. Human returns results back to system (Chat / Docs)
4. Architect + Critic validate results

## Allowed Flow

Step 1 — SQL Generation
- Cursor prepares SQL scripts in repo
- Stored under:
  docs/AUDITS/... or SQL folders
- SQL must be:
  - explicit
  - auditable
  - idempotent where possible
  - marked with execution instructions

Step 2 — Manual Execution
- User executes SQL in Supabase SQL Editor
- No automated execution allowed

Step 3 — Result Capture
User returns:
- execution result (SUCCESS / FAILED)
- affected rows
- SELECT verification output

Step 4 — Validation
- Architect validates logic
- Critic validates safety and correctness

## Strict Rules

Cursor MUST NOT:
- connect to Supabase directly
- use supabase CLI for execution
- request DB password
- store secrets
- simulate DB responses
- assume execution success without user confirmation

User MUST:
- execute SQL manually
- provide real DB results
- not skip verification step

## Classification

This pattern is considered:

- MVP workaround
- governance-compliant
- security-preserving
- NOT a limitation of architecture
- TEMPORARY until secure DB integration is implemented

## Success Criteria

MVP is considered successful if:

- all DB changes are traceable via SQL files
- no secrets leaked
- no silent execution
- full audit trail exists
- system works with manual DB bridge

## Future Transition

This policy will be deprecated when:

- secure DB access layer is implemented
- service-role access is properly isolated
- Cursor can execute controlled DB operations

## Tag

MVP_DB_BRIDGE_ACTIVE
