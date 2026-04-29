# Stage 4A Template Protection

## Environment

- Stage: Stage 4A — Google Sheet Core Template Protection + Structured Input Layer
- GAS file: `gas/Stage3D_KZO_Handshake.gs`
- Setup function: `setupStage4ATemplateShell()`
- Run function: `runStage4AKzoTemplateFlow()`
- Target sheet: `Stage4A_MVP`
- Input range: `B2:B14`
- Output range: `D2:E8`

## Objective

Move from the Stage 3F test writeback loop to a controlled MVP shell:

```text
protected template -> fixed input zone -> API request -> fixed output zone
```

## Template Map

Stage 4A defines one deterministic MVP sheet:

`Stage4A_MVP`

The sheet contains:

- fixed input labels in column `A`
- user-editable input values in column `B`
- output labels in column `D`
- API output values in column `E`

## MVP Cell Map

Input zone:

| Cell | Field |
|---|---|
| `B2` | `object_number` |
| `B3` | `product_type` |
| `B4` | `logic_version` |
| `B5` | `voltage_class` |
| `B6` | `busbar_current` |
| `B7` | `configuration_type` |
| `B8` | `quantity_total` |
| `B9` | `CELL_INCOMER` |
| `B10` | `CELL_OUTGOING` |
| `B11` | `CELL_PT` |
| `B12` | `CELL_BUS_SECTION` |
| `B13` | `status` |
| `B14` | `breaker_type` |

Output zone:

| Cell | Field |
|---|---|
| `E2` | `validation_status` |
| `E3` | `object_number` |
| `E4` | `product_type` |
| `E5` | `voltage_class` |
| `E6` | `busbar_current` |
| `E7` | `http_code` |
| `E8` | `stage` |

## Input / Output Zone Governance

Allowed user-editable range:

`B2:B14`

Protected structure:

- template title
- field labels
- output labels
- output values
- non-input cells

Structured input layer:

- `product_type` enum: `KZO`
- `logic_version` enum: `KZO_MVP_V1`
- `voltage_class` enum: `VC_06`, `VC_10`, `VC_20`, `VC_35`
- `configuration_type` enum: `CFG_SINGLE_BUS`, `CFG_SINGLE_BUS_SECTION`
- `status` enum: `DRAFT`
- numeric guards for busbar current, quantity, and cell counts

## GAS Scope

GAS remains a thin client only:

- read fixed cells
- build request
- send API request
- parse response
- write fixed outputs

No business logic is added to GAS.

## Explicitly Not Added

- Sidebar
- buttons
- menus
- batch flow
- DB
- Supabase
- AUTH expansion
- BOM
- costing
- production transfer
- multi-product support
- advanced UI
- architecture expansion

## Execution Result

Status: `VERIFIED_MVP_ONLY`

Manual Stage 4A template setup and protected-shell execution were observed.

Template setup log:

```text
13:11:06  Execution started
13:11:49  {"stage":"4A","status":"template_shell_prepared","sheet":"Stage4A_MVP","input_range":"B2:B14","output_range":"D2:E8"}
13:11:09  Execution completed
```

Template flow execution log:

```text
13:11:31  Execution started
13:12:12  {"stage":"4A","http_code":200,"status":"success","error":null}
13:12:12  {"stage":"4A","status":"writeback_completed","sheet":"Stage4A_MVP","range":"D2:E8"}
13:11:32  Execution completed
```

Verified:

- sheet `Stage4A_MVP` exists
- input zone `B2:B14` was prepared
- output zone `D2:E8` was prepared
- enum dropdowns are visible for structured fields
- GAS reached Render
- endpoint responded with HTTP `200`
- response status was `success`
- fixed output zone `D2:E8` was written
- visible output values were confirmed

Visible output evidence:

- `validation_status` = `VALIDATED`
- `object_number` = `7445-B`
- `product_type` = `KZO`
- `voltage_class` = `VC_10`
- `busbar_current` = `1250`
- `http_code` = `200`
- `stage` = `4A`

Scope result:

- no Sidebar
- no buttons
- no menus
- no DB
- no Supabase
- no AUTH expansion
- no BOM
- no costing
- no production transfer
- no multi-product support

## Success Definition

Stage 4A is verified only when:

- protected sheet `Stage4A_MVP` exists
- only `B2:B14` is user-editable
- enum-safe inputs are active
- fixed input cells build a valid KZO request
- API returns a successful response
- fixed output zone `D2:E8` is written
- protected structure remains intact

## Next Gate

Next stage must be created through a separate normalized task.

Stage 4A is verified as an MVP-only protected template shell baseline.
