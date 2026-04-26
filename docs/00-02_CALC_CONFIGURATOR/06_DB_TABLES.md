# DB Tables

## Stage 2 preparation

Таблиці БД для `00-02_CALC_CONFIGURATOR` ще не затверджені.

На цьому етапі фіксується тільки потреба зберігати базовий об’єкт розрахунку після погодження MVP scope.

## Candidate data object

Майбутня таблиця або набір таблиць мають базуватись на Base Calculation Object:

- `calculation_id`
- `version`
- `object_number`
- `product_type`
- `status`
- `parameters`
- `result`
- `created_at`
- `updated_at`

## Правила

- структура БД не реалізується на цьому етапі
- таблиці створюються тільки після окремого TASK
- структура БД має відповідати `04_DATA_CONTRACTS.md`
- статуси бізнес-об’єкта мають відповідати `02_GLOBAL_RULES.md`
- `object_number` може бути порожнім на статусі `draft`
- продукт-специфічні поля не додаються без окремої документації
