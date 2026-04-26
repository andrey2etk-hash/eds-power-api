# Inputs

## Вхідні дані

Модуль AUTH отримує:

- email користувача
- пароль або token
- user_id
- module
- action

AUTH є винятком: пароль передається тільки в action login і не зберігається в логах.

## Приклад запиту

```json
{
  "meta": {
    "request_id": "uuid",
    "source": "gas",
    "user_id": "anonymous",
    "timestamp": "2026-04-25T12:00:00Z"
  },
  "module": "AUTH",
  "action": "login",
  "payload": {
    "email": "user@example.com",
    "password": "password"
  }
}
```
