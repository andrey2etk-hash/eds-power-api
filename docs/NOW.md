# NOW

## Поточна мета

Створити системний фундамент EDS Power для подальшої розробки модулів, API, БД, UI та AI-агентів.

## Поточний етап

Stage 5B — Physical Footprint MVP (Render verification gate active). 29.04.2026

## Stage 5B snapshot

- IDEA-0009 = `DEPLOYMENT_CANDIDATE_PENDING_RENDER_VERIFICATION` until live Render exposes `data.physical_summary`
- Successful live checklist → `VERIFIED_RENDER_PENDING_OPERATOR_VISIBLE_INTEGRATION` (audit: `docs/AUDITS/2026-04-29_STAGE_5B_PHYSICAL_FOOTPRINT_RENDER_GATE.md`)
- Operator-visible Sheet integration for `physical_summary` = separate optional task — not verified by Render gate alone

## Активний сервер

https://eds-power-api.onrender.com

## Активні модулі

1. 00-01_AUTH — авторизація (frozen MVP / draft_ready)
2. 00-02_CALC_CONFIGURATOR — конфігуратор (Stage 5B deployment candidate; pending live Render `physical_summary`)
3. 00-02_CALC_CONFIGURATOR/09_KZO — KZO MVP (Stage 5B Render gate)

## Що робимо зараз

- Stage 3E = VERIFIED_WITH_COLD_START_NOTE
- Stage 3F = VERIFIED
- Stage 4A = VERIFIED_MVP_ONLY
- Stage 4B = VERIFIED_STRUCTURAL_PREFLIGHT
- Stage 4C = VERIFIED_OPERATOR_SHELL
- Stage 5A-Output-Integration = `VERIFIED_OPERATOR_VISIBLE`
- Stage 5B `physical_summary` = `DEPLOYMENT_CANDIDATE_PENDING_RENDER_VERIFICATION` (push to GitHub → Render deploy → `POST /api/calc/prepare_calculation` checklist in Stage 5B Render gate audit)
- після проходження live checklist: `VERIFIED_RENDER_PENDING_OPERATOR_VISIBLE_INTEGRATION` — без змін GAS/Sheet у межах цього gate
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
- Stage 5B physical footprint MVP implemented in API locally; Render verification gate documented (`docs/AUDITS/2026-04-29_STAGE_5B_PHYSICAL_FOOTPRINT_RENDER_GATE.md`); `IDEA-0009` = `DEPLOYMENT_CANDIDATE_PENDING_RENDER_VERIFICATION` until live checklist passes

## What remains next (plan)

- run Stage 5B live Render checklist (`POST /api/calc/prepare_calculation`) after GitHub → Render deploy; then move `IDEA-0009` to `VERIFIED_RENDER_PENDING_OPERATOR_VISIBLE_INTEGRATION` per audit
- keep Stage 5A narrow: no design, BOM, pricing, DB, GAS logic, or Sheet redesign
- keep GAS thin
- avoid sidebar, buttons, menus, DB, Supabase, AUTH, costing, BOM, and production logic unless separately tasked
