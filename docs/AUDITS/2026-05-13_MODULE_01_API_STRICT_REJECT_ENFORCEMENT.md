# Module 01 API STRICT_REJECT enforcement — backend only

- **Date:** 2026-05-13
- **Mode:** **bounded backend implementation** — **no** GAS, **no** UI/HTML, **no** SQL/migrations, **no** DB schema changes, **no** legacy data mutation.

---

## Objective

Implement **`STRICT_REJECT`** parent-hierarchy enforcement on **`POST /api/module01/calculations/items/add`**: **child-only** **`item_type`** values **must not** be created when **`parent_item_id`** is **null**.

---

## Source governance

- **`docs/AUDITS/2026-05-13_MODULE_01_PARENT_PRODUCT_HIERARCHY_DOC_CASCADE_GEMINI_PASS.md`** — verdict **`DOC_CASCADE_VERIFIED_STRICT_REJECT_LOCKED`**.
- Policy: **`STRICT_REJECT`** — valid roots are parent products only (**`MEDIUM_VOLTAGE_SWITCHGEAR_10KV`**, **`MEDIUM_VOLTAGE_SWITCHGEAR_6KV`**, **`KTP`**) with **`item_kind` = `CONTAINER`**; **`KZO_CELL`**, **`SHOS_CABINET`**, **`SERVICE_ITEM`** (+ legacy **`KZO`**, **`SHCHO`**) are **child-only** at the API layer for this enforcement slice.

---

## Scope

| In scope | Out of scope |
|----------|----------------|
| Backend validation before insert on **items add** | GAS / sidebar / modal |
| Error code **`PARENT_REQUIRED_FOR_CHILD_ITEM`** | Delete Item |
| Dynamic human-readable **`message`** + **`source_field`:` parent_item_id`** | Slice 03 |
| Service + route envelope (existing Module 01 items style) | Auto-parent / normalization of stored **`item_type`** |
| Unit tests (`pytest`) | Full **authenticated** Render proof — **operator session** required (see **Render Verification**) |

---

## Backend files changed

- **`services/module01_calculation_items_service.py`** — **`_CHILD_ONLY_ITEM_TYPES`**, **`is_child_only_item_type`**, **`parent_required_for_child_item_message`**, check in **`add_calculation_item_v1`** after draft version gate.
- **`main.py`** — import **`parent_required_for_child_item_message`**, **`_MODULE01_ITEMS_ERROR_MESSAGES`** entry for **`PARENT_REQUIRED_FOR_CHILD_ITEM`**, route builds type-specific message when service returns this code.

---

## Validation rule implemented

If **`parent_item_id`** is **null** and **`item_type`** (case-insensitive) is one of:

- **`KZO_CELL`**, **`KZO`**, **`SHOS_CABINET`**, **`SHCHO`**, **`SERVICE_ITEM`**

→ return **`PARENT_REQUIRED_FOR_CHILD_ITEM`** with **`source_field` = `parent_item_id`**, **no** insert, **no** sibling sort queries.

**Not** implemented in this slice: whitelist rejection for non–child-only roots with invalid **`item_type`** (e.g. generic **`CONTAINER` + `T`**) — existing behavior unchanged.

---

## Error code

- **`error_code`:** **`PARENT_REQUIRED_FOR_CHILD_ITEM`**
- **`message`:** type-specific ( **`KZO_CELL`/`KZO`**, **`SHOS_CABINET`/`SHCHO`**, **`SERVICE_ITEM`** ) — all state *cannot be created as root* and *select or create parent product first*.
- **`source_field`:** **`parent_item_id`**
- **`module` / `action`:** **`MODULE_01`** / **`calculation_items`** (existing envelope).

---

## Tests added / run

**File:** **`tests/test_module01_calculation_items_api.py`**

- Helper tests: **`is_child_only_item_type`**, **`parent_required_for_child_item_message`**.
- **A:** root **`CONTAINER` + `MEDIUM_VOLTAGE_SWITCHGEAR_10KV`**, null parent — **allowed**.
- **B:** root **`CONTAINER` + `KTP`**, null parent — **allowed**.
- **C–F:** root **`KZO_CELL`**, **`KZO`**, **`SHOS_CABINET`**, **`SHCHO`**, null parent — **`PARENT_REQUIRED_FOR_CHILD_ITEM`**.
- **G:** root **`SERVICE_ITEM`**, null parent — **`PARENT_REQUIRED_FOR_CHILD_ITEM`**.
- **H:** child **`KZO_CELL`** under parent with **`item_type` = `MEDIUM_VOLTAGE_SWITCHGEAR_10KV`** — **allowed** (existing parent validation unchanged).
- **Endpoint:** **`test_add_parent_required_error_message_on_endpoint`** — envelope + **SHCHO** → **SHOS_CABINET** message text.

