# Config

## Base calculation config

Базова структура параметрів:

```json
{
  "parameters": {
    "common": {},
    "product_specific": {},
    "options": {}
  }
}
```

## External API action

На етапі документаційної підготовки CALC має одну зовнішню API дію:

- `prepare_calculation`

Validation, normalization і calculation є внутрішніми API етапами.

GAS не викликає внутрішні етапи окремо.

Реалізація action у коді не входить у цей етап.

## Calculation Object Lifecycle

Для calculation object використовується модульний lifecycle:

- draft
- validated
- error
- calculated
- locked
- archived

Правила:

- `draft` — об’єкт створено або готується
- `validated` — об’єкт пройшов API validation
- `error` — об’єкт має помилку підготовки або розрахунку
- `calculated` — результат розрахунку сформовано
- `locked` — результат зафіксовано і не змінюється без окремої дії
- `archived` — об’єкт більше не активний, але зберігається в історії
- `object_number` може бути порожнім на статусі `draft`

## Conditions for `planned` → `draft_ready`

Модуль може перейти з `planned` у `draft_ready`, коли:

- створено повний documentation skeleton
- `02_INPUTS.md` узгоджений з `04_DATA_CONTRACTS.md`
- `04_OUTPUTS.md` узгоджений з `04_DATA_CONTRACTS.md`
- process flow описаний без продукт-специфічної логіки
- validation responsibility описана
- Base Calculation Object підтверджений
- Stage 2 MVP scope погоджений через TASK

## Заборонено

- додавати продукт-специфічні формули без TASK
- реалізовувати API endpoints на цьому етапі
- створювати таблиці БД без окремого погодження
- змінювати глобальні data contracts з цього модуля
