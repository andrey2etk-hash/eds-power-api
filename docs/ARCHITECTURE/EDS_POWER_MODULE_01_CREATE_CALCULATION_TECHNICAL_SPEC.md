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
| **`product_type` / `comment` / `external_reference` gaps** | **CONFIRMED:** no dedicated columns on **`module01_calculations`**. **V1:** all three map into **`module01_calculation_versions.notes`** via a **structured notes template** (operator closeout). See **§ Confirmed V1 Persistence Mapping**. |
| **Initial version row** | **Create immediately** in the same backend transaction as header: `version_suffix` = **`-00`** (matches default in DDL). Required so `module01_calculation_status_history` can reference **`calculation_version_id`**. |
| **`MODULE01_CREATE_CALCULATION` registry** | Must exist as a **permission/registry action** before implementation ships to production users. **No SQL in this task** — prepare **S02** manual SQL / migration planning only (**§14**). |

## 4. Existing Schema Summary

**Sources:** (1) repository migration `supabase/migrations/20260504190000_module01_schema_slice_01.sql`; (2) **operator read-only Supabase evidence** (columns, constraints, indexes, row counts) — recorded in **§ Schema Confirmation Result**.

**Remote vs repo:** **CONFIRMED** — operator evidence matches the migration-derived expectations below for the three calculation tables (no drift reported for this confirmation slice).

### `public.module01_calculations`

| Column | Type | Constraints / notes |
|--------|------|----------------------|
| `id` | uuid | PK, `gen_random_uuid()` |
| `calculation_base_number` | text | NOT NULL, **UNIQUE**, CHECK **`^[0-9]{12}$`** — **CONFIRMED** (operator) |
| `title` | text | nullable — **CONFIRMED** |
| `potential_customer` | text | nullable — **CONFIRMED** |
| `sales_manager_user_id` | uuid | FK → `module01_users`, nullable |
| `created_by_user_id` | uuid | NOT NULL, FK → `module01_users` — **CONFIRMED** |
| `current_status` | text | NOT NULL, default **`DRAFT`**, status enum CHECK — **CONFIRMED** |
| `is_archived` | boolean | NOT NULL, default **false** — **CONFIRMED** |
| `created_at` / `updated_at` | timestamptz | NOT NULL |

**CONFIRMED absent (no dedicated columns):** **`product_type`**, **`external_reference`**, **`comment`**, **`metadata` / JSONB** on this table — **interim** persistence via **`module01_calculation_versions.notes`** (**§ Confirmed V1 Persistence Mapping**).

### `public.module01_calculation_versions`

| Column | Type | Constraints / notes |
|--------|------|----------------------|
| `id` | uuid | PK |
| `calculation_id` | uuid | NOT NULL, FK → `module01_calculations` — **CONFIRMED** |
| `version_suffix` | text | NOT NULL, default **`-00`**, CHECK **`^-[0-9]{2}$`**, **unique per** `(calculation_id, version_suffix)` — **CONFIRMED** |
| `calculation_version_number` | text | NOT NULL, **globally unique** — **CONFIRMED** |
| `status` | text | NOT NULL, default **`DRAFT`**, status enum CHECK — **CONFIRMED** |
| `created_by_user_id` | uuid | NOT NULL — **CONFIRMED** |
| `source_version_id` | uuid | nullable, self-FK |
| `locked_at`, `locked_by_user_id`, `lock_reason` | — | lock invariant |
| `notes` | text | nullable — **CONFIRMED** (V1 structured payload for `product_type` / `comment` / `external_reference`) |
| `created_at` / `updated_at` | timestamptz | NOT NULL |

### `public.module01_calculation_status_history`

| Column | Type | Constraints / notes |
|--------|------|----------------------|
| `id` | uuid | PK |
| `calculation_version_id` | uuid | NOT NULL, FK → `module01_calculation_versions` — **CONFIRMED** (required) |
| `old_status` | text | nullable (CHECK) |
| `new_status` | text | NOT NULL (CHECK) — **CONFIRMED** |
| `changed_by_user_id` | uuid | NOT NULL — **CONFIRMED** |
| `changed_at` | timestamptz | NOT NULL |
| `reason`, `notes` | text | nullable |
| `request_id` | uuid | nullable |
| `source_client` | text | nullable |

**Implication (CONFIRMED):** **status history requires `calculation_version_id`** — create flow must insert **version `-00`** before history.

