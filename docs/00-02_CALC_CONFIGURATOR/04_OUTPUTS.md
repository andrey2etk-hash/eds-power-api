# Outputs

## Базова відповідь

Модуль `00-02_CALC_CONFIGURATOR` повертає відповідь у форматі `docs/00_SYSTEM/04_DATA_CONTRACTS.md`.

Відповідь завжди містить:

- `status`
- `data`
- `error`
- `meta`

## Успішна відповідь

```json
{
  "status": "success",
  "data": {
    "calculation": {
      "calculation_id": "calc_001",
      "version": "1.0",
      "object_number": null,
      "product_type": "PRODUCT_TYPE_CODE",
      "status": "validated",
      "parameters": {
        "common": {},
        "product_specific": {},
        "options": {}
      },
      "result": {},
      "created_at": "2026-04-25T12:00:00Z",
      "updated_at": "2026-04-25T12:00:01Z"
    }
  },
  "error": null,
  "meta": {
    "request_id": "uuid",
    "processed_at": "2026-04-25T12:00:01Z"
  }
}
```

## Помилка валідації

```json
{
  "status": "validation_error",
  "data": {},
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Calculation payload is invalid",
    "details": {
      "field": "payload.calculation"
    }
  },
  "meta": {
    "request_id": "uuid",
    "processed_at": "2026-04-25T12:00:01Z"
  }
}
```

## Правила

- `status` відповідає статусам з `04_DATA_CONTRACTS.md`
- `data.calculation` базується на Base Calculation Object
- `data.calculation.status` відповідає Calculation Object Lifecycle
- `error` дорівнює `null`, якщо помилки немає
- `object_number` може бути `null` на статусі `draft`
- продукт-специфічний `result` не деталізується на цьому етапі
