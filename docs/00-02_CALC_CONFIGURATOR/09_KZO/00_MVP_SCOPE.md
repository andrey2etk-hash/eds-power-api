# KZO MVP Scope

## Status

planned

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

## Optional parameters

Опціональні параметри V1:

- object_number
- notes
- customer_reference
- delivery_region
- additional_options

Правило:

`object_number` — optional at draft stage, required before production transfer

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
- basic_result_summary
- validation_errors, якщо є помилки

## Stage alignment

KZO MVP scope відповідає Stage 2 preparation.

Правила:

- KZO є першим MVP product для CALC
- scope залишається product-specific but MVP only
- Base Calculation Object залишається основою для payload
- `prepare_calculation` залишається єдиним зовнішнім API entry point
- деталізація алгоритму допускається тільки після TASK approval
- статус цього scope: `planned`
