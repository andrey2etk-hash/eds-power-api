const API_URL = "https://YOUR_RENDER_URL/api/calc/prepare_calculation";
const MVP_TIMEOUT_NOTE = "Render free tier may cold-start; Stage 3E manual test may need rerun after wake-up.";

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
