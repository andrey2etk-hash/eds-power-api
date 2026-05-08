# Module 01 Calculation Items API V1 — Live Backend Smoke Test

**Date:** 2026-05-08  
**Mode:** Live verification only — no code, GAS, SQL, DB schema, Render env, or implementation changes in this step.

## Objective

Verify the **deployed** Render backend supports Module 01 **Calculation Items API V1** **`add`** / **`list`** endpoints and behavioral expectations (hierarchy, errors), using the **public** API base referenced in repo governance.

## Environment

| Field | Value |
|--------|--------|
| **API base** | `https://eds-power-api.onrender.com` |
| **`POST` add** | `/api/module01/calculations/items/add` |
| **`GET` list** | `/api/module01/calculations/{calculation_id}/versions/{version_id}/items` |
| **Control probe** | `GET /api/module01/auth/session/status` (Module 01 auth envelope) |

**Tooling:** `curl` from operator/Cursor environment (JSON bodies; no secrets logged in this doc).

## Preconditions (intended full smoke)

For scenarios **1–6** below, a valid **Bearer** session and a **DRAFT** **`calculation_id`** / **`calculation_version_id`** owned by that session user are required. This run **did not** use stored credentials (no `.env` in workspace); **unauthenticated** behavior is **not** applicable for item validation because auth runs **before** payload validation in route handlers.

## Test scenarios

| # | Scenario | Expected (if routes + auth OK) | Result (this run) |
|---|----------|--------------------------------|-------------------|
| 1 | Add top-level **CONTAINER** | `status` success; `item_kind` **CONTAINER**; `parent_item_id` null; `total_quantity` = `local_quantity`; `display_index` **"1"** (first item) | **Not executed** — **`POST`** returned **HTTP 404** |
| 2 | Add top-level **PRODUCT** | Success; `display_index` increments vs prior siblings | **Not executed** — **404** |
| 3 | Child **PRODUCT** under **CONTAINER** | `parent_item_id` = container id; `total_quantity` = parent × local; `display_index` like **"1.1"** | **Not executed** — **404** |
| 4 | **List** items | Flat preorder array; parent before child; stable `display_index` / `total_quantity`; includes `parent_item_id` | **Not executed** — **`GET`** returned **HTTP 404** |
| 5 | Child under **PRODUCT** | **`ITEM_PARENT_NOT_CONTAINER`** | **Not executed** — **404** |
| 6a | Invalid quantity | **`ITEM_INVALID_QUANTITY`** | **Not executed** — **404** |
| 6b | Wrong parent version/calculation | **`ITEM_PARENT_VERSION_MISMATCH`** | **Not executed** — **404** |
| 6c | Non-DRAFT version | **`VERSION_NOT_DRAFT`** if practical | **Not executed** — **404** |
| **C** | Control: session status | Module 01 JSON envelope (e.g. **`AUTH_INVALID_TOKEN`** for bogus Bearer) | **PASS** — **HTTP 200**, structured auth error |

### Commands (evidence)

**Control:**

```http
GET https://eds-power-api.onrender.com/api/module01/auth/session/status
Authorization: Bearer x
```

**Response (abbreviated):** `status` = **`auth_error`**, **`error_code`** = **`AUTH_INVALID_TOKEN`**, **`api_version`** present — confirms **live service** and **Module 01 router** for this path.

**Items add:**

```http
POST https://eds-power-api.onrender.com/api/module01/calculations/items/add
Content-Type: application/json
{}
```

**Response:** **HTTP 404**, body **`{"detail":"Not Found"}`** (FastAPI default — route not registered on this deploy).

**Items list:**

```http
GET https://eds-power-api.onrender.com/api/module01/calculations/00000000-0000-0000-0000-000000000001/versions/00000000-0000-0000-0000-000000000002/items
Authorization: Bearer x
```

**Response:** **HTTP 404**, **`{"detail":"Not Found"}`**.

## Results

