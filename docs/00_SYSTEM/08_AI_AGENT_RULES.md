# EDS Power AI Agent Rules

## 1. Призначення

Цей файл визначає правила роботи AI-інструментів у системі EDS Power.

AI використовується як керований інструмент розвитку системи, а не як самостійне джерело архітектурних рішень.

---

## 2. Основний принцип

Жоден AI не є джерелом правди.

Джерело правди:

- GitHub repository
- System documentation (`docs/`)
- Approved architecture
- Approved global rules
- Approved data contracts
- User final decision

---

## 3. Ролі AI-інструментів

### 3.1. Cursor — Builder Agent

Cursor використовується для:

- створення файлів
- редагування структури
- реалізації коду
- рефакторингу
- технічних перевірок
- роботи з GitHub

Cursor не має права:

- самостійно змінювати архітектуру
- вигадувати нові модулі
- змінювати system rules без TASK
- змінювати data contracts без погодження
- хаотично перебудовувати структуру
- реалізовувати raw user ideas без normalized classification
- preparing non-approved ideas

---

### 3.2. GPT — Architect / Critic Agent

GPT використовується для:

- системної архітектури
- нормалізації ідей
- логічного контролю
- виявлення конфліктів
- проектування модулів
- аналізу ризиків
- управління roadmap
- daily review
- changelog strategy
- idea normalization

GPT не має права:

- бути єдиним джерелом рішень
- змінювати GitHub напряму
- обходити system docs
- ігнорувати approved structure

GPT = Idea Normalizer allowed.

Cursor forbidden from implementing or preparing non-approved ideas.

---

### 3.3. Gemini — External Critic Agent

Gemini використовується для:

- альтернативного критичного аналізу
- зовнішньої перевірки
- пошуку слабких місць
- перевірки логіки “зі сторони”

Gemini не використовується як головний архітектор системи.

---

## 4. User Role

Користувач є фінальним decision maker.

Тільки користувач:

- затверджує архітектуру
- погоджує зміни
- приймає або відхиляє AI-пропозиції
- дозволяє commit / push
- визначає пріоритети

---

## 5. Робочий цикл AI

Будь-яка нова ідея проходить шлях:

```text
Idea → GPT normalization → TASK / BACKLOG → Cursor analysis → GPT/Gemini critique → User approval → Cursor implementation → Docs update → Commit → Push
```

## 6. Gemini Audit Protocol

Gemini використовується як External Critic Agent тільки на контрольних точках системи або за окремою командою користувача.

### Основна задача Gemini:

- виявлення архітектурних конфліктів
- виявлення логічних слабкостей
- пошук overengineering
- перевірка масштабованості
- перевірка MVP-ризиків

### Gemini не використовується для:

- побудови архітектури з нуля
- зміни roadmap
- створення нових модулів
- зміни system rules без погодження

---

### Контрольні точки Gemini:

- після завершення `00_SYSTEM`
- після завершення кожного базового модуля (`AUTH`, `CALC`, тощо)
- перед критичною API-реалізацією
- перед MVP запуском
- за прямою командою користувача

---

### Формат роботи:

1. Cursor або User формує Gemini Audit Report
2. Gemini виконує external critique
3. GPT аналізує Gemini critique
4. User приймає рішення
5. Cursor реалізує тільки погоджені зміни

---

### Команда запуску:

"Prepare Gemini Audit Report"

---

### Правило:

Gemini працює тільки на основі структурованого звіту, а не хаотичного контексту.

## 7. Audit Cycle Protocol

Для критичних перевірок системи використовується папка:

`docs/AUDITS/`

Кожен аудит створюється як окремий файл.

### Правило

Cursor не має права самостійно створювати audit-файл без завершеного audit cycle.

---

### 7.1. Етапи audit cycle

Кожен audit cycle проходить тільки в такій послідовності:

1. User дає Cursor команду підготувати вибірку подій після останнього audit.
2. Cursor формує structured audit input для Gemini.
3. User передає вибірку Gemini.
4. Gemini повертає external critique.
5. User передає critique в GPT.
6. GPT аналізує critique як Architect / Critic Agent.
7. GPT визначає:
   - що прийняти
   - що відхилити
   - що відкласти
   - які дії передати Cursor
8. User передає Cursor команду від GPT.
9. Cursor виконує погоджені дії.
10. Cursor створює audit report у `docs/AUDITS/`.
11. User перевіряє audit report.
12. Тільки після цього зміни можна commit / push.

---

### 7.2. Команда для запуску audit cycle

Стандартна команда:

`Prepare Gemini Audit Input since last audit`

Cursor повинен:

- знайти останній audit-файл у `docs/AUDITS/`
- визначити зміни після нього
- підготувати structured audit input
- не змінювати файли системи
- не створювати audit report на цьому етапі

---

### 7.3. Структура Gemini Audit Input

Cursor формує:

- Current stage
- Last audit date / last audit file
- Files changed since last audit
- Key decisions since last audit
- New risks
- Open questions
- What Gemini must critique
- Restrictions for Gemini

---

### 7.4. Створення audit report

Audit report створюється тільки після:

- Gemini critique отримана
- GPT interpretation отримана
- User decision отримане
- Cursor action виконано

---

### 7.5. Структура audit report

Кожен audit report має містити:

- Audit date
- Audit trigger
- Last audit reference
- Files reviewed
- Gemini critique summary
- GPT interpretation
- Accepted items
- Rejected items
- Deferred items
- Cursor actions performed
- User final decision
- Status

---

### 7.6. Заборонено

Заборонено:

- створювати audit report до Gemini critique
- створювати audit report без GPT interpretation
- створювати audit report без User decision
- виконувати Gemini recommendations напряму без GPT review
- використовувати Gemini як final decision maker
- комітити audit changes без перевірки User
