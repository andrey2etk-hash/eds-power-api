# NOW

## Поточна мета

Створити системний фундамент EDS Power для подальшої розробки модулів, API, БД, UI та AI-агентів.

## Поточний етап

Stage 4A — Google Sheet Core Template Protection. 29.04.2026

## Активний сервер

https://eds-power-api.onrender.com

## Активні модулі

1. 00-01_AUTH — авторизація (frozen MVP / draft_ready)
2. 00-02_CALC_CONFIGURATOR — конфігуратор розрахунків (Stage 4A verified MVP only)
3. 00-02_CALC_CONFIGURATOR/09_KZO — KZO MVP (Stage 4A verified MVP only)

## Що робимо зараз

- Stage 3E = VERIFIED_WITH_COLD_START_NOTE
- Stage 3F = VERIFIED
- Stage 4A = VERIFIED_MVP_ONLY
- тримаємо `00-01_AUTH` frozen at MVP
- тримаємо `00-02_CALC_CONFIGURATOR` у межах KZO MVP
- готуємо наступний етап тільки через окрему normalized task
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
- Stage 3F Sheet Writeback MVP verified
- Stage 4A protected template shell verified as MVP-only baseline
- Idea Normalizer foundation created

## What remains next (plan)

- define next stage only through Idea Normalizer
- keep Stage 4A as protected MVP shell baseline
- keep GAS thin
- avoid sidebar, buttons, menus, DB, Supabase, AUTH, costing, BOM, and production logic unless separately tasked
