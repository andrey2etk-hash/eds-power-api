const MODULE01_AUTH_MENU_TITLE = "EDS Power Auth";

function module01AuthBuildSafeDebugMessage_(httpStatus, envelope) {
  const status = envelope && typeof envelope.status === "string" ? envelope.status : "unknown";
  const errorObj = envelope && envelope.error && typeof envelope.error === "object" ? envelope.error : {};
  const errorCode = typeof errorObj.error_code === "string" ? errorObj.error_code : "";
  const errorMessage = typeof errorObj.message === "string" ? errorObj.message : "";
  const requestId = envelope && envelope.metadata && typeof envelope.metadata.request_id === "string"
    ? envelope.metadata.request_id
    : "";
  const lines = [
    "HTTP: " + String(httpStatus),
    "status: " + status,
    "error_code: " + (errorCode || "n/a"),
    "request_id: " + (requestId || "n/a")
  ];
  if (errorMessage) {
    lines.push("error_message: " + errorMessage);
  }
  return lines.join("\n");
}

function module01AuthBuildSafeDebugObject_(httpStatus, envelope) {
  const status = envelope && typeof envelope.status === "string" ? envelope.status : "unknown";
  const errorObj = envelope && envelope.error && typeof envelope.error === "object" ? envelope.error : {};
  const errorCode = typeof errorObj.error_code === "string" ? errorObj.error_code : "";
  const errorMessage = typeof errorObj.message === "string" ? errorObj.message : "";
  const requestId = envelope && envelope.metadata && typeof envelope.metadata.request_id === "string"
    ? envelope.metadata.request_id
    : "";
  return {
    http_status: httpStatus,
    status: status,
    error_code: errorCode || "",
    request_id: requestId || "",
    error_message: errorMessage || ""
  };
}

function module01AuthBuildTransportDebugObject_(error) {
  const err = error && typeof error === "object" ? error : {};
  const code = typeof err.code === "string" ? err.code : "AUTH_TRANSPORT_FETCH_FAILED";
  const message = typeof err.message === "string" ? err.message : "";
  const apiBaseUrlPresent = err.api_base_url_present === true ? "YES" : "NO";
  const endpointPath = typeof err.endpoint_path === "string" ? err.endpoint_path : "/api/module01/auth/login";
  const endpointUrlRedacted = typeof err.endpoint_url_redacted === "string" ? err.endpoint_url_redacted : "";
  return {
    http_status: "n/a",
    status: "transport_error",
    error_code: code,
    request_id: "n/a",
    error_message: "",
    transport_error_message: message,
    api_base_url_present: apiBaseUrlPresent,
    endpoint_path: endpointPath,
    endpoint_url_redacted: endpointUrlRedacted
  };
}

function module01AuthOnOpen_() {
  const ui = SpreadsheetApp.getUi();
  const menu = ui.createMenu(MODULE01_AUTH_MENU_TITLE);
  const sessionData = module01AuthGetSession_();
  const isLoggedIn = !!sessionData && !module01AuthIsExpired_(sessionData);

  if (isLoggedIn) {
    menu
      .addItem("Оновити меню", "module01AuthRefreshMenu")
      .addItem("Вийти", "module01AuthLogout");
  } else {
    menu.addItem("Авторизуватись", "module01AuthLogin");
  }

  menu.addToUi();
}

function module01AuthRefreshMenu() {
  module01AuthOnOpen_();
  SpreadsheetApp.getUi().alert("Меню авторизації оновлено.");
}

function module01AuthLogin() {
  const html = HtmlService
    .createHtmlOutputFromFile("AuthLoginDialog")
    .setWidth(420)
    .setHeight(320);
  SpreadsheetApp.getUi().showModalDialog(html, "Module 01 Auth Login");
}

function module01AuthSubmitLogin(email, password) {
  const normalizedEmail = String(email || "").trim().toLowerCase();
  const rawPassword = String(password || "");
  if (!normalizedEmail) {
    return {ok: false, message: "Email є обов'язковим."};
  }
  if (!rawPassword) {
    return {ok: false, message: "Пароль є обов'язковим."};
  }

  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  if (!spreadsheet) {
    return {ok: false, message: "Не вдалося визначити активну таблицю."};
  }
  const spreadsheetId = spreadsheet.getId();

  try {
    const result = module01AuthLoginTransport_(normalizedEmail, rawPassword, spreadsheetId);
    const envelope = result.envelope;
    if (result.http_status >= 500 || envelope.status === "error") {
      return {
        ok: false,
        message: "Сервіс авторизації тимчасово недоступний.",
        debug: module01AuthBuildSafeDebugObject_(result.http_status, envelope)
      };
    }
    if (envelope.status !== "success" || !envelope.data || !envelope.data.session) {
      return {
        ok: false,
        message: "Помилка авторизації. Перевірте облікові дані.",
        debug: module01AuthBuildSafeDebugObject_(result.http_status, envelope)
      };
    }

    const session = envelope.data.session || {};
    const user = envelope.data.user || {};
    const token = String(session.session_token || "").trim();
    const expiresAt = String(session.expires_at || "").trim();
    if (!token) {
      return {ok: false, message: "Сервіс повернув некоректну сесію."};
    }

    module01AuthStoreSession_({
      session_token: token,
      expires_at: expiresAt,
      user_email: String(user.email || normalizedEmail).trim().toLowerCase(),
      role_codes: Array.isArray(user.role_codes) ? user.role_codes : []
    });
    module01AuthOnOpen_();
    return {ok: true, message: "Авторизація успішна."};
  } catch (error) {
    return {
      ok: false,
      message: "Не вдалося виконати авторизацію. Спробуйте пізніше.",
      debug: module01AuthBuildTransportDebugObject_(error)
    };
  }
}

function module01AuthLogout() {
  module01AuthClearSession_();
  module01AuthOnOpen_();
  SpreadsheetApp.getUi().alert("Сесію очищено. Необхідна повторна авторизація.");
}
