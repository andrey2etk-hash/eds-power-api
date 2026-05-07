# EDS Power DB-Driven Menu — Post-Audit Cleanup

**Date:** 2026-05-07  
**Mode:** Cleanup only (no new product features, calculation logic, schema/migrations, SQL execution by Cursor, or GAS business expansion).

---

## Objective

Close **`PASS_WITH_CLEANUP`** follow-ups after live validation of the DB-driven menu registry: gate temporary auth diagnostics, document registry label restoration governance, align naming notes with **EDS Power / EDSPowerCore**, and keep foundation scope stable.

**External audit verdict:** **`PASS_WITH_CLEANUP`**

**Already validated (unchanged by this cleanup):** GAS → Render → Supabase Auth → Supabase registry → Render payload → GAS menu; `menu_source = registry`; HTTP 200; `rendered_items = 3`; visual Supabase label proof (see **`docs/AUDITS/2026-05-07_EDS_POWER_DB_DRIVEN_MENU_FINAL_OPERATOR_VALIDATION.md`**).

---

## Audit verdict

- **Gemini / governance:** **`PASS_WITH_CLEANUP`**
- **This repo slice:** diagnostic env-gate + documentation; **no** auth or menu registry logic changes.

---

## Cleanup scope

| Area | Action |
|------|--------|
| Backend login diagnostics | Env-gated (**default OFF**) |
| Registry menu labels | Documented canonical labels; **operator** restores in Supabase Dashboard if needed — **Cursor did not run SQL** |
| Naming | Canonical product naming **EDS Power / EDSPowerCore**; historical audit quotes may say “Sakura” — see **Naming correction** |
| Tests | Full suite re-run |

---

## Diagnostic cleanup performed

**Prefix:** `EDS_POWER_AUTH_LOGIN_DIAG`

**Gate:** `main._auth_login_diag_enabled()` → **`_truthy_env("EDS_POWER_AUTH_DEBUG_LOGS")`**

- **Default:** variable **missing** or **falsy** → **no** stdout diagnostic lines.
- **Triage only:** set `EDS_POWER_AUTH_DEBUG_LOGS` to `1` / `true` / `yes` / `on` (same semantics as `EDS_MENU_FORCE_MOCK`).

**Documented in:** `docs/AUDITS/2026-05-07_RENDER_SUPABASE_AUTH_PATH_DIAGNOSTIC.md`, `.env.example` (comment only).

**Unchanged:** Auth branches, HTTP bodies, terminal binding, password handling; diagnostics still **never** emit password, `password_hash`, session token, or service role key.

---

## Menu label restoration status

**Cursor / repo:** **No SQL** executed. Restoration is **operator** responsibility in **Supabase Dashboard SQL Editor** (or equivalent) if temporary proof labels (e.g. ВАРІАНТ 1–3) remain after validation.

**Expected canonical labels** (action_key → `menu_label`):

| action_key | Expected menu_label |
|------------|---------------------|
| `REFRESH_MENU` | Оновити меню |
| `SESSION_STATUS` | Перевірити сесію |
| `LOGOUT` | Вийти |
| `MODULE_01_PLACEHOLDER` | Module 01 — Розрахунки (planned) |

**Status token:** **`OPERATOR_RESTORE_GOVERNED`** — confirm in Supabase that registry rows match the table above after cleanup.

---

## Naming correction

- **Canonical** naming for this codebase and terminal stack: **EDS Power**, **EDSPowerCore**, **EDS Power Client Core** (per `docs/00_SYSTEM/02_GLOBAL_RULES.md` and naming audits).
- Some **historical** or **external Gemini** audit excerpts may still say **“Sakura”** in Module 01 or Sheets context. Where those quotes are preserved, interpret as **legacy wording**; **current** system name is **EDS Power** / **EDSPowerCore**, not SakuraCore for this product.

---

## Tests performed

- **Command:** `python -m pytest tests/`
- **Result:** **126 passed** (after diagnostic env-gate; auth/menu tests unchanged).

---

## What was NOT changed

- Auth **behavior** and **response contract**
- Menu registry **resolution** logic (`MenuRegistryService`, `/api/module01/auth/menu`)
- **DB schema**, **migrations**, **GAS** business/menu logic (no new features)
- **Render** production env values (only **`.env.example`** documents optional flag; operators set env explicitly if triage needs logs)
- **Calculation / product** modules — **not** opened

---

## Final cleanup verdict

**`EDS_POWER_DB_DRIVEN_MENU_POST_AUDIT_CLEANUP_COMPLETED`**

**Follow-up:** operator confirms registry labels per **Menu label restoration status**; then **Module 01 calculation planning** only under a future explicit task (not activated by this cleanup).
