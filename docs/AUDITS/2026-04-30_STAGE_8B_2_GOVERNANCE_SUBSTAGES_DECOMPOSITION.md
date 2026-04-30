# STAGE 8B.2 — GOVERNANCE SUB-STAGES (EXECUTION DECOMPOSITION)

**Parent handle:** **`STAGE_8B_2_CLIENT_AGNOSTIC_FLOW_STABILIZATION`** · **Canonical TASK:** **`TASK-2026-08B-013`** (**`ACTIVE`**) — **`COMPLETE`** only when slices **2A–2E** + parent synthesis deliverables are closed (**`TASK`** update).

**Label:** **`STAGE_8B_2_GOVERNANCE_SUBSTAGES_DECOMPOSED`**

**Scope:** Governance artifacts **only** (docs / audits). **No** code, API, GAS, DB.

**Overlap rule:** Each slice owns named decisions; downstream slices **reference** upstream closes — **do not redefine** (**2B** never re-proves idempotency keys; **2C** never widens **`KZO_MVP_SNAPSHOT_V1`** semantics — that is **2D** only).

---

## STAGE_8B_2A_IDEMPOTENCY_DUPLICATE_GOVERNANCE

| # | Field | Definition |
|---|--------|-------------|
| 1 | **TITLE** | **8B.2A** — Idempotency & duplicate-request / duplicate-artifact governance |
| 2 | **PRIMARY OBJECTIVE** | Зафіксувати **нейтральні** правила повторних відправлень (**retries**) і **семантичних дублікатів** (**same intent / same bounded payload**) до того, як фазові межі (**prepare** / **save**) та текст помилок ускладнють узгодження. |
| 3 | **CORE RISK BLOCKED** | **Duplicate drift** та **replay drift**: неоднозначність «ще один рядок у БД чи той самий логічний результат», роз’їждження між клієнтами через неписані припущення. |
| 4 | **ALLOWED ACTIONS** | Документи-політики; глосарій термінів; матриця сценаріїв (повтор того ж `request_id` / новий запит з ідентичним навантаженням тощо); критерії «що рахуємо дуплікатом»; посилання на **API authority** (без опису реалізації). |
| 5 | **FORBIDDEN ACTIONS** | Імплементація; нові черги/async; DDL; зміна **`main.py`** / **`kzo_snapshot_persist.py`** / **GAS**; розширення **AUTH/UI**; **Stage 9** теми; **продуктова** семантика поза дорогою **`prepare_calculation` → snapshot → `save_snapshot`**. |
| 6 | **SUCCESS CONDITION** | Підписаний офлайн або в репо «заморожений» пакет правил (**idempotency** + **duplicate doctrine**), на який явно посилаються **2B–2E** без переозначення. |
| 7 | **FAILURE CONDITION** | Політики залишаються на рівні гасла; або в один документ втягнуто **prepare/save** чи **error schema** (**scope bleed** у сусідні зрізи). |
| 8 | **EXECUTION COMPLEXITY** | **Medium** — мало тексту обсягом, високі вимоги до точності формулювань (**edge cases** retries). |
| 9 | **DEPENDENCY ORDER** | **`1`** — **без апстрім-залежностей** у межах **8B.2**. |

---

## STAGE_8B_2B_PREPARE_SAVE_SPLIT_OUTCOME_GOVERNANCE

