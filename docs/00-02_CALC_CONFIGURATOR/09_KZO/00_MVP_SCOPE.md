# KZO MVP Scope

## Status

scope_governed

KZO MVP Scope governed.

Цей scope ще не має статусу `draft_ready`.

## Goal

Визначити перший MVP product для `00-02_CALC_CONFIGURATOR` як `KZO`.

Цей файл описує тільки V1 MVP scope для підготовки першого продукт-специфічного розрахунку.

## Mandatory parameters

Обов’язкові параметри V1:

- product_type: `KZO`
- quantity
- voltage_class
- cabinet_count
- configuration_type

Правило:

- quantity = cabinet units

## Optional parameters

Опціональні параметри V1:

- object_number
- notes
- option_ids

Правило:

- `object_number` — optional at draft stage, required before final / production transition
- `option_ids` — predefined option IDs only, no open text

## Validation rules

- invalid `voltage_class` + `configuration_type` combinations must return `validation_error`

## Excluded scope

У V1 не входить:

- deep BOM
- CAD
- production routes
- supplier complexity
- детальна логіка комплектації
- автоматичний підбір постачальників
- розрахунок виробничого маршруту
- генерація комерційної пропозиції

## Expected outputs

Очікувані outputs V1:

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

## Stage alignment

KZO MVP scope відповідає Stage 2 preparation.

Правила:

- KZO є першим MVP product для CALC
- scope залишається product-specific but MVP only
- Base Calculation Object залишається основою для payload
- `prepare_calculation` залишається єдиним зовнішнім API entry point
- деталізація алгоритму допускається тільки після TASK approval
- статус цього scope: `scope_governed`
