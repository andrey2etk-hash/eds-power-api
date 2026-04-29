# Idea Master Log

This file is the single source of truth for all normalized ideas in EDS Power.

## Status Values

- `NEW`
- `ACTIVE`
- `BACKLOG`
- `FUTURE`
- `PARKED`
- `IMPLEMENTED`
- `REJECTED`
- `RENORMALIZED`

## Master Table

| Idea_ID | Date | Raw Idea | Classification | Priority | Decision | Stage Target | Trigger Condition | Key Thesis | Status |
|---|---|---|---|---|---|---|---|---|---|
| IDEA-0001 | 2026-04-29 | Create Idea Normalizer | `IMMEDIATE_CRITICAL` | `P0` | `URGENT_TASK` | System governance | Anti-drift protection required before future idea intake | Create an idea intake firewall before raw ideas can influence implementation | `IMPLEMENTED` |
| IDEA-0002 | 2026-04-29 | Develop Google Sheets Sidebar UI as an interface layer for EDS Power navigation, module access, quick actions, logic, and scenarios without changing core architecture | `NORMAL_BUT_LATER` | `P2` | `BACKLOG` | Post-Google Sheets Core Structure Draft | After stable sheet architecture, module map, and user role logic | Develop Google Sheets Sidebar UI as structured operational control panel for EDS Power modules after core logic is defined | `BACKLOG` |
| IDEA_20260426_001 | 2026-04-29 | Run Stage 3E manual `testKzoPrepareCalculation()` execution to verify GAS -> API handshake on Render | `RIGHT_NOW` | `P1` | `TASK` | Stage 3E | Stage 3D handshake baseline exists and manual log verification is the active gate before any UI expansion | Verify the data pipeline between Google and Render without adding a UI layer | `ACTIVE` |

## Idea Notes

### IDEA-0002 — Google Sheets Sidebar UI

Review stage:

- Re-evaluate after first usable operational spreadsheet framework.

Possible future sidebar blocks:

- Dashboard
- Objects
- Configurator
- Production Transfer
- Kitting
- Supply
- Analytics
- Admin / Rules

Scope guard:

- allowed now: collect UX ideas
- allowed now: mockup/design concepts
- forbidden now: build full production UI architecture
- forbidden now: shift focus away from core system logic

### IDEA_20260426_001 — Stage 3E Manual GAS Execution

Critic audit notes:

- Render free tier may cold-start; first manual request may exceed the normal response window.
- Stage 3E must verify the endpoint path `/api/calc/prepare_calculation`.
- Stage 3E must verify clean execution logs with `logic_version` before any Stage 3F cell-writing work.

Builder scope guard:

- allowed now: manual Apps Script execution of `testKzoPrepareCalculation()`
- allowed now: collect Execution Log output for verification
- forbidden now: create table buttons
- forbidden now: change Google Sheets structure
- forbidden now: add UI, sidebar, or cell-writing behavior
