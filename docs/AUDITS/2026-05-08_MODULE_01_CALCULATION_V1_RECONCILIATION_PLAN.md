# MODULE 01 CALCULATION V1 RECONCILIATION PLAN

## 1. Objective

Resolve the gap between:

- **Target doctrine:** **`docs/00-02_CALC_CONFIGURATOR/MODULE_01_CALCULATION_RECORD_VERSIONED_EDITOR_FLOW_V1.md`** (calculation-record-first; equipment/product type at **item** level; versioning rules).
- **Existing shipped slice:** **Create Calculation V1** — API, GAS modal, tests, technical spec — which today treats **`product_type`** as part of **create payload** and persists it at **version `notes`** granularity as a **whole-calculation** stand-in.

**Gemini verdict (governance input):** **PASS / READY_FOR_RECONCILIATION** on the target doctrine document.

This file is **DOC ONLY** — read-only inspection was used to build the inventory and matrix. **No implementation** was performed.

---

## 2. Target Doctrine (summary)

| Rule | Statement |
|------|-----------|
| Record-first | Module 01 starts from **calculation record** creation, not **product-type-first** selection. |
| Type locus | **Equipment / product type** belongs to **calculation item** level, **not** calculation header at create time. |
| Initial version | Always **`-00`**; full display **`<base_calculation_number>-00`**. |
| Revisions | **`-00` → `-01` → `-02` → …**; **committed** baselines must **not** be silently overwritten. |
| Container | A **calculation** is a commercial/engineering **container** for many heterogeneous items. |

---

## 3. Existing Implementation Inventory (`product_type` and related)

Read-only inspection. **Create Calculation V1** path only called out in detail; unrelated demo/KZO sheet code listed only where it confuses naming.

### 3.1 Backend — `services/module01_calculations_service.py`

| Location | Behavior | Doctrine conflict? |
|----------|----------|---------------------|
| `build_structured_notes_v1(..., product_type=...)` | Writes **`PRODUCT_TYPE:`** line into **`module01_calculation_versions.notes`**. | **BLOCKING** — encodes **whole-version/calculation-level** product type in absence of `calculation_items`. |
| `validate_create_payload` | Requires `payload.product_type` **string exactly `KZO`**; else **`MODULE01_CREATE_PRODUCT_TYPE_UNSUPPORTED`**. | **BLOCKING** — mandatory **product-type-first** at create. |
| `create_calculation_v1` | Normalized payload includes **`"product_type": "KZO"`**; `notes` built with **`build_structured_notes_v1(product_type="KZO", ...)`** (hardcoded after validation). | **BLOCKING** — persists KZO as version-scoped semantic default. |
| Response `data["calculation"]["product_type"]` | Always **`"KZO"`** in success envelope. | **BLOCKING** relative to “type is per-item” (OK as legacy display **only** if doctrine allows a **placeholder**; currently implies **calculation-level** type). |
| Sidebar display string | `sidebar_line = f"{display} — KZO — DRAFT"` | **MINOR** — UX string hardcodes **KZO** for all new calcs. |

### 3.2 Backend — `main.py`

| Location | Behavior | Doctrine conflict? |
|----------|----------|---------------------|
| `POST /api/module01/calculations/create` | Thin route; delegates to **`validate_create_payload`** / **`create_calculation_v1`**. | **NONE** at router — conflict is in **service contract**. |

### 3.3 Backend — `services/module01_sidebar_service.py`

| Location | Behavior | Doctrine conflict? |
|----------|----------|---------------------|
| `_parse_product_type_from_notes_v1` | Parses **`PRODUCT_TYPE:`** from version **notes**. | **MINOR** — assumes **version notes** carry a **single** product type for display. |
| `active_calculation` / defaults | Uses parsed type or defaults **`"KZO"`**. | **MINOR** — reinforces **KZO** as default **calculation-level** display. |

### 3.4 GAS — `gas/Module01CreateCalculationModal.gs`

| Location | Behavior | Doctrine conflict? |
|----------|----------|---------------------|
| `module01CreateCalculationBuildPayload_` | Sets **`product_type: "KZO"`** in nested **`payload`**. | **BLOCKING** — client always sends mandatory **whole-calculation** type. |

### 3.5 GAS — `gas/Module01CreateCalculationModalHtml.html`

| Location | Behavior | Doctrine conflict? |
|----------|----------|---------------------|
| `<select id="product_type" disabled>` with only **KZO** | UI presents **product type** on **create** form (even if disabled). | **BLOCKING** UX — signals **product-type-first** mental model at creation. |
| Success panel | Shows **`calc.product_type`** from API. | **MINOR** — inherits API **calculation-level** field. |

### 3.6 Tests

