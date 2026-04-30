# EDS Power Data Contracts

## 1. Призначення файлу

Цей файл описує єдиний стандарт обміну даними між рівнями системи:

```text
UI / GAS → API → Database → API → UI / GAS
```

Data Contract — це правило, яке визначає:

- які дані передаються
- у якому форматі
- які поля обов’язкові
- як виглядає відповідь
- як передаються помилки

## 2. Головне правило

Усі дані між рівнями системи передаються у форматі JSON.

Заборонено:

- передавати неструктуровані масиви
- передавати зайві поля
- змінювати формат без оновлення цього файлу
- використовувати різні формати для різних модулів

## 3. Базова структура запиту

Кожен запит до API має структуру:

```json
{
  "meta": {
    "request_id": "uuid",
    "source": "gas",
    "user_id": "uuid",
    "session_token": "session_token",
    "timestamp": "2026-04-25T12:00:00Z"
  },
  "module": "CALC_CONFIGURATOR",
  "action": "calculate",
  "payload": {}
}
```

## 4. Опис полів запиту

- meta — обов’язкове поле; службова інформація запиту
- meta.request_id — обов’язкове поле; унікальний ID запиту
- meta.source — обов’язкове поле; джерело запиту: gas / web / api
- meta.user_id — обов’язкове поле; ID користувача
- meta.session_token — обов’язкове поле для авторизованої сесії; токен активної сесії
- meta.timestamp — обов’язкове поле; час створення запиту
- module — обов’язкове поле; модуль системи
- action — обов’язкове поле; дія всередині модуля
- payload — обов’язкове поле; дані для виконання дії

### 4.1. Universal Request Header

Universal Request Header є стандартною частиною `meta` для всіх API-запитів.

Базовий формат:

```json
{
  "meta": {
    "request_id": "uuid",
    "session_token": "session_token",
    "user_id": "user_001",
    "timestamp": "2026-04-25T12:00:00Z",
    "source": "gas"
  }
}
```

Правила:

- `request_id` використовується для трасування запиту
- `session_token` використовується тільки для перевірки активної сесії
- `user_id` визначається через `00-01_AUTH`
- `timestamp` фіксує час створення запиту
- `source` визначає джерело запиту
- `session_token` не зберігається в логах як відкрите значення

## 5. Базова структура відповіді

Кожна відповідь API має структуру:

```json
{
  "status": "success",
  "data": {},
  "error": null,
  "metadata": {
    "request_id": "uuid",
    "api_version": "0.1.0",
    "logic_version": "string | null",
    "execution_time_ms": 0
  }
}
```

## 6. Опис полів відповіді

- status — обов’язкове поле; результат виконання
- data — обов’язкове поле; корисні дані відповіді
- error — обов’язкове поле; опис помилки або null
- metadata — обов’язкове поле; службова інформація відповіді
- metadata.request_id — обов’язкове поле; ID запиту
- metadata.api_version — обов’язкове поле; версія API
- metadata.logic_version — обов’язкове поле; версія логіки або null
- metadata.execution_time_ms — обов’язкове поле; час виконання в мілісекундах

## 7. Статуси відповіді

Можливі значення status:

- success — дія виконана успішно
- validation_error — помилка перевірки вхідних даних
- auth_error — помилка авторизації
- permission_error — недостатньо прав
- not_found — потрібні дані не знайдені
- server_error — внутрішня помилка API

## 8. Структура помилки

Якщо виникла помилка, поле error має таку структуру:

```json
{
  "code": "VALIDATION_ERROR",
  "message": "Required field product_type is missing",
  "details": {
    "field": "product_type"
  }
}
```

Для API response використовується Global Error Contract, описаний нижче в цьому файлі.

Якщо помилки немає:

```json
"error": null
```

## 9. Приклад запиту для конфігуратора

```json
{
  "meta": {
    "request_id": "7f3a2c9b-1a44-4bb0-9f88-3a1d1e7a1001",
    "source": "gas",
    "user_id": "user_001",
    "session_token": "session_token",
    "timestamp": "2026-04-25T12:00:00Z"
  },
  "module": "CALC_CONFIGURATOR",
  "action": "calculate",
  "payload": {
    "object_number": "7445-В",
    "product_type": "KSO",
    "quantity": 5,
    "parameters": {}
  }
}
```

## 10. Приклад відповіді для конфігуратора