- **Control path:** **PASS** — deployed API responds with Module 01 auth envelope.
- **Calculation Items V1 paths:** **FAIL / not available** on **`https://eds-power-api.onrender.com`** at smoke time — **HTTP 404** for both **`add`** and **`list`**.
- **Interpretation:** Public deploy is **behind** repo commits that register **`module01_calculation_items_add`** / **`module01_calculation_items_list`** (or equivalent). **No** calculation/item UUIDs were created on production by this smoke (no writes).
- **Created test item IDs:** **None** (endpoints unreachable on public base).

## Errors observed

| Observation | Detail |
|-------------|--------|
| **404 Not Found** | Items **`add`** / **`list`** on public Render |
| **Deploy / routing** | Not an application-level **`ITEM_*`** / **`VERSION_NOT_DRAFT`** — route absent on this host |

## What was NOT tested

- All **authenticated** happy-path and negative-path item scenarios (**1–6**) — blocked by **404**.
- **Concurrent** sort / **`ITEM_SORT_CONFLICT`** — not in scope of this smoke.
- **GAS** — explicitly out of scope (**deferred**).

## Deployment Recovery Attempt

**Date:** 2026-05-08 (recovery / alignment pass — doc + probes only; no Render dashboard access from agent).

### Previous blocker

- **HTTP 404** on **`POST /api/module01/calculations/items/add`** and **`GET .../items`** on **`https://eds-power-api.onrender.com`**.

### Local route registration (working tree)

| Check | Result |
|--------|--------|
| **`POST /api/module01/calculations/items/add`** on **`app`** | **Registered** in **local** `main.py` (`module01_calculation_items_add`). |
| **`GET /api/module01/calculations/{calculation_id}/versions/{version_id}/items`** | **Registered** (`module01_calculation_items_list`). |
| **Service module** | **`services/module01_calculation_items_service.py`** present locally (**untracked** in git at recovery time). |
| **Separate router include** | **None** — routes are **direct `@app` handlers** on the FastAPI app (no path prefix mismatch vs smoke URLs). |

### Git / deployment alignment (recorded)

| Field | Value (at recovery attempt) |
|--------|-----------------------------|
| **Local `HEAD`** | **`dc755945adef1328e365f8677a7a42ae77466f55`** (`Normalize audit filenames to 2026-05-08 chronology`) |
| **`main` vs `origin/main`** | **`main` ahead by 8 commits** (local branch diverged) |
| **`git show HEAD:main.py` / `origin/main:main.py`** | **No** `calculations/items` strings — **items routes not in committed history on `origin/main`** |
| **Implementation on GitHub** | **Items API not pushed** — working tree has **`M main.py`** (items wiring) + **`?? services/module01_calculation_items_service.py`** + **`?? tests/test_module01_calculation_items_api.py`** |
| **Render branch/commit** | **Inferred:** Render builds **`origin/main`** (typical); exact commit SHA is **operator-confirmed in Render UI** — **not** available from repo alone |
| **Redeploy** | **Not triggered** from this environment (no Render API / dashboard step). **Redeploy alone cannot fix 404** until **commit + push** includes items routes |

**Root cause (confirmed):** **404 is not a mystery routing bug in local code** — the **deployed** revision **lacks** the handlers because **`origin/main` lacks them**. Redeploy without push **reproduces** the same 404.

### Control probe (post-recovery check)

```http
GET https://eds-power-api.onrender.com/api/module01/auth/session/status
```
(no `Authorization` header)

**Result:** **HTTP 200**, **`status`:** **`auth_error`**, **`error_code`:** **`AUTH_MISSING_TOKEN`** — service **live**, Module 01 auth route **active**.

### Route existence probe

```http
POST https://eds-power-api.onrender.com/api/module01/calculations/items/add
Content-Type: application/json
{}
```

**Result:** **HTTP 404**, **`{"detail":"Not Found"}`** — **not acceptable** per route-existence gate (**still no route** on public deploy).

### Full authed smoke

- **Not run** — **404** blocks all scenarios; no Bearer smoke until deploy contains routes.
- **Operator token / DRAFT calculation:** **N/A** for this pass.

### Unblock resolution (operator / follow-on task, not executed here)

