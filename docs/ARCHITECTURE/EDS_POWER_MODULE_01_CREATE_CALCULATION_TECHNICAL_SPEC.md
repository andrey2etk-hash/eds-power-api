# EDS Power Module 01 — Create Calculation Technical Spec

## 1. Purpose

Define the **exact technical contract** for **Create Calculation Modal V1** before any implementation.

No code in this document.

## 2. Source Documents

| Document | Path / note |
|----------|-------------|
| Create Calculation Modal V1 Planning | `docs/ARCHITECTURE/EDS_POWER_MODULE_01_CREATE_CALCULATION_MODAL_V1_PLANNING.md` |
| Module 01 Sidebar Technical Spec | `docs/ARCHITECTURE/EDS_POWER_MODULE_01_SIDEBAR_TECHNICAL_SPEC.md` |
| Terminal UI Shell Doctrine | `docs/ARCHITECTURE/EDS_POWER_TERMINAL_UI_SHELL_DOCTRINE.md` |
| Render Thinking / GAS Thin UI Rule | `docs/00_SYSTEM/02_GLOBAL_RULES.md` |
| main.py Thin Router Rule | `docs/00_SYSTEM/02_GLOBAL_RULES.md` |
| Manual SQL Apply Governance Rule | `docs/00_SYSTEM/02_GLOBAL_RULES.md` (Manual SQL Apply) |
| Module 01 schema (repo evidence) | `supabase/migrations/20260504190000_module01_schema_slice_01.sql` |
| DB-driven registry (repo evidence) | `supabase/migrations/20260507100000_eds_power_dynamic_menu_registry_s01.sql` |

**Gemini planning audit (task assumption):** **`PASS` / `READY_FOR_TECHNICAL_SPEC`**.

## 3. Gemini Audit Findings Addressed

| Finding | Spec resolution |
|---------|-----------------|
| **12-digit `calculation_base_number`** | **`^[0-9]{12}$`** per DDL — store **only** 12 digits in `module01_calculations.calculation_base_number`. **Never** store `YYYYMMDDHHMM-XX` in this column. |
| **UI display vs DB** | **Display** = `{base_number}-{version_suffix_digits}` e.g. `202605071904-00` where the suffix digits are the two digits from `version_suffix` **without** the leading hyphen for display concatenation logic — i.e. base `202605071904` + `-` + `00` from `-00`. |
| **`product_type` / `comment` / `external_reference` gaps** | No `product_type` or `external_reference` on `module01_calculations` in repo DDL. **`comment`** has no dedicated header column; **`module01_calculation_versions.notes`** exists. See **§5** and **§8**. |
| **Initial version row** | **Create immediately** in the same backend transaction as header: `version_suffix` = **`-00`** (matches default in DDL). Required so `module01_calculation_status_history` can reference **`calculation_version_id`**. |
| **`MODULE01_CREATE_CALCULATION` registry** | Must exist as a **permission/registry action** before implementation ships to production users. **No SQL in this task** — prepare **S02** manual SQL / migration planning only (**§14**). |

## 4. Existing Schema Summary

**Source:** repository migration only (`20260504190000_module01_schema_slice_01.sql`). **Not** live Supabase-connected.

### `public.module01_calculations`

| Column | Type | Constraints / notes |
|--------|------|----------------------|
| `id` | uuid | PK, `gen_random_uuid()` |
| `calculation_base_number` | text | NOT NULL, **unique**, CHECK **`^[0-9]{12}$`** |
| `title` | text | nullable |
| `potential_customer` | text | nullable |
| `sales_manager_user_id` | uuid | FK → `module01_users`, nullable |
| `created_by_user_id` | uuid | NOT NULL, FK → `module01_users` |
| `current_status` | text | NOT NULL, default **`DRAFT`**, status enum CHECK |
| `is_archived` | boolean | NOT NULL, default false |
| `created_at` / `updated_at` | timestamptz | NOT NULL |

**Unknown without operator read-only query:** whether **remote** DB matches this file exactly (drift, manual hotfixes). Mark **UNKNOWN** if operator verification fails.

**Confirmed absent in this migration:** **`product_type`**, **`external_reference`**, **`comment`**, **`metadata` / JSONB** on this table.

### `public.module01_calculation_versions`

| Column | Type | Constraints / notes |
|--------|------|----------------------|
| `id` | uuid | PK |
| `calculation_id` | uuid | NOT NULL, FK → `module01_calculations` |
| `version_suffix` | text | NOT NULL, default **`-00`**, CHECK **`^-[0-9]{2}$`**, **unique per** `(calculation_id, version_suffix)` |
| `calculation_version_number` | text | NOT NULL, **globally unique** |
| `status` | text | NOT NULL, default **`DRAFT`**, status enum CHECK |
| `created_by_user_id` | uuid | NOT NULL |
| `source_version_id` | uuid | nullable, self-FK |
| `locked_at`, `locked_by_user_id`, `lock_reason` | — | lock invariant |
| `notes` | text | nullable |
| `created_at` / `updated_at` | timestamptz | NOT NULL |

