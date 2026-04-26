# KZO Data Model

## Purpose

Цей файл описує KZO як ієрархічну product-specific модель для `00-02_CALC_CONFIGURATOR`.

Документ є частиною Stage 2C preparation і не містить:

- BOM
- CAD
- production routes
- supplier logic
- commercial offer logic
- deep calculation formulas

## Model hierarchy

KZO model складається з рівнів:

1. Assembly / RP level
2. Cell type level
3. Cell quantity level
4. Cell instance level
5. Layout sequence level
6. Row layout level
7. Edge cell rules
8. Busbar bridge rules

## Assembly-level parameters

Assembly-level parameters застосовуються до всієї KZO/RP збірки.

Базові параметри:

- voltage_class
- busbar_current
- operating_current_type
- breaker_type
- general equipment preferences
- cabinet_count
- configuration_type

Правила:

- ці параметри не повторюються для кожної cell instance
- ці параметри використовуються як common parameters
- зміна assembly-level параметра впливає на всі залежні cell groups

## Cell types

KZO може містити такі cell types:

- INPUT
- LINE
- TVP
- VT
- SECTION_BREAKER
- SECTION_DISCONNECTOR
- CABLE_ASSEMBLY
- BUS_BRIDGE
- BUS_BRIDGE_WITH_DISCONNECTOR

## Cell quantities

Кожен cell type може мати quantity.

Приклад:

- INPUT: 2
- LINE: 12
- VT: 2
- SECTION_BREAKER: 1

Правила:

- quantity описує кількість cells певного типу
- quantity не описує BOM
- quantity не створює production route
- сумарна кількість cells має відповідати cabinet_count або бути перевірена validation matrix

## Cell instances

Cell instance — це конкретна комірка в layout sequence.

Cell instance може мати:

- instance_id
- cell_type
- position_index
- row_id
- edge_role
- type_specific_overrides

Правила:

- instance-level параметри задаються тільки коли конкретна cell відрізняється від group defaults
- не можна дублювати однакові питання для всіх однотипних cells без потреби
- instance-level overrides не повинні перетворюватись на deep algorithm

## Layout sequence

Layout sequence визначає порядок комірок.

Базові правила:

- кожна cell instance має позицію
- порядок комірок важливий для mechanical interpretation
- left edge і right edge cells мають різні механічні ролі
- layout sequence не є CAD layout
- layout sequence не є production route

## Row layout

KZO може мати:

- single-row layout
- double-row layout

Single-row system:

- має 2 edge cells
- має left edge cell
- має right edge cell

Double-row system:

- може мати 4 edge cells
- має edge cells для кожного row
- може потребувати distance between fronts
- може потребувати busbar bridge rules

## Edge cell rules

Edge cell rules описують позиційну роль комірок на краях ряду.

Базові edge roles:

- LEFT_EDGE
- RIGHT_EDGE
- INNER

Правила:

- left edge і right edge cells відрізняються механічно
- edge role визначається з layout sequence
- edge role не повинен задавати BOM напряму
- edge role може впливати на validation_state

## Busbar bridge rules

Busbar bridge може бути потрібен для double-row layout або спеціальної схеми.

Базові типи:

- BUS_BRIDGE
- BUS_BRIDGE_WITH_DISCONNECTOR

Правила:

- busbar bridge описується як cell type або layout requirement
- busbar bridge не створює production route
- busbar bridge не деталізується до BOM на Stage 2C
- для double-row layout може знадобитись distance_between_fronts

## Stage 2C boundaries

Цей data model потрібен для KZO Validation Matrix.

Дозволено:

- описувати hierarchical model
- описувати cell types
- описувати layout concepts
- описувати validation inputs

Заборонено:

- створювати KZO algorithm
- створювати BOM
- створювати CAD model
- створювати production route
- створювати supplier logic
- створювати commercial logic
