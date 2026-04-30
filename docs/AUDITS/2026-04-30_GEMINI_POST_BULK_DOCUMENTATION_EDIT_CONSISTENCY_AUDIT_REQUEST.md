# Gemini — **Post–bulk documentation edit** governance consistency audit request

## Контекст (укр.)

Після великої хвилі правок узгодження документації потрібен **фокусований зовнішній аудит** на **протиріччя**, **split-brain** між **`00_SYSTEM`**, дорогою **`TASK-013` / Stage 8B.2**, та аудит-корпусом. Мета — **перевірити узгодженість**, а **не** писати нову архітектуру чи код.

---

## Artefacts under review (**primary sweep**)

| Priority | Path | Why |
| --- | --- | --- |
| **P1** | **`docs/00_SYSTEM/02_GLOBAL_RULES.md`** | Нова «виняткова» логіка **objective truth** vs стандартний цикл «док → код». |
| **P1** | **`docs/00_SYSTEM/04_DATA_CONTRACTS.md`** (**§§16–20**) | **`§16`–`§18`** (**`NON-CANONICAL` / `LEGACY`**) для **`save_snapshot`**; **`§19`** workflow-only; **`§20`** → **`13_`** + **`11_`** (**single payload authority routing**). |
| **P1** | **`docs/00_SYSTEM/13_CLIENT_AGNOSTIC_PERSISTENCE_CONTRACT_V1.md`** | Узгодженість з **§20** pointer story (**read-only cross-check** — **no rewrite mandate** unless contradiction). |
| **P2** | **`docs/TASKS.md`** (**`TASK-2026-08B-013`**, Stage **8B.2** rollup) | Чи не суперечить таблиця слайсів / **`FORBIDDEN`** новим правилам у **`02_`/`04_`**. |
| **P2** | **`docs/AUDITS/2026-04-30_STAGE_8B_2_PRE_GATE_SCOPE.md`** | Вирівнювання з оновленим **`04_§20`** / **`13_`**. |
| **P2** | **`docs/NOW.md`**, **`docs/CHANGELOG.md`**, **`docs/00_SYSTEM/12_IDEA_MASTER_LOG.md`**, **`docs/AUDITS/00_AUDIT_INDEX.md`**, **`docs/00-02_CALC_CONFIGURATOR/09_STATUS.md`**, **`docs/00-02_CALC_CONFIGURATOR/09_KZO/08_STATUS.md`** | Реєстрова цілісність після масових правок. |
| **P3** | **`docs/AUDITS/2026-04-30_STAGE_8B_2C_MACHINE_READABLE_PERSISTENCE_ERROR_DOCTRINE.md`** | Чи **§9 / §10** узгоджені з новим **§20 routing** (фази **`P`/`S`**, без дублювання payload authority). |

**Out of scope for this request:** зміни **`main.py`**, **`kzo_snapshot_persist.py`**, **`gas/`**, **DDL** — лише згадка, якщо текст **заявляє** факт, що суперечить коду (**DOC FIX** recommendation **to docs only**).

---

## Role

**External critical auditor** — шукати **внутрішні суперечності**, **подвійний канон**, **розмиті FORBIDDEN**, **приховану імплементаційну мандатну силу** в governance-тексті.

**NOT** implementer · **NOT** feature author.

---

## Strict forbidden (this audit)

Вимоги **міняти код/БД** під виглядом аудиту — **REJECT**; позначати **DEFERRED** до окремого **TASK**.

---

## Mandatory questions

1. **GLOBAL_RULES — «objective truth» exception:** Чи **чітко обмежено**, щоб виняток **не** скасовував **IDEA → TASK** для змін контракту? Чи немає **loop-hole** «будь-яка реалізація = правда» без верифікації?
2. **DATA_CONTRACTS §16–§20:** Чи **узгоджено**, що **§16–§18** **явно LEGACY / NON-CANONICAL** для **`save_snapshot`**, **`§19` = лише workflow**, а **канон полів** лише **`§20` + `13_` + `11_`**? Чи **немає** залишкового split-brain?
3. **Cross-file canon:** Чи існує **хоч одне** речення в **`TASKS` / `NOW` / `08_STATUS` / `09_STATUS` / `12_IDEA_MASTER_LOG`**, яке **імпліцитно** робить **`04_DATA_CONTRACTS`** джерелом полів **`save_snapshot`**, **суперечачи §20**?
4. **Stage 8B.2 lane:** Чи нові формулювання **`02_`/`04_`** **не** розширюють **FORBIDDEN** lane **8B.2** (async, redesign, product creep) **словесно**?
5. **8B.2C doctrine:** Чи **persistence_phase `P`/`S`** та каталог **`SNAPSHOT_*`/`KZO_*`** **не суперечать** новій маршрутизації канону (**без** змішування «контракт у `04_`» vs «контракт у `13_`»)?
6. **CHANGELOG / INDEX truth:** Чи **верхні записи** відображають **фактичний** стан репо (документи з’явились / змінені) **без** «phantom CLOSEOUT»?
7. **Verdict:** **PASS** / **PASS WITH DOC FIXES** / **BLOCKED** — перелік **конкретних** правок **лише markdown** (**шлях + §**).

---

## Output lodging

Operator lodges **`docs/AUDITS/YYYY-MM-DD_GEMINI_POST_BULK_DOCUMENTATION_EDIT_CONSISTENCY_AUDIT.md`** with:

- **`GEMINI_POST_BULK_DOC_EDIT_CONSISTENCY_PASS`** (**or** **DOC FIXES**),
- Explicit **fix list** mapped to repo paths.

Registry label (**proposed**): **`STAGE_GEMINI_POST_BULK_DOC_EDIT_CONSISTENCY_REVIEW`** — record in **`CHANGELOG`** + **`00_AUDIT_INDEX.md`** upon closeout.

---

_End._
