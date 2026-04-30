const API_URL = "https://eds-power-api.onrender.com/api/calc/prepare_calculation";
/** Stage 8A — insert-only persistence of frozen ``KZO_MVP_SNAPSHOT_V1`` (thin transport; no calc in GAS). */
const KZO_SAVE_SNAPSHOT_URL = "https://eds-power-api.onrender.com/api/kzo/save_snapshot";
const MVP_TIMEOUT_NOTE = "Render free tier may cold-start; Stage 3E manual test may need rerun after wake-up.";
const STAGE_3F_TEST_SHEET_NAME = "Stage3F_Test";
const STAGE_3F_WRITEBACK_RANGE_A1 = "A1:B5";
const STAGE_4A_SHEET_NAME = "Stage4A_MVP";
const STAGE_4A_INPUT_RANGE_A1 = "B2:B14";
const STAGE_4A_OUTPUT_RANGE_A1 = "D2:E8";
const STAGE_4B_OUTPUT_RANGE_A1 = "D2:E11";
const STAGE_4A_PROTECTION_DESCRIPTION = "Stage 4A protected MVP shell";
const STAGE_4C_OUTPUT_RANGE_A1 = "E4:F14";
const STAGE_4C_PROTECTION_DESCRIPTION = "Stage 4C operator-safe KZO shell";
const STAGE_4C_INPUT_RANGES_A1 = ["C4:C6", "C9:C10", "C13:C20"];
const STAGE_5A_OUTPUT_INTEGRATION_RANGE_A1 = "E4:F19";
const STAGE_5C_SHEET_OUTPUT_RANGE_A1 = "E21:F26";
/** Stage 6A — reserved operator block (shell infrastructure only; no Stage 6 engineering logic). */
const STAGE_6A_RESERVED_OPERATOR_BLOCK_RANGE_A1 = "E27:F40";
const STAGE_6A_BLOCK_NAME = "STAGE_6_RESERVED_OPERATOR_BLOCK";
const STAGE_6A_SHELL_BLOCK_VERSION = "KZO_STAGE_6A_OPERATOR_SHELL_V1";
/** Stage 6B — thin writeback for `engineering_class_summary` (same Stage 6 band `E27:F40`). */
const STAGE_6B_ENGINEERING_CLASSIFICATION_RANGE_A1 = STAGE_6A_RESERVED_OPERATOR_BLOCK_RANGE_A1;
/** Stage 6C — thin writeback for `engineering_burden_summary` (same governed Stage 6 band `E27:F40`; overwrites display when run). */
const STAGE_6C_ENGINEERING_BURDEN_RANGE_A1 = STAGE_6A_RESERVED_OPERATOR_BLOCK_RANGE_A1;
/** Stage 7A — unified MVP writes `engineering_class_summary` + `engineering_burden_summary` in one `E27:F40` setValues (same band; no new API math). */
const STAGE_7A_KZO_MVP_STAGE6_BAND_RANGE_A1 = STAGE_6A_RESERVED_OPERATOR_BLOCK_RANGE_A1;
const STAGE_4A_CELL_MAP = {
  object_number: "B2",
  product_type: "B3",
  logic_version: "B4",
  voltage_class: "B5",
  busbar_current: "B6",
  configuration_type: "B7",
  quantity_total: "B8",
  cell_incomer: "B9",
  cell_outgoing: "B10",
  cell_pt: "B11",
  cell_bus_section: "B12",
  status: "B13",
  breaker_type: "B14"
};
const STAGE_4C_CELL_MAP = {
  object_number: "C4",
  product_type: "C5",
  logic_version: "C6",
  voltage_class: "C9",
  busbar_current: "C10",
  configuration_type: "C13",
  quantity_total: "C14",
  cell_incomer: "C15",
  cell_outgoing: "C16",
  cell_pt: "C17",
  cell_bus_section: "C18",
  status: "C19",
  breaker_type: "C20"
};
const STAGE_4B_REQUIRED_FIELDS = [
  "object_number",
  "product_type",
  "logic_version",
  "voltage_class",
  "busbar_current",
  "configuration_type",
  "quantity_total",
  "cell_incomer",
  "cell_outgoing",
  "cell_pt",
  "cell_bus_section",
  "status"
];
const STAGE_4B_ENUM_FIELDS = {
  product_type: ["KZO"],
  logic_version: ["KZO_MVP_V1"],
  voltage_class: ["VC_06", "VC_10", "VC_20", "VC_35"],
  configuration_type: ["CFG_SINGLE_BUS", "CFG_SINGLE_BUS_SECTION"],
  status: ["DRAFT"]
};
const STAGE_4B_NUMBER_FIELDS = [
  "busbar_current",
  "quantity_total",
  "cell_incomer",
  "cell_outgoing",
  "cell_pt",
  "cell_bus_section"
];

/**
 * Stage 3D minimal GAS -> Render API handshake.
 *
 * GAS is a thin client only:
 * - builds one valid KZO MVP request
 * - sends JSON to the API
 * - logs the API response
 * - does not perform validation, calculation, costing, BOM, DB, or production logic
 */
function buildStage3DKzoPayload() {
  return {
    meta: {
      request_id: Utilities.getUuid(),
      source: "gas",
      user_id: "manual_test_user",
      session_token: "manual_test_session",
      timestamp: new Date().toISOString()
    },
    module: "CALC_CONFIGURATOR",
    action: "prepare_calculation",
    payload: {
      object_number: "7445-B",
      product_type: "KZO",
      logic_version: "KZO_MVP_V1",
      voltage_class: "VC_10",
      busbar_current: 1250,
      configuration_type: "CFG_SINGLE_BUS_SECTION",
      quantity_total: 22,
      cell_distribution: {
        CELL_INCOMER: 2,
        CELL_OUTGOING: 16,
        CELL_PT: 2,
        CELL_BUS_SECTION: 2
      },
      status: "DRAFT",
      breaker_type: null,
      notes: null
    }
  };
}

function testKzoPrepareCalculation() {
  const requestBody = buildStage3DKzoPayload();
  const options = {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(requestBody),
    muteHttpExceptions: true
  };

  try {
    const response = UrlFetchApp.fetch(API_URL, options);
    const httpCode = response.getResponseCode();
    const responseText = response.getContentText();
    const responseJson = JSON.parse(responseText);

    Logger.log(JSON.stringify({
      http_code: httpCode,
      status: responseJson.status || null,
      error: responseJson.error || null
    }));

    if (responseJson.status === "success") {
      Logger.log(JSON.stringify({
        basic_result_summary: responseJson.data && responseJson.data.basic_result_summary
          ? responseJson.data.basic_result_summary
          : null
      }));
      return;
    }

    if (responseJson.status === "timeout") {
      Logger.log(JSON.stringify({
        status: "timeout",
        note: MVP_TIMEOUT_NOTE,
        error: responseJson.error || {
          error_code: "REQUEST_TIMEOUT",
          message: "Request timed out"
        },
        retry: false
      }));
      return;
    }

    Logger.log(JSON.stringify({
      status: responseJson.status || "error",
      error: responseJson.error || {
        error_code: "UNKNOWN_API_RESPONSE",
        message: "API returned a non-success response"
      }
    }));
  } catch (error) {
    Logger.log(JSON.stringify({
      status: "request_failed",
      error: {
        error_code: "GAS_REQUEST_FAILED",
        message: error && error.message ? error.message : String(error),
        note: MVP_TIMEOUT_NOTE
      },
      retry: false
    }));
  }
}

/**
 * Stage 3F minimal visible Sheet writeback.
 *
 * GAS remains request / response / writeback only:
 * - reuses the Stage 3D request
 * - reads the API response
 * - writes selected normalized response fields into a fixed test range
 * - does not calculate, validate, format UI, create buttons, or change architecture
 */
function testKzoPrepareCalculationWithSheetWriteback() {
  const requestBody = buildStage3DKzoPayload();
  const options = {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(requestBody),
    muteHttpExceptions: true
  };

  try {
    const response = UrlFetchApp.fetch(API_URL, options);
    const httpCode = response.getResponseCode();
    const responseText = response.getContentText();
    const responseJson = JSON.parse(responseText);

    Logger.log(JSON.stringify({
      stage: "3F",
      http_code: httpCode,
      status: responseJson.status || null,
      error: responseJson.error || null
    }));

    if (responseJson.status !== "success") {
      Logger.log(JSON.stringify({
        stage: "3F",
        status: "writeback_skipped",
        reason: "API response was not successful"
      }));
      return;
    }

    writeStage3FTestRange(responseJson);
  } catch (error) {
    Logger.log(JSON.stringify({
      stage: "3F",
      status: "request_or_writeback_failed",
      error: {
        error_code: "GAS_STAGE_3F_FAILED",
        message: error && error.message ? error.message : String(error),
        note: MVP_TIMEOUT_NOTE
      },
      retry: false
    }));
  }
}