| Path | Behavior | Doctrine conflict? |
|------|----------|---------------------|
| `tests/test_module01_calculations_service.py` | Asserts structured notes, validation, response **`product_type` KZO**. | **BLOCKING** once contract changes — tests **lock in** current doctrine. |
| `tests/test_module01_calculations_create_endpoint.py` | **`test_invalid_product_type`**, payloads with **`product_type": "KZO"`** / **`OTHER`**. | **BLOCKING** — enforces **KZO-only** create. |

### 3.7 Documentation — Create Calculation V1

| Path | Behavior | Doctrine conflict? |
|------|----------|---------------------|
| `docs/ARCHITECTURE/EDS_POWER_MODULE_01_CREATE_CALCULATION_TECHNICAL_SPEC.md` | **`product_type`** required **`KZO`** on create; stored in **version `notes`** template. | **BLOCKING** — normative spec contradicts **item-level** doctrine. |
| `docs/ARCHITECTURE/EDS_POWER_MODULE_01_CREATE_CALCULATION_MODAL_V1_PLANNING.md` | Modal planning assumed **KZO** / product framing (historical). | **MINOR** — planning doc; superseded by reconciliation. |
| `docs/ARCHITECTURE/EDS_POWER_MODULE_01_SIDEBAR_TECHNICAL_SPEC.md` | Examples include **`product_type`** on **active_calculation**. | **MINOR** — contract examples need **future** alignment. |

### 3.8 Database (read-only inference from docs / code)

| Area | Behavior | Doctrine conflict? |
|------|----------|---------------------|
| `module01_calculations` | No dedicated **`product_type`** column (per technical spec). | **NONE** at **header** DDL — conflict is **semantic** / **API** / **notes**. |
| `module01_calculation_versions` | **`notes`** text holds **`EDS_POWER_CALC_NOTES_V1`** including **`PRODUCT_TYPE:`**. | **BLOCKING** — version row carries **whole-calculation** type proxy until **items** exist. |
| **`calculation_items` table** | **Not** present in Create Calculation V1 slice. | **BLOCKING** for full doctrine — **items** have **no** first-class persistence yet. |

**Note:** Legacy **demo / Stage 3D** **`product_type`** in `gas/Stage3D_KZO_Handshake.gs`, **`calculation_snapshots`**, etc., are **out of scope** for this reconciliation matrix except as **naming** confusion risk — they are **not** the Module 01 **create calculation** API path.

---

## 4. Conflict Matrix

| Area | Current Behavior | Target Doctrine | Conflict Level | Proposed Resolution (planning only) |
|------|------------------|-----------------|----------------|-------------------------------------|
| Create API payload | **`product_type` mandatory `KZO`** | No whole-calculation type at create | **BLOCKING** | Remove or optionalize per §5; update spec + tests in a **bounded** implementation task. |
| Version `notes` template | **`PRODUCT_TYPE: KZO`** required line | Type belongs on **items**; version notes may hold only non-type metadata until items exist | **BLOCKING** | Evolve template (e.g. omit type line, or **`PRODUCT_TYPE: N/A`** / migration rules) + **items** table later. |
| GAS modal | Disabled **KZO** selector + payload sends **`product_type`** | No type choice at **create** | **BLOCKING** | Remove control + field from payload when API allows. |
| Success / sidebar **`product_type`** | **`KZO`** constant in API + sidebar parser default | Per-item types; display may be **summary** or **empty** until items | **MINOR** / **BLOCKING** for display spec | Define **display rule**: e.g. **no** calculation-level type; show **“mixed”** / item count / **—** until items. |
| Versioning **`-00`** | Initial insert uses **`version_suffix = '-00'`** | Initial **always `-00`** | **NONE** | **PASS** — keep; align naming docs with doctrine **full_calculation_number**. |
| Revision **`-01+`** | **Not** implemented in Create Calculation V1 | Revisions create new rows | **BLOCKING** (missing capability) | **Future task:** revision API + rules (draft vs commit). |
| **`calculation_items`** | Absent | Items own **`item_type`** | **BLOCKING** (gap) | **Future task:** conceptual → schema → API (outside this plan execution). |
| Technical spec | Normative **KZO** on create | Record-first | **BLOCKING** | **Amend spec** after audit approval; version spec. |

---

## 5. `product_type` Reconciliation Decision (recommendation — **not** implemented)

**Preferred target (doctrine-aligned):** **`product_type` must not be mandatory** on **calculation header / create** as a **whole-calculation** discriminator. Future authoritative locus: **`calculation_items.item_type`** (or equivalent).