| # | Field | Definition |
|---|--------|-------------|
| 1 | **TITLE** | **8B.2B** — Prepare / Save **split outcome** governance |
| 2 | **PRIMARY OBJECTIVE** | Формалізувати **окремі результати** двох фаз оркестрації (**prepare** успіх при **save** відмові частковій/повній, або повтор **`save`**), лініяж «що є джерелом правди на кордоні API» без **Sheet-as-truth** та без **тонкого клієнта-мозку**. |
| 3 | **CORE RISK BLOCKED** | **Orphan persistence** наратив: незрозуміло, що вважається «валідним проміжним» станом системи й що клієнт **може**/ **не може** легітимно робити далі (**thin client**). |
| 4 | **ALLOWED ACTIONS** | Сценарні таблиці; state machine на **paper** (governance); вимоги до обов’язкових полів на кожній фазі **на рівні контрактної мови**; посилання на **2A** для повторів/дублікатів. |
| 5 | **FORBIDDEN ACTIONS** | Нові транспортні «розумні» правила у **GAS**; побудова **failed persistence subsystem**; async; зміна **V1 snapshot** складу (**2D**); повний перелік машинних кодів помилок (**2C**). |
| 6 | **SUCCESS CONDITION** | Узгоджений набір **outcome класів** по фазах + чітке «хто є authority» після кожної відповіді API (**без** імплементації). |
| 7 | **FAILURE CONDITION** | Залишаються дірки («інколи ок») між **prepare** та **save**; або документ дублює **2A**/**2C**. |
| 8 | **EXECUTION COMPLEXITY** | **Medium–High** — багато перетинів із помилковими траєкторіями, але тільки **організація думки**, не код. |
| 9 | **DEPENDENCY ORDER** | **`2`** — **після `2A`** (retry/duplicate мова уже зафіксована). |

---

## STAGE_8B_2C_MACHINE_READABLE_PERSISTENCE_ERROR_DOCTRINE

| # | Field | Definition |
|---|--------|-------------|
| 1 | **TITLE** | **8B.2C** — Machine-readable persistence **error** doctrine |
| 2 | **PRIMARY OBJECTIVE** | Визначити **нейтральний** для клієнта мінімум: стабільні **коди**/категорії, зв’язок з **фазою** (**prepare** vs **save** з **2B**), і що **має бути парсибельним** без знання Sheets/Web — **contract boundary**. |
| 3 | **CORE RISK BLOCKED** | **Слабка машиночитність**: клієнти (включно з **thin GAS**) відтворюють різні гілки на однакових збоях або парсять текст людини як протокол. |
| 4 | **ALLOWED ACTIONS** | Таксономія помилок; таблиця code → meaning; принципи версіонування доктрини; приклади **JSON-shape** як **normative appendix** (**not** shipped code change). |
| 5 | **FORBIDDEN ACTIONS** | Редагування кодової бази/API; занурення у **повну** archival failed-row систему; **DB redesign**; зміна **V1 полів продукту** під виглядом «поліпшити помилку». |
| 6 | **SUCCESS CONDITION** | Достатньо однозначна доктрина, щоб **2D** (integrity fail) та **2E** (audit) могли посилатися на **стабільні ідентифікатори** категорій збоїв. |
| 7 | **FAILURE CONDITION** | Лише опис «human message» без категорій; або змішування **engineering validation** збоїв із **transport** без поділу (**2D** конфлікт). |
| 8 | **EXECUTION COMPLEXITY** | **Medium** — узгодження таблиць імен; уникнути заточки під один клієнт. |
| 9 | **DEPENDENCY ORDER** | **`3`** — **після `2B`** (фази є опорою для класифікації помилки). |

**Registry update (**2026-04-30** — doctrine lodged):** **`STAGE_8B_2C_NORMALIZED_FOR_ACTIVE_SUBSTAGE`** — **`docs/AUDITS/2026-04-30_STAGE_8B_2C_MACHINE_READABLE_PERSISTENCE_ERROR_IDEA_NORMALIZATION.md`**. **`STAGE_8B_2C_DOCTRINE_PUBLISHED`** — **`docs/AUDITS/2026-04-30_STAGE_8B_2C_MACHINE_READABLE_PERSISTENCE_ERROR_DOCTRINE.md`**. **Gemini REQUEST** — **`docs/AUDITS/2026-04-30_GEMINI_STAGE_8B_2C_FOCUSED_AUDIT_REQUEST.md`** (Gemini closeout **`STAGE_8B_2C_GEMINI_FOCUSED_AUDIT_PASS`** pending).

---

## STAGE_8B_2D_SNAPSHOT_INTEGRITY_VALIDATION_GOVERNANCE

