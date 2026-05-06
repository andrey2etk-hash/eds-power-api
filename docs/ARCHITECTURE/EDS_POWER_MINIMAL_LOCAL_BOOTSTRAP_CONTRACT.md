# EDS Power Minimal Local Bootstrap Contract

## 1. Purpose

Define the minimal local bound script that may exist inside each Google Sheet terminal.

Goal:
The local script must be stable, tiny, boring, and rarely changed.

## 2. Context

This contract supports:
- 40-60 terminal fleet governance
- Hybrid Model C
- Central GAS Core
- API-driven menu
- role/module access control
- future module rollout without local script drift

## 3. Local Bootstrap Principle

The local terminal script is not the client application.
It is only a loader/bridge into EDS Power Client Core.

## 4. Allowed Local Responsibilities

Local bound script may contain only:

- onOpen()
- emergency fallback menu
- terminal_id read/init bridge
- call EDSPowerCore_refreshMenu()
- call EDSPowerCore_login()
- call EDSPowerCore_logout()
- call EDSPowerCore_openModule(module_id or action_key)
- safe wrapper functions required by Google Sheets menu callbacks
- minimal error display if Central Core is unavailable

## 5. Forbidden Local Responsibilities

Local bound script must NOT contain:

- engineering calculations
- business logic
- role/permission decisions
- module access decisions
- calculation payload interpretation
- API response business interpretation
- direct Supabase access
- direct SQL
- hardcoded production module menu
- local UI styling except emergency fallback
- duplicated dialogs/sidebars
- token validation logic
- token decoding
- password handling beyond passing login input to EDSPowerCore
- per-cell API calls
- onEdit calculation requests

## 6. Required Stable Function Names

Define planned stable local entrypoints conceptually:

- onOpen()
- edsPowerRefreshMenu()
- edsPowerLogin()
- edsPowerLogout()
- edsPowerOpenModule(actionKey)
- edsPowerShowFallbackError(message)

NOTE:
Names are contract placeholders only.
No implementation in this task.

## 7. terminal_id Doctrine

Define:
- each terminal must have unique terminal_id
- terminal_id identifies the Sheet terminal, not the user
- terminal_id must be sent to API as terminal context
- terminal_id must not be used as authentication proof alone
- user session token + terminal_id + backend validation are required together
- terminal_id must be evaluated by backend against EDS Power Terminal Assignment Doctrine

Open decision:
Exact terminal_id storage method:
- ScriptProperties
- hidden sheet cell
- document properties
- protected metadata
- other approved registry method

This task does not decide final storage implementation unless already canonical.

Reference:
`docs/ARCHITECTURE/EDS_POWER_TERMINAL_ASSIGNMENT_DOCTRINE.md`

## 8. Central Core Dependency

Local bootstrap depends on Central GAS Core / EDSPowerCore.

If EDSPowerCore is unavailable:
- show fallback menu/message
- do not attempt local business fallback
- do not calculate locally
- do not bypass auth

## 9. Menu Callback Model

Because Google Sheets menu items require callable local functions,
local bootstrap may expose thin wrapper functions.

These wrappers must only delegate to EDSPowerCore.

Example concept:
local function -> EDSPowerCore action dispatcher

No business logic inside wrappers.

## 10. Security Boundaries

Local bootstrap must never:
- log session token
- store password in docs/sheets
- expose token hash
- validate token cryptographically
- decide whether user has access
- write directly to DB

## 11. Update Governance

Local bootstrap should be designed so it almost never changes.

If local bootstrap must change:
- reason must be documented
- rollout impact must be assessed
- change must be versioned
- terminal fleet update plan required

## 12. Relation to Dynamic Menu

Local bootstrap does not define menu content.

It calls Central GAS Core.
Central GAS Core/API determine menu.

## 13. Relation to Batch Request Rule

Local bootstrap must not trigger calculation API calls on every edit.

Server calls must be explicit batch actions only.

## 14. What This Does NOT Implement

This document does not implement:
- Apps Script local code
- Central GAS Core
- API menu endpoint
- terminal registry schema
- module access registry
- clasp rollout
- any calculation logic

## 15. Verdict

EDS Power Minimal Local Bootstrap Contract is required before creating clean terminal templates.

EDS Power Client Core Contract:
`docs/ARCHITECTURE/EDS_POWER_CLIENT_CORE_CONTRACT.md`

Note:
Minimal bootstrap implementation is blocked until EDSPowerCore public interface is approved.