### `public.module01_calculation_status_history`

| Column | Type | Constraints / notes |
|--------|------|----------------------|
| `id` | uuid | PK |
| `calculation_version_id` | uuid | NOT NULL, FK → `module01_calculation_versions` |
| `old_status` | text | nullable (CHECK) |
| `new_status` | text | NOT NULL (CHECK) |
| `changed_by_user_id` | uuid | NOT NULL |
| `changed_at` | timestamptz | NOT NULL |
| `reason`, `notes` | text | nullable |
| `request_id` | uuid | nullable |
| `source_client` | text | nullable |

**Implication:** **status history requires a version id** — header-only insert is **insufficient** if history is written on create.

### JSONB elsewhere (not calculation header)

`public.module01_audit_events` includes **`metadata jsonb`** — acceptable for **audit telemetry**, not as the **authoritative** store for `product_type` / header fields unless a **separate** audited design says otherwise. This spec treats **calculation facts** as **row/column (or S02)** only.

### Roles / registry (repo)

- `module01_roles`, `module01_user_roles` — in same Module 01 slice migration.
- `eds_power_module_actions`, `eds_power_role_module_access` — registry S01; **`action_type`** enum includes e.g. **`OPEN_DIALOG`** (suitable for a future **`MODULE01_CREATE_CALCULATION`** row — **planning only**).

## 5. Field Mapping Table

| Modal field | Required | Backend validation | DB target | Notes |
|-------------|----------|-------------------|-----------|--------|
| `calculation_title` | **yes** | Non-empty string; max length **TBD** (confirm before implementation) | **Direct:** `module01_calculations.title` | DDL allows NULL; backend enforces NOT NULL on create. |
| `potential_customer` | **yes** | Non-empty string; max length **TBD** | **Direct:** `module01_calculations.potential_customer` | Same as title for nullability vs validation. |
| `product_type` | **yes** | Must be **`KZO`** for V1 | **requires S02 migration** (recommended: add `product_type` to `module01_calculations` with CHECK, or add `header_metadata jsonb` with documented keys) | **No** suitable authoritative column in current repo DDL. **Do not** pretend `audit_events.metadata` is source of truth without a new audit. |
| `comment` | optional | Length / safety **TBD** | **Direct:** `module01_calculation_versions.notes` (initial **`-00`** row) | If both `comment` and `external_reference` are non-empty and `external_reference` is not yet in S02, backend may **merge** into `notes` with a **stable, documented** text template (interim). |
| `external_reference` | optional | Length / safety **TBD** | **Preferred:** **S02** — e.g. `module01_calculations.external_reference` | **Interim:** merge into **`module01_calculation_versions.notes`** with labeled line (`Ref:`) until S02 lands — document in implementation, remove after S02. |

**No invented columns in this spec:** targets marked **S02** require an **audited migration** and **manual apply** per governance.

## 6. Calculation Number Contract

### `calculation_base_number` (persisted)

- **Exactly 12 digits**, match **`^[0-9]{12}$`**.
- **Semantic format (V1):** **`YYYYMMDDHHMM`** (12 chars) — wall-clock **UTC** or operator-approved TZ **must be fixed at implementation** (open: UTC only recommended).
- **Generated only by backend** after successful payload checks.
- **Collision handling:** on unique violation, regenerate per **§11** `MODULE01_CREATE_NUMBER_COLLISION` (retry with new base within same minute or increment strategy — **implementation detail**, not in this doc).

### Version suffix (initial)

- **`version_suffix`** stored as **`-00`** (matches DDL default and CHECK).
- **UI display number:** **`{calculation_base_number}-{two_digit_suffix}`** e.g. `202605071904-00`.
- **Do not** persist hyphenated display in **`calculation_base_number`**.

### `calculation_version_number` (persisted, globally unique)

- Repo DDL: **`calculation_version_number`** `text NOT NULL` **UNIQUE** (no format CHECK).
- **Recommended value:** **same as UI display number** **`{base}-00`** e.g. `202605071904-00`, **if** global uniqueness holds (base unique + `-00` first version).
- **Open:** if product requires a different internal key, keep **display** stable and use alternate `calculation_version_number` — **requires schema/ops confirmation**.

## 7. Create Transaction Sequence

Backend sequence (single **transaction** recommended):