```json
{
  "status": "success",
  "data": {
    "calculation_id": "calc_001",
    "result_status": "completed"
  },
  "error": null,
  "metadata": {
    "request_id": "7f3a2c9b-1a44-4bb0-9f88-3a1d1e7a1001",
    "api_version": "0.1.0",
    "logic_version": "string | null",
    "execution_time_ms": 0
  }
}
```

## 11. Правило payload

payload залежить від конкретного модуля та дії.

Але він завжди має бути:

- об’єктом JSON
- структурованим
- описаним у файлі відповідного модуля

Наприклад:

- docs/00-02_CALC_CONFIGURATOR/02_INPUTS.md
- docs/00-02_CALC_CONFIGURATOR/04_OUTPUTS.md

## 12. Заборонено

Заборонено передавати:

```json
[
  "7445-В",
  "KSO",
  5
]
```

Тому що такий формат:

- не самодокументований
- легко ламається
- незрозумілий для API
- незручний для AI

Правильно:

```json
{
  "object_number": "7445-В",
  "product_type": "KSO",
  "quantity": 5
}
```

## 13. Принцип мінімальних даних

Кожен запит має передавати тільки ті дані, які потрібні для конкретної дії.

Заборонено передавати:

- зайві персональні дані
- паролі
- токени
- службові ключі
- дані інших модулів без потреби

## 14. Версійність контракту

Кожен контракт має версію.

Базова версія:

```text
contract_version: 1.0
```

У майбутньому версія може передаватися в meta:

```json
{
  "meta": {
    "contract_version": "1.0"
  }
}
```

## 15. Глобальний auth/session контекст

AUTH/session контекст є частиною `meta` і використовується для ідентифікації користувача, сесії та джерела запиту.

Базовий формат:

```json
{
  "meta": {
    "request_id": "uuid",
    "source": "gas",
    "user_id": "user_001",
    "session_token": "session_token",
    "timestamp": "2026-04-25T12:00:00Z"
  }
}
```

Правила:

- `user_id` визначається через `00-01_AUTH`
- `session_token` використовується тільки якщо сесія вже створена
- пароль не входить у `meta`
- токени, паролі та службові ключі не зберігаються в логах
- AUTH є винятком: пароль передається тільки в `action: login`

## 16. Base Calculation Object Contract (**NON-CANONICAL / LEGACY**)

Цей блок є базовим placeholder для підготовки `00-02_CALC_CONFIGURATOR`.

Базовий об’єкт розрахунку:

```json
{
  "calculation": {
    "calculation_id": "calc_001",
    "version": "1.0",
    "logic_version": "logic_version",
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

Правила:

- детальний payload описується в документації `00-02_CALC_CONFIGURATOR`
- цей блок не створює нову логіку
- цей блок не замінює module-specific inputs / outputs
- цей блок фіксує базову форму об’єкта для майбутнього CALC MVP
- `version` фіксує версію структури об’єкта розрахунку
- `logic_version` фіксує версію алгоритму або логіки, яка створила результат
- `logic_version` потрібен, щоб старі записи не ставали несумісними після зміни алгоритмів
- `object_number` може бути `null` на статусі `draft`
- `parameters.common` містить параметри, спільні для різних виробів
- `parameters.product_specific` містить параметри конкретного типу виробу
- `parameters.options` містить додаткові опції без зміни базового контракту
- `created_at` фіксує час створення об’єкта
- `updated_at` фіксує час останнього оновлення об’єкта
- нові групи параметрів додаються тільки після опису в документації `00-02_CALC_CONFIGURATOR`

## 17. Global Error Contract (**NON-CANONICAL / LEGACY**)

All API errors must follow this structure:

```json
{
  "status": "validation_error",
  "data": null,
  "error": {
    "error_code": "KZO_REQUIRED_FIELD_MISSING",
    "message": "Required field is missing",
    "source_field": "voltage_class",
    "module": "CALC_CONFIGURATOR",
    "action": "prepare_calculation"
  },
  "metadata": {
    "request_id": "uuid",
    "api_version": "0.1.0",
    "logic_version": "kzo_mvp_v0.1",
    "execution_time_ms": 124
  }
}
```

Rules:

- `error_code` is mandatory
- `message` is mandatory
- `source_field` is required for validation errors
- `module` is mandatory
- `action` is mandatory
- UI must not receive generic system errors without `error_code`
- all API responses must include `metadata`
- `metadata.request_id` is mandatory
- `metadata.api_version` is mandatory
- `metadata.logic_version` is mandatory and may be `null`
- `metadata.execution_time_ms` is mandatory

## 18. MVP Timeout Rule (**NON-CANONICAL / LEGACY**)

GAS client uses synchronous request for MVP.

If API exceeds timeout threshold, return:

```json
{
  "status": "timeout",
  "error": {
    "error_code": "REQUEST_TIMEOUT",
    "message": "Processing exceeded MVP sync threshold"
  }
}
```

Rule:

- No async queue required for Stage 3 MVP

## 19. Головне правило зміни контракту (**process — не payload authority для persistence**)

Цей розділ описує лише потік (workflow), структура даних регулюється виключно §20 та файлом **13_CLIENT_AGNOSTIC_PERSISTENCE_CONTRACT_V1.md** (**«13_» у реєстрах документації**).

**Status:** **`ACTIVE`** for **workflow** only.

**§19 = workflow governance only.** **Payload authority** для **`POST /api/kzo/save_snapshot`**, відповіді з **`persistence_status` / `failure` / `error_code`** та JSON **`KZO_MVP_SNAPSHOT_V1`** **визначається виключно** через маршрут **`§20`** + **`docs/00_SYSTEM/13_CLIENT_AGNOSTIC_PERSISTENCE_CONTRACT_V1.md`** + **`docs/00-02_CALC_CONFIGURATOR/09_KZO/11_KZO_MVP_SNAPSHOT_V1_CONTRACT.md`**. **`§16`–`§18`** для цього шляху — **LEGACY / NON-CANONICAL** (історія / **`prepare_calculation`-band**), **не** джерело полів **`save_snapshot`**.

Будь-яка зміна формату запиту або відповіді:

- Спочатку описується в документації
- Потім погоджується
- Потім реалізується в API
- Потім тестується
- Потім використовується в GAS/UI

Заборонено змінювати контракт тільки в коді.

**Non-split-brain clause:** Для **`POST /api/kzo/save_snapshot`**, **`persistence_status`**, **`failure` / `error_code`** та тіла **`KZO_MVP_SNAPSHOT_V1`** цей параграф **не** робить **`04_DATA_CONTRACTS.md`** джерелом полів — **канонічне визначення див. `§20`** і **`13_CLIENT_AGNOSTIC_PERSISTENCE_CONTRACT_V1.md`**. Зміни туди йдуть **згідно з цим же процесом** (**IDEA → TASK**), але **текст правди** живе в **`13_` + `11_KZO_MVP_SNAPSHOT_V1_CONTRACT`**, а не в дзеркалі тут.

## 20. KZO MVP persistence (`save_snapshot` / client-agnostic path) (**canonical routing — single active pointer**)

### Canonical (**single active contract truth**)

**Persistence response shape** (**success**, **failure**, **`failure`/`error_code`** mirror, **`X-EDS-Client-Type`**, **`persistence_status`**) і **canonical client flow**:

- **`docs/00_SYSTEM/13_CLIENT_AGNOSTIC_PERSISTENCE_CONTRACT_V1.md`**

**Snapshot JSON body** (`KZO_MVP_SNAPSHOT_V1`):

- **`docs/00-02_CALC_CONFIGURATOR/09_KZO/11_KZO_MVP_SNAPSHOT_V1_CONTRACT.md`**

### This file (**`04_DATA_CONTRACTS.md`**) — DEFERRED mirror (**NON-CANONICAL for persistence payloads**)

**`§16`–`§18`** = **baseline / historical patterns** (**`prepare_calculation` band**, timeouts, generic errors) — **`LEGACY / NON-SUPERSEDING`** relative to **`save_snapshot`**. They **must not** be read as defining persistence success/failure envelopes.

Duplicate field-by-field persistence payloads **must not** grow here unsupervised (**split-brain risk**). **`§20`** is the **only** in-file routing pointer for persistence; **payload authority** = **`13_`** (+ **`11_`** snapshot body).

**Until** an explicit **`TASK`** activates a merged section: persistence HTTP semantics are **canonical in `13_` only**.

**`§19`** still governs **how** approved changes land (docs → agreement → API); it does **not** relocate canonical text into **`§16`–`§18`** for persistence.
