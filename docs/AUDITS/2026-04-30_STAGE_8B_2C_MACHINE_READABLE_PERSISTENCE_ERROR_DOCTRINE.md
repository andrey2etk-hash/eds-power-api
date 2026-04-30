# 1. STAGE TITLE

**Stage 8B.2C — Machine-Readable Persistence Error Doctrine**

| Field | Value |
| --- | --- |
| **Normative slice** | **`STAGE_8B_2C_MACHINE_READABLE_PERSISTENCE_ERROR_DOCTRINE`** |
| **Parent gate** | **`TASK-2026-08B-013`** (**`ACTIVE`**) · **IDEA-0023** |
| **Normalization source** | **`docs/AUDITS/2026-04-30_STAGE_8B_2C_MACHINE_READABLE_PERSISTENCE_ERROR_IDEA_NORMALIZATION.md`** |
| **Depends on (read-only)** | **`8B.2A`** + **`8B.2B`** |
| **Execution class** | Doctrine authoring only (**no implementation**) |

---

# 2. PURPOSE

Define a bounded, client-neutral governance doctrine for machine-readable persistence failures so all clients read the same failure semantics across **prepare (`P`)** and **save (`S`)** without changing transport, API surface, or runtime behavior.

---

# 3. CORE RISK BLOCKED

- Human-message parsing instead of stable machine signals.
- Phase confusion (`prepare` validation rejection vs `save` persistence failure).
- Retry drift (unsafe retries on terminal classes).
- Duplicate/orphan drift outside `8B.2A` and `8B.2B` semantics.
- Split-brain interpretation between clients.

---

# 4. DEFINITIONS

- **persistence failure**: non-success persistence outcome in governed flow that must be machine-interpretable by stable classification.
- **phase error (P/S)**: failure mapped to **`P`** (`prepare_calculation`) or **`S`** (`save_snapshot`) boundary.
- **retryable**: governance class where another attempt may be allowed, subject to `8B.2A`/`8B.2B` constraints.
- **terminal**: governance class where the same attempt must not be retried without input/policy correction.
- **duplicate-aware failure**: failure whose reading depends on idempotency/duplicate doctrine from `8B.2A`.
- **orphan-aware failure**: failure where `prepare` and `save` outcomes diverge and must be interpreted by `8B.2B` phase doctrine.
- **legacy_flat_error**: legacy compatibility posture where flat top-level `error_code` can coexist with structured failure object.

---

# 5. CANONICAL ERROR TAXONOMY

Canonical governance classes (bounded, non-bloated):

| Class | Intent |
| --- | --- |
| **`P_INPUT_VALIDATION`** | Invalid/unsupported input envelope at prepare phase. |
| **`P_ENGINEERING_REJECT`** | Deterministic prepare-phase rejection by governed rules. |
| **`S_ENVELOPE_SHAPE`** | Snapshot envelope/shape reject at save phase. |
| **`S_PERSISTENCE_INFRA`** | Save-phase infrastructure/storage path unavailable/failed. |
| **`S_POLICY_DUPLICATE`** | Duplicate/idempotency policy reading per `8B.2A`. |
| **`S_SEMANTIC_INTEGRITY_PREVIEW`** | Integrity-aligned preview marker only; `8B.2D` remains locked in this stage. |

---

# 6. PHASE-AWARE ERROR GROUPING

- **`P` group**: failures from `prepare_calculation` path.
- **`S` group**: failures from `save_snapshot` path.
- Cross-phase reading (`orphan-aware`) is interpreted by referencing `8B.2B` outcome doctrine, not redefined here.

---

# 7. RETRYABILITY GOVERNANCE

Allowed doctrine hints only (not retry engine design):

- **`RETRY_NEUTRAL`**: retry may be acceptable after phase/duplicate checks.
- **`RETRY_DISCOURAGED`**: retry requires operator reconciliation.
- **`TERMINAL_FOR_ATTEMPT`**: same-attempt retry is not allowed until correction.

Retryability is always subordinate to `8B.2A` duplicate doctrine and `8B.2B` phase/orphan semantics.

---

# 8. CLIENT-NEUTRAL MACHINE-READABLE ERROR CONTRACT

Minimal machine-readable spine:

- stable `error_code` (or equivalent stable machine identifier),
- phase binding (`P` or `S`),
- taxonomy class,
- retryability hint,
- optional duplicate/orphan interpretation flags when explicitly signaled.

Client type (GAS/web/mobile/agent) must not alter semantic interpretation.

---

# 9. THIN CLIENT RULE

Thin client behavior is transport + display only:

- consume and surface machine failure fields as returned,
- do not invent local persistence truth,
- do not add local retry orchestration,
- do not reinterpret failure classes by client platform.

---

# 10. LEGACY COEXISTENCE

- Legacy flat top-level `error_code` may coexist with structured failure representation (`legacy_flat_error`).
- Structured machine contract is canonical reading path.
- Coexistence does not authorize new handler shapes in this stage.

---

# 11. TRANSPORT vs PERSISTENCE FAILURE BOUNDARY

- **Transport/system access failures** (network timeout, DNS, gateway, runtime access) remain transport-layer facts and are **not redesigned** in `8B.2C`.
- **Persistence governance failures** are semantic classes above transport (`P/S` + taxonomy class + retryability hint).
- This stage defines interpretation doctrine only and does not redesign transport stack.

---

# 12. ALLOWED

- Authoring this bounded doctrine file as the single `8B.2C` canon.
- Mapping known failure meanings into the taxonomy classes above.
- Referencing `8B.2A` / `8B.2B` / canonical V1 contracts by pointer.
- Preparing for focused Gemini audit readiness.

---

# 13. FORBIDDEN

- Any code, API, GAS, DB, migration, or handler changes.
- Validation redesign (`8B.2D` ownership).
- Rewriting `8B.2A` or `8B.2B`.
- Retry engine, async subsystem, or new persistence subsystem design.
- Taxonomy bloat beyond bounded class set in this dossier.

---

# 14. SUCCESS CONDITION

- Doctrine is fully authored, bounded, and governance-safe in this file.
- Stage stays strictly documentation-only.
- Dossier is ready for focused Gemini audit using:
  **`docs/AUDITS/2026-04-30_GEMINI_STAGE_8B_2C_FOCUSED_AUDIT_REQUEST.md`**.

---

# 15. FAILURE CONDITION

- Scope drifts into implementation or transport redesign.
- `2D` integrity design is authored inside `2C`.
- Retry subsystem or handler-level mechanics appear in doctrine text.
- Multiple competing `8B.2C` doctrine canons are created.

---

# 16. STAGE BOUNDARY

**Inside `8B.2C`:**
- machine-readable persistence error taxonomy,
- phase-aware grouping (`P/S`),
- retryability governance hints,
- duplicate-aware and orphan-aware semantic interpretation doctrine.

**Outside `8B.2C`:**
- runtime/handler/API/DB changes,
- integrity redesign (`8B.2D` remains locked / not authorized),
- client UX/transport architecture redesign.

---

# 17. NEXT STEP: Gemini Focused Audit only

1. Run focused Gemini audit for this dossier only:
   **`docs/AUDITS/2026-04-30_GEMINI_STAGE_8B_2C_FOCUSED_AUDIT_REQUEST.md`**
2. Lodge closeout:
   **`docs/AUDITS/YYYY-MM-DD_GEMINI_STAGE_8B_2C_FOCUSED_AUDIT.md`**
3. No stage progression in this step; `8B.2C` remains in authoring/audit cycle until closeout is accepted.