1. Validate Bearer session.
2. Resolve **user** from session (reject payload `user_id`).
3. Resolve **role(s)** and **permission** for **`MODULE01_CREATE_CALCULATION`** (registry / static allowlist — **implementation choice**, must be backend-only).
4. Validate **active terminal** and **`spreadsheet_id`** match session binding.
5. Validate payload (required fields, `product_type` = **`KZO`**, lengths).
6. If **`product_type`** persistence requires S02 and S02 is **not** applied: fail with **`MODULE01_CREATE_SCHEMA_UNSUPPORTED`** (or narrow feature flag — **governance decision**).
7. Generate **`calculation_base_number`** (12 digits).
8. **Insert** `module01_calculations` row: `title`, `potential_customer`, `created_by_user_id`, `current_status` = **`DRAFT`**, `calculation_base_number`, optional S02 columns when present.
9. **Insert** `module01_calculation_versions` row: `calculation_id`, **`version_suffix` = `'-00'`**, **`calculation_version_number`** per **§6**, `status` = **`DRAFT`**, `notes` per **§5**, `created_by_user_id`.
10. **Insert** `module01_calculation_status_history`: `calculation_version_id` = new version id, `old_status` = **null**, `new_status` = **`DRAFT`**, `changed_by_user_id`, `source_client`, `request_id` if available.
11. **Commit**; return **§10** success envelope including **`sidebar_update`**.

All DB writes **backend-owned** (service role / repository), never from GAS.

## 8. Persistence Rules

- **Immediate persist** required.
- **Header status:** **`DRAFT`** (`current_status` on `module01_calculations`; version **`status`** also **`DRAFT`** initially).
- **Initial version:** **`-00`**, **same transaction** as header.
- **Status history:** **mandatory** on create if invariant is “every version has auditable status” — requires **step 10**.
- **Gaps:** **`product_type`** and **`external_reference`** — **S02** or interim **`notes`** merge (**§5**). Document removal of interim once S02 is live.

## 9. Request Contract

**Endpoint:** `POST /api/module01/calculations/create`

**Body:**

```json
{
  "source_client": "GAS",
  "terminal_id": "...",
  "spreadsheet_id": "...",
  "payload": {
    "calculation_title": "...",
    "potential_customer": "...",
    "product_type": "KZO",
    "comment": "...",
    "external_reference": "..."
  }
}
```

**Rules:**

- **`user_id`** never accepted from payload.
- **Role** never accepted from payload.
- **Calculation numbers** never accepted from payload.
- **Product permission** decided only by backend (session + registry/role rules).
- **`terminal_id` / `spreadsheet_id`** revalidated against session (mismatch → **`MODULE01_CREATE_TERMINAL_MISMATCH`**).

## 10. Response Contract

**Success:**

```json
{
  "status": "success",
  "data": {
    "calculation": {
      "calculation_id": "...",
      "calculation_base_number": "202605071904",
      "calculation_display_number": "202605071904-00",
      "version": "00",
      "status": "DRAFT",
      "product_type": "KZO",
      "title": "...",
      "potential_customer": "...",
      "created_at": "..."
    },
    "sidebar_update": {
      "active_calculation_id": "...",
      "active_calculation_display": "202605071904-00 — KZO — DRAFT"
    }
  },
  "error": null,
  "metadata": {
    "request_id": "...",
    "api_version": "..."
  }
}
```

**Notes:**

- **`product_type`** in response reflects **request + validation** until a DB column proves stored value.
- **`sidebar_update`** must align with whatever **`GET /api/module01/sidebar/context`** will expose after implementation (exact field names — **sidebar spec follow-up**).

## 11. Error Map

| Error code | Backend cause | Modal UI behavior |
|------------|---------------|------------------------|
| `MODULE01_CREATE_AUTH_REQUIRED` | Missing / invalid session | Show auth summary; no sidebar change; suggest re-login |
| `MODULE01_CREATE_PERMISSION_DENIED` | Role / registry denies **`MODULE01_CREATE_CALCULATION`** | Show permission message; cancel or escalate |
| `MODULE01_CREATE_INVALID_PAYLOAD` | Schema / required field / length | Show field errors + summary; keep modal open |
| `MODULE01_CREATE_PRODUCT_TYPE_UNSUPPORTED` | Not **`KZO`** | Show message; keep modal open |
| `MODULE01_CREATE_TERMINAL_MISMATCH` | Terminal / spreadsheet not bound to session | Show mismatch; keep modal open |
| `MODULE01_CREATE_SCHEMA_UNSUPPORTED` | Required DDL missing (e.g. `product_type` column not migrated) | Show “system not ready”; **no** partial writes |
| `MODULE01_CREATE_NUMBER_COLLISION` | Unique violation on base or version number after retries exhausted | Show retry / support message |
| `MODULE01_CREATE_VERSION_CREATE_FAILED` | Version insert failed after header | **Rollback** transaction; show error |
| `MODULE01_CREATE_STATUS_HISTORY_FAILED` | History insert failed | **Rollback**; show error |
| `MODULE01_CREATE_BACKEND_UNAVAILABLE` | DB down / timeout / 5xx | Show retry; keep modal open |

