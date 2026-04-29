# GEMINI STAGE 5C — Sheet Operator Verification (External Audit Request)

**Призначення.** Цей документ є **промптом для зовнішнього аудитора Gemini**. Не аудит Gemini стосовно себе самого — він описує роботу Gemini як **сторонній критик** щодо тонкого інтеграційного прошарку (**thin GAS → Sheet**) після **ручного PASS** операторської перевірки.

**Строго:** Gemini **не впроваджує** логіку, не редагує репозиторій, лише аналізує наданий контекст і відповіді на аудиторські запитання нижче.

---

## Контекст виконання (факт із ручного тесту)

- Виконано **`runStage5CSheetOutputIntegrationFlow()`** у Apps Script.
- Execution log містить принаймні:
  - `stage` = `5C_SHEET_OUTPUT_INTEGRATION`
  - `telemetry_tag` = `stage=5C-sheet-output-integration`
  - `http_code` = `200`
  - upstream `status` = `success` (за логами пакета відповіді)
  - `physical_topology_summary_present` = `true`
  - writeback completed на **`Stage4A_MVP!E21:F26`**
- **Етап API/Render Stage 5C** уже був верифікований раніше (окремий Render gate аудит).

---

## Пререквізити (що Gemini має перевірити)

1. Stage 5C **API** уже віддає `data.physical_topology_summary` на live Render (**не тема цього аудиту**, але умова смислової повноти).
2. На листі очікується **адитивний** блок **E21:F26**, без перерозкладки всього операторського Shell.

---

## Файли для ревью (перелік)

Переглянути лише узгодженість **governance** і поведінки **GAS** (без альтернативної архітектури):

| Шлях | Навіщо |
|------|--------|
| `gas/Stage3D_KZO_Handshake.gs` | функції Stage 5C Sheet output: запуск API, парсинг, writeback **`E21:F26`** |
| `docs/AUDITS/2026-04-29_STAGE_5C_SHEET_OUTPUT_INTEGRATION.md` | задокументовані межі та очікувана поведінка |
| `docs/00_SYSTEM/12_IDEA_MASTER_LOG.md` | **IDEA-0010** та статуси життєвого циклу |
| `docs/CHANGELOG.md` | зафіксовані зміни Stage 5C (API Render + Sheet thin GAS) |
| `docs/NOW.md` | поточний зріз статусів (можуть бути неконсистентні з IDEA після операторського PASS — це перевірити) |
| `docs/00-02_CALC_CONFIGURATOR/09_STATUS.md` | модульний статус |
| `docs/00-02_CALC_CONFIGURATOR/09_KZO/08_STATUS.md` | KZO-локальний статус |

---

## Контекстові питання (обовʼязково відповісти Gemini)

**A. Thin client / мапінг**

1. Чи залишається **GAS thin client** щодо Stage 5C (немає бізнес-топології в скрипті)?
2. Чи виконується лише **мапінг** полів з `responseJson.data.physical_topology_summary` у клітинки (**без альтернативних формул/підрахунків топології**)?
3. Чи містить код **розрахунок/інтеренцію топології** поза простим **`JSON.stringify`** для відображення масиву (**display-only** допустимий)?

**B. Безпека writeback**

4. Чи **адитивний** і безпечний writeback **`E21:F26`** щодо існуючих зон Stage 5A (**`E4:F19`**, **`E20:F20`**) згідно з описом в аудиті?

**C. Operator-visible closure**

5. Чи з цього погляду **операційно замкнуто** operator-visible інтеграцію Stage 5C (API truth + операторська видимість на Sheet через тонкий GAS), навіть якщо залишаються **інші майбутні TASK** поза межами топології?

**D. IDEA-0010 → «VERIFIED_COMPLETE»**

6. Ставка столбця **Status** у master table IDEA підтримує значення типу **`IMPLEMENTED`** / **`RENORMALIZED`** (див. `12_IDEA_MASTER_LOG.md` — блок **Status Values**). Строк **`VERIFIED_COMPLETE`** у цьому переліку **може відсутні**. Чи доречно:
   - залишити **окремий** governance-ярлик операторської верифікації в нотах IDEA (**наприклад** оператор **`OPERATOR_VISIBLE_VERIFIED`** / **`VERIFIED_OPERATOR_SHEET`**), або
   - підняти **IDEA-0010** до **`IMPLEMENTED`** після узгодження всієї док-довідності,
   - або **узгодити** лише текст у `NOW`/status файлах **без** вигадування нової метки в master table без TASK на governance?

Gemini має явно висловити **найбезризиковіше** узгодження з огляду на файл master log.

**E. Консистентність доків**

7. Перевірити **протиріччя** між: `NOW.md`, `CHANGELOG.md`, `09_STATUS.md`, `09_KZO/08_STATUS.md`, `12_IDEA_MASTER_LOG.md`, зокрема там, де **Render-verified API** описаний паралельно з **operator Sheet pending** або навпаки.
8. Після узгодження документів через **«doc-fix мінімум»** чи є **безпечно** переходити далі лише док-пасом (**без** зміни коду в цьому аудиті)?

---

## Спостереження для Gemini (можлива перевірочна точка для Q7)

На момент підготовки цього запиту **`NOW.md`** згадує **IDEA-0010** у контексті **Render-verified API**, а **master table** IDEA-0010 може тримати **`OPERATOR_VISIBLE_INTEGRATION_PENDING_TEST`**. Якщо ручний Sheet PASS підтверджено логами/скрином — Gemini має перевірити, чи потрібен **мінімальний doc-pass** синхронізації (без зміни кодової логіки).

---

## Вимога до формату відповіді Gemini

Повернути відповідь **строго** з нижченаведеною структурою заголовків:

```markdown
# GEMINI STAGE 5C SHEET OPERATOR VERIFICATION AUDIT

## PASS ITEMS

## RISKS

## DOC FIXES REQUIRED

## GOVERNANCE STATUS

## FINAL VERDICT

PASS / PASS WITH DOC FIXES / FAIL
```

**Примітка про вердикт**

- **PASS** — thin GAS відповідає governance, блок E21:F26 адитивний, доки можна синхронізувати косметично або вже узгоджені.
- **PASS WITH DOC FIXES** — код GAS ок, але **NOW/IDEA/status** потребує явного вирівнювання текстів (перелік!).
- **FAIL** — є ознаки **інтерпретації топології в GAS**, небезпечний конфлікт діапазонів або суттєве порушення governance.

---

## Заборона для аудитора (нема робити під час аудиту)

- не пропонувати нову логіку топології в API
- не переписувати Sheet layout
- не вимагати розширення GAS понад транспорт/відображення
- не вимагати BOM / CAD / вагу / прайсинг

---

_End of Gemini audit request._