| Option | Description | Fit |
|--------|-------------|-----|
| **A** | Remove **`product_type`** from Create Calculation modal + API create payload; stop writing **`PRODUCT_TYPE:`** in **notes** (or replace with explicit **neutral** token agreed in spec). | **Best** alignment; **highest** coordinated change (API + GAS + tests + spec + sidebar). |
| **B** | Keep field **optional**; backend **ignores** if present; no **notes** line for type until first item. | **Transitional**; risk of **ambiguous** client behavior if not deprecated clearly. |
| **C** | Optional **`product_type`** only as **“seed first item”** hint (creates a **draft** item row in future). | **Conceptually nice**; requires **items** API — **not** minimal first step. |

**Recommendation for governance:** **Option A** as **north star** for the **next implementation epic**, executed in **bounded slices** (e.g. contract change + GAS + tests in one PR; **notes** template migration strategy in the same or follow-on PR). If **items** are not ready, **interim** **Option B** may be used **only** with explicit **deprecation** and **`MODULE01_CREATE_PRODUCT_TYPE_UNSUPPORTED`** **removed** or narrowed — **decision** belongs post **Gemini audit** of **this** reconciliation plan.

---

## 6. Versioning Reconciliation

**Canonical (target):**

- **Base:** `base_calculation_number` (e.g. 12-digit UTC minute in current impl).
- **Suffix:** `version_suffix` (e.g. **`-00`**, **`-01`**).
- **Full display:** `<base_calculation_number>-<suffix_digits>` (e.g. **`202605081430-00`**).

**Current implementation:** **PASS** for **initial** version — service inserts **`version_suffix = '-00'`** and **`calculation_version_number`** = **`<base>-00`**.

**Gap:** **Revision** creation (**`-01`**, **`-02`**, …) and **non-overwrite** rules for **committed** versions — **not** in Create Calculation V1 — **future tasks**.

---

## 7. Draft vs Commit Rule (target — **not** implemented)

**Target behavior (doctrine):**

| State | Behavior |
|-------|----------|
| **DRAFT** | Editable **inside** the same **version** suffix; **item** edits **do not** mint **`-01`** on every keystroke. |
| **Committed / locked / baseline** | **Cannot** be silently overwritten; next published change creates **new** **`version_suffix`**. |

**Naming:** Final enum labels (**DRAFT** vs **COMMITTED** vs **LOCKED** vs **BASELINE**) — **open decision**;must be chosen before **revision** API design.

**Current code:** Module 01 tables use **`DRAFT`** status on header and version; **no** “commit” transition or **revision** path — **documented as gap**.

---

## 8. Calculation Editor Flow (target)

1. Create **calculation record**.  
2. Create **initial version `-00`**.  
3. Open **editor** scoped to **that version**.  
4. User **adds items**.  
5. **Each item** has its own **`item_type` / `product_type`**.  
6. **Draft** edits stay in **current draft version**.  
7. **Post-commit** edits → **new** version suffix.

**Current:** Steps **1–2** exist via **Create Calculation V1**; steps **3–7** **not** implemented as **editor**.

---

## 9. Minimal `calculation_items` Concept (V1 **conceptual only**)

**Strict:** **No** DDL, **no** migration, **no** API.

Possible fields for **future** design discussion:

- `id`  
- `calculation_id`  
- `calculation_version_id`  
- `item_index`  
- `item_type` (replaces **whole-calculation** `product_type`)  
- `item_name`  
- `quantity`  
- `status`  
- `payload_json` (equipment-specific blob)  
- `created_at` / `updated_at`  

---

## 10. Required Future Implementation Tasks (do **not** execute here)

- Amend **`EDS_POWER_MODULE_01_CREATE_CALCULATION_TECHNICAL_SPEC.md`** after audit-approved reconciliation.  
- Update **`POST /api/module01/calculations/create`** contract (payload, validation, notes template, response shape).  
- Update **GAS** Create Calculation modal (remove / neutralize **product type** UX).  
- Update **`module01_sidebar_service`** display rules (no **KZO** assumption).  
- **Calculation Editor V1** (UI + server) — scoped separately.  
- Define **`calculation_items`** schema + migrations (**operator-gated** SQL).  
- Define **revision** creation flow + permissions.  
- Replace / extend **tests** (`test_module01_calculations_*`).  
- **Gemini audit** of **this reconciliation plan** before first implementation PR.  
- **Gemini audit** of **implementation** plan after contract freeze.

---

## 11. Out of Scope

- **No** code, **no** GAS, **no** API, **no** DB migration, **no** SQL execution, **no** Render changes in the preparation of this document.  
- **No** product calculation engine, **no** BOM, **no** pricing, **no** KZO/KTP/BMZ **item** engines.  
- **No** removal of **`product_type`** in repo **as part of this task**.

---

## 12. Verdict

**`RECONCILIATION_PLAN_READY_FOR_GEMINI_AUDIT`**