## 12. Modal UI Behavior

**On open:** fields empty; **`product_type`** default **`KZO`** or from **backend-provided** allowlist (V1: fixed **KZO**).

**Submit:** loading; **disable double submit**; **one** POST; on success show **success summary**; then close; then **refresh** sidebar.

**On error:** modal stays open; show **backend** error summary; **no** sidebar change.

## 13. Sidebar Sync After Success

- **`DocumentProperties`** cache **`active_calculation_id`** — **optional**; backend remains source of truth.
- **Refresh** sidebar via **`GET /api/module01/sidebar/context`** (or equivalent).
- **Display** (minimum): **`calculation_display_number`**, status **`DRAFT`**, **`product_type`**, **`title`**, **`potential_customer`** — exact JSON path = sidebar implementation task.

## 14. Registry / Permission Action

**Action key:** **`MODULE01_CREATE_CALCULATION`**

**Purpose:** backend permission gate and (optionally) menu/sidebar visibility contract.

**This task:** **no SQL execution.**

**Repo evidence:** `eds_power_module_actions` supports **`action_key`**, **`action_type`** (e.g. **`OPEN_DIALOG`**), **`metadata` jsonb`; `eds_power_role_module_access` binds **role** + **action**.

**Recommendation:** **S02** migration or **manual SQL** pack (operator-governed) to insert:

- `MODULE01_CREATE_CALCULATION` action row,
- `eds_power_role_module_access` rows for roles allowed to create (e.g. **TEST_OPERATOR** / production roles),

**before** enabling create in production. Align with **`docs/AUDITS/2026-05-07_EDS_POWER_SQL_REGISTRY_S01_MANUAL_APPLY_REPORT.md`** governance.

## 15. Backend Architecture

- **`main.py`** stays **thin** (wiring only).
- **Route:** `main.py` or router module.
- **Service:** `services/module01_calculations_service.py` (name as in sidebar tech spec trajectory).
- **Repository:** only if needed for testability / SQL isolation.
- **No** calculation engine, KZO, or BOM logic in create transaction.

## 16. GAS Boundary

**GAS may:** open modal, collect fields, POST with Bearer, show success/error, refresh sidebar.

**GAS must not:** generate numbers, decide permissions, deep business validation, Supabase writes, engineering logic.

## 17. Required Pre-Implementation Checks

1. Confirm **`module01_calculations`** matches migration in **target** Supabase (operator read-only).
2. Confirm **`module01_calculation_versions`** idem.
3. Confirm **no `metadata` JSONB** on calculations table unless S02 added.
4. Confirm **status history** requires **`calculation_version_id`** (repo: yes).
5. Confirm **`calculation_base_number`** CHECK still **`^[0-9]{12}$`** remotely.
6. Confirm **registry** approach for **`MODULE01_CREATE_CALCULATION`**: manual SQL vs **S02** migration file.
7. **Gemini audit** of **this** technical spec.
8. **User approval** for implementation TASK.

## 18. Out of Scope

Implementation; SQL execution; migrations authoring in this task; backend/GAS/HTML code; KZO logic; calculation engine; BOM; snapshots beyond header/version/status history for create.

## 19. Risk Register

1. **Schema mismatch** — remote DB ≠ repo migration.
2. **Number format collision** — high concurrency on 12-digit minute bucket.
3. **Client-side validation creep** in GAS.
4. **Missing registry permission** — button visible but backend denies, or inverse.
5. **Header without version** — breaks status history / future APIs.
6. **Status history orphaning** — partial transaction if not transactional.
7. **Sidebar drift** — cache without refresh.
8. **UX** — modal closes too fast; user misses success / error.

## 20. Verdict

**`MODULE_01_CREATE_CALCULATION_TECH_SPEC_READY_FOR_SCHEMA_CONFIRMATION_AND_AUDIT`**

---

## Appendix A — Operator read-only SQL (do not run in Cursor)

**Use only** in Supabase SQL Editor (or read replica) by **operator**, for drift checks.

### A.1 Columns

```sql
select table_name, column_name, data_type, is_nullable
from information_schema.columns
where table_schema = 'public'
  and table_name in (
    'module01_calculations',
    'module01_calculation_versions',
    'module01_calculation_status_history'
  )
order by table_name, ordinal_position;
```

### A.2 Constraints

```sql
select
  conrelid::regclass as table_name,
  conname,
  pg_get_constraintdef(oid) as constraint_def
from pg_constraint
where conrelid::regclass::text in (
  'module01_calculations',
  'module01_calculation_versions',
  'module01_calculation_status_history'
)
order by table_name::text, conname;
```
