# MODULE 01 CALCULATION RECORD + VERSIONED EDITOR FLOW V1

## Status

**SCOPE DEFINITION / DOC ONLY**

This document records **user doctrine** and **scope boundaries** only. It is **not** an implementation spec, **not** a DB design, and **not** an API contract until reviewed and audited.

---

## Core Doctrine

**Module 01 starts from calculation record creation, not equipment type selection.**

A **calculation** is a **container** (commercial/engineering record) that may hold **many items** of **different** equipment or service types. The user **must not** choose a single equipment/product type for the **whole calculation** at creation time.

**Canonical order:**

1. **Calculation Record** exists first (parent container).
2. **Version** is created for that record (immutable identity via **mandatory** `version_suffix`).
3. **Items** are authored **inside** a version; **each item** may carry its own type (KZO, KTP, BMZ, manual, service, future types).

---

## Calculation Record

The **calculation record** defines the **commercial/engineering calculation container** (header-level identity and metadata).

**Possible fields** (conceptual — not a committed schema):

| Field | Role (conceptual) |
|-------|-------------------|
| `base_calculation_number` | System-generated base identifier (format TBD — see Open Questions) |
| `full_calculation_number` | Display / logical full number, typically `<base>-<version_suffix>` |
| `version_suffix` | Mandatory on every **version** row; initial is always **`-00`** |
| `customer` | Commercial counterparty (may align with “potential customer” in current V1 header) |
| `object_name` | Site / object / project label |
| `sales_manager` | Commercial owner |
| `calculation_author` | Technical/authoring owner |
| `created_at` | Audit timestamp |
| `status` | Lifecycle (e.g. DRAFT) — exact states TBD |
| `comment` | Free-text or structured note (may overlap with existing `notes` patterns) |

**Governance:** the **record** does **not** own a single “product type” for the whole calculation; **types belong to items** inside a version.

---

## Version Rule

**No calculation version may exist without a version suffix.**

- **Initial version** is always **`-00`**.
- **Full number format:**

  `<base_calculation_number>-<version_suffix>`

  Where `version_suffix` includes the leading hyphen convention already used in Module 01 (e.g. **`-00`**, **`-01`**).

**Examples:**

- `202605081430-00`
- `202605081430-01`
- `202605081430-02`

**Revision rule (doctrine):** editing a **saved/committed** calculation **does not** silently overwrite an existing version; a **new** version row is created with the next suffix (**`-01`**, **`-02`**, …). Prior versions remain for **history and comparison** (mechanism TBD — see Open Questions).

---

## Create Flow

1. User opens **Create Calculation** entry point (modal or successor UI — **not** specified as implementation here).
2. User enters **general calculation information** only (no whole-calculation equipment type).
3. **Backend** creates **calculation record** (container).
4. **Backend** creates **initial version** with suffix **`-00`**.
5. **UI** shows **full calculation number** (e.g. `…-00`).
6. **UI** transitions into **Calculation Editor** mode scoped to that **version**.

---

## Editor Flow

The **editor** operates **inside a specific calculation version** (not “the calculation” as a flat document without version context).

**Allowed editor actions** (conceptual only):

- Add item  
- Edit **draft** item  
- Remove **draft** item  
- View item details  
- Add **equipment-type-specific** item **later** (per-item type: KZO, KTP, BMZ, manual, service, custom, future types)

**Not defined** in this scope doc: persistence shape, API routes, GAS modals, validation rules, or engine integration.

---

## Calculation Items

**Equipment / product type belongs to the item level, not the calculation record level.**

**Item examples** (non-exhaustive):

- KZO item  
- KTP item  
- BMZ item  
- Manual line item  
- Service item  
- Custom / future equipment types  

One version may contain **heterogeneous** items.

---

## Revision Flow

- **`-00`** is **never** silently overwritten **after commit** (definition of “commit” TBD — see Open Questions).
- **`-01`** is created from the **committed** **`-00`** baseline (conceptually “branch forward,” not overwrite).
- **`-02`** from **`-01`**, etc.
- **Old versions** remain available for **history** and **comparison**.

---

## What This Is NOT

- **Not** the final calculation engine  
- **Not** BOM  
- **Not** pricing  
- **Not** product configurator implementation  
- **Not** DB migration or table design  
- **Not** API endpoint implementation  
- **Not** GAS / Sheets UI implementation  
- **Not** a decision to keep or remove any legacy “whole-calculation `product_type`” field in existing code — **reconciliation** with deployed V1 is an **open governance** topic (see Open Questions)

---

## Governance Rules

| Rule | Statement |
|------|-----------|
| Parent container | **Calculation** is the parent container. |
| Editable state | **Version** is the unit of **versioned editable state**. |
| Items | **Items** belong to a **version**. |
| Type locus | **Product / equipment type** belongs to the **item**, not the calculation record. |
| Suffix | **Version suffix is mandatory** on every version. |
| Initial | **Initial version is always `-00`**. |

---

## Open Questions

Record for **audit / user review** — **no answers implied** by this doc:

1. **Exact `base_calculation_number` format** (length, timezone, collision policy) vs existing Module 01 implementation (e.g. 12-digit UTC minute bucket).
2. **Mandatory fields** on **create** modal: title only? customer? object? author? — alignment with **`EDS_POWER_MODULE_01_CREATE_CALCULATION_TECHNICAL_SPEC.md`** and **deprecation of calculation-level `product_type`**.
3. **When** does a version become **committed / locked**? (transition from draft edits to immutable baseline for revision.)
4. **Who** may create a **revision** (role / permission model).
5. **Draft edits** inside **`-00`** before **first commit**: allowed, limited, or not?
6. **Item ordering** within a version: explicit `sort_order`, tree, or grouping?
7. **Deleted items**: soft-delete with history vs hard-delete; appear in diffs?
8. **Customer / object directory**: picker vs free text; integration timing.
9. **Reconciliation** with current DB/API/GAS that store **`product_type` at version or header** for V1 — migration path vs greenfield editor (doctrine vs legacy).
10. **Status history** per version vs per calculation header — consistency with existing `module01_calculation_status_history`.

---

## Verdict

**Ready for user review before implementation planning.**

Next governance step (per **`docs/NOW.md`**): **Gemini audit** (or equivalent) of this scope definition — **no implementation** until audit + explicit TASK.
