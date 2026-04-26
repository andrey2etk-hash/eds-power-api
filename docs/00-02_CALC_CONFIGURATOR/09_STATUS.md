# Status

## Поточний статус

skeleton_governed

CALC skeleton = governed foundation complete.

Модуль ще не має статусу `draft_ready`.

## Stage 1 foundation

`00-02_CALC_CONFIGURATOR` підготовлений як наступний бізнес-модуль після `00-01_AUTH`.

На Stage 1 дозволено тільки:

- зафіксувати base calculation object
- зафіксувати extensible parameter architecture
- підготувати документаційну основу для Stage 2

## Stage 2 preparation refinement

На Stage 2 preparation зафіксовано:

- `prepare_calculation` як єдиний зовнішній API entry point
- validation, normalization і calculation як внутрішні API етапи
- Calculation Object Lifecycle
- auth/session requirements для protected module flow
- error path без продукт-специфічної логіки

## Governance state

Зафіксовано:

- повний documentation skeleton
- Base Calculation Object
- єдиний зовнішній API entry point `prepare_calculation`
- внутрішні API етапи validation / normalization / calculation
- product-specific documentation rule
- KZO MVP Scope як перший product-specific scope

Для переходу в `draft_ready` ще потрібно:

- Stage 2C — KZO Validation Matrix
- approved TASK
- approved first calculation scenario
- approved product-specific parameter rules

## Що не входить у Stage 1

- реалізація алгоритмів розрахунку
- API endpoints для розрахунків
- таблиці БД для розрахунків
- UI / GAS реалізація
- інтеграція з комерційними пропозиціями або виробництвом
