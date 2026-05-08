# Terminal UX Stabilization V1 — Single EDS Power Menu + Auto Sidebar

## Objective

Stabilize Google Sheets terminal UX before KZO calculation work: **one canonical top-level menu** (`EDS Power`), predictable item order, **no duplicate** `EDS Power Auth` menu, **auto-open Module 01 sidebar** when a **non-expired** session exists on `onOpen`, and a reliable **«Відкрити бокову панель»** fallback.

## Root cause (duplicate menus)

1. **`module01AuthOnOpen_()`** (`gas/AuthMenu.gs`) registered a second top-level menu **`EDS Power Auth`** via `createMenu` + `addToUi`.
2. **`EDSPowerCore_refreshMenu` / `EDSPowerCore_renderDynamicMenu_`** registered **`EDS Power`** from registry-backed items.
3. **`onOpen`** in **`EDSPowerLocalBootstrap.gs`** invoked **both** auth menu registration and core refresh → **two top-level menus**; Google Sheets does not guarantee stable ordering across reloads → operator confusion.
4. **`registerModule01DemoMenu_()`** (demo / third menu) was invoked on every open — removed from `onOpen` for stabilization (demo functions remain in project for editor-driven use if needed).

## Files changed

| File | Role |
|------|------|
| `gas/core/EDSPowerCore.gs` | Unified renderer: shell block + registry items (deduped callbacks); static fallback uses same shell + diagnostics |
| `gas/terminal/EDSPowerLocalBootstrap.gs` | `onOpen`: no demo/auth duplicate registration; `edsPowerTryAutoOpenModule01Sidebar_`; emergency menu titled **EDS Power**; `user_session_present` respects **expiry** |
| `gas/AuthMenu.gs` | `module01AuthOnOpen_` → **`edsPowerRefreshMenu` only** (no second menu); login/logout refresh unified menu; post-login auto-open sidebar |
| `gas/Module01Sidebar.gs` | Auth copy: point to **EDS Power → Авторизуватись** |

## Final top-level menu structure (canonical)

**Title:** `EDS Power`

**Shell block (fixed order):**

1. **Авторизуватись** *or* **Перевірити сесію** (if valid non-expired session)
2. **Відкрити бокову панель** → `edsPowerOpenModule01Sidebar`
3. **Оновити меню** → `edsPowerRefreshMenu`
4. **Module 01 — Розрахунки** → `edsPowerOpenModule01Sidebar`
5. **Вийти** (session only) → `module01AuthLogout`
6. *(separator)*
7. **Registry-driven items** (visibility/sort from API), excluding actions whose callbacks duplicate the shell (refresh, sidebar, session, login, logout)

**Static fallback (menu API unavailable):** same shell + **Діагностика** entries (`edsPowerFallbackSetupRequired_`, `edsPowerRefreshSetupCheck_`).

## `onOpen` sidebar behavior

After **`EDSPowerCore_onTerminalOpen(context)`** succeeds:

- If **`context.user_session_present === true`** (token present **and not expired**): **`edsPowerOpenModule01Sidebar()`** in try/catch.
- On failure: **`SpreadsheetApp.getActiveSpreadsheet().toast(...)`** with pointer to **EDS Power → Відкрити бокову панель**.
- If no session: **no** auto-open (menu still usable).

## Manual fallback

**EDS Power → Відкрити бокову панель** (and **Module 01 — Розрахунки**) call **`edsPowerOpenModule01Sidebar`**.

## Scope confirmation

- **No** DB / SQL / migrations / Render env / backend changes.
- **No** KZO / product / calculation engine logic.
- **No** permission or numbering decisions in GAS beyond existing transport/session hints.

## Operator sync

1. Deploy/sync: `EDSPowerCore.gs`, `EDSPowerLocalBootstrap.gs`, `AuthMenu.gs`, `Module01Sidebar.gs`.
2. Close and reopen the Sheet (or reload).
3. Confirm **only one** custom menu: **EDS Power**.
4. With valid session: sidebar should open on load; if not, use **Відкрити бокову панель**.
5. Log out → menu should show **Авторизуватись**; no second auth menu.

## Verdict

**`TERMINAL_UX_STABILIZATION_V1_IMPLEMENTED`** — pending operator live verification.
