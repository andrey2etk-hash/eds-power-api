# Status

## Поточний статус

planned

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

## Що не входить у Stage 1

- реалізація алгоритмів розрахунку
- API endpoints для розрахунків
- таблиці БД для розрахунків
- UI / GAS реалізація
- інтеграція з комерційними пропозиціями або виробництвом
