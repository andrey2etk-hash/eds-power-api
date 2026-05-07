# EDS Power Module 01 — Calculation Slice 01 Planning

**Date:** 2026-05-07  
**Mode:** Documentation / planning only. **No** Python, GAS, DB, SQL, migrations, Render implementation, or product/calculation engine code in this artifact.

---

## 1. Purpose

Define the **first minimal, bounded** Module 01 calculation flow **after** DB-driven menu registry live validation — sufficient to plan an end-to-end **authenticated** “calculation request → backend → bounded response” path without committing to full KZO engineering, BOM, or production workflows.

---

## 2. Starting Point

The following foundation is **live validated** and **post-audit cleanup completed** (see governance closeouts):

- Module 01 **auth/session** and **terminal** binding — **PASS**  
- **Dynamic menu** — `menu_source = registry` — **PASS**  
- **Registry labels** reflected in Google Sheets — **PASS**  
- Temporary auth stdout diagnostics — **env-gated** (`EDS_POWER_AUTH_DEBUG_LOGS`)  
- No active registry blockers for **planning** the next slice  

References:

- `docs/AUDITS/2026-05-07_EDS_POWER_DB_DRIVEN_MENU_FINAL_OPERATOR_VALIDATION.md`  
- `docs/AUDITS/2026-05-07_EDS_POWER_DB_DRIVEN_MENU_POST_AUDIT_CLEANUP.md`  

---

## 3. Slice 01 Boundary

**Smallest safe slice** (recommended):

| Aspect | Slice 01 intent |
|--------|------------------|
| Caller | **Authenticated** user (Bearer session from existing Module 01 auth path). |
| Context | **Terminal** (and thus `user_id`) resolved **only** on the server from the session — not trusted from the raw JSON body for authorization. |
| Request | **One** calculation “prepare” (or equivalent) HTTP request per operator action (batch-friendly; no per-cell API spam). |
| Backend | **Validate** payload shape, `product_type`, and allowed action; **no** heavy engineering. |
| Engine | **Deterministic mock or minimal placeholder** response (e.g. echo + `logic_version`, trivial computed field) — **no** real KZO node/busbar/BOM logic unless **explicitly** approved in a later task. |
| Product logic | **Out** unless a separate audit approves a thin slice. |

This slice proves: **Sheet → GAS → Render (auth) → Module 01 calc endpoint → envelope → optional persistence plan** — not product maturity.

---

## 4. Candidate Product Scope

**Candidates** (discussion only — **no** commitment until user + Gemini audit):

1. **KZO planning entry point** — later wiring to `00-02` configurator; Slice 01 would only reserve **contract** and **routing**, not DNA/engine.  
2. **Generic Module 01 calculation shell** — product-agnostic `prepare` that validates auth + payload and returns a **stub** `data` block.  
3. **Calculation proposal record** — align naming with existing `module01_calculations` / `module01_calculation_versions` schema **conceptually**; persistence optional in Slice 01 (see §10).  
4. **NCR baseline** — only if product owner elevates NCR; **default defer** for Slice 01.  

**Do not** choose a full engineering engine in Slice 01 planning without **user approval** and **audit**.

---

## 5. Input Payload Draft

**Conceptual** JSON body (fields may be refined after audit):

```json
{
  "calculation_id": null,
  "calculation_number": "...",
  "product_type": "KZO",
  "source_client": "GAS",
  "terminal_id": "...",
  "spreadsheet_id": "...",
  "inputs": {}
}
```

**Planning notes:**

- `calculation_id` **null** on first create; server may assign identifiers if persistence is in scope.  
- `calculation_number` must align with existing validation rules if persisted (`module01_calculations` — e.g. format constraints in migrations).  
- `terminal_id` / `spreadsheet_id` in body may be used for **diagnostics or correlation only**; **authorization** must use **session-bound** terminal (same pattern as login).  
- `inputs` — empty object acceptable for **mock** slice; structure to be fixed in payload contract task.  

---

## 6. Backend Endpoint Concept

**Namespace:** Module 01 routes already use `/api/module01/auth/...`. Calculation should follow the same prefix for clarity and policy.

**Planned (candidate) endpoint:**

`POST /api/module01/calculations/prepare`

**Existing repo note:** The codebase exposes **`POST /api/calc/prepare_calculation`** for the **CALC_CONFIGURATOR** / KZO demo path (`action: prepare_calculation`). Slice 01 should **not** silently overload that contract; prefer **`/api/module01/calculations/...`** for Module 01–owned calculation orchestration, unless a future audit explicitly unifies routes.

