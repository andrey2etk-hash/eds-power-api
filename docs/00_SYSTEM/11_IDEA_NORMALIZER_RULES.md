# Idea Normalizer Rules

## PURPOSE

Idea intake firewall for EDS Power.

Idea Normalizer prevents raw ideas from creating scope drift, hidden implementation work, architecture drift, module sprawl, or premature preparation.

## CLASSIFICATIONS

Every new idea must receive exactly one classification:

- `SHLAK` — rejected noise, duplicate, unsafe, vague, irrelevant, or not useful for EDS Power.
- `NORMAL_BUT_LATER` — valid idea, but not needed for the current stage.
- `NORMAL_LONG_TERM` — valid strategic idea for future system growth.
- `RIGHT_NOW` — valid idea that belongs to the current stage.
- `IMMEDIATE_CRITICAL` — urgent blocker, governance breach, data-contract risk, or critical system risk.

## PRIORITY

Priority is derived from classification:

- `P0` = `IMMEDIATE_CRITICAL` only
- `P1` = `RIGHT_NOW`
- `P2` = `NORMAL_BUT_LATER`
- `P3` = `NORMAL_LONG_TERM`

No manual priority override is allowed without renormalization.

## COMPATIBILITY MATRIX

Each classification has exactly one allowed decision:

| Classification | Allowed Decision |
|---|---|
| `SHLAK` | `REJECT` only |
| `NORMAL_BUT_LATER` | `BACKLOG` only |
| `NORMAL_LONG_TERM` | `FUTURE` only |
| `RIGHT_NOW` | `TASK` only |
| `IMMEDIATE_CRITICAL` | `URGENT_TASK` only |

No incompatible classification, priority, or decision combinations are allowed.

## DECISION FORMULA

If:

```text
IMMEDIATE_CRITICAL + P0 = URGENT_TASK
RIGHT_NOW + P1 = TASK
```

All other classifications are record-only and must not create Cursor implementation work.

## ANTI-PREP RULE

Cursor may NOT:

- create preparatory files
- create structures
- scaffold modules
- modify architecture

for:

- `SHLAK`
- `NORMAL_BUT_LATER`
- `NORMAL_LONG_TERM`

Any such action = governance breach.

## RENORMALIZATION RULE

Any recorded idea may be re-evaluated if:

- stage changed
- blocker changed
- architecture changed

Renormalization must create an updated record in `docs/00_SYSTEM/12_IDEA_MASTER_LOG.md` and mark the previous record as `RENORMALIZED`.

## MANDATORY FLOW

All new project ideas must pass through this flow:

```text
IDEA -> NORMALIZE -> RECORD -> PRIORITIZE -> TASK (if approved)
```

## FINAL RULE

No raw idea directly influences implementation.