| # | Field | Definition |
|---|--------|-------------|
| 1 | **TITLE** | **8B.2D** — Snapshot **integrity validation** governance ( **`KZO_MVP_SNAPSHOT_V1`** stance ) |
| 2 | **PRIMARY OBJECTIVE** | Зафіксувати **governance-межу** між «валідним знімком для збереження» та «відхилити до зміни версії контракту» — строго **без інфляції продуктової семантики** у **V1**. |
| 3 | **CORE RISK BLOCKED** | **Shallow validation** / **silent acceptance**: неясно, які порушення цілісності блокують **save**, а які зобовʼязує гарантувати **prepare**; ризик **GAS**-специфічних обхідних шляхів. |
| 4 | **ALLOWED ACTIONS** | Чіткі **integrity rule lists** governance; зв’язок із **existing** **`11_KZO_MVP_SNAPSHOT_V1_CONTRACT.md`** (посилання, не rewrite без **IDEA**); як **2C** кодують **failure** класи для integrity. |
| 5 | **FORBIDDEN ACTIONS** | DDL; нові MVP шари в контракті; зміна **prepare** для «підлікувати» integrity в **save** (**product creep**); імплементація в коді до окремого **implementation gate**. |
| 6 | **SUCCESS CONDITION** | Audit-ready перелік **integrity expectations** узгоджений із **thin client**: клієнт не «підтягує» поля — все на боці контракту/API story. |
| 7 | **FAILURE CONDITION** | Правила дублюють **2C** текстом або розмивають межу контракт/продукт (**V2-привид** без **IDEA**). |
| 8 | **EXECUTION COMPLEXITY** | **Medium** — високий ризик **scope creep**, тільки якщо дозволити «маленькі» політичні доповнення. |
| 9 | **DEPENDENCY ORDER** | **`4`** — **після `2C`** (клас збою для integrity fail має бути в доктрині помилок). |

---

## STAGE_8B_2E_CLIENT_NEUTRALITY_VERIFICATION

| # | Field | Definition |
|---|--------|-------------|
| 1 | **TITLE** | **8B.2E** — Client-neutrality **verification** audit |
| 2 | **PRIMARY OBJECTIVE** | Перевірити, що **2A–2D** разом не створюють **GAS-примушення**, **Sheet-truth**, або платформених «відступів» (**adapter creep**) — лише аудит висновків, опційно контрольний чеклист. |
| 3 | **CORE RISK BLOCKED** | **GAS-centric drift** та порушення **API orchestrates persistence truth**. |
| 4 | **ALLOWED ACTIONS** | Окремий audit dossier (**dated**); трасування кожної норми **2A–2D** до «будь-який клієнт однаково»; фіксація residual risks як **defer**, не stealth implementation. |
| 5 | **FORBIDDEN ACTIONS** | Нові фічі під виглядом аудиту; **web/mobile rollout** рішень; код; DDL; занесення нових задач без **TASK** апдейту. |
| 6 | **SUCCESS CONDITION** | PASS/FAIL із явним списком **gaps**, які або закривають наступним **doc-only** рядком, або **defer** із забороною робити у **implementation** без нового TASK. |
| 7 | **FAILURE CONDITION** | Аудит «все загальне ок» без прив’язки до **2A–2D**; або він додає **нові обов’язки** без окремої зміни scope. |
| 8 | **EXECUTION COMPLEXITY** | **Low–Medium** — читання й перехресні посилання на вже створені документи. |
| 9 | **DEPENDENCY ORDER** | **`5`** — **після `2A`, `2B`, `2C`, `2D`** (verification — останній шар). |

---

# EXECUTION ORDER RECOMMENDATION

**Recommended sequence:** **`2A` → `2B` → `2C` → `2D` → `2E`**.

**Rationale ( drift minimization ):**
- **`2A`** фіксує **identity / repetition / duplicate** мову; без цього **2B** легко суперечить повторному **save** або «той самий знімок знов».
- **`2B`** розділяє **фазові** відповідальності й часткові траєкторії; інакше **2C** змішає код помилки двох контекстів.
- **`2C`** стабілізує **parseable failures** перед **2D**, де integrity-порушення **мають** відображатися в уже визначену таксономію.
- **`2D`** залежить від стабільних **failure categories** й не повинна роздувати семантику **V1**.
- **`2E`** узагальнює лише коли локальні зрізи **закриті** — запобігає «переписувати 2A–2D» під один клієнт або одну платформу.

---

_End — governance decomposition only._
