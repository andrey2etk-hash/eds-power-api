# Module 01 Delete Item — Backend Implementation Closeout

**Date:** 2026-05-13

---

## Objective

Record **bounded backend-only** implementation of **Module 01** **single-item delete** per locked **Slice 03** scope and backend design (**hard delete**, **DRAFT** only, **`ITEM_HAS_CHILDREN`**, **`NO_REINDEX_ON_DELETE`**, **`POST /api/module01/calculations/items/delete`**).

---

## Source design

- **`docs/AUDITS/2026-05-13_MODULE_01_CALCULATION_EDITOR_GAS_CLIENT_V1_SLICE_03_DELETE_ITEM_SCOPE.md`**
- **`docs/AUDITS/2026-05-13_MODULE_01_DELETE_ITEM_BACKEND_IMPLEMENTATION_DESIGN.md`**
- Assumed design audit verdict for code gate: **`BACKEND_DESIGN_PASS_READY_FOR_CODE`** (operator/task).

---

## Scope

- **Implemented:** `validate_items_delete_payload`, `delete_calculation_item_v1`, **`POST /api/module01/calculations/items/delete`** in **`main.py`**, **pytest** coverage in **`tests/test_module01_calculation_items_api.py`**.
- **Not in scope:** GAS/UI, SQL/migrations/schema, Render env, soft/cascade/bulk delete, reindex, legacy migration, parent-first modal.

---

## Backend files changed

| File | Change |
|------|--------|
| **`services/module01_calculation_items_service.py`** | Delete validation + **`delete_calculation_item_v1`**, **`_item_has_children_in_version`** |
| **`main.py`** | Route **`module01_calculation_items_delete`**, error messages, imports |
| **`tests/test_module01_calculation_items_api.py`** | Delete service + endpoint tests |

---

## Route added

- **`POST /api/module01/calculations/items/delete`**
- **Auth:** same **`AUTH_CALCULATION_ITEMS_ACTION`** (`calculation_items`) as **`/items/add`**.
- **Body:** **`calculation_id`**, **`calculation_version_id`**, **`item_id`** (UUID strings).

---

## Service function added

- **`validate_items_delete_payload(body)`** → **`(normalized, error_code, source_field)`**
  - Non-dict body → **`ITEM_DELETE_FAILED`**, `source_field` **`None`**
  - Invalid/missing **`calculation_id`** / **`calculation_version_id`** / **`item_id`** (not a UUID string) → **`ITEM_DELETE_FAILED`** with the respective **`source_field`**
- **`delete_calculation_item_v1`** → same tuple style as **`add_calculation_item_v1`**

---

## Validation sequence implemented

1. Payload shape + UUID fields (**`validate_items_delete_payload`**).
2. **Auth** in route (**existing** session/`calculation_items` pattern).
3. Calculation fetch + **`created_by_user_id`** vs **`user_id`** → **`CALCULATION_NOT_FOUND`**.
4. Version fetch + **`calculation_id`** match → **`CALCULATION_VERSION_NOT_FOUND`**.
5. **`status`** = **`DRAFT`** → else **`VERSION_NOT_DRAFT`**.
6. Item fetch by **`item_id`** → missing **`ITEM_NOT_FOUND`**, `source_field` **`item_id`**.
7. Item **`calculation_id`** / **`calculation_version_id`** must match request → else **`ITEM_NOT_FOUND`**, **`item_id`** (**privacy-safe**; not **`ITEM_VERSION_MISMATCH`**).
8. At least one child in same **`calculation_version_id`** with **`parent_item_id`** = item → **`ITEM_HAS_CHILDREN`**, **`item_id`** (**no `child_count`** in payload).
9. **Hard delete** with **`delete().eq(id).eq(calculation_version_id).eq(calculation_id)`**; empty **`data`** → **`ITEM_NOT_FOUND`** (race / already deleted).
10. Success payload includes **`deleted_item_id`**, **`parent_item_id`**, **`deleted_display_index`**, **`refresh_required`**: **`true`**, optional **`deleted_item_type`** / **`deleted_item_name`**.

**No** sibling **`sort_order`** / **`display_index`** updates. **No** cascade.

---

## Error codes

Mapped in **`_MODULE01_ITEMS_ERROR_MESSAGES`** and route/service:

- **`ITEM_NOT_FOUND`**, **`ITEM_HAS_CHILDREN`** (“Item has child items. Delete children first.”), **`ITEM_DELETE_FAILED`**
- Plus existing: **`CALCULATION_NOT_FOUND`**, **`CALCULATION_VERSION_NOT_FOUND`**, **`VERSION_NOT_DRAFT`**
- Auth errors unchanged (**`AUTH_*`** via auth layer).

---

## Tests added / run

**Command:** `python -m pytest tests/test_module01_calculation_items_api.py -q`
**Result:** **36 passed** (2026-05-13, local).

Coverage includes: leaf delete, empty root delete, parent with children (**`ITEM_HAS_CHILDREN`**, delete not called), non-DRAFT, wrong version (**`ITEM_NOT_FOUND`**), invalid **`item_id`** in JSON (**`ITEM_DELETE_FAILED`**), double delete (**`ITEM_NOT_FOUND`** second), legacy root **`KZO`** no children, no **`update()`** on items table (no reindex), endpoint success + **`ITEM_HAS_CHILDREN`** envelopes.

---

## What was NOT changed

- **GAS** / HTML sidebars
- **SQL** / migrations / DB schema / seeds
- **Render** configuration
- **Dynamic menu** / unrelated auth
- **Soft delete**, **cascade**, **bulk**, **reindex**

---

## Legacy orphan handling

- Rows such as legacy root **`KZO`** with **`parent_item_id`** null are **not** rejected by delete service on type alone; if **DRAFT**, owned, **no children**, they can be removed (**same** as scope). **No** normalization or migration job.

---

## Result

- Backend **delete** path is **implemented** and **unit-tested** locally.
- **Render** / operator **live** verification **not** claimed in this document.

---

## Verdict

**`DELETE_ITEM_BACKEND_IMPLEMENTED_PENDING_RENDER_VERIFICATION`**

**Next:** **Render** (or equivalent) **authenticated** verification of **`POST /api/module01/calculations/items/delete`**. **GAS** delete UI remains a **separate** task.