function writeStage3FTestRange(responseJson) {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = spreadsheet ? spreadsheet.getSheetByName(STAGE_3F_TEST_SHEET_NAME) : null;

  if (!sheet) {
    Logger.log(JSON.stringify({
      stage: "3F",
      status: "writeback_skipped",
      error: {
        error_code: "STAGE_3F_TEST_SHEET_MISSING",
        message: "Create a test sheet named Stage3F_Test before running Stage 3F writeback."
      }
    }));
    return;
  }

  const data = responseJson.data || {};
  const summary = data.basic_result_summary || {};
  const normalizedPayload = data.normalized_payload || {};
  const rows = [
    ["validation_status", firstDefined(data.validation_status, summary.validation_status)],
    ["object_number", firstDefined(normalizedPayload.object_number, null)],
    ["product_type", firstDefined(summary.product_type, normalizedPayload.product_type)],
    ["voltage_class", firstDefined(summary.voltage_class, normalizedPayload.voltage_class)],
    ["busbar_current", firstDefined(summary.busbar_current, normalizedPayload.busbar_current)]
  ];

  sheet.getRange(STAGE_3F_WRITEBACK_RANGE_A1).setValues(rows);

  Logger.log(JSON.stringify({
    stage: "3F",
    status: "writeback_completed",
    sheet: STAGE_3F_TEST_SHEET_NAME,
    range: STAGE_3F_WRITEBACK_RANGE_A1
  }));
}

function firstDefined(primaryValue, fallbackValue) {
  return primaryValue === undefined || primaryValue === null ? fallbackValue : primaryValue;
}

/**
 * Stage 4A protected template shell setup.
 *
 * This creates only a deterministic MVP shell:
 * - fixed input cells
 * - fixed output cells
 * - enum-safe input validation where possible
 * - sheet protection with input cells left editable
 *
 * It does not add sidebar, buttons, menus, formulas, DB, Supabase, AUTH, BOM,
 * costing, production transfer, or business logic.
 */
function setupStage4ATemplateShell() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  if (!spreadsheet) {
    Logger.log(JSON.stringify({
      stage: "4A",
      status: "setup_failed",
      error: {
        error_code: "SPREADSHEET_NOT_FOUND",
        message: "Active spreadsheet is required for Stage 4A template setup."
      }
    }));
    return;
  }

  const sheet = getOrCreateStage4ASheet_(spreadsheet);
  writeStage4AShellLayout_(sheet);
  applyStage4AInputValidation_(sheet);
  protectStage4AShell_(sheet);

  Logger.log(JSON.stringify({
    stage: "4A",
    status: "template_shell_prepared",
    sheet: STAGE_4A_SHEET_NAME,
    input_range: STAGE_4A_INPUT_RANGE_A1,
    output_range: STAGE_4A_OUTPUT_RANGE_A1
  }));
}

/**
 * Stage 4A fixed-cell operational shell.
 *
 * GAS remains thin:
 * - reads fixed cells
 * - builds the request
 * - sends the API request
 * - parses response
 * - writes fixed outputs
 */
function runStage4AKzoTemplateFlow() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = spreadsheet ? spreadsheet.getSheetByName(STAGE_4A_SHEET_NAME) : null;

  if (!sheet) {
    Logger.log(JSON.stringify({
      stage: "4A",
      status: "run_skipped",
      error: {
        error_code: "STAGE_4A_TEMPLATE_SHEET_MISSING",
        message: "Run setupStage4ATemplateShell() before Stage 4A execution."
      }
    }));
    return;
  }

  const requestBody = buildStage4AKzoPayloadFromSheet_(sheet);
  const options = {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(requestBody),
    muteHttpExceptions: true
  };

  try {
    const response = UrlFetchApp.fetch(API_URL, options);
    const httpCode = response.getResponseCode();
    const responseText = response.getContentText();
    const responseJson = JSON.parse(responseText);

    Logger.log(JSON.stringify({
      stage: "4A",
      http_code: httpCode,
      status: responseJson.status || null,
      error: responseJson.error || null
    }));

    writeStage4AOutput_(sheet, responseJson, httpCode);
  } catch (error) {
    Logger.log(JSON.stringify({
      stage: "4A",
      status: "request_or_writeback_failed",
      error: {
        error_code: "GAS_STAGE_4A_FAILED",
        message: error && error.message ? error.message : String(error),
        note: MVP_TIMEOUT_NOTE
      },
      retry: false
    }));
  }
}

function getOrCreateStage4ASheet_(spreadsheet) {
  const existingSheet = spreadsheet.getSheetByName(STAGE_4A_SHEET_NAME);
  return existingSheet || spreadsheet.insertSheet(STAGE_4A_SHEET_NAME);
}

function writeStage4AShellLayout_(sheet) {
  sheet.getRange("A1:E14").setValues([
    ["Stage 4A MVP Configurator Shell", "", "", "Stage 4A Outputs", ""],
    ["object_number", "7445-B", "", "validation_status", ""],
    ["product_type", "KZO", "", "object_number", ""],
    ["logic_version", "KZO_MVP_V1", "", "product_type", ""],
    ["voltage_class", "VC_10", "", "voltage_class", ""],
    ["busbar_current", 1250, "", "busbar_current", ""],
    ["configuration_type", "CFG_SINGLE_BUS_SECTION", "", "http_code", ""],
    ["quantity_total", 22, "", "stage", ""],
    ["CELL_INCOMER", 2, "", "local_input_status", ""],
    ["CELL_OUTGOING", 16, "", "error_code", ""],
    ["CELL_PT", 2, "", "error_field", ""],
    ["CELL_BUS_SECTION", 2, "", "", ""],
    ["status", "DRAFT", "", "", ""],
    ["breaker_type", "", "", "", ""]
  ]);
}

function applyStage4AInputValidation_(sheet) {
  setListValidation_(sheet.getRange(STAGE_4A_CELL_MAP.product_type), ["KZO"]);
  setListValidation_(sheet.getRange(STAGE_4A_CELL_MAP.logic_version), ["KZO_MVP_V1"]);
  setListValidation_(sheet.getRange(STAGE_4A_CELL_MAP.voltage_class), ["VC_06", "VC_10", "VC_20", "VC_35"]);
  setListValidation_(sheet.getRange(STAGE_4A_CELL_MAP.configuration_type), ["CFG_SINGLE_BUS", "CFG_SINGLE_BUS_SECTION"]);
  setListValidation_(sheet.getRange(STAGE_4A_CELL_MAP.status), ["DRAFT"]);

  const positiveNumberRule = SpreadsheetApp.newDataValidation()
    .requireNumberGreaterThan(0)
    .setAllowInvalid(false)
    .build();

  [
    STAGE_4A_CELL_MAP.busbar_current,
    STAGE_4A_CELL_MAP.quantity_total,
    STAGE_4A_CELL_MAP.cell_incomer,
    STAGE_4A_CELL_MAP.cell_outgoing,
    STAGE_4A_CELL_MAP.cell_pt,
    STAGE_4A_CELL_MAP.cell_bus_section
  ].forEach(function(cellA1) {
    sheet.getRange(cellA1).setDataValidation(positiveNumberRule);
  });
}

function setListValidation_(range, values) {
  const rule = SpreadsheetApp.newDataValidation()
    .requireValueInList(values, true)
    .setAllowInvalid(false)
    .build();

  range.setDataValidation(rule);
}

function protectStage4AShell_(sheet) {
  const existingProtections = sheet.getProtections(SpreadsheetApp.ProtectionType.SHEET);
  existingProtections.forEach(function(protection) {
    if (protection.getDescription() === STAGE_4A_PROTECTION_DESCRIPTION && protection.canEdit()) {
      protection.remove();
    }
  });

  const protection = sheet.protect().setDescription(STAGE_4A_PROTECTION_DESCRIPTION);
  protection.setWarningOnly(false);
  protection.setUnprotectedRanges([sheet.getRange(STAGE_4A_INPUT_RANGE_A1)]);
}

function buildStage4AKzoPayloadFromSheet_(sheet) {
  return {
    meta: {
      request_id: Utilities.getUuid(),
      source: "gas",
      user_id: "manual_test_user",
      session_token: "manual_test_session",
      timestamp: new Date().toISOString()
    },
    module: "CALC_CONFIGURATOR",
    action: "prepare_calculation",
    payload: {
      object_number: getStage4ACellValue_(sheet, "object_number"),
      product_type: getStage4ACellValue_(sheet, "product_type"),
      logic_version: getStage4ACellValue_(sheet, "logic_version"),
      voltage_class: getStage4ACellValue_(sheet, "voltage_class"),
      busbar_current: Number(getStage4ACellValue_(sheet, "busbar_current")),
      configuration_type: getStage4ACellValue_(sheet, "configuration_type"),
      quantity_total: Number(getStage4ACellValue_(sheet, "quantity_total")),
      cell_distribution: {
        CELL_INCOMER: Number(getStage4ACellValue_(sheet, "cell_incomer")),
        CELL_OUTGOING: Number(getStage4ACellValue_(sheet, "cell_outgoing")),
        CELL_PT: Number(getStage4ACellValue_(sheet, "cell_pt")),
        CELL_BUS_SECTION: Number(getStage4ACellValue_(sheet, "cell_bus_section"))
      },
      status: getStage4ACellValue_(sheet, "status"),
      breaker_type: getStage4ACellValue_(sheet, "breaker_type") || null,
      notes: null
    }
  };
}

