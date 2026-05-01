# IDEA NORMALIZATION REPORT

## 1. IDEA TITLE

**Stage 8B.3A — API Idempotency + Duplicate Snapshot Protection MVP**

---

## 2. CLASSIFICATION

**Type:** Bounded Implementation Readiness Slice  
**Priority:** Critical  
**Domain:** Persistence Protection / API Idempotency / Duplicate Prevention  
**Layer:** Post-8B.2 Governance -> First Controlled Implementation  
**Execution Scope:** Implementation Boundary Normalization Only  
**Complexity:** Medium  
**Mode:** Narrow Safe Implementation Planning

---

## 3. CONTEXT SNAPSHOT

### Governance state:

**Stage 8B.2 CLOSED**

- 2A Identity / Duplicate / Replay CLOSED
- 2B Prepare / Save split CLOSED
- 2C Machine-readable errors CLOSED
- 2D Integrity / V1 enforcement CLOSED

### Current state:

System governance is ready.  
Implementation lane opens.

### Active gap:

`save_snapshot` still requires first practical bounded duplicate/replay protection implementation.

### Current risk:

Without first implementation slice:

- duplicate snapshot persistence
- replay save drift
- accidental repeated writes
- governance remains theoretical
- persistence trust weakens operationally

### Strategic transition:

From:  
Governance doctrine  
To:  
Minimal practical enforcement

---

## 4. PRIMARY OBJECTIVE

Normalize the smallest safe implementation slice that answers:

### "How does API prevent duplicate or replayed snapshot saves

without persistence redesign?"

---

## 5. IMPLEMENTATION BOUNDARY

### Required implementation target:

`save_snapshot` duplicate / replay protection only

### Scope:

- API-side only
- request identity enforcement
- duplicate snapshot save prevention
- bounded idempotency enforcement
- existing request_id / snapshot envelope leverage
- minimal implementation footprint

### Explicitly NOT:

- prepare_calculation redesign
- Supabase architecture redesign
- async queue
- platform orchestration redesign
- broad persistence framework rewrite

### Core law:

Implement doctrine,  
not platform reinvention.

---

## 6. ALLOWED FILES

### Likely safe implementation zones:

- `main.py` (save_snapshot boundary only)
- persistence validation layer directly tied to save_snapshot
- existing snapshot envelope validation utilities
- audit docs
- TASK docs
- CHANGELOG

### Conditional:

- Minimal migration only if absolutely required by implementation proof

### Otherwise:

No DB structural mutation preferred

---

## 7. FORBIDDEN ACTIONS

### Explicitly blocked:

- BOM
- pricing
- KZO engineering expansion
- GAS logic growth
- UI redesign
- AUTH
- Stage 8B.2E
- broad persistence redesign
- async queue
- new modules
- Supabase platform redesign
- Sheet-first assumptions
- client-specific duplicate logic

---

## 8. SUCCESS CONDITION

A bounded implementation exists where:

### DUPLICATE:

Repeated identical save request does not silently create duplicate truth

### REPLAY:

Replay attempts are governance-safe

### API:

Remains source of idempotency truth

### GAS:

Remains thin client

### SYSTEM:

Implements doctrine with minimal mutation

---

## 9. FAILURE CONDITION

Any of:

- broad persistence redesign
- DB-first redesign without necessity
- GAS orchestration expansion
- new module creep
- async overreach
- identity doctrine mutation beyond bounded implementation
- code spread beyond minimal slice
- implementation inflation

---

## 10. TEST REQUIREMENTS

### Required proof:

1. First save = SUCCESS
2. Identical replay = DUPLICATE / SAFE BLOCK
3. Distinct valid save = SUCCESS
4. Machine-readable duplicate response aligns with 8B.2C
5. No GAS business logic added
6. No Stage 8B.2 doctrine regression

### Audit class:

Operator-verifiable + governance-verifiable

---

## 11. ROLLBACK RULE

### If implementation:

- breaks existing save_snapshot
- mutates V1 contract
- introduces persistence ambiguity
- causes governance drift

### Then:

Immediate rollback to Stage 8B.1B verified baseline

### Core law:

Protection may not destabilize proven persistence.

---

## 12. NORMALIZER VERDICT

### APPROVED AS:

**First Bounded Persistence Protection Implementation Slice**

### Reason:

This is the correct first move after governance closure:  
small,  
auditable,  
high-value,  
architecture-safe.

### Strategic note:

This is NOT persistence expansion.  
This is doctrine becoming minimally real.

---

## 13. EXECUTION CLASS

**BOUNDED IMPLEMENTATION READINESS ONLY**

### Meaning:

Define  
Constrain  
Protect  
Prepare

### Do NOT:

Implement yet  
Broaden  
Redesign  
Overbuild

---

## 14. ONE-LINE EXECUTIVE SUMMARY

**Stage 8B.3A is the first narrow implementation bridge where closed idempotency governance becomes minimal API-side duplicate snapshot protection without allowing persistence hardening to mutate into platform redesign.**