**Command:** `python -m pytest tests/test_module01_calculation_items_api.py -q` → **24 passed** (local).

---

## What was NOT changed

- **GAS** / **HTML** sidebar files.
- **SQL** / **migrations** / **schema**.
- **Render** environment.
- **List** endpoint, **auth** menu, unrelated modules.
- **Delete Item**, **Slice 03**, parent-first UI.

---

## Legacy data handling

- **No** migration, **no** updates to existing **root `KZO`** / orphan rows.
- Enforcement applies to **new** **`POST /items/add`** requests only.

---

## Result

Backend **STRICT_REJECT** for **child-only types at root** is **implemented** and covered by **service + route** tests.

---

## Verdict

**`API_STRICT_REJECT_IMPLEMENTED_PENDING_RENDER_VERIFICATION`** (superseded for live gate — see **Render Verification** below).

---

## Render Verification

**Date recorded:** 2026-05-13
**API base:** `https://eds-power-api.onrender.com`
**Endpoint:** `POST /api/module01/calculations/items/add`

### Deployment / repo reference

| Item | Value |
|------|--------|
| **Local repo `HEAD` at documentation time** | `a0ad013dd68b4a3053e21a176970c440318130d3` (**note:** Render may lag until deploy picks up this commit; operator should confirm **deployed** revision) |
| **GAS / UI / HTML** | **No changes** in this verification task |
| **SQL / migrations / DB schema** | **No changes** |
| **Legacy orphan rows** | **Not mutated** |

### Automated probes (no secrets — Cursor/agent environment)

| Probe | HTTP | Envelope / note |
|--------|------|------------------|
| **`POST .../items/add`** with **invalid** Bearer (placeholder string, **not** a real token) | **200** | `status` = **`auth_error`**, **`error_code`** = **`AUTH_INVALID_TOKEN`**, **`module`** = **`MODULE_01_AUTH`**, **`action`** = **`calculation_items`** — confirms **route registered** on public Render and **auth runs before** item payload / **STRICT_REJECT** |

**Redaction:** No session token, password, hash, or service role key logged.

### Authenticated live tests (required for full **STRICT_REJECT** gate)

**Executor:** operator with **valid Module 01 Bearer** and **DRAFT** **`calculation_id`** / **`calculation_version_id`** owned by that user (same flow as historical **`runModule01CalculationItemsAuthedSmokeTest()`** / Sheet terminal).

**Not executed** in this documentation pass: **agent environment** has **no** stored **`MODULE01`** session token or owned calculation UUIDs (**by security design**).

| Test | Case | Expected | Result (this run) |
|------|------|----------|-------------------|
| **1** | Root **`KZO_CELL`**, `parent_item_id` null | **`PARENT_REQUIRED_FOR_CHILD_ITEM`**, `source_field` **`parent_item_id`**, no insert | **Pending operator** |
| **2** | Root legacy **`KZO`**, null parent | Same | **Pending operator** |
| **3** | Root **`CONTAINER` + `MEDIUM_VOLTAGE_SWITCHGEAR_10KV`**, null parent | **`status` success**, row inserted; record **`id`** for Test 4 | **Pending operator** |
| **4** | **`KZO_CELL`** child under **`parent_item_id`** from Test 3 | Success, `display_index` like **`1.1`** | **Pending operator** |
| **5** | Root **`SHOS_CABINET`** | **`PARENT_REQUIRED_FOR_CHILD_ITEM`** | **Pending operator** (optional) |
| **6** | Root **`SHCHO`** | **`PARENT_REQUIRED_FOR_CHILD_ITEM`** | **Pending operator** (optional) |
| **7** | Root **`SERVICE_ITEM`** | **`PARENT_REQUIRED_FOR_CHILD_ITEM`** | **Pending operator** (optional) |

**If** operator creates rows during verification: treat as **test evidence**; **do not delete** in this slice (**Delete Item** remains a **later** task).

### Evidence policy

Record only: path, HTTP status, top-level `status`, `error_code`, `source_field`, `item_type` under test, **non-secret** item **UUIDs** if needed. **Never** log Bearer token, passwords, hashes, or Supabase secrets.

### Verdict (live gate)

- **`API_STRICT_REJECT_RENDER_ROUTE_AND_AUTH_GATE_VERIFIED`** — public Render exposes **`POST .../items/add`**; **invalid token** path matches Module 01 auth envelope (`action` **`calculation_items`**).
- **`API_STRICT_REJECT_RENDER_VERIFIED`** (full policy proof on deployed API) — **not recorded here** because **Tests 1–4 (+ optional 5–7)** require an **operator-authenticated** run. When those **all PASS**, update this section: set verdict to **`API_STRICT_REJECT_RENDER_VERIFIED`** and replace **Pending operator** with **PASS** rows.

**Next:** operator **authenticated** run on Render **or** closeout in a follow-up audit after smoke.