function getStage4ACellValue_(sheet, fieldName) {
  return sheet.getRange(STAGE_4A_CELL_MAP[fieldName]).getValue();
}

function writeStage4AOutput_(sheet, responseJson, httpCode) {
  const data = responseJson.data || {};
  const summary = data.basic_result_summary || {};
  const normalizedPayload = data.normalized_payload || {};
  const rows = [
    ["validation_status", firstDefined(data.validation_status, summary.validation_status)],
    ["object_number", firstDefined(normalizedPayload.object_number, null)],
    ["product_type", firstDefined(summary.product_type, normalizedPayload.product_type)],
    ["voltage_class", firstDefined(summary.voltage_class, normalizedPayload.voltage_class)],
    ["busbar_current", firstDefined(summary.busbar_current, normalizedPayload.busbar_current)],
    ["http_code", httpCode],
    ["stage", "4A"]
  ];

  sheet.getRange(STAGE_4A_OUTPUT_RANGE_A1).setValues(rows);

  Logger.log(JSON.stringify({
    stage: "4A",
    status: "writeback_completed",
    sheet: STAGE_4A_SHEET_NAME,
    range: STAGE_4A_OUTPUT_RANGE_A1
  }));
}

/**
 * Stage 4B resilient manual-input flow.
 *
 * GAS performs pre-flight safety only:
 * - normalize raw Sheet values
 * - block obvious structural input mistakes locally
 * - send only a safe request shape to the API
 *
 * Final validation remains the API source of truth.
 */
function runStage4BKzoTemplateFlow() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = spreadsheet ? spreadsheet.getSheetByName(STAGE_4A_SHEET_NAME) : null;

  if (!sheet) {
    Logger.log(JSON.stringify({
      stage: "4B",
      status: "run_skipped",
      error: {
        error_code: "STAGE_4A_TEMPLATE_SHEET_MISSING",
        message: "Run setupStage4ATemplateShell() before Stage 4B execution."
      }
    }));
    return;
  }

  const preflight = buildStage4BPreflightPayload_(sheet);

  if (!preflight.ok) {
    writeStage4BLocalInputError_(sheet, preflight.error);
    Logger.log(JSON.stringify({
      stage: "4B",
      status: "local_input_error",
      error: preflight.error
    }));
    return;
  }

  const requestBody = buildStage4BRequestBody_(preflight.values);
  const options = {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(requestBody),
    muteHttpExceptions: true
  };

  try {
    const response = UrlFetchApp.fetch(API_URL, options);
    const httpCode = response.getResponseCode();
    const responseText = response.getContentText();
    const responseJson = JSON.parse(responseText);

    Logger.log(JSON.stringify({
      stage: "4B",
      http_code: httpCode,
      local_input_status: "OK",
      status: responseJson.status || null,
      error: responseJson.error || null
    }));

    writeStage4BOutput_(sheet, responseJson, httpCode, {
      local_input_status: "OK",
      error_code: null,
      error_field: null
    });
  } catch (error) {
    Logger.log(JSON.stringify({
      stage: "4B",
      status: "request_or_writeback_failed",
      error: {
        error_code: "GAS_STAGE_4B_FAILED",
        message: error && error.message ? error.message : String(error),
        note: MVP_TIMEOUT_NOTE
      },
      retry: false
    }));
  }
}

function buildStage4BPreflightPayload_(sheet) {
  return buildStage4PreflightPayload_(sheet, STAGE_4A_CELL_MAP);
}

function buildStage4PreflightPayload_(sheet, cellMap) {
  const values = {};

  Object.keys(cellMap).forEach(function(fieldName) {
    values[fieldName] = normalizeStage4BCellValue_(getStage4CellValue_(sheet, fieldName, cellMap));
  });

  for (let i = 0; i < STAGE_4B_REQUIRED_FIELDS.length; i += 1) {
    const fieldName = STAGE_4B_REQUIRED_FIELDS[i];
    if (values[fieldName] === null) {
      return {
        ok: false,
        error: {
          error_code: "INPUT_ERROR_MISSING_REQUIRED",
          message: "Required input is missing",
          error_field: fieldName
        }
      };
    }
  }

  const enumFields = Object.keys(STAGE_4B_ENUM_FIELDS);
  for (let i = 0; i < enumFields.length; i += 1) {
    const fieldName = enumFields[i];
    if (STAGE_4B_ENUM_FIELDS[fieldName].indexOf(values[fieldName]) === -1) {
      return {
        ok: false,
        error: {
          error_code: "INPUT_ERROR_BAD_ENUM",
          message: "Input does not match allowed enum values",
          error_field: fieldName
        }
      };
    }
  }

  for (let i = 0; i < STAGE_4B_NUMBER_FIELDS.length; i += 1) {
    const fieldName = STAGE_4B_NUMBER_FIELDS[i];
    const parsedNumber = parseStage4BNumber_(values[fieldName]);

    if (parsedNumber === null) {
      return {
        ok: false,
        error: {
          error_code: "INPUT_ERROR_BAD_NUMBER",
          message: "Input must be a valid number",
          error_field: fieldName
        }
      };
    }

    values[fieldName] = parsedNumber;
  }

  return {
    ok: true,
    values: values
  };
}

function getStage4CellValue_(sheet, fieldName, cellMap) {
  return sheet.getRange(cellMap[fieldName]).getValue();
}

function normalizeStage4BCellValue_(value) {
  if (value === null || value === undefined) {
    return null;
  }

  if (typeof value === "string") {
    const trimmedValue = value.trim();

    if (trimmedValue === "" || trimmedValue.toUpperCase() === "N/A") {
      return null;
    }

    return trimmedValue;
  }

  return value;
}

function parseStage4BNumber_(value) {
  if (typeof value === "number" && isFinite(value)) {
    return value;
  }

  if (typeof value !== "string") {
    return null;
  }

  const normalizedValue = value.trim();

  if (!/^-?\d+(\.\d+)?$/.test(normalizedValue)) {
    return null;
  }

  const parsedNumber = Number(normalizedValue);
  return isFinite(parsedNumber) ? parsedNumber : null;
}

function buildStage4BRequestBody_(values) {
  return {
    meta: {
      request_id: Utilities.getUuid(),
      source: "gas",
      user_id: "manual_test_user",
      session_token: "manual_test_session",
      timestamp: new Date().toISOString()
    },
    module: "CALC_CONFIGURATOR",
    action: "prepare_calculation",
    payload: {
      object_number: values.object_number,
      product_type: values.product_type,
      logic_version: values.logic_version,
      voltage_class: values.voltage_class,
      busbar_current: values.busbar_current,
      configuration_type: values.configuration_type,
      quantity_total: values.quantity_total,
      cell_distribution: {
        CELL_INCOMER: values.cell_incomer,
        CELL_OUTGOING: values.cell_outgoing,
        CELL_PT: values.cell_pt,
        CELL_BUS_SECTION: values.cell_bus_section
      },
      status: values.status,
      breaker_type: values.breaker_type,
      notes: null
    }
  };
}

function writeStage4BLocalInputError_(sheet, error) {
  const rows = [
    ["validation_status", null],
    ["object_number", null],
    ["product_type", null],
    ["voltage_class", null],
    ["busbar_current", null],
    ["http_code", null],
    ["stage", "4B"],
    ["local_input_status", "ERROR"],
    ["error_code", error.error_code],
    ["error_field", error.error_field]
  ];

  sheet.getRange(STAGE_4B_OUTPUT_RANGE_A1).setValues(rows);
}

function writeStage4BOutput_(sheet, responseJson, httpCode, localStatus) {
  const data = responseJson.data || {};
  const summary = data.basic_result_summary || {};
  const normalizedPayload = data.normalized_payload || {};
  const rows = [
    ["validation_status", firstDefined(data.validation_status, summary.validation_status)],
    ["object_number", firstDefined(normalizedPayload.object_number, null)],
    ["product_type", firstDefined(summary.product_type, normalizedPayload.product_type)],
    ["voltage_class", firstDefined(summary.voltage_class, normalizedPayload.voltage_class)],
    ["busbar_current", firstDefined(summary.busbar_current, normalizedPayload.busbar_current)],
    ["http_code", httpCode],
    ["stage", "4B"],
    ["local_input_status", localStatus.local_input_status],
    ["error_code", localStatus.error_code],
    ["error_field", localStatus.error_field]
  ];

  sheet.getRange(STAGE_4B_OUTPUT_RANGE_A1).setValues(rows);

  Logger.log(JSON.stringify({
    stage: "4B",
    status: "writeback_completed",
    sheet: STAGE_4A_SHEET_NAME,
    range: STAGE_4B_OUTPUT_RANGE_A1
  }));
}

/**
 * Stage 4C operator-safe shell setup.
 *
 * This hardens the existing KZO shell for operator use:
 * - grouped input sections
 * - clearer labels and operator notes
 * - protected zones around non-input cells
 * - stable dropdowns and numeric cells
 *
 * It does not add sidebar, buttons, menus, formulas, pricing, BOM, DB,
 * Supabase, multi-product flow, or business logic.
 */
