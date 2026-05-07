# EDS Power SQL Registry S01 Manual Apply Report

## Objective

Record successful manual SQL apply of SQL Registry S01.

## Apply Method

Supabase Dashboard SQL Editor.

## Migration File

`supabase/migrations/20260507100000_eds_power_dynamic_menu_registry_s01.sql`

## Governance Boundary

Cursor did not execute SQL.

User/operator manually applied SQL.

## Verification Results

**Tables created (operator-reported):**

- `public.eds_power_modules`
- `public.eds_power_module_actions`
- `public.eds_power_role_module_access`

**Counts:**

- `modules_count` = **2**
- `actions_count` = **4**
- `role_bindings_count` = **40**

**Triggers verified (operator-reported):** **3**

- `trg_eds_power_module_actions_updated_at` on `eds_power_module_actions`
- `trg_eds_power_modules_updated_at` on `eds_power_modules`
- `trg_eds_power_role_module_access_updated_at` on `eds_power_role_module_access`

## Created Modules

| code | title | status | sort_order | active |
|------|--------|--------|------------|--------|
| SYSTEM_SHELL | System shell | RELEASED | 10 | true |
| MODULE_01 | Module 01 | PLANNED | 20 | true |

## Created Actions

| code | action_type | label | enabled | sort_order |
|------|-------------|-------|---------|------------|
| MODULE_01_PLACEHOLDER | PLACEHOLDER_DISABLED | Module 01 — Розрахунки (planned) | false | 10 |
| REFRESH_MENU | REFRESH_MENU | Оновити меню | true | 10 |
| SESSION_STATUS | SESSION_STATUS | Статус сесії | true | 20 |
| LOGOUT | LOGOUT | Вийти | true | 30 |

## Trigger Verification

All three `updated_at` triggers listed above were reported present after apply.

## Errors

None reported after final successful apply.

## Boundary Confirmation

- no Cursor SQL execution
- no db push by Cursor
- no backend changes
- no GAS changes
- no Render changes
- no migration file edits during closeout (assumed unchanged approved migration unless operator states otherwise)
- no secrets stored

## Verdict

**EDS_POWER_SQL_REGISTRY_S01_APPLY_SUCCESS**
