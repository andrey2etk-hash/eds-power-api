# Module 01 Sidebar Static Context V1 — Live Operator Test Closeout

## Objective

Record a **successful live operator smoke test** of **`MODULE_01_SIDEBAR_STATIC_CONTEXT_V1`**: Google Sheets bound Apps Script, authenticated **`GET /api/module01/sidebar/context`** on Render, Supabase-backed session/user/role, and **`Module01SidebarHtml`** sidebar UI — **no** new implementation in this document.

## Preconditions

- **Implementation** documented: **`docs/AUDITS/2026-05-07_MODULE_01_SIDEBAR_STATIC_CONTEXT_V1_IMPLEMENTATION.md`**
- Operator **manually synced** repo GAS into the **bound** Apps Script project (per Manual Sync / Deployment doctrine).
- **HTML naming:** bound project requires **different base names** for paired `.gs` / `.html` — repo uses **`Module01Sidebar.gs`** + **`Module01SidebarHtml.html`** (see **`docs/AUDITS/2026-05-07_MODULE_01_SIDEBAR_STATIC_CONTEXT_V1_IMPLEMENTATION.md`** § HTML file naming).
- Render API deployed with **`GET /api/module01/sidebar/context`**; operator session valid (Bearer).

## GAS sync evidence

- **Operator attestation:** GAS sources were **manually copied** from the repository into the bound Apps Script project before the smoke test.
- **Files in scope for this slice (conceptual):** `Module01Sidebar.gs`, `Module01SidebarHtml.html`, supporting **`AuthTransport.gs`** (sidebar context transport), **`EDSPowerCore.gs`** (menu callback to **`edsPowerOpenModule01Sidebar`** where used), plus existing auth/session files as already installed on the terminal.
- **No** Cursor or agent execution against Supabase; **no** SQL in this closeout.

## Render / backend status

- **Endpoint:** `GET https://<render-host>/api/module01/sidebar/context` (operator environment).
- **Auth:** Bearer session; identity and role from backend session path (not from client-declared user_id in sidebar GET).
- **Outcome (operator):** HTTP success path observed; sidebar envelope provided **`data.sidebar`** with user, session timing, **`active_calculation: null`**, and static sections per V1 design.

## Live UI evidence

**Operator-reported visible UI (Google Sheets sidebar):**

| Check | Result |
|--------|--------|
| Title | **Module 01 — Розрахунки** |
| Session / user block | **Visible** |
| User display | **Test Auth User** |
| Role | **TEST_OPERATOR** |
| Session expiry | **Visible** (UTC / ISO as returned) |
| Remaining seconds | **Visible** |
| Current calculation | **No active calculation** |
| Primary actions block | **Visible** |
| Buttons | **Disabled** / placeholder (V1) |
| Blank white sidebar | **None** — loading/error/success panels behaved as designed |

*No passwords, tokens, or hashes are recorded in this audit.*

## Validated path

```text
Google Sheets (bound GAS)
  → Module01Sidebar.gs (`edsPowerOpenModule01Sidebar` / `module01SidebarServerGetContext`)
  → Render GET /api/module01/sidebar/context
  → Supabase (auth / session / user / role resolution — backend-owned)
  → Sidebar context JSON
  → Module01SidebarHtml (UI)
  → Google Sheets Sidebar
```

## HTML naming issue and resolution

- **Issue:** Apps Script **bound** projects **do not allow** a `.gs` and `.html` file to share the **same base name** (e.g. `Module01Sidebar.gs` + `Module01Sidebar.html` was blocked on sync).
- **Resolution (repo):** HTML file **`Module01SidebarHtml.html`**; **`HtmlService.createHtmlOutputFromFile("Module01SidebarHtml")`** — recorded in implementation closeout and **dfedce0** fix commit trajectory.
- **Operator impact:** sync **`Module01Sidebar.gs`** and **`Module01SidebarHtml.html`** as **two** distinct file names.

## What was NOT tested

- **Create Calculation** modal or **`POST /api/module01/calculations/create`**
- **Registry** menu row **`OPEN_MODULE_01_SIDEBAR`** (if absent, operator may use editor-run **`edsPowerOpenModule01Sidebar`**)
- **DocumentProperties** `active_calculation_id` cache (V1 remains null from API)
- **Non–TEST_OPERATOR** roles, expired-session edge re-check beyond this smoke, multi-terminal fleet matrix

## What was NOT changed

- **No** new GAS, backend, SQL, migrations, Render env, product, or calculation logic in **this** closeout task (documentation only).

## Verdict

**`MODULE_01_SIDEBAR_STATIC_CONTEXT_V1_LIVE_PASS`**

**Next governance lane (DOC / planning only until tasked):** **Module 01 Create Calculation Modal V1** planning — **do not** set modal **implementation** active without explicit TASK.