function setupStage4COperatorShell() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  if (!spreadsheet) {
    Logger.log(JSON.stringify({
      stage: "4C",
      telemetry_tag: "stage=4C",
      status: "setup_failed",
      error: {
        error_code: "SPREADSHEET_NOT_FOUND",
        message: "Active spreadsheet is required for Stage 4C operator shell setup."
      }
    }));
    return;
  }

  const sheet = getOrCreateStage4ASheet_(spreadsheet);
  writeStage4COperatorShellLayout_(sheet);
  applyStage4CInputValidation_(sheet);
  protectStage4COperatorShell_(sheet);

  Logger.log(JSON.stringify({
    stage: "4C",
    telemetry_tag: "stage=4C",
    status: "operator_shell_prepared",
    sheet: STAGE_4A_SHEET_NAME,
    input_ranges: STAGE_4C_INPUT_RANGES_A1,
    output_range: STAGE_4C_OUTPUT_RANGE_A1,
    operator_flow_improvements: [
      "grouped identity inputs",
      "grouped electrical inputs",
      "grouped cell distribution inputs",
      "operator notes added",
      "non-input zones protected"
    ]
  }));
}

/**
 * Stage 4C operator shell flow.
 *
 * GAS remains a thin client:
 * - reads the Stage 4C fixed cell map
 * - performs only structural preflight inherited from Stage 4B
 * - sends the request to the API
 * - writes telemetry-tagged output
 */
function runStage4CKzoOperatorShellFlow() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = spreadsheet ? spreadsheet.getSheetByName(STAGE_4A_SHEET_NAME) : null;

  if (!sheet) {
    Logger.log(JSON.stringify({
      stage: "4C",
      telemetry_tag: "stage=4C",
      status: "run_skipped",
      error: {
        error_code: "STAGE_4C_OPERATOR_SHELL_MISSING",
        message: "Run setupStage4COperatorShell() before Stage 4C execution."
      }
    }));
    return;
  }

  const preflight = buildStage4PreflightPayload_(sheet, STAGE_4C_CELL_MAP);

  if (!preflight.ok) {
    writeStage4CLocalInputError_(sheet, preflight.error);
    Logger.log(JSON.stringify({
      stage: "4C",
      telemetry_tag: "stage=4C",
      status: "local_input_error",
      error: preflight.error
    }));
    return;
  }

  const requestBody = buildStage4BRequestBody_(preflight.values);
  const options = {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(requestBody),
    muteHttpExceptions: true
  };

  try {
    const response = UrlFetchApp.fetch(API_URL, options);
    const httpCode = response.getResponseCode();
    const responseText = response.getContentText();
    const responseJson = JSON.parse(responseText);

    Logger.log(JSON.stringify({
      stage: "4C",
      telemetry_tag: "stage=4C",
      http_code: httpCode,
      local_input_status: "OK",
      status: responseJson.status || null,
      error: responseJson.error || null
    }));

    writeStage4COutput_(sheet, responseJson, httpCode, {
      local_input_status: "OK",
      error_code: null,
      error_field: null
    });
  } catch (error) {
    Logger.log(JSON.stringify({
      stage: "4C",
      telemetry_tag: "stage=4C",
      status: "request_or_writeback_failed",
      error: {
        error_code: "GAS_STAGE_4C_FAILED",
        message: error && error.message ? error.message : String(error),
        note: MVP_TIMEOUT_NOTE
      },
      retry: false
    }));
  }
}

function writeStage4COperatorShellLayout_(sheet) {
  sheet.clear();
  sheet.getRange("A1:F22").clearDataValidations();
  sheet.getRange("A1:F22").setValues([
    ["Stage 4C KZO Operator Shell", "", "", "", "Stage 4C Outputs", ""],
    ["Use only the input cells in column C. Protected zones define labels, notes, and results.", "", "", "", "", ""],
    ["Section", "Field", "Operator input", "Operator note", "Output field", "Output value"],
    ["Object identity", "object_number", "7445-B", "Required. API validates final format.", "validation_status", ""],
    ["Object identity", "product_type", "KZO", "Dropdown locked to KZO.", "object_number", ""],
    ["Object identity", "logic_version", "KZO_MVP_V1", "Dropdown locked to current MVP version.", "product_type", ""],
    ["", "", "", "", "voltage_class", ""],
    ["Electrical parameters", "", "", "", "busbar_current", ""],
    ["Electrical parameters", "voltage_class", "VC_10", "Dropdown from MVP allowed values.", "http_code", ""],
    ["Electrical parameters", "busbar_current", 1250, "Positive number only.", "stage", ""],
    ["", "", "", "", "local_input_status", ""],
    ["Cell distribution", "", "", "", "error_code", ""],
    ["Cell distribution", "configuration_type", "CFG_SINGLE_BUS_SECTION", "Dropdown from MVP allowed values.", "error_field", ""],
    ["Cell distribution", "quantity_total", 22, "Positive number only.", "operator_shell_status", ""],
    ["Cell distribution", "CELL_INCOMER", 2, "Positive number only.", "", ""],
    ["Cell distribution", "CELL_OUTGOING", 16, "Positive number only.", "", ""],
    ["Cell distribution", "CELL_PT", 2, "Positive number only.", "", ""],
    ["Cell distribution", "CELL_BUS_SECTION", 2, "Positive number only.", "", ""],
    ["Workflow status", "status", "DRAFT", "Dropdown locked to DRAFT for MVP.", "", ""],
    ["Optional input", "breaker_type", "", "Optional. Blank is allowed and sent as null.", "", ""],
    ["Operator rule", "Run flow only after reviewing all column C inputs.", "", "Telemetry tag", "stage=4C", ""],
    ["Scope guard", "No practical KZO logic, pricing, BOM, DB, sidebar, buttons, or menus in Stage 4C.", "", "", "", ""]
  ]);

  sheet.setFrozenRows(3);
  sheet.getRange("A1:F1").setFontWeight("bold");
  sheet.getRange("A3:F3").setFontWeight("bold");
  sheet.getRange("C4:C20").setFontWeight("bold");
  sheet.autoResizeColumns(1, 6);
}

function applyStage4CInputValidation_(sheet) {
  setListValidation_(sheet.getRange(STAGE_4C_CELL_MAP.product_type), ["KZO"]);
  setListValidation_(sheet.getRange(STAGE_4C_CELL_MAP.logic_version), ["KZO_MVP_V1"]);
  setListValidation_(sheet.getRange(STAGE_4C_CELL_MAP.voltage_class), ["VC_06", "VC_10", "VC_20", "VC_35"]);
  setListValidation_(sheet.getRange(STAGE_4C_CELL_MAP.configuration_type), ["CFG_SINGLE_BUS", "CFG_SINGLE_BUS_SECTION"]);
  setListValidation_(sheet.getRange(STAGE_4C_CELL_MAP.status), ["DRAFT"]);

  const positiveNumberRule = SpreadsheetApp.newDataValidation()
    .requireNumberGreaterThan(0)
    .setAllowInvalid(false)
    .build();

  [
    STAGE_4C_CELL_MAP.busbar_current,
    STAGE_4C_CELL_MAP.quantity_total,
    STAGE_4C_CELL_MAP.cell_incomer,
    STAGE_4C_CELL_MAP.cell_outgoing,
    STAGE_4C_CELL_MAP.cell_pt,
    STAGE_4C_CELL_MAP.cell_bus_section
  ].forEach(function(cellA1) {
    sheet.getRange(cellA1).setDataValidation(positiveNumberRule);
  });
}

function protectStage4COperatorShell_(sheet) {
  const existingProtections = sheet.getProtections(SpreadsheetApp.ProtectionType.SHEET);
  existingProtections.forEach(function(protection) {
    const description = protection.getDescription();
    if (
      protection.canEdit()
      && (description === STAGE_4A_PROTECTION_DESCRIPTION || description === STAGE_4C_PROTECTION_DESCRIPTION)
    ) {
      protection.remove();
    }
  });

  const unprotectedRanges = STAGE_4C_INPUT_RANGES_A1.map(function(rangeA1) {
    return sheet.getRange(rangeA1);
  });
  const protection = sheet.protect().setDescription(STAGE_4C_PROTECTION_DESCRIPTION);
  protection.setWarningOnly(false);
  protection.setUnprotectedRanges(unprotectedRanges);
}

function writeStage4CLocalInputError_(sheet, error) {
  const rows = [
    ["validation_status", null],
    ["object_number", null],
    ["product_type", null],
    ["voltage_class", null],
    ["busbar_current", null],
    ["http_code", null],
    ["stage", "4C"],
    ["local_input_status", "ERROR"],
    ["error_code", error.error_code],
    ["error_field", error.error_field],
    ["operator_shell_status", "STRUCTURAL_INPUT_BLOCKED"]
  ];

  sheet.getRange(STAGE_4C_OUTPUT_RANGE_A1).setValues(rows);
}

