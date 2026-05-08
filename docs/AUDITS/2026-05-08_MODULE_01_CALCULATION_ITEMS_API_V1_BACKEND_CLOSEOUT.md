# Module 01 Calculation Items API V1 — Backend Closeout

**Date:** 2026-05-08  
**Mode:** DOC ONLY — no code / GAS / DB / SQL / Render changes in this step.

## Objective

Close the **backend implementation phase** for **Module 01 Calculation Items API V1** after **Gemini** audit **PASS WITH PERFORMANCE/CONCURRENCY NOTE**, recording **`CALCULATION_ITEMS_API_V1_VERIFIED`** as the current result and fixing the governance verdict **`CALCULATION_ITEMS_API_V1_BACKEND_VERIFIED`** for the backend slice.

## Scope

**In scope for this closeout:** documentation only — attestation that add/list implementation, validation, tests, and accepted notes align with audit.

**Out of scope:** any new implementation, GAS/UI, editor, product engine, BOM, pricing, SQL, migrations.

## Gemini audit summary

| Field | Value |
|--------|--------|
| **Verdict** | **PASS WITH PERFORMANCE/CONCURRENCY NOTE** |
| **Interpretation** | Implementation acceptable for **V1**; concurrency and numeric presentation caveats **documented and accepted** (see below). |

## Backend endpoints implemented

Reference implementation: **`docs/AUDITS/2026-05-08_MODULE_01_CALCULATION_ITEMS_API_V1_IMPLEMENTATION.md`**.

- **`POST /api/module01/calculations/items/add`** — add one item to a **DRAFT** calculation version.
- **`GET /api/module01/calculations/{calculation_id}/versions/{version_id}/items`** — flat item list for a version.

## Validation rules verified

- **Authenticated** session (**existing Module 01 auth pattern**).
- **Calculation** exists and **`created_by_user_id`** matches session user (else **`CALCULATION_NOT_FOUND`** / equivalent posture).
- **Version** exists, belongs to calculation, **`status = DRAFT`** where required.
- **`item_kind`** constrained to allowed CHECK set.
- **`local_quantity > 0`**.
- **Max depth = 2** — no child-of-child; parent must be **top-level** (`**parent.parent_item_id**` null).
- **Parent must be `CONTAINER`** for nested items.
- **Parent / version / calculation mismatch** returns **`ITEM_PARENT_VERSION_MISMATCH`** / related codes per contract.
- **Machine-readable errors** for known failures (no unstructured generic errors for those cases).

## total_quantity / display_index behavior

- **Backend** computes **`total_quantity`**: top-level = **`local_quantity`**; child = **`parent.total_quantity * local_quantity`** (see implementation).
- **Backend** computes **`display_index`**: top-level ordinals **`1`**, **`2`**, …; children **`parent.display_index` + "." + ordinal** (append-only V1).

## Sorting behavior

- **List** response: **preorder** (stable tree walk: parents by **`sort_order`**, then children by **`sort_order`**) so **GAS/UI** can render without recomputing hierarchy order.

## Tests run

- **`python -m pytest tests/`** (full suite at verification time).
- **Result:** **158 passed**.

## Accepted limitations

1. **Concurrency:** **Read max `sort_order` → insert** is **not** a single DB transaction; concurrent appends may yield **`ITEM_SORT_CONFLICT`**. **Accepted for V1.** Future hardening may use **transaction / retry / DB-side allocation**.
2. **Numeric wire shape:** **`Decimal` → `float`** in JSON response **accepted** for V1 because **GAS is display-only** for these fields and does not re-derive business quantities from raw wire types.

## What was NOT implemented

- **GAS** / sidebar / editor UI.
- Edit / delete / reorder (beyond append on add), commit / clone version.
- Product calculation logic, KZO/KTP/BMZ, BOM, pricing.
- New DB migrations, SQL execution, RLS policy expansion, Render env changes.

## Verdict

**`CALCULATION_ITEMS_API_V1_BACKEND_VERIFIED`**

**Current result token:** **`CALCULATION_ITEMS_API_V1_VERIFIED`** (backend slice post-audit).

**Next allowed step (governance):** **Module 01 Calculation Items API V1 — Live Backend Smoke Test** — **GAS still not active** until separately scoped after live smoke.
