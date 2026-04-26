# Outputs

## Успішна відповідь

```json
{
  "status": "success",
  "data": {
    "user_id": "user_001",
    "email": "user@example.com",
    "role": "ADMIN",
    "permissions": []
  },
  "error": null,
  "meta": {
    "request_id": "uuid",
    "processed_at": "2026-04-25T12:00:01Z"
  }
}
```

## Помилка

```json
{
  "status": "auth_error",
  "data": {},
  "error": {
    "code": "AUTH_ERROR",
    "message": "Invalid email or password"
  },
  "meta": {
    "request_id": "uuid",
    "processed_at": "2026-04-25T12:00:01Z"
  }
}
```