function writeStage4COutput_(sheet, responseJson, httpCode, localStatus) {
  const data = responseJson.data || {};
  const summary = data.basic_result_summary || {};
  const normalizedPayload = data.normalized_payload || {};
  const rows = [
    ["validation_status", firstDefined(data.validation_status, summary.validation_status)],
    ["object_number", firstDefined(normalizedPayload.object_number, null)],
    ["product_type", firstDefined(summary.product_type, normalizedPayload.product_type)],
    ["voltage_class", firstDefined(summary.voltage_class, normalizedPayload.voltage_class)],
    ["busbar_current", firstDefined(summary.busbar_current, normalizedPayload.busbar_current)],
    ["http_code", httpCode],
    ["stage", "4C"],
    ["local_input_status", localStatus.local_input_status],
    ["error_code", localStatus.error_code],
    ["error_field", localStatus.error_field],
    ["operator_shell_status", "OPERATOR_SHELL_FLOW_COMPLETED"]
  ];

  sheet.getRange(STAGE_4C_OUTPUT_RANGE_A1).setValues(rows);

  Logger.log(JSON.stringify({
    stage: "4C",
    telemetry_tag: "stage=4C",
    status: "writeback_completed",
    sheet: STAGE_4A_SHEET_NAME,
    range: STAGE_4C_OUTPUT_RANGE_A1,
    protected_zone_map: {
      sheet_protection: STAGE_4C_PROTECTION_DESCRIPTION,
      editable_input_ranges: STAGE_4C_INPUT_RANGES_A1
    }
  }));
}

/**
 * Stage 5A output visibility integration.
 *
 * GAS remains transport/writeback only:
 * - reads the already verified Stage 4C input map
 * - calls the API
 * - displays existing Stage 5A structural output
 *
 * It does not interpret structure, duplicate API logic, calculate, price, build
 * BOM, redesign the Sheet, or migrate product logic into GAS.
 */
function runStage5AOutputIntegrationFlow() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = spreadsheet ? spreadsheet.getSheetByName(STAGE_4A_SHEET_NAME) : null;

  if (!sheet) {
    Logger.log(JSON.stringify({
      stage: "5A_OUTPUT_INTEGRATION",
      telemetry_tag: "stage=5A-output-integration",
      status: "run_skipped",
      error: {
        error_code: "STAGE_4C_OPERATOR_SHELL_MISSING",
        message: "Run setupStage4COperatorShell() before Stage 5A output integration."
      }
    }));
    return;
  }

  const preflight = buildStage4PreflightPayload_(sheet, STAGE_4C_CELL_MAP);

  if (!preflight.ok) {
    writeStage5AOutputIntegrationError_(sheet, preflight.error);
    Logger.log(JSON.stringify({
      stage: "5A_OUTPUT_INTEGRATION",
      telemetry_tag: "stage=5A-output-integration",
      status: "local_input_error",
      error: preflight.error
    }));
    return;
  }

  const requestBody = buildStage4BRequestBody_(preflight.values);
  const options = {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(requestBody),
    muteHttpExceptions: true
  };

  try {
    const response = UrlFetchApp.fetch(API_URL, options);
    const httpCode = response.getResponseCode();
    const responseText = response.getContentText();
    const responseJson = JSON.parse(responseText);

    Logger.log(JSON.stringify({
      stage: "5A_OUTPUT_INTEGRATION",
      telemetry_tag: "stage=5A-output-integration",
      http_code: httpCode,
      local_input_status: "OK",
      status: responseJson.status || null,
      structural_summary_present: Boolean(
        responseJson.data && responseJson.data.structural_composition_summary
      ),
      error: responseJson.error || null
    }));

    writeStage5AOutputIntegration_(sheet, responseJson, httpCode, {
      local_input_status: "OK",
      error_code: null,
      error_field: null
    });
  } catch (error) {
    Logger.log(JSON.stringify({
      stage: "5A_OUTPUT_INTEGRATION",
      telemetry_tag: "stage=5A-output-integration",
      status: "request_or_writeback_failed",
      error: {
        error_code: "GAS_STAGE_5A_OUTPUT_INTEGRATION_FAILED",
        message: error && error.message ? error.message : String(error),
        note: MVP_TIMEOUT_NOTE
      },
      retry: false
    }));
  }
}

function writeStage5AOutputIntegrationError_(sheet, error) {
  const rows = [
    ["validation_status", null],
    ["object_number", null],
    ["product_type", null],
    ["voltage_class", null],
    ["busbar_current", null],
    ["http_code", null],
    ["stage", "5A_OUTPUT_INTEGRATION"],
    ["local_input_status", "ERROR"],
    ["error_code", error.error_code],
    ["error_field", error.error_field],
    ["operator_shell_status", "STRUCTURAL_INPUT_BLOCKED"],
    ["stage5a_summary_version", null],
    ["total_cells", null],
    ["incoming_count", null],
    ["outgoing_count", null],
    ["pt_count", null]
  ];

  sheet.getRange(STAGE_5A_OUTPUT_INTEGRATION_RANGE_A1).setValues(rows);
}

function writeStage5AOutputIntegration_(sheet, responseJson, httpCode, localStatus) {
  const data = responseJson.data || {};
  const summary = data.basic_result_summary || {};
  const normalizedPayload = data.normalized_payload || {};
  const structuralSummary = data.structural_composition_summary || {};
  const lineupSummary = structuralSummary.lineup_summary || {};
  const cellComposition = structuralSummary.cell_composition || {};
  const structuralFlags = structuralSummary.structural_flags || [];

  const rows = [
    ["validation_status", firstDefined(data.validation_status, summary.validation_status)],
    ["object_number", firstDefined(normalizedPayload.object_number, null)],
    ["product_type", firstDefined(summary.product_type, normalizedPayload.product_type)],
    ["voltage_class", firstDefined(summary.voltage_class, normalizedPayload.voltage_class)],
    ["busbar_current", firstDefined(summary.busbar_current, normalizedPayload.busbar_current)],
    ["http_code", httpCode],
    ["stage", "5A_OUTPUT_INTEGRATION"],
    ["local_input_status", localStatus.local_input_status],
    ["error_code", structuralSummary.summary_version ? localStatus.error_code : "STAGE_5A_STRUCTURAL_SUMMARY_MISSING"],
    ["error_field", localStatus.error_field],
    ["operator_shell_status", structuralSummary.summary_version ? "STAGE_5A_OUTPUT_VISIBLE" : "STAGE_5A_OUTPUT_MISSING"],
    ["stage5a_summary_version", firstDefined(structuralSummary.summary_version, null)],
    ["total_cells", firstDefined(lineupSummary.total_cells, null)],
    ["incoming_count", firstDefined(cellComposition.incoming, null)],
    ["outgoing_count", firstDefined(cellComposition.outgoing, null)],
    ["pt_count", firstDefined(cellComposition.pt, null)]
  ];

  sheet.getRange(STAGE_5A_OUTPUT_INTEGRATION_RANGE_A1).setValues(rows);
  sheet.getRange("E20:F20").setValues([
    ["structural_flags", structuralFlags.join(", ")]
  ]);

  Logger.log(JSON.stringify({
    stage: "5A_OUTPUT_INTEGRATION",
    telemetry_tag: "stage=5A-output-integration",
    status: "writeback_completed",
    sheet: STAGE_4A_SHEET_NAME,
    range: STAGE_5A_OUTPUT_INTEGRATION_RANGE_A1,
    flags_range: "E20:F20",
    structural_summary_present: Boolean(structuralSummary.summary_version)
  }));
}

/**
 * Stage 5C physical topology — operator-visible integration (thin transport only).
 *
 * Maps API `data.physical_topology_summary` into a fixed output range. No topology
 * computation, no API changes, no BOM/CAD/pricing. If the field is absent, values
 * remain empty and a warning is logged (no GAS fallback calculations).
 */
function runStage5CSheetOutputIntegrationFlow() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = spreadsheet ? spreadsheet.getSheetByName(STAGE_4A_SHEET_NAME) : null;

  if (!sheet) {
    Logger.log(JSON.stringify({
      stage: "5C_SHEET_OUTPUT_INTEGRATION",
      telemetry_tag: "stage=5C-sheet-output-integration",
      status: "run_skipped",
      error: {
        error_code: "STAGE_4C_OPERATOR_SHELL_MISSING",
        message: "Run setupStage4COperatorShell() before Stage 5C Sheet output integration."
      }
    }));
    return;
  }

  const preflight = buildStage4PreflightPayload_(sheet, STAGE_4C_CELL_MAP);

  if (!preflight.ok) {
    writeStage5CSheetOutputIntegrationError_(sheet, preflight.error);
    Logger.log(JSON.stringify({
      stage: "5C_SHEET_OUTPUT_INTEGRATION",
      telemetry_tag: "stage=5C-sheet-output-integration",
      status: "local_input_error",
      error: preflight.error
    }));
    return;
  }

  const requestBody = buildStage4BRequestBody_(preflight.values);
  const options = {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(requestBody),
    muteHttpExceptions: true
  };

  try {
    const response = UrlFetchApp.fetch(API_URL, options);
    const httpCode = response.getResponseCode();
    const responseText = response.getContentText();
    const responseJson = JSON.parse(responseText);

    Logger.log(JSON.stringify({
      stage: "5C_SHEET_OUTPUT_INTEGRATION",
      telemetry_tag: "stage=5C-sheet-output-integration",
      http_code: httpCode,
      local_input_status: "OK",
      status: responseJson.status || null,
      physical_topology_summary_present: Boolean(
        responseJson.data && responseJson.data.physical_topology_summary
      ),
      error: responseJson.error || null
    }));

    writeStage5CSheetOutputIntegration_(sheet, responseJson, httpCode, {
      local_input_status: "OK",
      error_code: null,
      error_field: null
    });
  } catch (error) {
    Logger.log(JSON.stringify({
      stage: "5C_SHEET_OUTPUT_INTEGRATION",
      telemetry_tag: "stage=5C-sheet-output-integration",
      status: "request_or_writeback_failed",
      error: {
        error_code: "GAS_STAGE_5C_SHEET_OUTPUT_INTEGRATION_FAILED",
        message: error && error.message ? error.message : String(error),
        note: MVP_TIMEOUT_NOTE
      },
      retry: false
    }));
  }
}

