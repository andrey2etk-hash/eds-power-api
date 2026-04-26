# KZO Questionnaire Logic

## Stage 3A MVP Inputs

This section defines active MVP inputs for KZO Calculation Object V1.

All fields must align with:

- `docs/00-02_CALC_CONFIGURATOR/09_KZO/07_VALIDATION.md`
- `docs/00_SYSTEM/04_DATA_CONTRACTS.md`
- `docs/00_SYSTEM/06_OBJECT_STATUSES.md`

### Required MVP Inputs

- object_number
- product_type
- logic_version
- voltage_class
- busbar_current
- configuration_type
- quantity_total
- cell_distribution
- status

Rules:

- `product_type` must be `KZO`
- `voltage_class` uses machine-safe enum keys from `07_VALIDATION.md`
- `configuration_type` uses machine-safe enum keys from `07_VALIDATION.md`
- `cell_distribution` uses machine-safe cell type keys from `07_VALIDATION.md`
- `status` uses global business object lifecycle statuses

### Optional MVP Inputs

- breaker_type
- notes

Rules:

- `breaker_type` is optional in DRAFT
- `breaker_type` is required in VALIDATED if required by selected cell type
- `notes` must not affect validation or calculation logic

### Deferred Inputs

Future only, not active in MVP:

- operating_current_type
- general equipment preferences
- row_layout
- layout_sequence
- edge cell positions
- busbar bridge required
- bridge type
- distance_between_fronts
- instance-level overrides

Rules:

- deferred inputs must not be required for Stage 3A
- deferred inputs must not block the first KZO API skeleton
- deferred inputs must not create BOM, CAD, production route, supplier, or commercial logic

## Purpose

NON-ACTIVE CONTEXT / FUTURE REFERENCE ONLY

Цей файл описує questionnaire logic для KZO у межах `00-02_CALC_CONFIGURATOR`.

Документ визначає, які питання ставляться на рівні:

- whole assembly / RP
- cell types
- cell quantities
- individual cell instances only when needed

Документ не містить:

- KZO algorithm
- BOM
- CAD
- production routes
- supplier logic
- commercial offer logic
- deep calculation formulas

## Questionnaire principle

Питання ставляться від загального до конкретного:

1. Assembly / RP questions
2. Cell type questions
3. Quantity questions
4. Conditional questions
5. Instance-level questions only when needed

Ціль — не повторювати однакове питання для кожної комірки, якщо відповідь однакова для всієї assembly або cell type group.

## Assembly / RP questions

Assembly-level questions задаються один раз для всієї KZO/RP.

Базові питання:

- voltage_class
- busbar_current
- operating_current_type
- breaker_type
- general equipment preferences
- cabinet_count
- configuration_type
- row_layout

Правила:

- ці питання не повторюються для кожної cell instance
- відповіді застосовуються як common parameters
- якщо відповідь впливає на всі cells, вона має бути assembly-level

## Cell type questions

Cell type questions задаються для кожного вибраного cell type.

Cell types:

- INPUT
- LINE
- TVP
- VT
- SECTION_BREAKER
- SECTION_DISCONNECTOR
- CABLE_ASSEMBLY
- BUS_BRIDGE
- BUS_BRIDGE_WITH_DISCONNECTOR

Базові питання:

- чи використовується цей cell type
- quantity для цього cell type
- чи є type-level preferences

Правила:

- питання ставиться один раз на cell type
- відповідь застосовується до всіх cells цього типу
- individual overrides дозволені тільки коли є відмінність конкретної cell

## Individual cell instance questions

Individual cell instance questions ставляться тільки коли потрібно відрізнити конкретну комірку.

Приклади умов:

- cell має нестандартне розташування
- cell має edge role
- cell має type-specific override
- layout sequence потребує уточнення позиції

Правила:

- не питати однакові параметри для кожної cell, якщо вони вже задані на assembly або cell type level
- instance-level питання не повинні перетворювати анкету на ручний BOM
- instance-level overrides мають бути мінімальними

## Conditional questions

Conditional questions залежать від попередніх відповідей.

Приклади:

- якщо `row_layout = double-row`, запитати `distance_between_fronts`
- якщо потрібен busbar bridge, запитати bridge type
- якщо bridge type має disconnector, використовувати `BUS_BRIDGE_WITH_DISCONNECTOR`
- якщо cell type quantity = 0, не ставити питання по цьому cell type
- якщо всі cells одного типу однакові, не ставити instance-level питання

## Rules to prevent repeated questions

Анкета повинна уникати дублювання.

Правила:

- assembly-level параметри ставляться один раз
- cell type parameters ставляться один раз на type group
- quantity визначає кількість instances без повторення однакових питань
- instance-level questions ставляться тільки для exceptions
- layout sequence може створити instance-level питання тільки для позиційних відмінностей

## Layout-related questions

Layout-related questions потрібні для опису sequence і row layout.

Можливі питання:

- row_layout: single-row / double-row
- layout_sequence
- edge cell positions
- busbar bridge required
- bridge type
- distance_between_fronts для double-row layout

Правила:

- layout questions не є CAD
- layout questions не є production route
- layout questions потрібні для validation matrix

## Edge cell questions

Edge cell questions виникають, якщо layout sequence потребує edge role.

Single-row:

- left edge cell
- right edge cell

Double-row:

- left edge cell for row 1
- right edge cell for row 1
- left edge cell for row 2
- right edge cell for row 2

Правила:

- edge role визначається позицією
- edge role не деталізується до BOM на Stage 2C
- edge differences мають бути validation inputs

## Busbar bridge questions

Busbar bridge questions виникають тільки якщо схема або layout цього потребує.

Можливі питання:

- busbar bridge required
- bridge type
- bridge with disconnector
- distance between fronts

Правила:

- busbar bridge не створює deep calculation на цьому етапі
- busbar bridge не створює production route
- busbar bridge не створює supplier logic

## Stage 2C boundaries

Цей questionnaire logic потрібен для підготовки KZO Validation Matrix.

Дозволено:

- описувати питання
- описувати залежності між відповідями
- описувати rules to prevent repeated questions
- описувати validation inputs

Заборонено:

- створювати KZO algorithm
- створювати BOM
- створювати CAD
- створювати production routes
- створювати commercial offer logic
- створювати supplier logic
