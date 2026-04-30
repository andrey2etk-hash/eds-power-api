# NOW

## Поточна мета

Створити системний фундамент EDS Power для подальшої розробки модулів, API, БД, UI та AI-агентів.

## Завершено — KZO MVP Stage 5C (факт перевірки, 29.04.2026)

- **Stage 5C** = **VERIFIED**: API `physical_topology_summary` (**Render**) + топологія на Sheet (**`Stage4A_MVP!E21:F26`**, thin GAS — `runStage5CSheetOutputIntegrationFlow()`).
- **IDEA-0010** = `IMPLEMENTED` (master table **Status Values**). Нотатка: Operator Sheet verification PASS 29.04.2026.

## Завершено — KZO Stage 5D Operator Layout Governance (documentation MVP, 29.04.2026)

- **Stage 5D** = **VERIFIED** (documentation MVP — реєстр shell у `docs/00-02_CALC_CONFIGURATOR/09_KZO/10_OPERATOR_LAYOUT.md`).
- **IDEA-0011** = `IMPLEMENTED`. Stage 5D Operator Layout Governance MVP **accepted** після governance verification **PASS WITH DOC FIXES** (doc-pass; без змін API/GAS/Sheet).

## Завершено — KZO Stage 6A Reserved operator block (**VERIFIED** operator, 29.04.2026)

- **Stage 6A** — reserved блок **`E27:F40`**: операторська перевірка **PASS** (активація + ресет + execution log). **`shell_block_version`**: **`KZO_STAGE_6A_OPERATOR_SHELL_V1`**; активація **`shell_status`** **`ACTIVE_RESERVED_BLOCK`**; после ресета в лозі **`RESERVED_DOC_ONLY`**; телеметрія з **`stage6_operator_shell_summary`**. **IDEA-0012** = `IMPLEMENTED`; **`ACTIVE_RESERVED_BLOCK`** / **`RESERVED_DOC_ONLY`** лише стани shell-блоку, не IDEA lifecycle.
- Audit оновлено: `docs/AUDITS/2026-04-29_STAGE_6A_RESERVED_BLOCK_ACTIVATION.md`.

## Завершено — KZO Stage 6B Engineering classification (формальне закриття, 29.04.2026)

- **Stage 6B** = **VERIFIED / IMPLEMENTED / CLOSED** — API **`engineering_class_summary`** (**`interpretation_scope`** **`ENGINEERING_CLASSIFICATION_ONLY_MVP`**) + thin GAS **`E27:F40`** (14-row writeback aligned; writeback mismatch fixed).
- **IDEA-0013** = **`IMPLEMENTED`** (master table only; операторська верифікація та Gemini — лише нотатки аудиту, без нових **Status Values**).
- Операторська верифікація **PASS**; зовнішній аудит Gemini — **`SAFE TO PROCEED TO STAGE 6C`**.
- Audit: `docs/AUDITS/2026-04-29_STAGE_6B_ENGINEERING_CLASSIFICATION.md`.

## Завершено — KZO Stage 7A End-to-end MVP cohesion (**operator verification PASS**, doc-pass, 29.04.2026)

- **`runKzoMvpFlow()`** — manual PASS: **`status`** **`success`**, **`http_code`** **200**, **`mvp_run_outcome`** **`MVP_RUN_SUCCESS`**.
- **`Stage4A_MVP`** — **`E4:F19`** + **`E20:F20`**, **`E21:F26`**, **`E27:F40`**; у **`data`** зафіксовано **`structural_composition_summary`**, **`physical_summary`**, **`physical_topology_summary`**, **`engineering_class_summary`**, **`engineering_burden_summary`**.
- **IDEA-0015** = **`IMPLEMENTED`**; аудит **`2026-04-29_STAGE_7A_KZO_END_TO_END_MVP_STABILIZATION.md`** доповнено operator PASS (**без нової інженерної логіки в GAS**).

## Завершено — KZO Stage 7B MVP snapshot contract freeze (**Gemini PASS**, formal closure, 29.04.2026)

- **`KZO_MVP_SNAPSHOT_V1`** frozen — `docs/00-02_CALC_CONFIGURATOR/09_KZO/11_KZO_MVP_SNAPSHOT_V1_CONTRACT.md` (verified layers: **`structural_composition_summary`**, **`physical_summary`**, **`physical_topology_summary`**, **`engineering_class_summary`**, **`engineering_burden_summary`**; SUCCESS/FAILED envelopes; **`snapshot_version`** + **`logic_version`** policy).
- Audit **`2026-04-29_STAGE_7B_KZO_MVP_SNAPSHOT_CONTRACT_FREEZE.md`** — external Gemini **`SAFE TO PROCEED TO STAGE 8A`**; Stage **7B** **CLOSED**; **`IDEA-0016`** **`IMPLEMENTED`** (unchanged Status Values).

## Stage 8A — код implementation (insert-only, 29.04.2026)

