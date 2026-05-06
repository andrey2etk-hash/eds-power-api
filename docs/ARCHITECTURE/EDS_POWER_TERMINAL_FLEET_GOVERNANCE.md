# EDS Power Terminal Fleet Governance

## 1. Selected Baseline

MODEL C — HYBRID TERMINAL GOVERNANCE

Definition:
- Terminal = entry point
- Local Bound Script = minimal bootstrap
- Central GAS Core = shared client shell
- Render API = auth / access / business truth
- Supabase = registry truth

## 2. Purpose

Define how 40-60 Google Sheet terminals are centrally governed without creating local script drift.

## 3. Problem Prevented

Without this model, the system risks:
- 40-60 divergent GAS copies
- outdated terminal scripts
- inconsistent menus
- inconsistent styles
- unsafe module rollout
- impossible mass update management

## 4. Local Terminal Bootstrap Doctrine

Local bound script responsibilities:

Allowed:
- onOpen()
- terminal_id handling
- connect to EDSPowerCore
- call central menu refresh
- call central login/logout wrappers
- emergency fallback message if core/API unavailable
- UI container access through SpreadsheetApp.getUi()

Forbidden:
- engineering logic
- role logic
- module access logic
- calculation logic
- direct Supabase writes
- hardcoded production module menu
- local style duplication
- local business rules

Principle:
Local bootstrap must be intentionally boring and rarely changed.

## 5. Central GAS Core Doctrine

Central GAS Core / Library responsibilities:

- API transport wrapper
- attach Authorization: Bearer token
- standard request envelope handling
- menu builder
- auth client helpers
- session client helpers
- shared dialogs/sidebars
- shared UI templates
- shared CSS/style tokens
- standard error display
- module launch helpers
- terminal health check helpers

Central GAS Core must NOT contain:
- engineering calculations
- business truth
- final role decisions
- direct Supabase writes

## 6. Dynamic Menu Doctrine

Menu is not hardcoded per terminal.

Flow:
1. Sheet opens.
2. Local onOpen calls Central GAS Core.
3. Central GAS Core sends authenticated/terminal-aware request to API.
4. API resolves:
   - user
   - session
   - terminal_id
   - role
   - module access
   - module status
5. API returns menu JSON.
6. GAS draws only allowed menu items.

## 7. API Menu Payload Concept

Conceptual payload only. No endpoint implementation in this task.

Example fields:
- module_id
- module_name
- module_status
- visibility
- allowed_actions
- menu_label
- action_key
- required_core_version
- metadata

Rules:
- API owns menu truth.
- GAS only renders allowed menu.
- Users must not see modules they cannot access.
- Admin may see DEV modules if registry allows.

## 8. Module Access and Admin Testing Doctrine

Production users:
- see only released modules
- use stable core
- must not see experimental modules

Admin/dev users:
- may see unreleased modules
- may use dev/testing core path
- may test Module 02/03 while Module 01 remains stable for production

Rule:
New modules must not break existing modules.

## 9. Version / Rollout Model

### Stable Core
Used by production terminals.

### Dev Core
Used by admin/test terminals.

### Library Version Reality
Apps Script library versions are not automatically updated across all bound scripts.

Governance implication:
- production rollout requires controlled version update process
- dev/head must not be silently exposed to production users
- future rollout tooling may use clasp or Apps Script API, but this task does not implement it

## 10. UI / Style Centralization

Shared UI and styles should be centralized in Central GAS Core where possible:
- dialogs
- sidebars
- CSS
- buttons
- warnings
- error banners
- module cards

Goal:
UI changes should not require editing 40-60 terminal scripts.

## 11. Mobile / Future Client Note

Hybrid Model C supports future mobile/web because:
- auth lives in API
- role/module access lives in API/Supabase
- business logic lives in backend
- mobile can become another client type later

But:
- GAS UI/menu code will not be reused in mobile
- mobile/web UI requires separate frontend later

## 12. Failure Modes / Risks

Document:
- Central Core outage affects terminal UX
- API outage affects dynamic menu
- library version rollout is not automatic
- local bootstrap drift is dangerous
- hardcoded local module access is forbidden
- dev/stable separation must be protected

## 13. Strict Boundaries

This architecture document does NOT implement:
- Central GAS Core
- Apps Script library
- clasp deployment
- dynamic menu endpoint
- Supabase schema
- admin panel
- module runtime
- calculation logic
- mobile app

## 14. Next Architecture Decisions

Open decisions:
- exact minimal local bootstrap contents
- terminal_id assignment/protection model
- library vs web-app UI strategy
- stable/dev core split mechanism
- menu payload endpoint ownership
- module version registry model
- rollout/update process for 40-60 terminals

EDS Power Minimal Local Bootstrap Contract:
`docs/ARCHITECTURE/EDS_POWER_MINIMAL_LOCAL_BOOTSTRAP_CONTRACT.md`

EDS Power Client Core Contract:
`docs/ARCHITECTURE/EDS_POWER_CLIENT_CORE_CONTRACT.md`

EDS Power Terminal Assignment Doctrine:
`docs/ARCHITECTURE/EDS_POWER_TERMINAL_ASSIGNMENT_DOCTRINE.md`

EDS Power Admin Provisioning Doctrine:
`docs/ARCHITECTURE/EDS_POWER_ADMIN_PROVISIONING_DOCTRINE.md`

EDS Power Dynamic Menu Payload Contract:
`docs/ARCHITECTURE/EDS_POWER_DYNAMIC_MENU_PAYLOAD_CONTRACT.md`

EDS Power Master Terminal Template Doctrine:
`docs/ARCHITECTURE/EDS_POWER_MASTER_TERMINAL_TEMPLATE_DOCTRINE.md`

## 15. Verdict

Hybrid Model C is the selected EDS Power terminal fleet baseline.