function writeStage5CSheetOutputIntegrationError_(sheet, error) {
  const empty = [
    ["topology_type", ""],
    ["total_sections", ""],
    ["section_cell_counts", ""],
    ["topology_version", ""],
    ["interpretation_scope", ""],
    ["basis", ""]
  ];
  sheet.getRange(STAGE_5C_SHEET_OUTPUT_RANGE_A1).setValues(empty);
}

function writeStage5CSheetOutputIntegration_(sheet, responseJson, httpCode, localStatus) {
  const data = responseJson.data || {};
  const topology = data.physical_topology_summary;

  if (!topology) {
    writeStage5CSheetOutputIntegrationError_(sheet, { error_code: "STAGE_5C_PHYSICAL_TOPOLOGY_MISSING" });
    Logger.log(JSON.stringify({
      stage: "5C_SHEET_OUTPUT_INTEGRATION",
      telemetry_tag: "stage=5C-sheet-output-integration",
      status: "writeback_completed",
      warning: "physical_topology_summary_missing",
      sheet: STAGE_4A_SHEET_NAME,
      range: STAGE_5C_SHEET_OUTPUT_RANGE_A1,
      http_code: httpCode
    }));
    return;
  }

  var sectionCellCountsDisplay = "";
  if (topology.section_cell_counts && typeof topology.section_cell_counts.length === "number") {
    sectionCellCountsDisplay = JSON.stringify(topology.section_cell_counts);
  }

  const rows = [
    ["topology_type", firstDefined(topology.topology_type, "")],
    ["total_sections", topology.total_sections !== undefined && topology.total_sections !== null ? topology.total_sections : ""],
    ["section_cell_counts", sectionCellCountsDisplay],
    ["topology_version", firstDefined(topology.topology_version, "")],
    ["interpretation_scope", firstDefined(topology.interpretation_scope, "")],
    ["basis", firstDefined(topology.basis, "")]
  ];

  sheet.getRange(STAGE_5C_SHEET_OUTPUT_RANGE_A1).setValues(rows);

  Logger.log(JSON.stringify({
    stage: "5C_SHEET_OUTPUT_INTEGRATION",
    telemetry_tag: "stage=5C-sheet-output-integration",
    status: "writeback_completed",
    sheet: STAGE_4A_SHEET_NAME,
    range: STAGE_5C_SHEET_OUTPUT_RANGE_A1,
    physical_topology_summary_present: true
  }));
}

/**
 * Stage 6A — activate reserved operator block E27:F40 (shell infrastructure only).
 * No API call, no topology, no engineering formulas. Writes placeholder governance labels
 * and logs `stage6_operator_shell_summary`-shaped telemetry for operator visibility.
 */
function runStage6AActivateReservedOperatorBlockFlow() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = spreadsheet ? spreadsheet.getSheetByName(STAGE_4A_SHEET_NAME) : null;
  var activationDateIso = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "yyyy-MM-dd");

  if (!sheet) {
    Logger.log(JSON.stringify({
      stage: "6A_RESERVED_OPERATOR_BLOCK",
      telemetry_tag: "stage=6A-reserved-operator-block",
      block_version: STAGE_6A_SHELL_BLOCK_VERSION,
      shell_status: "ACTIVATION_SKIPPED",
      error: {
        error_code: "STAGE_4C_OPERATOR_SHELL_MISSING",
        message: "Sheet " + STAGE_4A_SHEET_NAME + " not found."
      }
    }));
    return;
  }

  writeStage6APlaceholderGovernanceBlock_(sheet, activationDateIso, "ACTIVE_RESERVED_BLOCK");

  var summaryPayload = buildStage6OperatorShellSummary_(activationDateIso, "ACTIVE_RESERVED_BLOCK");

  Logger.log(JSON.stringify({
    stage: "6A_RESERVED_OPERATOR_BLOCK",
    telemetry_tag: "stage=6A-reserved-operator-block",
    block_version: STAGE_6A_SHELL_BLOCK_VERSION,
    shell_status: "ACTIVE_RESERVED_BLOCK",
    sheet: STAGE_4A_SHEET_NAME,
    range: STAGE_6A_RESERVED_OPERATOR_BLOCK_RANGE_A1,
    block_name: STAGE_6A_BLOCK_NAME,
    status: "placeholder_writeback_completed",
    stage6_operator_shell_summary: summaryPayload.stage6_operator_shell_summary
  }));
}

/**
 * Stage 6A — clear only E27:F40 to empty strings (does not touch Stage 5A/5C zones).
 */
function runStage6AResetReservedOperatorBlockOnly() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = spreadsheet ? spreadsheet.getSheetByName(STAGE_4A_SHEET_NAME) : null;

  if (!sheet) {
    Logger.log(JSON.stringify({
      stage: "6A_RESERVED_OPERATOR_BLOCK",
      telemetry_tag: "stage=6A-reserved-operator-block",
      block_version: STAGE_6A_SHELL_BLOCK_VERSION,
      shell_status: "RESET_SKIPPED",
      error: { error_code: "STAGE_4C_OPERATOR_SHELL_MISSING", message: "Sheet not found." }
    }));
    return;
  }

  var emptyRows = [];
  var r;
  for (r = 0; r < 14; r++) {
    emptyRows.push(["", ""]);
  }
  sheet.getRange(STAGE_6A_RESERVED_OPERATOR_BLOCK_RANGE_A1).setValues(emptyRows);

  var summaryPayload = buildStage6OperatorShellSummary_("", "RESERVED_DOC_ONLY");

  Logger.log(JSON.stringify({
    stage: "6A_RESERVED_OPERATOR_BLOCK",
    telemetry_tag: "stage=6A-reserved-operator-block",
    block_version: STAGE_6A_SHELL_BLOCK_VERSION,
    shell_status: "RESERVED_DOC_ONLY",
    action: "block_reset",
    sheet: STAGE_4A_SHEET_NAME,
    range: STAGE_6A_RESERVED_OPERATOR_BLOCK_RANGE_A1,
    stage6_operator_shell_summary: summaryPayload.stage6_operator_shell_summary
  }));
}

function buildStage6OperatorShellSummary_(activationDateIso, shellStatus) {
  return {
    stage6_operator_shell_summary: {
      shell_block_version: STAGE_6A_SHELL_BLOCK_VERSION,
      reserved_range: "E27:F40",
      shell_status: shellStatus,
      shell_activation_date: activationDateIso || "",
      shell_type: "SHELL_VERTICAL_EXPANSION",
      interpretation_scope: "SHELL_ONLY_NO_ENGINEERING"
    }
  };
}

function writeStage6APlaceholderGovernanceBlock_(sheet, activationDateIso, shellStatus) {
  var rows = [
    ["stage6_block_label", STAGE_6A_BLOCK_NAME],
    ["stage_header", "Stage 6A — Reserved operator block (shell infrastructure)"],
    ["governance", "Reserved / Locked — no Stage 6 engineering until Stage 6B+ TASK"],
    ["future_use", "Future Stage 6 engineering — gated"],
    ["shell_block_version", STAGE_6A_SHELL_BLOCK_VERSION],
    ["reserved_range", "E27:F40"],
    ["shell_status", shellStatus],
    ["shell_activation_date", activationDateIso],
    ["shell_type", "SHELL_VERTICAL_EXPANSION"],
    ["interpretation_scope", "SHELL_ONLY_NO_ENGINEERING"],
    ["payload_note", "stage6_operator_shell_summary logged from GAS only (no API field in Stage 6A)"],
    ["", ""],
    ["", ""],
    ["", ""]
  ];
  sheet.getRange(STAGE_6A_RESERVED_OPERATOR_BLOCK_RANGE_A1).setValues(rows);
}

/**
 * Stage 6B — engineering classification thin writeback (`data.engineering_class_summary` → Stage 6 band only).
 */
