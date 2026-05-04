# MODULE 01 SUPABASE SCHEMA SLICE 01 REMOTE MIGRATION EXECUTION PLAN

## Status
DOC ONLY / REMOTE EXECUTION PLANNING / NO REMOTE EXECUTION

## Purpose

Define a controlled plan for applying the approved Module 01 Supabase Schema Slice 01 migration to remote Supabase.

Migration file:
`supabase/migrations/20260504190000_module01_schema_slice_01.sql`

## Current Verified State

Confirmed:
- local/dev execution PASS
- all 8 module01_ tables verified locally
- 9 roles verified locally
- local RLS warning accepted / deferred
- migration file approved
- remote execution not performed

## Remote Target Environment

This plan must identify the remote target as:
- development remote / staging remote / production remote

Required rule:
Remote execution requires explicit user approval immediately before execution.

If remote is production:
- require additional confirmation
- require backup/snapshot awareness
- require stronger rollback boundary

Recommended:
Use development/staging remote first if available.

## Remote Preflight Checks

Before remote execution, verify:

1. Repository status clean.
2. Migration file exists and matches approved file:
   `supabase/migrations/20260504190000_module01_schema_slice_01.sql`
3. Supabase CLI available.
4. Supabase project link points to intended remote project.
5. Confirm remote project identity before execution.
6. Confirm remote database baseline is known.
7. Confirm migration history state.
8. Confirm no conflicting remote tables exist:
   - module01_users
   - module01_roles
   - module01_user_roles
   - module01_user_terminals
   - module01_calculations
   - module01_calculation_versions
   - module01_calculation_status_history
   - module01_audit_events
9. Confirm existing legacy tables are not affected.
10. Confirm no API/GAS changes during migration execution.
11. Confirm no RLS/triggers/functions will be added by this migration.
12. Confirm remote execution is explicitly approved by user.

## Remote Execution Command Planning

Plan remote migration command according to project convention.

Do not include secrets in docs.

Example placeholder:
`supabase db push`

or project-approved remote migration command.

Rules:
- command must be confirmed before execution
- do not run in this planning task
- do not execute if target project identity is uncertain

## Remote Verification Queries

After successful remote execution, verify:

1. All 8 tables exist remotely:
- module01_users
- module01_roles
- module01_user_roles
- module01_user_terminals
- module01_calculations
- module01_calculation_versions
- module01_calculation_status_history
- module01_audit_events

2. Role seed exists remotely:
Expected role count = 9

Expected role codes:
- OWNER
- ADMIN
- DIRECTOR
- SALES_MANAGER
- CALCULATION_ENGINEER
- CONSTRUCTOR
- TECHNOLOGIST
- PRODUCTION
- KITTING

3. Constraints exist:
- unique email
- unique role_code
- unique spreadsheet_id
- unique user_id in user_terminals
- unique calculation_base_number
- unique calculation_version_number
- unique calculation_id + version_suffix

4. Pattern checks exist:
- calculation_base_number = 12 digits
- version_suffix = -NN

5. No excluded tables created:
- commercial_products
- calculation_product_items
- product_composition_items
- module_routes
- object_conversion_links

6. No excluded behavior:
- no new RLS policies
- no new triggers
- no new functions
- no ERP/procurement/warehouse/pricing/CAD columns

7. Existing legacy/public tables remain present and unaffected.

## Remote Failure Handling

If remote migration fails:
- stop immediately
- capture exact error
- do not retry blindly
- do not patch remote DB manually
- do not edit migration in same task
- do not run rollback without explicit approval
- create remote failure report
- return to migration fix planning

## Remote Rollback Boundary

For remote:
- no automatic destructive rollback
- no table drops without explicit user approval
- if rollback needed, create separate rollback plan
- preserve error details and DB state

Reverse dependency order for possible future rollback planning:
1. module01_audit_events
2. module01_calculation_status_history
3. module01_calculation_versions
4. module01_calculations
5. module01_user_terminals
6. module01_user_roles
7. module01_roles
8. module01_users

## Post-Execution Documentation

After successful remote execution, create:

`docs/AUDITS/2026-05-04_MODULE_01_SUPABASE_SCHEMA_SLICE_01_REMOTE_MIGRATION_EXECUTION_RESULT.md`

It must include:
- remote target project
- command used
- timestamp
- migration file path
- preflight result
- execution result
- verification results
- role seed confirmation
- excluded scope confirmation
- RLS/triggers/functions verification
- final verdict PASS / FAIL

## Governance Boundary

This plan does not authorize:
- remote migration execution
- DDL execution
- table creation
- DB writes
- API implementation
- GAS implementation
- RLS implementation
- triggers/functions
- production deployment
- procurement/warehouse/ERP
- pricing/CAD

## Next Allowed Step

After this plan:
- Gemini audit of Remote Migration Execution Plan
- if PASS: execute remote migration as separate narrow task
- remote execution requires explicit user approval immediately before execution