**Row counts (operator read-only):** **`module01_calculations`**, **`module01_calculation_versions`**, **`module01_calculation_status_history`** — **0** rows each at confirmation time.

### JSONB elsewhere (not calculation header)

`public.module01_audit_events` includes **`metadata jsonb`** — acceptable for **audit telemetry** only. **V1 authoritative** storage for `product_type` / free-text fields without header columns is **`module01_calculation_versions.notes`** using the **structured notes template** (**§ Confirmed V1 Persistence Mapping**).

### Roles / registry (repo)

- `module01_roles`, `module01_user_roles` — in same Module 01 slice migration.
- `eds_power_module_actions`, `eds_power_role_module_access` — registry S01; **`action_type`** enum includes e.g. **`OPEN_DIALOG`** (suitable for a future **`MODULE01_CREATE_CALCULATION`** row — **planning only**).

## 5. Field Mapping Table

| Modal field | Required | Backend validation | DB target | Notes |
|-------------|----------|-------------------|-----------|--------|
| `calculation_title` | **yes** | Non-empty string; max length **TBD** | **Direct:** `module01_calculations.title` | **CONFIRMED** column; backend enforces NOT NULL on create. |
| `potential_customer` | **yes** | Non-empty string; max length **TBD** | **Direct:** `module01_calculations.potential_customer` | **CONFIRMED** column. |
| `product_type` | **yes** | Must be **`KZO`** for V1 | **`module01_calculation_versions.notes`** (structured template) | **CONFIRMED V1** — no header column; **§ Confirmed V1 Persistence Mapping**. |
| `comment` | optional | Length / safety **TBD** | **`module01_calculation_versions.notes`** (structured template) | **CONFIRMED V1**. |
| `external_reference` | optional | Length / safety **TBD** | **`module01_calculation_versions.notes`** (structured template) | **CONFIRMED V1**. |

**Structured `notes`:** implementation MUST use a **versioned, deterministic** template (e.g. line-oriented `PRODUCT_TYPE:`, `COMMENT:`, `REF:`) so future migrations can parse or migrate to dedicated columns without ambiguity.

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

- **CONFIRMED:** NOT NULL, **globally UNIQUE** (operator + repo).
- **V1 value:** **same as UI display number** **`{calculation_base_number}-{suffix_digits}`** e.g. `202605071904-00` (base **12 digits** + hyphen + **`00`** from **`version_suffix`** `-00`).

## 7. Create Transaction Sequence

Backend sequence (single **transaction** recommended):

1. Validate Bearer session.
2. Resolve **user** from session (reject payload `user_id`).
3. Resolve **role(s)** and **permission** for **`MODULE01_CREATE_CALCULATION`** (registry / static allowlist — **implementation choice**, must be backend-only).
4. Validate **active terminal** and **`spreadsheet_id`** match session binding.
5. Validate payload (required fields, `product_type` = **`KZO`**, lengths; ensure structured **`notes`** payload fits DB **`text`** limits — **TBD** max).
6. Generate **`calculation_base_number`** (12 digits, **`^[0-9]{12}$`**).
7. **Insert** `module01_calculations` row: `title`, `potential_customer`, `created_by_user_id`, `current_status` = **`DRAFT`**, `calculation_base_number`, `is_archived` default false.
8. **Insert** `module01_calculation_versions` row: `calculation_id`, **`version_suffix` = `'-00'`**, **`calculation_version_number`** per **§6**, `status` = **`DRAFT`**, `notes` = **structured template** from **`product_type`**, **`comment`**, **`external_reference`** (**§ Confirmed V1 Persistence Mapping**), `created_by_user_id`.
9. **Insert** `module01_calculation_status_history`: `calculation_version_id` = new version id, `old_status` = **null**, `new_status` = **`DRAFT`**, `changed_by_user_id`, `source_client`, `request_id` if available.
10. **Commit**; return **§10** success envelope including **`sidebar_update`**.

**All-or-nothing:** steps **7–9** MUST run in **one** database transaction; any failure **rolls back** — **§ Confirmed Create Transaction**.

All DB writes **backend-owned** (service role / repository), never from GAS.

## 8. Persistence Rules

