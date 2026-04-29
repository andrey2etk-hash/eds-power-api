# Stage 4B Input Normalization

## Environment

- Stage: Stage 4B — Input Normalization Layer for Google Sheet MVP Shell
- GAS file: `gas/Stage3D_KZO_Handshake.gs`
- Run function: `runStage4BKzoTemplateFlow()`
- Target sheet: `Stage4A_MVP`
- Input range: `B2:B14`
- Output range: `D2:E11`

## Objective

Convert the protected Stage 4A shell into a resilient human-operable MVP shell:

```text
manual input -> GAS preflight -> safe request -> API validation -> stable output
```

## What Was Added

- Stage 4B run function
- input normalization helpers
- required field gate
- enum verification
- safe numeric parsing
- local input error writeback
- output additions for local preflight status

## Input Normalization Rules

Empty normalization:

- blank -> `null`
- `N/A` -> `null`
- whitespace trim

Required fields:

- `object_number`
- `product_type`
- `logic_version`
- `voltage_class`
- `busbar_current`
- `configuration_type`
- `quantity_total`
- `CELL_INCOMER`
- `CELL_OUTGOING`
- `CELL_PT`
- `CELL_BUS_SECTION`
- `status`

Optional fields:

- `breaker_type`

## Enum Verification

Allowed local enum maps:

- `product_type`: `KZO`
- `logic_version`: `KZO_MVP_V1`
- `voltage_class`: `VC_06`, `VC_10`, `VC_20`, `VC_35`
- `configuration_type`: `CFG_SINGLE_BUS`, `CFG_SINGLE_BUS_SECTION`
- `status`: `DRAFT`

Enum mismatch writes a local error and blocks the API call.

## Numeric Parsing

Numeric fields:

- `busbar_current`
- `quantity_total`
- `CELL_INCOMER`
- `CELL_OUTGOING`
- `CELL_PT`
- `CELL_BUS_SECTION`

Rules:

- trim string input
- parse only deterministic numeric values
- reject malformed values
- no silent coercion

## Local Input Error Codes

Stage 4B local errors:

- `INPUT_ERROR_MISSING_REQUIRED`
- `INPUT_ERROR_BAD_ENUM`
- `INPUT_ERROR_BAD_NUMBER`

If a local input error occurs:

- no API request is sent
- output zone is written locally
- `local_input_status` = `ERROR`
- `error_code` is written
- `error_field` is written

## Output Zone Additions

Stage 4B writes `D2:E11`:

| Cell | Field |
|---|---|
| `E2` | `validation_status` |
| `E3` | `object_number` |
| `E4` | `product_type` |
| `E5` | `voltage_class` |
| `E6` | `busbar_current` |
| `E7` | `http_code` |
| `E8` | `stage` |
| `E9` | `local_input_status` |
| `E10` | `error_code` |
| `E11` | `error_field` |

## Thin Client Law

Allowed in GAS:

- sanitize
- format
- structure validate
- transport
- write local preflight errors

Forbidden in GAS:

- business calculations
- engineering logic
- product intelligence
- hidden rule engine

## API Law

Final validation remains API responsibility.

GAS preflight only blocks obvious local input mistakes before transport.

## Explicitly Not Added

- Sidebar
- advanced UI
- batch
- DB
- Supabase
- product expansion
- business rule migration
- API contract changes

## Execution Result

Status: `VERIFIED_STRUCTURAL_PREFLIGHT`

Manual Stage 4B input resilience tests were observed.

Observed missing required input test:

```text
13:35:00  Execution started
13:35:41  {"stage":"4B","status":"local_input_error","error":{"error_code":"INPUT_ERROR_MISSING_REQUIRED","message":"Required input is missing","error_field":"object_number"}}
13:35:02  Execution completed
```

Observed valid input flows:

```text
13:35:36  Execution started
13:36:18  {"stage":"4B","http_code":200,"local_input_status":"OK","status":"success","error":null}
13:36:18  {"stage":"4B","status":"writeback_completed","sheet":"Stage4A_MVP","range":"D2:E11"}
13:35:37  Execution completed

13:36:21  Execution started
13:37:03  {"stage":"4B","http_code":200,"local_input_status":"OK","status":"success","error":null}
13:37:03  {"stage":"4B","status":"writeback_completed","sheet":"Stage4A_MVP","range":"D2:E11"}
13:36:23  Execution completed

13:37:08  Execution started
13:37:50  {"stage":"4B","http_code":200,"local_input_status":"OK","status":"success","error":null}
13:37:50  {"stage":"4B","status":"writeback_completed","sheet":"Stage4A_MVP","range":"D2:E11"}
13:37:10  Execution completed
```

Observed invalid enum test:

- input: `voltage_class = VC_999`
- result: `local_input_error`
- error code: `INPUT_ERROR_BAD_ENUM`
- error field: `voltage_class`

Observed bad number test:

- input: `busbar_current = abc`
- result: `local_input_error`
- error code: `INPUT_ERROR_BAD_NUMBER`
- error field: `busbar_current`

Verified:

- missing required input is blocked locally
- no API request is sent for missing `object_number`
- local error code `INPUT_ERROR_MISSING_REQUIRED` is emitted
- local error field `object_number` is emitted
- invalid enum input is blocked locally
- local error code `INPUT_ERROR_BAD_ENUM` is emitted
- local error field `voltage_class` is emitted
- malformed numeric input is blocked locally
- local error code `INPUT_ERROR_BAD_NUMBER` is emitted
- local error field `busbar_current` is emitted
- valid input reaches Render
- HTTP code `200` is returned
- response status is `success`
- `local_input_status` is `OK`
- output range `D2:E11` is written

Observation:

- non-empty `object_number` values are treated as structurally present by Stage 4B preflight.
- object number format validation remains outside Stage 4B unless separately normalized as a future rule.

## Success Definition

Stage 4B is verified only when:

- imperfect manual data is normalized safely
- obvious local mistakes are blocked before API call
- local errors write `local_input_status`, `error_code`, and `error_field`
- valid payloads are sent to API
- API validation still returns the final result
- stable output is written to `D2:E11`

## Next Gate

Manual resilience tests:

1. Missing required input. `VERIFIED`
2. Bad enum input. `VERIFIED`
3. Bad numeric input. `VERIFIED`
4. Valid normalized input. `VERIFIED`

Stage 4B = `VERIFIED_STRUCTURAL_PREFLIGHT`.