function runStage6BEngineeringClassificationFlow() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = spreadsheet ? spreadsheet.getSheetByName(STAGE_4A_SHEET_NAME) : null;

  if (!sheet) {
    Logger.log(JSON.stringify({
      stage: "6B_ENGINEERING_CLASSIFICATION",
      telemetry_tag: "stage=6b-engineering-class",
      status: "run_skipped",
      error: {
        error_code: "STAGE_4C_OPERATOR_SHELL_MISSING",
        message: "Run setupStage4COperatorShell() before Stage 6B engineering classification."
      }
    }));
    return;
  }

  const preflight = buildStage4PreflightPayload_(sheet, STAGE_4C_CELL_MAP);

  if (!preflight.ok) {
    writeStage6BEngineeringClassificationError_(sheet);
    Logger.log(JSON.stringify({
      stage: "6B_ENGINEERING_CLASSIFICATION",
      telemetry_tag: "stage=6b-engineering-class",
      status: "local_input_error",
      error: preflight.error
    }));
    return;
  }

  const requestBody = buildStage4BRequestBody_(preflight.values);
  const options = {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(requestBody),
    muteHttpExceptions: true
  };

  try {
    const response = UrlFetchApp.fetch(API_URL, options);
    const httpCode = response.getResponseCode();
    const responseText = response.getContentText();
    const responseJson = JSON.parse(responseText);

    Logger.log(JSON.stringify({
      stage: "6B_ENGINEERING_CLASSIFICATION",
      telemetry_tag: "stage=6b-engineering-class",
      http_code: httpCode,
      local_input_status: "OK",
      status: responseJson.status || null,
      engineering_class_summary_present: Boolean(
        responseJson.data && responseJson.data.engineering_class_summary
      ),
      error: responseJson.error || null
    }));

    writeStage6BEngineeringClassification_(sheet, responseJson, httpCode);
  } catch (error) {
    Logger.log(JSON.stringify({
      stage: "6B_ENGINEERING_CLASSIFICATION",
      telemetry_tag: "stage=6b-engineering-class",
      status: "request_or_writeback_failed",
      error: {
        error_code: "GAS_STAGE_6B_ENGINEERING_CLASSIFICATION_FAILED",
        message: error && error.message ? error.message : String(error),
        note: MVP_TIMEOUT_NOTE
      },
      retry: false
    }));
  }
}

function writeStage6BEngineeringClassificationError_(sheet) {
  var emptyRows = [];
  var r;
  for (r = 0; r < 14; r++) {
    emptyRows.push(["", ""]);
  }
  sheet.getRange(STAGE_6B_ENGINEERING_CLASSIFICATION_RANGE_A1).setValues(emptyRows);
}

function writeStage6BEngineeringClassification_(sheet, responseJson, httpCode) {
  const data = responseJson.data || {};
  const ecs = data.engineering_class_summary;

  if (!ecs) {
    writeStage6BEngineeringClassificationError_(sheet);
    Logger.log(JSON.stringify({
      stage: "6B_ENGINEERING_CLASSIFICATION",
      telemetry_tag: "stage=6b-engineering-class",
      status: "writeback_completed",
      warning: "engineering_class_summary_missing",
      sheet: STAGE_4A_SHEET_NAME,
      range: STAGE_6B_ENGINEERING_CLASSIFICATION_RANGE_A1,
      http_code: httpCode
    }));
    return;
  }

  var profileDisplay = "";
  if (ecs.section_complexity_profile && ecs.section_complexity_profile.length !== undefined) {
    profileDisplay = JSON.stringify(ecs.section_complexity_profile);
  }

  var rows = [
    ["classification_version", firstDefined(ecs.classification_version, "")],
    ["lineup_complexity_class", firstDefined(ecs.lineup_complexity_class, "")],
    ["lineup_scale_class", firstDefined(ecs.lineup_scale_class, "")],
    ["section_complexity_profile", profileDisplay],
    ["total_cells_basis", ecs.total_cells_basis !== undefined && ecs.total_cells_basis !== null ? ecs.total_cells_basis : ""],
    ["topology_basis", firstDefined(ecs.topology_basis, "")],
    ["interpretation_scope", firstDefined(ecs.interpretation_scope, "")],
    ["stage_note", "Stage 6B — MVP (thin GAS; API truth); HTTP " + httpCode],
    ["", ""],
    ["", ""],
    ["", ""],
    ["", ""],
    ["", ""],
    ["", ""]
  ];
  sheet.getRange(STAGE_6B_ENGINEERING_CLASSIFICATION_RANGE_A1).setValues(rows);

  Logger.log(JSON.stringify({
    stage: "6B_ENGINEERING_CLASSIFICATION",
    telemetry_tag: "stage=6b-engineering-class",
    status: "writeback_completed",
    sheet: STAGE_4A_SHEET_NAME,
    range: STAGE_6B_ENGINEERING_CLASSIFICATION_RANGE_A1,
    engineering_class_summary_present: true
  }));
}

/**
 * Stage 6C — engineering burden thin writeback (`data.engineering_burden_summary` → Stage 6 band only).
 */
function runStage6CEngineeringBurdenFlow() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = spreadsheet ? spreadsheet.getSheetByName(STAGE_4A_SHEET_NAME) : null;

  if (!sheet) {
    Logger.log(JSON.stringify({
      stage: "6C_ENGINEERING_BURDEN",
      telemetry_tag: "stage=6c-engineering-burden",
      status: "run_skipped",
      error: {
        error_code: "STAGE_4C_OPERATOR_SHELL_MISSING",
        message: "Run setupStage4COperatorShell() before Stage 6C engineering burden."
      }
    }));
    return;
  }

  const preflight = buildStage4PreflightPayload_(sheet, STAGE_4C_CELL_MAP);

  if (!preflight.ok) {
    writeStage6CEngineeringBurdenError_(sheet);
    Logger.log(JSON.stringify({
      stage: "6C_ENGINEERING_BURDEN",
      telemetry_tag: "stage=6c-engineering-burden",
      status: "local_input_error",
      error: preflight.error
    }));
    return;
  }

  const requestBody = buildStage4BRequestBody_(preflight.values);
  const options = {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(requestBody),
    muteHttpExceptions: true
  };

  try {
    const response = UrlFetchApp.fetch(API_URL, options);
    const httpCode = response.getResponseCode();
    const responseText = response.getContentText();
    const responseJson = JSON.parse(responseText);

    Logger.log(JSON.stringify({
      stage: "6C_ENGINEERING_BURDEN",
      telemetry_tag: "stage=6c-engineering-burden",
      http_code: httpCode,
      local_input_status: "OK",
      status: responseJson.status || null,
      engineering_burden_summary_present: Boolean(
        responseJson.data && responseJson.data.engineering_burden_summary
      ),
      error: responseJson.error || null
    }));

    writeStage6CEngineeringBurden_(sheet, responseJson, httpCode);
  } catch (error) {
    Logger.log(JSON.stringify({
      stage: "6C_ENGINEERING_BURDEN",
      telemetry_tag: "stage=6c-engineering-burden",
      status: "request_or_writeback_failed",
      error: {
        error_code: "GAS_STAGE_6C_ENGINEERING_BURDEN_FAILED",
        message: error && error.message ? error.message : String(error),
        note: MVP_TIMEOUT_NOTE
      },
      retry: false
    }));
  }
}

function writeStage6CEngineeringBurdenError_(sheet) {
  var emptyRows = [];
  var r;
  for (r = 0; r < 14; r++) {
    emptyRows.push(["", ""]);
  }
  sheet.getRange(STAGE_6C_ENGINEERING_BURDEN_RANGE_A1).setValues(emptyRows);
}

function writeStage6CEngineeringBurden_(sheet, responseJson, httpCode) {
  const data = responseJson.data || {};
  const ebs = data.engineering_burden_summary;

  if (!ebs) {
    writeStage6CEngineeringBurdenError_(sheet);
    Logger.log(JSON.stringify({
      stage: "6C_ENGINEERING_BURDEN",
      telemetry_tag: "stage=6c-engineering-burden",
      status: "writeback_completed",
      warning: "engineering_burden_summary_missing",
      sheet: STAGE_4A_SHEET_NAME,
      range: STAGE_6C_ENGINEERING_BURDEN_RANGE_A1,
      http_code: httpCode
    }));
    return;
  }

  var rows = [
    ["burden_version", firstDefined(ebs.burden_version, "")],
    ["structural_burden_class", firstDefined(ebs.structural_burden_class, "")],
    ["assembly_burden_class", firstDefined(ebs.assembly_burden_class, "")],
    ["estimated_mass_class", firstDefined(ebs.estimated_mass_class, "")],
    ["complexity_basis", firstDefined(ebs.complexity_basis, "")],
    ["topology_basis", firstDefined(ebs.topology_basis, "")],
    ["footprint_basis", firstDefined(ebs.footprint_basis, "")],
    ["interpretation_scope", firstDefined(ebs.interpretation_scope, "")],
    ["stage_note", "Stage 6C — MVP (thin GAS; API truth); not kg/BOM — HTTP " + httpCode],
    ["", ""],
    ["", ""],
    ["", ""],
    ["", ""],
    ["", ""]
  ];
  sheet.getRange(STAGE_6C_ENGINEERING_BURDEN_RANGE_A1).setValues(rows);

  Logger.log(JSON.stringify({
    stage: "6C_ENGINEERING_BURDEN",
    telemetry_tag: "stage=6c-engineering-burden",
    status: "writeback_completed",
    sheet: STAGE_4A_SHEET_NAME,
    range: STAGE_6C_ENGINEERING_BURDEN_RANGE_A1,
    engineering_burden_summary_present: true
  }));
}