- **`POST /api/kzo/save_snapshot`** у репозиторії (`kzo_snapshot_persist.py`; DDL **`supabase/migrations/_pending_after_remote_baseline/20260429120000_calculation_snapshots_v1.sql`** — **hold** до replay PASS; baseline **`20260429110000`** — **фактичний DDL імпортовано** (**8A.0.6** **`REAL_BASELINE_CAPTURED_PENDING_REPLAY`**)). **`TABLE=SYSTEM`**/**`ROW=PRODUCT`** — **8A.0.1**/**8A.0.2**. **`prepare_calculation`** без змін.
- Thin GAS **`saveKzoSnapshotV1()`** — лише транспорт JSON.
- Аудит імплементації: **`2026-04-29_STAGE_8A_SUPABASE_FIRST_PERSISTENCE_MVP.md`**; mapping **`13_KZO_MVP_SNAPSHOT_V1_SQL_MAPPING.md`**.

## Активний gate — Stage 8A Supabase (**8A.0.7** replay **BLOCKED_BY_DOCKER**)

- **8A.0.7:** локальний **`supabase db reset`** — **не виконано**: **немає** Docker / Supabase CLI на PATH у агент-сесії. Статус: **`BLOCKED_BY_DOCKER`** — **`docs/AUDITS/2026-04-29_STAGE_8A_0_7_BASELINE_REPLAY_VERIFICATION.md`**. **`calculation_snapshots`** — **лише** **`_pending_after_remote_baseline/`**; **не переносити** до **8A.0.8**. Ціль **`BASELINE_REPLAY_VERIFIED`** — після replay на машині оператора або disposable DB.
- **8A.0.6:** baseline DDL у **`20260429110000_remote_legacy_baseline.sql`** — **DONE** (**`REAL_BASELINE_CAPTURED_PENDING_REPLAY`**). Аудит **`docs/AUDITS/2026-04-29_STAGE_8A_0_6_ACTUAL_REMOTE_BASELINE_CAPTURE.md`**.
- **8A.0.5:** tooling precheck — **`docs/AUDITS/2026-04-29_STAGE_8A_0_5_LOCAL_TOOLING_PRECHECK.md`**.
- **8A.0.3 (ordering):** файл **`supabase/migrations/20260429110000_remote_legacy_baseline.sql`** у root (**порядок \<** hold **`20260429120000_calculation_snapshots_v1.sql`**); тепер містить **фактичний** DDL (**8A.0.6**). **`LEGACY_REMOTE_BASELINE.md`** freeze залишається доки replay не **`PASS`** — аудити **8A.0.3**/**8A.0.6**.
- **8A.0.2 (governance, closed):** remote **`public`** не порожній — **`LEGACY_REMOTE_SCHEMA_DETECTED`**; **`IDEA-0020`** **`IMPLEMENTED`**.
- **Live gate:** `docs/AUDITS/2026-04-29_STAGE_8A_SUPABASE_LIVE_VERIFICATION_GATE.md` — після baseline: застосувати міграції, env на Render, redeploy, **POST** живий → рядок у **`calculation_snapshots`** (`product_type` = **`KZO`**).
- Automated probe **`eds-power-api.onrender.com`** (2026-04-29): **`404`** на **`/api/kzo/save_snapshot`** → **live PASS ще не зафіксований** (ймовірно stale deploy без Stage 8A route або інший сервіс).
- **IDEA-0017** = **`ACTIVE`** (**operative:** **`PENDING_SUPABASE_VERIFICATION`**) до запису **LIVE PASS** у live gate аудиті → тоді **`IMPLEMENTED`**.

## Поточний етап і наступний gate

- Після **LIVE PASS** Stage 8A: **IDEA-0017** → **`IMPLEMENTED`**; окремий **IDEA/TASK** на retrieval / історію UI / analytics (поза **8A** verification scope).

## Як узгоджено з Gemini doc-pass (Зовнішній аудит)

- Gemini Stage 5C Sheet operator verification: **`PASS WITH DOC FIXES`** → застосовано лише синхронізація доків (без змін API/GAS). Використано статус IDEA **`IMPLEMENTED`**, без нових міток у master table beyond `Status Values`.
- Stage 6B external Gemini audits: **`SAFE TO PROCEED TO STAGE 6C`** — **Stage 6C** (**`IDEA-0014`**) потім закритий імплементацією `engineering_burden_summary`.
- Stage **7B** snapshot contract — external Gemini **`SAFE TO PROCEED TO STAGE 8A`**; **`KZO_MVP_SNAPSHOT_V1`** frozen (**`IDEA-0016`** **`IMPLEMENTED`**). Stage **8A** code shipped; **live Supabase verification** — **`ACTIVE`** (**`IDEA-0017`**, **`PENDING_SUPABASE_VERIFICATION`** до live PASS).

https://eds-power-api.onrender.com

## Активні модулі

1. 00-01_AUTH — авторизація (frozen MVP / draft_ready)
2. 00-02_CALC_CONFIGURATOR — конфігуратор (KZO Stage 5A–5C operator-visible path для structural / footprint API / topology API + топологія на Sheet верифіковані)
3. 00-02_CALC_CONFIGURATOR/09_KZO — KZO MVP (**7A/** **7B** **`IMPLEMENTED`**; **8A** persistence code + **live gate OPEN** — **`IDEA-0017`** **`ACTIVE`** / **`PENDING_SUPABASE_VERIFICATION`** until live PASS; retrieval/history/analytics — окремий IDEA)

## Що робимо зараз

- Stage 3E = VERIFIED_WITH_COLD_START_NOTE
- Stage 3F = VERIFIED
- Stage 4A = VERIFIED_MVP_ONLY
- Stage 4B = VERIFIED_STRUCTURAL_PREFLIGHT
- Stage 4C = VERIFIED_OPERATOR_SHELL
- Stage 5A-Output-Integration = `VERIFIED_OPERATOR_VISIBLE`
- Stage 5B `physical_summary` = `VERIFIED_RENDER_PENDING_OPERATOR_VISIBLE_INTEGRATION` on live Render (Stage 5B Render gate)
- тримаємо `00-01_AUTH` frozen at MVP
- тримаємо `00-02_CALC_CONFIGURATOR` у межах KZO MVP поки нема окремого TASK на розширення
- підтримуємо синхронність GitHub / Cursor / Docs
- Idea Normalizer = ACTIVE GOVERNANCE

## Що не робимо зараз

- не ускладнюємо ролі
- не пишемо великий функціонал
- не реалізуємо всі модулі одразу
- не змінюємо архітектуру без TASK
- не порушуємо data contracts
- не переходимо до full CALC implementation без окремого TASK
- не додаємо Supabase/DB/AUTH без окремого TASK; retrieval/history/dashboard — те саме
- не додаємо BOM / costing / expansion до live gate (**live PASS** оператор робить лише перевірку по **`docs/AUDITS/2026-04-29_STAGE_8A_SUPABASE_LIVE_VERIFICATION_GATE.md`**, без нової продукт-логіки)

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
- Stage 5C physical topology MVP verified on deployed Render (`data.physical_topology_summary` checklist PASS per Stage 5C Render gate audit)
- Stage 5C operator-visible topology on Sheet verified via thin GAS (`runStage5CSheetOutputIntegrationFlow()`; **`E21:F26`**; Gemini Sheet audit PASS WITH DOC FIXES → doc-sync)
- Stage 5D operator layout governance documentation MVP closed (verification gate PASS WITH DOC FIXES → doc-pass; **IDEA-0011** = `IMPLEMENTED`)
- Stage 6A reserved block **`E27:F40`** — GAS activation + **operator verification PASS** 29.04.2026 (doc-pass sync) (**IDEA-0012** `IMPLEMENTED`; audit `docs/AUDITS/2026-04-29_STAGE_6A_RESERVED_BLOCK_ACTIVATION.md`)
- Stage 6B **closed** — operator verification PASS + Gemini **`SAFE TO PROCEED TO STAGE 6C`**; formal doc-pass (**IDEA-0013** `IMPLEMENTED`; audit `docs/AUDITS/2026-04-29_STAGE_6B_ENGINEERING_CLASSIFICATION.md`)
- Stage 6C Render + **`runStage6CEngineeringBurdenFlow()`** operator **PASS** (**IDEA-0014** **`IMPLEMENTED`**; **`2026-04-29_STAGE_6C_ENGINEERING_BURDEN_RENDER_GATE.md`**)
- Stage 7A **`runKzoMvpFlow()`** manual operator **PASS** — **`mvp_run_outcome`** **`MVP_RUN_SUCCESS`**, **`http_code`** **200**, zones **`E4:F19`/`E20:F20`**, **`E21:F26`**, **`E27:F40`**, summaries present (**IDEA-0015** **`IMPLEMENTED`**; doc-pass **`2026-04-29_STAGE_7A_KZO_END_TO_END_MVP_STABILIZATION.md`**)
- Stage **7B** **`KZO_MVP_SNAPSHOT_V1`** — formal closure (**Gemini** **`SAFE TO PROCEED TO STAGE 8A`**; **`2026-04-29_STAGE_7B_KZO_MVP_SNAPSHOT_CONTRACT_FREEZE.md`** updated; **`IDEA-0016`** **`IMPLEMENTED`**)

## What remains next (plan)

- **Stage 8A.0.2 technical follow-up (operator):** import/generate **baseline** migrations for remote legacy **`public`** (see **`supabase/schema_registry/LEGACY_REMOTE_BASELINE.md`**, audit **`2026-04-29_STAGE_8A_0_2_SUPABASE_REMOTE_BASELINE_ALIGNMENT.md`**) → **then** restore **`calculation_snapshots`** DDL from **`_pending_after_remote_baseline/`** into **`migrations/`** before any **`db push`**
- **Stage 8A live gate** — **`docs/AUDITS/2026-04-29_STAGE_8A_SUPABASE_LIVE_VERIFICATION_GATE.md`**: after baseline, apply migrations, env on Render, redeploy, **`POST /api/kzo/save_snapshot`**, verify row — then **`IDEA-0017`** → **`IMPLEMENTED`**
- keep Stage narrow: no BOM, pricing, retrieval dashboard, or unmanaged Sheet expansion unless separately tasked
- keep GAS thin on future operator-visible transports
