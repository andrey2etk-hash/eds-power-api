# Process Flow

## Generic calculation flow

1. Користувач вводить базові дані розрахунку в UI.
2. UI / GAS виконує первинну перевірку заповнення.
3. GAS формує JSON request за `04_DATA_CONTRACTS.md` з `action: prepare_calculation`.
4. API приймає запит.
5. API перевіряє Universal Request Header.
6. API перевіряє права користувача через `00-01_AUTH`.
7. API перевіряє структуру `payload.calculation`.
8. API перевіряє структуру `parameters`.
9. API нормалізує дані розрахунку.
10. API виконує внутрішній етап calculation preparation.
11. API визначає статус розрахунку.
12. API формує відповідь у стандартному форматі.
13. GAS отримує відповідь.
14. UI показує користувачу статус або помилку.

## Internal API stages

`prepare_calculation` є єдиною зовнішньою API дією CALC на цьому етапі.

Внутрішні етапи API:

- validation
- normalization
- calculation preparation
- response formation

GAS не викликає внутрішні етапи окремо.

## Validation error flow

1. API знаходить помилку у `meta`, `module`, `action` або `payload`.
2. API зупиняє flow до normalization і calculation preparation.
3. API не змінює calculation object як успішно підготовлений.
4. API повертає `status: validation_error`.
5. UI показує користувачу повідомлення про помилку.

## Error path

1. API знаходить системну або бізнес-помилку після базової валідації.
2. API переводить calculation object у статус `error`, якщо об’єкт уже створений у межах flow.
3. API повертає стандартну error response.
4. GAS передає відповідь у UI без додаткової бізнес-логіки.
5. UI показує користувачу помилку.

## Stage 2 restriction

Цей flow не описує конкретні алгоритми розрахунку.

Продукт-специфічний process flow додається тільки після окремого TASK.
