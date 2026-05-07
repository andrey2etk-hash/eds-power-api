# Module 01 — Create Calculation Modal Submit UX + Duplicate Guard

## Objective

Fix live issue: після успішного **Створити** записи в Supabase з’являлись, але модалка візуально лишалась у стані форми / без явного успіху, що провокувало повторні кліки й дублікати.

## Root cause

1. **Приватний виклик з HTML після успіху:** у `onSubmitResult` викликався `google.script.run.module01CreateCalculationRememberActiveId_(...)`. Як і з bootstrap, **функції з суфіксом `_` не призначені для `google.script.run` з HtmlService** — виклик міг **переривати success handler до `showOk` / приховування форми**, тож UI не оновлювався попри успіх API.
2. **UX:** не було окремого тексту завантаження під час сабміту, явної панелі успіху та кнопки **«Закрити»**; після помилкових гілок submit інколи одразу вмикався знову.

## Response shape (unchanged contract)

- **GAS `module01CreateCalculationSubmit`** повертає:
  - успіх транспорту: `{ ok: true, http_status, envelope }`, де `envelope` — тіло JSON API (`status`, `data`, `error`, `metadata`);
  - помилка мережі/парсингу: `{ ok: false, message, ... }`.
- **HTML** очікує успіх операції: `res.ok === true`, `envelope.status === "success"`, `envelope.data.calculation` — об’єкт з `calculation_id`, `calculation_display_number`, `status`, `product_type` (як у `module01_calculations_service.py`).

Несумління формату envelope з бекенду не виявлено; проблема була в **клієнтському GAS/HTML** після успіху.

## Fix summary

| Area | Change |
|------|--------|
| `Module01CreateCalculationModal.gs` | Публічний **`module01CreateCalculationRememberActiveId`** → делегує в `_`. |
| `Module01CreateCalculationModalHtml.html` | Пам’ять активного id через **публічну** функцію; **submitInFlight**; під час сабміту — **«Створюємо розрахунок...»**, блок **Скасувати**; панель успіху **«Розрахунок створено»** + номер, статус, KZO + підказка про sidebar + **«Закрити»**; без авто-close; при некоректній відповіді — **залишити submit вимкненим**, щоб уникнути сліпих повторів. |

## Duplicate guard

- Повторний клік **Створити** ігнорується, поки `submitInFlight`.
- У разі успіху **Створити** лишається disabled; закриття лише через **Закрити**.
- **Скасувати** заблокований під час запиту.

## Scope confirmation

- **Немає** змін БД, SQL, міграцій, registry, бекенду, продуктової / KZO / engine логіки.

## Verdict

**`MODULE_01_CREATE_CALCULATION_MODAL_SUBMIT_UX_FIX_IMPLEMENTED`** — оператору: оновити GAS з репозиторію та перевірити один успішний create + один навмисний другий клік (має не створювати дубль).
