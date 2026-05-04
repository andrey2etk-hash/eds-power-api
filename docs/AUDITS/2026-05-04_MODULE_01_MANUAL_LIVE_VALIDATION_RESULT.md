# MODULE 01 MANUAL LIVE VALIDATION RESULT

## Status

PASS / LIVE VALIDATED

## Scope

Manual live validation of Module 01 Google Sheets -> GAS -> API -> Engine -> Sheets chain.

## Environment

- API base URL: `https://eds-power-api.onrender.com`
- endpoint: `POST /api/demo/module-01/kzo/run`
- Google Sheet: `MODULE_01_DEMO`
- mode: `MODULE_01_DEMO`
- demo_id: `MODULE_01_KZO_DEMO_001`
- client_type: `GAS_DEMO`

## Success Scenario Result

Live chain validated:

Google Sheets UI
-> GAS thin client
-> Render API endpoint
-> Module 01 Python engine/demo runner
-> API response
-> GAS writeback
-> Google Sheets output blocks

Recorded success evidence:

- Run Status: `PASS`
- Last Request ID: `93a5430f-0c5a-478e-811a-640b9f863fda`
- Last Run Time: `2026-05-04T12:20:55.931467+00:00`
- status: `success`
- demo_status: `PASS`
- demo_id: `MODULE_01_KZO_DEMO_001`
- demo_version: `demo_v1`

## Engineering Output Verification

Status flow confirmed:

- `DOC36 = PASS`
- `KZO_DEMO_NODE_A_DOC37_S1 = PASS`
- `KZO_DEMO_NODE_A_DOC37_S2 = PASS`
- `KZO_DEMO_NODE_B_DOC37_S1 = PASS`
- `KZO_DEMO_NODE_B_DOC37_S2 = PASS`
- `DOC37_S1 = PASS`

Node results confirmed:

- `KZO_DEMO_NODE_A total_busbar_length_mm = 1290`
- `KZO_DEMO_NODE_B total_busbar_length_mm = 1200`
- `BUSBAR_SIDE_CONNECTIONS joint stack = 30`
- `EQUIPMENT_SIDE_CONNECTIONS joint stack = 18`

Fastener decisions confirmed:

- Node A BUSBAR_SIDE: required `48.5 mm`, `M12x45 REJECTED`, `M12x55 SELECTED`
- Node A EQUIPMENT_SIDE: required `36.5 mm`, `M12x45 SELECTED`
- Node B BUSBAR_SIDE: required `48.5 mm`, `M12x45 REJECTED`, `M12x55 SELECTED`
- Node B EQUIPMENT_SIDE: required `36.5 mm`, `M12x45 SELECTED`

Kit issue lines confirmed:

- `DEMO_BOLT_M12X55 = 6 pcs`
- `DEMO_BOLT_M12X45 = 6 pcs`
- `DEMO_NUT_M12 = 12 pcs`
- `DEMO_FLAT_WASHER_M12 = 24 pcs`
- `DEMO_DISC_SPRING_WASHER_M12 = 12 pcs`

Traceability confirmed:

- `source_node_ids` visible
- `source_line_ids` visible
- `traceability_refs` visible
- `registry_version = demo_v1` visible

Boundary note confirmed:

- Local demo only
- Not production data
- Not final ERP BOM
- Not procurement
- Not warehouse
- Not ERP/1C
- Not pricing
- Not CAD
- No API/GAS/DB

Management summary confirmed:

"System reads registry truth, validates every engineering step, selects local fasteners, and aggregates traceable kit issue lines. This is not final ERP BOM."

## Negative Scenario Result

Invalid API URL used:

- `https://eds2power-api.onrender.com`

Observed:

- Run Status: `TRANSPORT_ERROR`
- Last Request ID: `c3f6c105-7293-4002-86b0-7efbf0f9541b`
- Last Run Time: `2026-05-04T12:24:36.730Z`
- old engineering blocks cleared
- error block displayed:
  - `status = TRANSPORT_ERROR`
  - `message = Invalid demo mode response header. Expected X-EDS-Power-Mode=DEMO.`
  - `timestamp = 2026-05-04T12:24:38.514Z`
- no stale PASS results remained visible
- no fallback calculation occurred

## Governance Confirmation

Confirmed:

- no engineering logic in GAS
- no fallback calculation
- no old PASS results after error
- no production data
- no final ERP BOM
- no procurement/warehouse/ERP
- no pricing/CAD
- no DB/Supabase

## Final Verdict

Module 01 live demo chain validated successfully.

## Next Allowed Step

- Module 01 live demo closeout / milestone commit and push
- or director demo preparation package
