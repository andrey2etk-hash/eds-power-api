# KZO MVP Scope

## Status

APPROVED_WITH_FIXES

KZO MVP Scope governed.

Цей scope ще не має статусу `draft_ready`.

## Goal

Визначити перший MVP product для `00-02_CALC_CONFIGURATOR` як `KZO`.

Цей файл описує тільки MVP scope для підготовки першого продукт-специфічного розрахунку.

## Mandatory parameters

Обов’язкові параметри MVP:

- product_type: `KZO`
- voltage_class
- busbar_current
- configuration_type
- quantity_total
- cell_distribution

Правило:

- quantity_total = cabinet units
- sum(cell_distribution) == quantity_total

## Optional parameters

Опціональні параметри MVP:

- object_number
- notes
- option_ids
- breaker_type

Правило:

- `object_number` — optional at draft stage, required before final / production transition
- `option_ids` — predefined option IDs only, no open text
- `breaker_type` — optional in draft, required in validated state when required by selected cell type

## Validation rules

- invalid `voltage_class` + `configuration_type` combinations must return `validation_error`

## Excluded scope

У MVP не входить:

- deep BOM
- CAD
- production routes
- supplier complexity
- детальна логіка комплектації
- автоматичний підбір постачальників
- розрахунок виробничого маршруту
- генерація комерційної пропозиції

## Expected outputs

Очікувані MVP outputs:

- calculation_id
- product_type
- object_number
- status
- normalized_parameters
- result_summary_version = KZO_MVP_V1
- result_summary:
  - configuration_type
  - estimated_dimensions_mm
  - main_equipment_class
  - estimated_cost_base
  - validation_state
- validation_errors, якщо є помилки

## First Approved MVP Scenario

Object:

7445-В

Parameters:

- voltage_class: VC_10 = 10kV
- configuration_type: CFG_SINGLE_BUS_SECTION = Single bus with section
- quantity_total: 22
- CELL_INCOMER: 2
- CELL_OUTGOING: 16
- CELL_PT: 2
- CELL_BUS_SECTION: 2

Purpose:

This scenario becomes baseline for first end-to-end validation and first API implementation.

## Stage alignment

KZO MVP scope відповідає Stage 2 preparation.

Правила:

- KZO є першим MVP product для CALC
- scope залишається product-specific but MVP only
- Base Calculation Object залишається основою для payload
- `prepare_calculation` залишається єдиним зовнішнім API entry point
- статус цього scope: `APPROVED_WITH_FIXES`
