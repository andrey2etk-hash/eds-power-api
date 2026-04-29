# NOW

## Поточна мета

Створити системний фундамент EDS Power для подальшої розробки модулів, API, БД, UI та AI-агентів.

## Поточний етап

Stage 3F — Sheet Writeback MVP. 29.04.2026

## Активний сервер

https://eds-power-api.onrender.com

## Активні модулі

1. 00-01_AUTH — авторизація (frozen MVP / draft_ready)
2. 00-02_CALC_CONFIGURATOR — конфігуратор розрахунків (Stage 3E verified with cold-start note)
3. 00-02_CALC_CONFIGURATOR/09_KZO — KZO MVP (Stage 3E verified with cold-start note)

## Що робимо зараз

- Stage 3E = VERIFIED_WITH_COLD_START_NOTE
- Next = Stage 3F — Sheet Writeback MVP
- тримаємо `00-01_AUTH` frozen at MVP
- тримаємо `00-02_CALC_CONFIGURATOR` у межах KZO MVP
- готуємо мінімальний безпечний sheet writeback scope після verified GAS → API handshake
- підтримуємо синхронність GitHub / Cursor / Docs
- Idea Normalizer = ACTIVE GOVERNANCE

## Що не робимо зараз

- не ускладнюємо ролі
- не пишемо великий функціонал
- не реалізуємо всі модулі одразу
- не змінюємо архітектуру без TASK
- не порушуємо data contracts
- не переходимо до full CALC implementation без окремого TASK
- не додаємо Supabase / DB / AUTH / costing / BOM / production logic

## What was completed today (fact)

- Stage 1 closed through Gemini/GPT audit fix pack
- AUTH frozen at MVP scope
- `00_SYSTEM` rules strengthened for contracts, validation layers and lifecycle
- Stage 2 CALC Skeleton governed
- Stage 2B KZO MVP Scope governed
- Audit reports created in `docs/AUDITS/`
- KZO product-specific docs moved under `09_KZO/`
- KZO MVP output summary, option rules and object number gate clarified
- Stage 2E KZO validation foundation approved with fixes
- Stage 3A KZO Calculation Object Contract committed
- Stage 3B API validation skeleton committed
- Stage 3C normalized result summary committed
- Stage 3D GAS API handshake committed
- Stage 3E manual GAS execution verified with Render cold-start observation
- Idea Normalizer foundation created

## What remains next (plan)

- Stage 3F — Sheet Writeback MVP
- define smallest safe sheet writeback scope
- keep GAS thin
- avoid sidebar, buttons, menus, DB, Supabase, AUTH, costing, BOM, and production logic unless separately tasked
