# 2026-05-06 — EDS Power GAS Skeleton Naming Rename

## Objective

Rename code-level Sakura/SakuraCore references in the active GAS terminal foundation skeleton to EDS Power / EDSPowerCore terminology without changing behavior.

## Reason

Documentation naming correction was completed first.
Active code-level skeleton naming needed alignment so current EDS Power project does not keep Sakura/SakuraCore as canonical runtime terminology.

## Files renamed

- `gas/core/SakuraCore.gs` -> `gas/core/EDSPowerCore.gs`
- `gas/terminal/SakuraLocalBootstrap.gs` -> `gas/terminal/EDSPowerLocalBootstrap.gs`

## Function/symbol rename map

Core public symbols:
- `SakuraCore_onTerminalOpen` -> `EDSPowerCore_onTerminalOpen`
- `SakuraCore_refreshMenu` -> `EDSPowerCore_refreshMenu`
- `SakuraCore_login` -> `EDSPowerCore_login`
- `SakuraCore_logout` -> `EDSPowerCore_logout`
- `SakuraCore_getSessionStatus` -> `EDSPowerCore_getSessionStatus`
- `SakuraCore_openModule` -> `EDSPowerCore_openModule`
- `SakuraCore_callApi` -> `EDSPowerCore_callApi`
- `SakuraCore_showError` -> `EDSPowerCore_showError`
- `SakuraCore_showFallback` -> `EDSPowerCore_showFallback`
- `SakuraCore_sanitizeContext_` -> `EDSPowerCore_sanitizeContext_`

Bootstrap symbols:
- `sakuraRefreshMenu` -> `edsPowerRefreshMenu`
- `sakuraLogin` -> `edsPowerLogin`
- `sakuraLogout` -> `edsPowerLogout`
- `sakuraOpenModule` -> `edsPowerOpenModule`
- `sakuraShowFallbackError` -> `edsPowerShowFallbackError`
- `buildSakuraTerminalContext_` -> `buildEDSPowerTerminalContext_`
- `runSakuraTerminalFoundationHandshakeTest` -> `runEDSPowerTerminalFoundationHandshakeTest`
- `addSakuraEmergencyFallbackMenu_` -> `addEDSPowerEmergencyFallbackMenu_`
- `sakuraShowFallbackSetupRequired_` -> `edsPowerShowFallbackSetupRequired_`

Constants/messages:
- `SAKURA_CORE_VERSION` -> `EDS_POWER_CORE_VERSION`
- `SAKURA_BOOTSTRAP_MENU_TITLE` -> `EDS_POWER_BOOTSTRAP_MENU_TITLE`
- `SAKURA_BOOTSTRAP_VERSION` -> `EDS_POWER_BOOTSTRAP_VERSION`
- `SAKURA_TERMINAL_ID_PROPERTY` -> `EDS_POWER_TERMINAL_ID_PROPERTY`
- visible labels/messages switched from "Sakura/SakuraCore" to "EDS Power/EDSPowerCore"

## Remaining Sakura references

Code-level remaining references:
- none in active GAS skeleton files.

Documentation-level remaining references:
- historical Module 01 audit records still contain Sakura wording as historical context.
- these were intentionally retained; no logic impact.

## What was NOT changed

- No business logic
- No engineering/calculation logic
- No API behavior
- No DB/schema/SQL
- No Render/env
- No dynamic menu implementation expansion

## Handshake test status

- Symbol renamed to `runEDSPowerTerminalFoundationHandshakeTest()`.
- Manual operator execution is pending in GAS runtime environment.

## Verdict

Code-level naming correction completed for active GAS skeleton.
Behavior is unchanged except naming.
Status: `IMPLEMENTATION_RENAME_PENDING_TEST`.
