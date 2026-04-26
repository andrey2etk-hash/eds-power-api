# Inputs

## Вхідні дані

Модуль `00-02_CALC_CONFIGURATOR` отримує дані тільки через API request у форматі `docs/00_SYSTEM/04_DATA_CONTRACTS.md`.

Базові вхідні дані:

- `meta` — Universal Request Header
- `module` — `CALC_CONFIGURATOR`
- `action` — тільки `prepare_calculation` як зовнішня API дія
- `payload` — дані розрахунку

GAS не викликає `validate_calculation`, `normalize_calculation` або розрахунок окремо.

Validation, normalization і calculation є внутрішніми етапами API.

## Auth/session requirements

Запит до `CALC_CONFIGURATOR` належить до protected module flow.

`meta` має містити:

- `request_id`
- `source`
- `user_id`
- `session_token`
- `timestamp`

Правила:

- `user_id` визначається через `00-01_AUTH`
- `session_token` потрібен для перевірки активної сесії
- пароль не передається в CALC payload
- GAS не змінює auth/session структуру
- API виконує фінальну перевірку доступу

## Base Calculation Object у payload

Базовий об’єкт розрахунку передається в `payload.calculation`.

```json
{
  "calculation": {
    "calculation_id": "calc_001",
    "version": "1.0",
    "object_number": null,
    "product_type": "PRODUCT_TYPE_CODE",
    "status": "draft",
    "parameters": {
      "common": {},
      "product_specific": {},
      "options": {}
    },
    "result": {},
    "created_at": "2026-04-25T12:00:00Z",
    "updated_at": "2026-04-25T12:00:00Z"
  }
}
```

На статусі `draft` поле `object_number` може бути `null`.

## Structured parameters

Параметри групуються так:

- `parameters.common` — спільні параметри для різних типів виробів
- `parameters.product_specific` — параметри конкретного типу виробу
- `parameters.options` — додаткові опції розрахунку

Продукт-специфічні поля не деталізуються на цьому етапі.

## Приклад запиту

```json
{
  "meta": {
    "request_id": "uuid",
    "source": "gas",
    "user_id": "user_001",
    "session_token": "session_token",
    "timestamp": "2026-04-25T12:00:00Z"
  },
  "module": "CALC_CONFIGURATOR",
  "action": "prepare_calculation",
  "payload": {
    "calculation": {
      "calculation_id": "calc_001",
      "version": "1.0",
      "object_number": null,
      "product_type": "PRODUCT_TYPE_CODE",
      "status": "draft",
      "parameters": {
        "common": {},
        "product_specific": {},
        "options": {}
      },
      "result": {},
      "created_at": "2026-04-25T12:00:00Z",
      "updated_at": "2026-04-25T12:00:00Z"
    }
  }
}
```

## Validation responsibility

UI / GAS може перевірити тільки:

- наявність обов’язкових полів
- простий формат введення
- явно порожній запит

API виконує фінальну перевірку:

- відповідність data contract
- права доступу
- структуру `payload`
- структуру `parameters`
- допустимість `module` та `action`
