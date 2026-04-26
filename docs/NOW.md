# NOW

## Поточна мета

Створити системний фундамент EDS Power для подальшої розробки модулів, API, БД, UI та AI-агентів.

## Поточний етап

Stage 2C — KZO Validation Matrix. 26.04.2026

## Активний сервер

https://eds-power-api.onrender.com

## Активні модулі

1. 00-01_AUTH — авторизація (frozen MVP / draft_ready)
2. 00-02_CALC_CONFIGURATOR — конфігуратор розрахунків (skeleton_governed)
3. 00-02_CALC_CONFIGURATOR/09_KZO — KZO MVP Scope (scope_governed)

## Що робимо зараз

- готуємо Stage 2C — KZO Validation Matrix
- тримаємо `00-01_AUTH` frozen at MVP
- ведемо `00-02_CALC_CONFIGURATOR` через governed skeleton
- ведемо KZO тільки як MVP scope
- підтримуємо синхронність GitHub / Cursor / Docs

## Що не робимо зараз

- не ускладнюємо ролі
- не пишемо великий функціонал
- не реалізуємо всі модулі одразу
- не змінюємо архітектуру без TASK
- не порушуємо data contracts
- не переходимо до full CALC implementation без validation matrix і TASK

## What was completed today (fact)

- Stage 1 closed through Gemini/GPT audit fix pack
- AUTH frozen at MVP scope
- `00_SYSTEM` rules strengthened for contracts, validation layers and lifecycle
- Stage 2 CALC Skeleton governed
- Stage 2B KZO MVP Scope governed
- Audit reports created in `docs/AUDITS/`
- KZO product-specific docs moved under `09_KZO/`
- KZO MVP output summary, option rules and object number gate clarified

## What remains next (plan)

- Stage 2C — KZO Validation Matrix
- approve predefined `option_ids`
- approve allowed `voltage_class` values
- approve allowed `configuration_type` values
- define first KZO calculation scenario
- prepare TASK before moving toward `draft_ready`
