# EDS Power Master Template Handshake Setup

## Purpose
Explain how to run the first handshake in the MASTER TERMINAL TEMPLATE.

## Current State
EDSPowerCore is not yet deployed as Apps Script Library.

## Temporary Handshake Mode
For first test only:
copy both files into the bound Apps Script project of:
EDS Power — MASTER TERMINAL TEMPLATE

Files:
- gas/core/EDSPowerCore.gs
- gas/terminal/EDSPowerLocalBootstrap.gs

## Steps
1. Open MASTER TERMINAL TEMPLATE.
2. Open Extensions -> Apps Script.
3. Add file EDSPowerCore.gs.
4. Paste contents from gas/core/EDSPowerCore.gs.
5. Add file EDSPowerLocalBootstrap.gs.
6. Paste contents from gas/terminal/EDSPowerLocalBootstrap.gs.
7. Save.
8. Run:
   runEDSPowerTerminalFoundationHandshakeTest()
9. Confirm logs.

## Expected Result
- core_reachable = true
- spreadsheet_id_present = true
- terminal_id = TERMINAL_TEMPLATE
- no token logged
- no secrets logged
- no business logic executed

## Important
This is temporary local-core handshake mode.
Final architecture will later move EDSPowerCore into central Apps Script Library.

## Forbidden
- do not add production terminal_id to template
- do not add calculation logic
- do not add dynamic menu logic
- do not add DB writes
- do not add secrets
