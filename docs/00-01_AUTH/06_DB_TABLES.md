# DB Tables

## users

| Поле | Тип | Опис |
|---|---|---|
| id | uuid | ID користувача |
| email | text | email |
| full_name | text | ПІБ |
| status | text | active / blocked / archived |
| avatar_file_id | uuid | посилання на файл аватарки |
| created_at | timestamp | дата створення |
| updated_at | timestamp | дата оновлення |

## roles

| Поле | Тип | Опис |
|---|---|---|
| id | uuid | ID ролі |
| code | text | код ролі |
| name | text | назва ролі |

## user_roles

| Поле | Тип | Опис |
|---|---|---|
| id | uuid | ID запису |
| user_id | uuid | користувач |
| role_id | uuid | роль |

## permissions

| Поле | Тип | Опис |
|---|---|---|
| id | uuid | ID дозволу |
| module | text | модуль |
| action | text | дія |
| description | text | опис |

## role_permissions

| Поле | Тип | Опис |
|---|---|---|
| id | uuid | ID запису |
| role_id | uuid | роль |
| permission_id | uuid | дозвіл |