function writeStage7AUnifiedStage6BandError_(sheet) {
  var emptyRows = [];
  var r;
  for (r = 0; r < 14; r++) {
    emptyRows.push(["", ""]);
  }
  sheet.getRange(STAGE_7A_KZO_MVP_STAGE6_BAND_RANGE_A1).setValues(emptyRows);
}

/**
 * Stage 7A — one-shot writeback for **`E27:F40`**: stacks 6B + 6C keys in 14 rows (single setValues).
 * Omits ECS `topology_basis` row (topology remains visible via Stage 5C + burden `topology_basis`).
 */
function writeStage7AUnifiedStage6Band_(sheet, responseJson, httpCode) {
  const data = responseJson.data || {};
  const ecs = data.engineering_class_summary;
  const ebs = data.engineering_burden_summary;

  var profileDisplay = "";
  if (ecs && ecs.section_complexity_profile && ecs.section_complexity_profile.length !== undefined) {
    profileDisplay = JSON.stringify(ecs.section_complexity_profile);
  }

  var rows = [
    ["classification_version", ecs ? firstDefined(ecs.classification_version, "") : ""],
    ["lineup_complexity_class", ecs ? firstDefined(ecs.lineup_complexity_class, "") : ""],
    ["lineup_scale_class", ecs ? firstDefined(ecs.lineup_scale_class, "") : ""],
    ["section_complexity_profile", profileDisplay],
    ["total_cells_basis", ecs && ecs.total_cells_basis !== undefined && ecs.total_cells_basis !== null ? ecs.total_cells_basis : ""],
    ["interpretation_scope", ecs ? firstDefined(ecs.interpretation_scope, "") : ""],
    ["burden_version", ebs ? firstDefined(ebs.burden_version, "") : ""],
    ["structural_burden_class", ebs ? firstDefined(ebs.structural_burden_class, "") : ""],
    ["assembly_burden_class", ebs ? firstDefined(ebs.assembly_burden_class, "") : ""],
    ["estimated_mass_class", ebs ? firstDefined(ebs.estimated_mass_class, "") : ""],
    ["complexity_basis", ebs ? firstDefined(ebs.complexity_basis, "") : ""],
    ["topology_basis", ebs ? firstDefined(ebs.topology_basis, "") : ""],
    ["footprint_basis", ebs ? firstDefined(ebs.footprint_basis, "") : ""],
    ["interpretation_scope_burden", ebs ? firstDefined(ebs.interpretation_scope, "") : ""]
  ];
  sheet.getRange(STAGE_7A_KZO_MVP_STAGE6_BAND_RANGE_A1).setValues(rows);

  Logger.log(JSON.stringify({
    stage: "7A_UNIFIED_STAGE6_BAND",
    telemetry_tag: "stage=7a-kzo-mvp-flow",
    status: "writeback_completed",
    sheet: STAGE_4A_SHEET_NAME,
    range: STAGE_7A_KZO_MVP_STAGE6_BAND_RANGE_A1,
    http_code: httpCode || null,
    engineering_class_summary_present: Boolean(ecs),
    engineering_burden_summary_present: Boolean(ebs)
  }));
}

/**
 * Stage 7A — end-to-end KZO MVP: one `prepare_calculation` POST, then orchestrated Sheet writeback
 * (Stage 5A integration + Stage 5C topology + unified Stage 6 band). No BOM/DB/pricing/new API math.
 */
function runKzoMvpFlow() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = spreadsheet ? spreadsheet.getSheetByName(STAGE_4A_SHEET_NAME) : null;

  if (!sheet) {
    Logger.log(JSON.stringify({
      stage: "7A_KZO_MVP_FLOW",
      telemetry_tag: "stage=7a-kzo-mvp-flow",
      mvp_run_outcome: "MVP_RUN_FAILED",
      status: "run_skipped",
      error: {
        error_code: "STAGE_4C_OPERATOR_SHELL_MISSING",
        message: "Run setupStage4COperatorShell() before runKzoMvpFlow()."
      }
    }));
    return;
  }

  const preflight = buildStage4PreflightPayload_(sheet, STAGE_4C_CELL_MAP);

  if (!preflight.ok) {
    writeStage5AOutputIntegrationError_(sheet, preflight.error);
    writeStage5CSheetOutputIntegrationError_(sheet, preflight.error);
    writeStage7AUnifiedStage6BandError_(sheet);
    Logger.log(JSON.stringify({
      stage: "7A_KZO_MVP_FLOW",
      telemetry_tag: "stage=7a-kzo-mvp-flow",
      mvp_run_outcome: "MVP_RUN_FAILED",
      status: "local_input_error",
      error: preflight.error
    }));
    return;
  }

  const requestBody = buildStage4BRequestBody_(preflight.values);
  const options = {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(requestBody),
    muteHttpExceptions: true
  };

  try {
    const response = UrlFetchApp.fetch(API_URL, options);
    const httpCode = response.getResponseCode();
    const responseText = response.getContentText();
    const responseJson = JSON.parse(responseText);

    const dataProbe = responseJson.data || {};
    Logger.log(JSON.stringify({
      stage: "7A_KZO_MVP_FLOW",
      telemetry_tag: "stage=7a-kzo-mvp-flow",
      http_code: httpCode,
      api_status: responseJson.status || null,
      structural_summary_present: Boolean(dataProbe.structural_composition_summary),
      physical_summary_present: Boolean(dataProbe.physical_summary),
      physical_topology_summary_present: Boolean(dataProbe.physical_topology_summary),
      engineering_class_summary_present: Boolean(dataProbe.engineering_class_summary),
      engineering_burden_summary_present: Boolean(dataProbe.engineering_burden_summary),
      error: responseJson.error || null
    }));

    if (responseJson.status !== "success") {
      Logger.log(JSON.stringify({
        stage: "7A_KZO_MVP_FLOW",
        telemetry_tag: "stage=7a-kzo-mvp-flow",
        mvp_run_outcome: "MVP_RUN_FAILED",
        status: "api_non_success",
        api_status: responseJson.status || null,
        http_code: httpCode,
        retry: Boolean(httpCode >= 500)
      }));
      return;
    }

    const localOk = {
      local_input_status: "OK",
      error_code: null,
      error_field: null
    };
    writeStage5AOutputIntegration_(sheet, responseJson, httpCode, localOk);
    writeStage5CSheetOutputIntegration_(sheet, responseJson, httpCode, localOk);
    writeStage7AUnifiedStage6Band_(sheet, responseJson, httpCode);

    Logger.log(JSON.stringify({
      stage: "7A_KZO_MVP_FLOW",
      telemetry_tag: "stage=7a-kzo-mvp-flow",
      mvp_run_outcome: "MVP_RUN_SUCCESS",
      status: "mvp_flow_completed",
      http_code: httpCode,
      physical_summary_present: Boolean(dataProbe.physical_summary)
    }));
  } catch (error) {
    Logger.log(JSON.stringify({
      stage: "7A_KZO_MVP_FLOW",
      telemetry_tag: "stage=7a-kzo-mvp-flow",
      mvp_run_outcome: "MVP_RUN_FAILED",
      status: "request_parse_or_writeback_failed",
      error: {
        error_code: "GAS_STAGE_7A_KZO_MVP_FLOW_FAILED",
        message: error && error.message ? error.message : String(error),
        note: MVP_TIMEOUT_NOTE
      },
      retry: false
    }));
  }
}

/**
 * Stage 8A — persist one ``KZO_MVP_SNAPSHOT_V1`` object (INSERT only on server).
 * Pass the full JSON snapshot; GAS does not build or alter contract fields here.
 */
function saveKzoSnapshotV1(snapshotObject) {
  var options = {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(snapshotObject),
    muteHttpExceptions: true
  };
  try {
    var response = UrlFetchApp.fetch(KZO_SAVE_SNAPSHOT_URL, options);
    var httpCode = response.getResponseCode();
    var responseText = response.getContentText();
    var responseJson = JSON.parse(responseText);
    Logger.log(JSON.stringify({
      stage: "8A_SAVE_SNAPSHOT",
      telemetry_tag: "stage=8a-save-snapshot",
      http_code: httpCode,
      status: responseJson.status || null,
      persistence_status: responseJson.persistence_status || null,
      snapshot_id: responseJson.snapshot_id || null,
      error_code: responseJson.error_code || null
    }));
    return responseJson;
  } catch (error) {
    Logger.log(JSON.stringify({
      stage: "8A_SAVE_SNAPSHOT",
      telemetry_tag: "stage=8a-save-snapshot",
      status: "request_failed",
      error: {
        error_code: "GAS_STAGE_8A_SAVE_SNAPSHOT_FAILED",
        message: error && error.message ? error.message : String(error),
        note: MVP_TIMEOUT_NOTE
      }
    }));
    return null;
  }
}