- **Immediate persist** required.
- **Header status:** **`DRAFT`** (`current_status` on `module01_calculations`; version **`status`** also **`DRAFT`** initially).
- **Initial version:** **`-00`**, **same transaction** as header.
- **Status history:** **mandatory** on create if invariant is “every version has auditable status” — requires **step 10**.
- **CONFIRMED V1:** **`product_type`**, **`comment`**, **`external_reference`** → **`module01_calculation_versions.notes`** (**structured template**). Future dedicated columns = separate **S02+** migration (out of scope for this confirmation).

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

- **`product_type`** in response reflects **payload + validation** and MUST match content serialized into **version `notes`** (parseable per structured template).
- **`sidebar_update`** must align with whatever **`GET /api/module01/sidebar/context`** will expose after implementation (exact field names — **sidebar spec follow-up**).

## 11. Error Map

| Error code | Backend cause | Modal UI behavior |
|------------|---------------|------------------------|
| `MODULE01_CREATE_AUTH_REQUIRED` | Missing / invalid session | Show auth summary; no sidebar change; suggest re-login |
| `MODULE01_CREATE_PERMISSION_DENIED` | Role / registry denies **`MODULE01_CREATE_CALCULATION`** | Show permission message; cancel or escalate |
| `MODULE01_CREATE_INVALID_PAYLOAD` | Schema / required field / length | Show field errors + summary; keep modal open |
| `MODULE01_CREATE_PRODUCT_TYPE_UNSUPPORTED` | Not **`KZO`** | Show message; keep modal open |
| `MODULE01_CREATE_TERMINAL_MISMATCH` | Terminal / spreadsheet not bound to session | Show mismatch; keep modal open |
| `MODULE01_CREATE_SCHEMA_UNSUPPORTED` | Required tables/columns missing vs operator-confirmed schema (unexpected drift) | Show “system not ready”; **no** partial writes |
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

1. ~~Confirm **`module01_calculations`** in target Supabase~~ — **DONE** (operator read-only schema confirmation; see **§ Schema Confirmation Result**).
2. ~~Confirm **`module01_calculation_versions`** / **`module01_calculation_status_history`**~~ — **DONE** (same).
3. ~~Confirm **no `metadata` JSONB** on calculations table~~ — **CONFIRMED**; V1 uses **`notes`** only.
4. ~~Confirm **status history** requires **`calculation_version_id`**~~ — **CONFIRMED**.
5. ~~Confirm **`calculation_base_number`** CHECK **`^[0-9]{12}$`** and **UNIQUE**~~ — **CONFIRMED**.
6. Confirm **registry** approach for **`MODULE01_CREATE_CALCULATION`**: manual SQL vs **S02** migration file (**still required** before production roll-out).
7. **Gemini audit** of **this** technical spec post–schema confirmation (**if** required by governance).
8. **User approval** / explicit **implementation TASK**.

## 18. Out of Scope

Implementation; SQL execution; migrations authoring in this task; backend/GAS/HTML code; KZO logic; calculation engine; BOM; snapshots beyond header/version/status history for create.

## 19. Risk Register

1. **Schema mismatch** — **mitigated** for this slice by operator confirmation; re-verify after any remote DDL change.
2. **Number format collision** — high concurrency on 12-digit minute bucket.
3. **Client-side validation creep** in GAS.
4. **Missing registry permission** — button visible but backend denies, or inverse.
5. **Header without version** — breaks status history / future APIs.
6. **Status history orphaning** — partial transaction if not transactional.
7. **Sidebar drift** — cache without refresh.
8. **UX** — modal closes too fast; user misses success / error.

## Schema Confirmation Result

**Mode:** operator **read-only** Supabase evidence (no Cursor SQL, no DB mutations). **Closeout:** this doc updated from **UNKNOWN** to **CONFIRMED** for the items below.

### Confirmed — `module01_calculations`

- **`calculation_base_number`:** `text` **NOT NULL**; **UNIQUE**; CHECK **`^[0-9]{12}$`**.
- **Columns present:** `title`, `potential_customer`, `created_by_user_id`, `current_status` default **`DRAFT`**, `is_archived` default **false** (plus PK/FK/timestamps per repo migration).
- **No dedicated columns** for `product_type`, `comment`, `external_reference`.

### Confirmed — `module01_calculation_versions`

- **`calculation_id`** FK to header.
- **`version_suffix`** default **`-00`**; **`calculation_version_number`** **NOT NULL**; **`status`** default **`DRAFT`**; **`created_by_user_id`**; **`notes`** (nullable `text`).
- Initial row **`-00`** is valid per default and per create contract.

