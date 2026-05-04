# MODULE 01 SUPABASE SCHEMA SLICE 01 MIGRATION EXECUTION PLAN

## Status
DOC ONLY / EXECUTION PLANNING / NO MIGRATION EXECUTION

## Purpose

Define a controlled plan for applying the approved Module 01 Supabase Schema Slice 01 migration.

Migration file:
`supabase/migrations/20260504190000_module01_schema_slice_01.sql`

## Current Approved State

Confirmed:
- migration file approved by Gemini
- migration file marked CLOSED / APPROVED
- boundary check CLEAN
- no required fixes
- no migration execution performed yet

## Target Environment Decision

Define target environment for first execution.

Recommended order:
1. local/dev Supabase environment if available
2. remote Supabase only after local/dev verification or explicit approval

Decision required:
- target environment = local/dev or remote

For this plan, record:
Execution against remote Supabase requires explicit user approval after this plan.

## Preflight Checks

Before execution, verify:

1. Repository status clean.
2. Migration file exists:
   `supabase/migrations/20260504190000_module01_schema_slice_01.sql`
3. Migration file has not been modified since Gemini approval.
4. Supabase CLI available if CLI execution is planned.
5. Supabase project linked if remote execution is planned.
6. Existing database schema inspected or baseline known.
7. No existing conflicting tables:
   - module01_users
   - module01_roles
   - module01_user_roles
   - module01_user_terminals
   - module01_calculations
   - module01_calculation_versions
   - module01_calculation_status_history
   - module01_audit_events
8. No production deployment actions active.
9. API/GAS are not modified during migration execution.

## Execution Command Planning

If local:
- use approved local Supabase migration command according to project convention.

If remote:
- use approved Supabase CLI command according to project convention.
- do not run without explicit user approval.

Do not include secrets in docs.

## Verification Queries

After migration execution, verify:

1. All 8 tables exist.

Expected tables:
- module01_users
- module01_roles
- module01_user_roles
- module01_user_terminals
- module01_calculations
- module01_calculation_versions
- module01_calculation_status_history
- module01_audit_events

2. Role seed exists.

Expected role count:
9

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
- no RLS policies
- no triggers
- no functions
- no ERP/procurement/warehouse/pricing/CAD columns

## Failure Handling

If migration fails:
- stop immediately
- capture error message
- do not retry blindly
- do not edit migration without separate fix task
- do not partially patch DB manually
- create failure report
- return to migration fix planning

## Rollback Considerations

For local/dev:
- rollback may drop tables in reverse dependency order if required.

For remote:
- destructive rollback is not automatic.
- create separate rollback plan if needed.
- do not drop remote tables without explicit user approval.

Reverse dependency order:
1. module01_audit_events
2. module01_calculation_status_history
3. module01_calculation_versions
4. module01_calculations
5. module01_user_terminals
6. module01_user_roles
7. module01_roles
8. module01_users

## Post-Execution Documentation

After successful execution, create result doc:

`docs/AUDITS/2026-05-04_MODULE_01_SUPABASE_SCHEMA_SLICE_01_MIGRATION_EXECUTION_RESULT.md`

It must include:
- execution environment
- command used
- timestamp
- migration file
- verification results
- role seed confirmation
- forbidden scope confirmation
- final verdict PASS / FAIL

## Governance Boundary

This plan does not authorize:
- migration execution
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
- Gemini audit of Migration Execution Plan
- if PASS: execute migration as separate narrow task
- execution requires explicit user approval

## Gemini Audit Status

- final verdict: PASS
- plan status: CLOSED / APPROVED
- required fixes: none
- recommended first target: local/dev
- next allowed step: Execute migration locally/dev as separate narrow task
- explicit note: remote execution requires separate approval
- no migration execution performed in this closeout