**Final path and handler names** — **TBD** in §13 checklist + audit.

---

## 7. Response Envelope

Use the **standard EDS Power** global envelope (see `docs/00_SYSTEM/04_DATA_CONTRACTS.md`):

```json
{
  "status": "success",
  "data": {},
  "error": null,
  "metadata": {
    "request_id": "...",
    "api_version": "...",
    "logic_version": "..."
  }
}
```

For Slice 01 **mock**, `data` might include e.g. `slice: "MODULE_01_CALC_SLICE_01"`, `echo_inputs`, `calculation_number` echo — **exact shape TBD**.

Error paths use `status` / `error` per contract (e.g. `validation_error`, `auth_error`, or module-specific statuses — **align in audit**).

---

## 8. Auth Boundary

- **Required:** `Authorization: Bearer <session_token>` from Module 01 session flow.  
- **Forbidden:** Treating `user_id`, `role`, or “is admin” from **GAS-supplied body** as authoritative.  
- **Server-side:** Reuse session validation patterns analogous to `/api/module01/auth/menu` (session → `user_id` → terminal → role checks as needed for **`TEST_OPERATOR`** or successor role).  
- **Slice 01:** Permission matrix may be minimal (single role) but **must** be **server-enforced**.  

---

## 9. GAS Thin Client Boundary

**GAS may:**

- Collect operator inputs (sheet ranges / form fields).  
- Send **one** (or bounded batch) **HTTP** request with Bearer token.  
- Render returned data (status, summary block, placeholders).  

**GAS must not:**

- Implement **engineering** or **calculation** logic.  
- Decide **permissions** or menu truth (registry/API owns that).  
- **Query Supabase** directly for business data.  
- **Store** canonical business rules.  

---

## 10. Supabase Persistence Planning

**Options** (choose in §13 — **no SQL in this document**):

| Option | Description |
|--------|-------------|
| **A — No persistence** | Slice 01 returns envelope only; proves transport + auth + validation. Lowest risk. |
| **B — Placeholder persistence** | Insert minimal row into existing **`module01_calculations`** / **`module01_calculation_versions`** (schema already in repo migrations) with **stub** outcome — **only** after separate DDL/data-model audit confirms columns and idempotency. |

**No new tables** in Slice 01 planning. **No** migration authoring in this task.

---

## 11. Error Contract

Planned **machine-facing** error codes (string examples; final list in data-contract task):

| Code | When |
|------|------|
| `CALC_AUTH_REQUIRED` | Missing/invalid Bearer or session. |
| `CALC_INVALID_PAYLOAD` | Schema / required field / format violation. |
| `CALC_PRODUCT_TYPE_UNSUPPORTED` | `product_type` not allowed for Slice 01. |
| `CALC_ENGINE_UNAVAILABLE` | Engine/mock layer not configured or fail-closed. |
| `CALC_SNAPSHOT_SAVE_FAILED` | If persistence option B fails. |
| `CALC_PERMISSION_DENIED` | Authenticated but role/terminal policy denies calc action. |

**Client-facing** messages stay **neutral** where security requires (reuse Module 01 auth patterns where applicable).

---

## 12. Out of Scope

Explicitly **excluded** from Slice 01 planning approval **until** separate tasks:

- Real **KZO** engineering logic (node matrix, busbar, fasteners, full topology).  
- **BOM** calculation, costing, production tasks.  
- **New Supabase tables** or migrations (beyond optional use of **existing** Module 01 calc tables under audit).  
- **GAS UI** expansion beyond thin transport/render.  
- **Render** deployment/env changes as part of *this* planning doc.  
- **Menu/registry** changes (already validated).  

---

## 13. Implementation Readiness Checklist

Before **any** code:

- [ ] **Exact** endpoint path and method (`POST /api/module01/calculations/prepare` or approved variant).  
- [ ] **Persistence:** Option A vs B; if B, confirm schema mapping and idempotency story.  
- [ ] **Product type** for first call (e.g. `KZO` stub only).  
- [ ] **Payload contract** frozen in a short data-contract doc or audit appendix.  
- [ ] **Gemini audit** of this planning + security boundary.  
- [ ] **User approval** to open an implementation task (implementation **not** active until then).  

---

## 14. Verdict

**`MODULE_01_CALC_SLICE_01_PLAN_READY_FOR_AUDIT`**

Next step: **Gemini audit** of this planning doc and **user** sign-off before implementation work is opened.