### Confirmed — `module01_calculation_status_history`

- Requires **`calculation_version_id`** (NOT NULL FK).
- Requires **`new_status`**, **`changed_by_user_id`** (and other columns per migration).

### Indexes and constraints

- **Constraints:** base-number format and uniqueness, FKs, status CHECKs — **confirmed** by operator evidence, consistent with `20260504190000_module01_schema_slice_01.sql`.
- **Indexes:** present on the three tables per operator read-out; **canonical inventory** remains the repo migration file + operator query output (not pasted here to avoid stale duplication).

### Row counts (at confirmation time)

| Table | Row count |
|-------|-----------|
| `module01_calculations` | **0** |
| `module01_calculation_versions` | **0** |
| `module01_calculation_status_history` | **0** |

### Final field mapping (summary)

Same as **§5** with **CONFIRMED V1** persistence: header fields on **`module01_calculations`**; **`product_type` / `comment` / `external_reference`** on **`module01_calculation_versions.notes`** via **structured template** (**§ Confirmed V1 Persistence Mapping**).

## Confirmed V1 Persistence Mapping

| Source | Target |
|--------|--------|
| `calculation_title` | `module01_calculations.title` |
| `potential_customer` | `module01_calculations.potential_customer` |
| `product_type` | **`module01_calculation_versions.notes`** (structured template — required line, V1 value **`KZO`**) |
| `comment` | **`module01_calculation_versions.notes`** (structured template — optional block) |
| `external_reference` | **`module01_calculation_versions.notes`** (structured template — optional block) |
| (generated) `calculation_base_number` | `module01_calculations.calculation_base_number` (**12 digits only**) |
| (initial) `version_suffix` | `module01_calculation_versions.version_suffix` = **`-00`** |
| (generated) `calculation_version_number` | `module01_calculation_versions.calculation_version_number` (V1 = display form e.g. `{base}-00`) |
| initial **DRAFT** status | `module01_calculations.current_status`, `module01_calculation_versions.status`, and `module01_calculation_status_history.new_status` |

**Structured notes template (normative for V1):** backend MUST serialize into a single `notes` string, e.g.:

```text
EDS_POWER_CALC_NOTES_V1
PRODUCT_TYPE: KZO
COMMENT: <optional>
EXTERNAL_REFERENCE: <optional>
```

- Omit **`COMMENT:`** / **`EXTERNAL_REFERENCE:`** lines when the modal field is empty.
- **Implementation** MUST parse this format when reading back for sidebar/API (until dedicated columns exist).

## Confirmed Create Transaction

**Required backend transaction (all-or-nothing):**

1. **Insert** calculation **header** (`module01_calculations`) with **`DRAFT`**, **`calculation_base_number`**, **`title`**, **`potential_customer`**, **`created_by_user_id`**.
2. **Insert** **initial version** row (`module01_calculation_versions`) with **`version_suffix` = `'-00'`**, matching **`calculation_version_number`**, **`status` = `DRAFT`**, **`notes`** from structured template.
3. **Insert** **status history** (`module01_calculation_status_history`) with **`calculation_version_id`**, **`old_status`** null, **`new_status` = `DRAFT`**, **`changed_by_user_id`**.

If any step fails: **rollback** — no partial header without version/history.

## 20. Verdict

**`TECH_SPEC_LOCKED_IMPLEMENTATION_V1_PENDING_OPERATOR_TEST`**

Implementation: **`EDS_POWER_MODULE_01_CREATE_CALCULATION_V1`** → **`IMPLEMENTED_PENDING_OPERATOR_DML_AND_LIVE_TEST`** — **`docs/AUDITS/2026-05-07_MODULE_01_CREATE_CALCULATION_V1_IMPLEMENTATION.md`**.

Prior schema gate record (superseded for status by line above): **`MODULE_01_CREATE_CALCULATION_TECH_SPEC_SCHEMA_CONFIRMED_READY_FOR_IMPLEMENTATION_TASKING`**.

---

## Appendix A — Operator read-only SQL (do not run in Cursor)

**Use only** in Supabase SQL Editor (or read replica) by **operator**, for **drift re-checks** after DDL changes. Schema for Create Calculation V1 was **operator-confirmed** prior to this closeout (see **§ Schema Confirmation Result**).

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
