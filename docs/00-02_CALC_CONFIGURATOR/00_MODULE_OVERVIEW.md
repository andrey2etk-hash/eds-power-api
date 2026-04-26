# 00-02_CALC_CONFIGURATOR Module Overview

## Призначення

Модуль `00-02_CALC_CONFIGURATOR` відповідає за підготовку та виконання розрахунків виробів у системі EDS Power.

На Stage 1 цей документ є тільки foundation placeholder для підготовки Stage 2.

## Base Calculation Object

Базовий об’єкт розрахунку описаний у:

`docs/00_SYSTEM/04_DATA_CONTRACTS.md`

Модуль використовує цей об’єкт як стартову форму для майбутнього CALC MVP.

## API Entry Point

Єдина зовнішня API дія модуля на цьому етапі:

- `prepare_calculation`

Validation, normalization і calculation є внутрішніми етапами API.

GAS не викликає ці етапи окремо.

## Extensible Parameter Architecture

Параметри розрахунку групуються так:

- `common` — спільні параметри для різних типів виробів
- `product_specific` — параметри конкретного типу виробу
- `options` — додаткові опції розрахунку

Правила:

- нові параметри додаються тільки через документацію модуля
- структура параметрів не змінює глобальний request/response contract
- модуль не реалізує розрахунок на Stage 1
- деталізація алгоритмів переноситься на Stage 2

## Calculation Object Lifecycle

Базовий lifecycle calculation object:

- draft
- validated
- error
- calculated
- locked
- archived

## Обмеження Stage 1

На Stage 1 модуль не містить:

- повного алгоритму розрахунку
- нових API endpoints
- таблиць БД
- UI-логіки
- інтеграції з іншими модулями
