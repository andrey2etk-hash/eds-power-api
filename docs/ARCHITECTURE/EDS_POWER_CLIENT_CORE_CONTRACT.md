# EDS Power Client Core Contract

## 1. Purpose

Define responsibilities and public interface of Central GAS Core / EDSPowerCore.

Central GAS Core is the shared client shell for all EDS Power Google Sheet terminals.

It supports:
- 40-60 terminal fleet governance
- minimal local bootstrap
- dynamic menu rendering
- authenticated API calls
- shared UI templates
- shared error handling

## 2. Architecture Position

EDSPowerCore sits between:

Local Bound Script
↓
Central GAS Core / EDSPowerCore
↓
Render API
↓
Supabase

EDSPowerCore is NOT the business logic layer.
EDSPowerCore is NOT the engineering calculation layer.
EDSPowerCore is NOT the database layer.

## 3. Core Responsibilities

EDSPowerCore may own:

- API transport wrapper
- auth request wrapper
- attach Authorization: Bearer token
- read/write session token from UserProperties through allowed client-side helpers
- login dialog orchestration
- logout orchestration
- session status check call
- dynamic menu request
- dynamic menu rendering
- standard response envelope handling
- standard error display
- shared dialogs
- shared sidebars
- shared CSS/style tokens
- module launcher helpers
- terminal health check helpers
- safe fallback handling

## 4. Forbidden Responsibilities

EDSPowerCore must NOT own:

- engineering calculations
- KZO/KTP/BMZ calculation logic
- BOM logic
- pricing logic
- role permission decisions
- final module access truth
- direct Supabase writes
- SQL
- token cryptographic validation
- password/hash storage
- DB schema logic
- per-cell calculation API calls
- hidden onEdit calculation requests

## 5. Required Public Interface

Define stable EDSPowerCore public functions conceptually:

- EDSPowerCore_onTerminalOpen(context)
- EDSPowerCore_refreshMenu(context)
- EDSPowerCore_login(context)
- EDSPowerCore_logout(context)
- EDSPowerCore_getSessionStatus(context)
- EDSPowerCore_openModule(actionKey, context)
- EDSPowerCore_callApi(request)
- EDSPowerCore_showError(error, context)
- EDSPowerCore_showFallback(message, context)

NOTE:
This is interface contract only.
No implementation in this task.

## 6. Local Bootstrap -> EDSPowerCore Call Contract

Local bootstrap may call EDSPowerCore only through approved public functions.

Local bootstrap must not call internal EDSPowerCore helpers.

Allowed local-to-core calls:
- onOpen -> EDSPowerCore_onTerminalOpen(context)
- edsPowerRefreshMenu -> EDSPowerCore_refreshMenu(context)
- edsPowerLogin -> EDSPowerCore_login(context)
- edsPowerLogout -> EDSPowerCore_logout(context)
- edsPowerOpenModule(actionKey) -> EDSPowerCore_openModule(actionKey, context)

## 7. Context Object Doctrine

EDSPowerCore calls must receive terminal context.

Conceptual context fields:
- terminal_id
- spreadsheet_id
- active_sheet_name
- client_type = "GAS"
- core_version
- bootstrap_version
- user_session_present = true/false

Rules:
- terminal_id identifies the Sheet terminal
- session token must not be logged
- session token must not be included in docs
- context is not authorization proof by itself

## 8. API Transport Doctrine

EDSPowerCore owns transport behavior:

- build request
- attach Authorization header when session exists
- attach terminal context headers/payload
- call Render API
- parse standard envelope
- return safe response to caller
- surface machine-readable errors

EDSPowerCore must not:
- reinterpret engineering results
- correct invalid business payloads
- bypass backend validation

## 9. Dynamic Menu Doctrine

EDSPowerCore requests menu payload from API.

EDSPowerCore renders menu based only on API response.

EDSPowerCore must not:
- decide module access locally
- hardcode production module visibility
- show hidden modules unless API allows

## 10. Auth Client Doctrine

EDSPowerCore may:
- collect login input from dialog
- send login request to API
- store returned session token in UserProperties
- clear token on logout
- request session status

EDSPowerCore must not:
- store password
- log password
- log token
- validate token cryptographically
- store token hash

## 11. UI Template Doctrine

EDSPowerCore may centralize:
- login dialog template
- error dialog template
- module launcher sidebar
- common CSS
- shared labels
- standard warnings

Goal:
UI changes should be centralized and not require editing every terminal.

## 12. Version / Rollout Doctrine

EDSPowerCore must expose or carry core_version.

Production terminals use Stable Core.
Admin/test terminals may use Dev Core.

Rules:
- production must not silently use experimental core
- core version compatibility may be checked by API
- rollout process is not implemented in this task

## 13. Failure Modes

If API unavailable:
- show safe fallback
- do not calculate locally
- do not bypass auth

If EDSPowerCore unavailable:
- local bootstrap shows emergency fallback only

If session expired:
- show AUTH_SESSION_EXPIRED message
- require re-login

## 14. Relation to Batch Request Rule

EDSPowerCore must not create per-cell API calls for calculation workflows.

All calculation calls must be explicit batch actions:
- menu command
- button
- approved operator action

## 15. What This Does NOT Implement

This document does not implement:
- EDSPowerCore code
- Apps Script Library
- clasp
- API menu endpoint
- DB schema
- terminal rollout
- calculation logic
- module runtime

## 16. Verdict

EDS Power Client Core Contract is required before EDS Power Minimal Local Bootstrap Implementation.

EDS Power Dynamic Menu Payload Contract:
`docs/ARCHITECTURE/EDS_POWER_DYNAMIC_MENU_PAYLOAD_CONTRACT.md`

Note:
EDSPowerCore menu rendering is blocked until this payload contract is approved.