1. **Commit** minimal backend slice: items **`main.py`** delta + **`services/module01_calculation_items_service.py`** + **`tests/test_module01_calculation_items_api.py`** (and any **registry** permission for action **`calculation_items`** if auth requires it — **separate SQL task**, out of scope here).
2. **Push** to **`origin/main`** (or branch Render tracks).
3. **Render:** wait until service **Live** on new commit.
4. **Re-run** control + route existence (**expect** `AUTH_MISSING_TOKEN` / **`ITEM_*`** / **422**, **not** 404), then full smoke with real session.

---

## Implementation sync, push, and redeploy (2026-05-08)

### Pre-commit inspection

- **`main.py`:** Items-only intent verified; one **unrelated** hunk (**removal** of **`MODULE01_CREATE_PRODUCT_TYPE_UNSUPPORTED`** from create-calculation messages) was **reverted** before commit so the deploy commit stayed **calculation-items-only**.
- **Staged:** `main.py`, `services/module01_calculation_items_service.py`, `tests/test_module01_calculation_items_api.py` only.

### Git record

| Field | Value |
|--------|--------|
| **Commit** | **`b3b5f824d203a4673f066b97cc940a346cc9ce55`** |
| **Message** | `feat(module01): implement calculation items api v1 add list` |
| **Push** | **`git push origin main`** — succeeded (`main` → `main`) |
| **Post-push** | **`HEAD`** == **`origin/main`** == **`b3b5f82`** |

### Render deploy (observed)

- **Trigger:** inferred **auto-deploy from GitHub** (not manually opened in Render dashboard from this environment).
- **Rollout lag:** **`POST .../items/add`** returned **404** for **~8 × 15 s** (~2 min) after push, then began returning Module 01 **auth_error** envelope — **deploy caught up**.
- **Deployed commit SHA on Render:** **operator** confirm in Render UI if needed; **functional proof** = non-404 items route below.

### Control probe (post-deploy)

```http
GET https://eds-power-api.onrender.com/api/module01/auth/session/status
```

**Result:** **HTTP 200**, **`AUTH_MISSING_TOKEN`**, **`action`:** **`session_status`** — **PASS**.

### Route existence probe (post-deploy)

```http
POST https://eds-power-api.onrender.com/api/module01/calculations/items/add
Content-Type: application/json
{}
```

**Result:** **HTTP 200**, **`status`:** **`auth_error`**, **`error_code`:** **`AUTH_MISSING_TOKEN`**, **`action`:** **`calculation_items`** — **PASS** (**not** 404; route **registered** on live host).

### Full live smoke (authenticated)

| Scenario | Result |
|----------|--------|
| Top-level CONTAINER, PRODUCT, child under CONTAINER, list, negative parent | **Not run** — **no valid Bearer / no operator DRAFT calculation** in this workspace |
| **Local tests** | **`pytest tests/test_module01_calculation_items_api.py`** — **14 passed** (post-commit sanity; not a substitute for live authed smoke) |

**Status token:** **`CALCULATION_ITEMS_API_V1_ROUTE_LIVE_AUTH_SMOKE_PENDING_OPERATOR_TOKEN`**

---

## Verdict

**`CALCULATION_ITEMS_API_V1_ROUTE_LIVE_AUTH_SMOKE_PENDING_OPERATOR_TOKEN`**

- **Resolved:** **`CALCULATION_ITEMS_API_V1_DEPLOYMENT_BLOCKED_ROUTE_404_PERSISTS`** — public Render **no longer** returns **404** for **`POST /api/module01/calculations/items/add`** after **`b3b5f82`** deploy roll-forward.
- **Pending:** Operator **Bearer** session + **DRAFT** **`calculation_id`** / **`version_id`** to execute hierarchy smoke (**CONTAINER** / **PRODUCT** / **`ITEM_PARENT_NOT_CONTAINER`**, list preorder) on **`https://eds-power-api.onrender.com`**. **Registry** must allow action **`calculation_items`** for the test role or smoke will fail with permission/auth errors — **operator SQL** if missing (**out of scope** here).

**Not claimed:** **`CALCULATION_ITEMS_API_V1_LIVE_BACKEND_SMOKE_VERIFIED`** until authed scenarios **PASS** and are recorded here.

**GAS / Editor:** **not** discussed or implemented.
