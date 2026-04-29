# NOW

## Поточна мета

Створити системний фундамент EDS Power для подальшої розробки модулів, API, БД, UI та AI-агентів.

## Поточний етап

Stage 5B — Physical Footprint MVP (`VERIFIED_RENDER_PENDING_OPERATOR_VISIBLE_INTEGRATION` on Render). 29.04.2026

## Stage 5B snapshot

- IDEA-0009 = `VERIFIED_RENDER_PENDING_OPERATOR_VISIBLE_INTEGRATION` (live Render returned `physical_summary`; audit `docs/AUDITS/2026-04-29_STAGE_5B_PHYSICAL_FOOTPRINT_RENDER_GATE.md`)
- Operator-visible Sheet wiring for `physical_summary` remains **out-of-scope** for Stage 5B Render gate unless separately tasked

## Активний сервер

https://eds-power-api.onrender.com

## Активні модулі

1. 00-01_AUTH — авторизація (frozen MVP / draft_ready)
2. 00-02_CALC_CONFIGURATOR — конфігуратор (Stage 5B `physical_summary` verified on Render)
3. 00-02_CALC_CONFIGURATOR/09_KZO — KZO MVP (Stage 5B footprint summary on API)

## Що робимо зараз

- Stage 3E = VERIFIED_WITH_COLD_START_NOTE
- Stage 3F = VERIFIED
- Stage 4A = VERIFIED_MVP_ONLY
- Stage 4B = VERIFIED_STRUCTURAL_PREFLIGHT
- Stage 4C = VERIFIED_OPERATOR_SHELL
- Stage 5A-Output-Integration = `VERIFIED_OPERATOR_VISIBLE`
- Stage 5B `physical_summary` = `VERIFIED_RENDER_PENDING_OPERATOR_VISIBLE_INTEGRATION` on live Render (`https://eds-power-api.onrender.com` checklist in Stage 5B Render gate audit)
- тримаємо `00-01_AUTH` frozen at MVP
- тримаємо `00-02_CALC_CONFIGURATOR` у межах KZO MVP
- утримуємо Stage 5A як узгоджену базу виконання (API meaning + операторський writeback без розширення GAS)
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
- Stage 4B structural preflight verified
- Stage 4C operator shell verified manually; warm run confirmed no cold start blocker
- Stage 5A structural composition verified on deployed Render API
- Stage 5A output integration verified in operator Sheet (`runStage5AOutputIntegrationFlow()`)
- Stage 5B physical footprint MVP verified on deployed Render (`data.physical_summary` checklist PASS per Render gate audit)

## What remains next (plan)

- keep Stage 5A narrow: no design, BOM, pricing, DB, GAS logic, or Sheet redesign
- keep GAS thin
- avoid sidebar, buttons, menus, DB, Supabase, AUTH, costing, BOM, and production logic unless separately tasked
