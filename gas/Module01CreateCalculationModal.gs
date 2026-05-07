/**
 * Create Calculation modal — thin shell (transport + modal host). No business rules beyond UI hints.
 */

function edsPowerModule01OpenCreateCalculationModal() {
  const html = HtmlService.createHtmlOutputFromFile("Module01CreateCalculationModalHtml")
    .setWidth(460)
    .setHeight(580);
  SpreadsheetApp.getUi().showModalDialog(html, "Створити розрахунок");
}

/**
 * Bootstrap: terminal_id from session status API; spreadsheet_id from active spreadsheet.
 */
function module01CreateCalculationBootstrap_() {
  var token = "";
  if (typeof module01AuthGetSession_ === "function") {
    var s = module01AuthGetSession_();
    token = s && typeof s.session_token === "string" ? String(s.session_token).trim() : "";
  }
  if (!token) {
    return {ok: false, code: "AUTH_MISSING_TOKEN", message: "Потрібна авторизація."};
  }
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  if (!ss) {
    return {ok: false, code: "NO_SPREADSHEET", message: "Відкрийте таблицю."};
  }
  var spreadsheetId = String(ss.getId() || "").trim();
  try {
    var tr = module01AuthSessionStatusTransport_(token);
    var env = tr.envelope || {};
    if (env.status === "auth_error") {
      return {ok: false, code: "AUTH_ERROR", message: "Сесія недійсна. Увійдіть знову."};
    }
    if (env.status !== "success" || !env.data) {
      return {ok: false, code: "SESSION_STATUS_FAILED", message: "Не вдалось отримати контекст сесії."};
    }
    var tid = String(env.data.terminal_id || "").trim();
    if (!tid) {
      return {ok: false, code: "TERMINAL_MISSING", message: "terminal_id відсутній у сесії."};
    }
    return {
      ok: true,
      terminal_id: tid,
      spreadsheet_id: spreadsheetId
    };
  } catch (error) {
    return {
      ok: false,
      code: "BOOTSTRAP_ERROR",
      message: String((error && error.message) || error || "Помилка bootstrap.")
    };
  }
}

function module01CreateCalculationBuildPayload_(form, bootstrap) {
  return {
    source_client: "GAS_TERMINAL_V1",
    terminal_id: String(bootstrap.terminal_id || "").trim(),
    spreadsheet_id: String(bootstrap.spreadsheet_id || "").trim(),
    payload: {
      calculation_title: String(form.calculation_title || "").trim(),
      potential_customer: String(form.potential_customer || "").trim(),
      product_type: "KZO",
      comment: String(form.comment || "").trim(),
      external_reference: String(form.external_reference || "").trim()
    }
  };
}

function module01CreateCalculationSubmit(form, bootstrap) {
  var token = "";
  if (typeof module01AuthGetSession_ === "function") {
    var s = module01AuthGetSession_();
    token = s && typeof s.session_token === "string" ? String(s.session_token).trim() : "";
  }
  if (!token) {
    return {ok: false, code: "AUTH_MISSING_TOKEN", message: "Потрібна авторизація."};
  }
  var body = module01CreateCalculationBuildPayload_(form, bootstrap);
  try {
    var tr = module01CreateCalculationTransport_(token, body);
    return {
      ok: true,
      http_status: tr.http_status,
      envelope: tr.envelope
    };
  } catch (error) {
    return {
      ok: false,
      code: "TRANSPORT_ERROR",
      message: String((error && error.message) || error || "Помилка мережі.")
    };
  }
}

/**
 * Optional: cache active calculation id (UI hint only).
 */
function module01CreateCalculationRememberActiveId_(spreadsheetId, calculationId) {
  var sid = String(spreadsheetId || "").trim();
  var cid = String(calculationId || "").trim();
  if (!sid || !cid) {
    return;
  }
  var key = "EDS_POWER_" + sid + "_MODULE01_ACTIVE_CALCULATION_ID";
  PropertiesService.getDocumentProperties().setProperty(key, cid);
}
