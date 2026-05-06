const EDSPowerCore_VERSION = "EDS_POWER_CORE_FOUNDATION_V1";
const EDS_POWER_BOOTSTRAP_MENU_TITLE = "EDS Power";
const EDS_POWER_DYNAMIC_MENU_ENDPOINT_PATH = "/api/module01/auth/menu";
const EDS_POWER_VISIBLE_STATUS = "VISIBLE";
const EDS_POWER_MENU_ALLOWED_ACTIONS = {
  REFRESH_MENU: true,
  SESSION_STATUS: true,
  LOGOUT: true,
  PLACEHOLDER_DISABLED: true
};

function EDSPowerCore_onTerminalOpen(context) {
  const safeContext = EDSPowerCore_sanitizeContext_(context);
  EDSPowerCore_renderStaticFallbackMenu_();
  return {
    status: "success",
    core_reachable: true,
    core_version: EDSPowerCore_VERSION,
    message: "EDSPowerCore foundation reachable",
    terminal_id: safeContext.terminal_id,
    terminal_id_present: !!safeContext.terminal_id,
    spreadsheet_id_present: !!safeContext.spreadsheet_id
  };
}

function EDSPowerCore_refreshMenu(context) {
  const safeContext = EDSPowerCore_sanitizeContext_(context);
  try {
    const transportResult = EDSPowerCore_fetchMenuEnvelope_(safeContext);
    const envelope = transportResult.envelope || {};
    const data = envelope.data || {};
    const menus = Array.isArray(data.menus) ? data.menus : [];
    const rendered = EDSPowerCore_renderDynamicMenu_(menus);
    const diagnostic = {
      stage: "EDS_POWER_DYNAMIC_MENU_REFRESH",
      menu_source: "mock_backend",
      base_url_present: transportResult.base_url_present === true,
      endpoint_path: transportResult.endpoint_path || EDS_POWER_DYNAMIC_MENU_ENDPOINT_PATH,
      endpoint_http_status: typeof transportResult.http_status === "number" ? transportResult.http_status : null,
      rendered_items: Number(rendered || 0),
      terminal_id_mode: safeContext.terminal_id_mode || "unknown",
      terminal_id_present: !!safeContext.terminal_id,
      core_version: EDSPowerCore_VERSION,
      error_code: null,
      error_message: null
    };
    Logger.log(JSON.stringify(diagnostic));
    return {
      status: "success",
      menu_source: "mock_backend",
      core_reachable: true,
      core_version: EDSPowerCore_VERSION,
      terminal_id: safeContext.terminal_id,
      rendered_items: rendered,
      endpoint_http_status: transportResult.http_status
    };
  } catch (error) {
    EDSPowerCore_renderStaticFallbackMenu_();
    if (typeof EDSPowerCore_showError === "function") {
      EDSPowerCore_showError(error, safeContext);
    }
    const errorCode = error && typeof error.code === "string"
      ? error.code
      : "EDS_POWER_MENU_REFRESH_FAILED";
    const errorMessage = error && typeof error.message === "string"
      ? error.message
      : "Unknown menu refresh error.";
    const diagnostic = {
      stage: "EDS_POWER_DYNAMIC_MENU_REFRESH",
      menu_source: "fallback_static",
      base_url_present: errorCode === "EDS_POWER_MENU_BASE_URL_MISSING" ? false : null,
      endpoint_path: EDS_POWER_DYNAMIC_MENU_ENDPOINT_PATH,
      endpoint_http_status: null,
      rendered_items: 2,
      terminal_id_mode: safeContext.terminal_id_mode || "unknown",
      terminal_id_present: !!safeContext.terminal_id,
      core_version: EDSPowerCore_VERSION,
      error_code: errorCode,
      error_message: errorMessage
    };
    Logger.log(JSON.stringify(diagnostic));
    return {
      status: "menu_refresh_failed",
      menu_source: "fallback_static",
      core_reachable: true,
      core_version: EDSPowerCore_VERSION,
      terminal_id: safeContext.terminal_id
    };
  }
}

function EDSPowerCore_login(context) {
  const safeContext = EDSPowerCore_sanitizeContext_(context);
  return {
    status: "placeholder",
    action: "login",
    core_version: EDSPowerCore_VERSION,
    terminal_id_present: !!safeContext.terminal_id
  };
}

function EDSPowerCore_logout(context) {
  const safeContext = EDSPowerCore_sanitizeContext_(context);
  return {
    status: "placeholder",
    action: "logout",
    core_version: EDSPowerCore_VERSION,
    terminal_id_present: !!safeContext.terminal_id
  };
}

function EDSPowerCore_getSessionStatus(context) {
  const safeContext = EDSPowerCore_sanitizeContext_(context);
  return {
    status: "placeholder",
    action: "session_status",
    core_version: EDSPowerCore_VERSION,
    user_session_present: !!safeContext.user_session_present
  };
}

function EDSPowerCore_openModule(actionKey, context) {
  const safeContext = EDSPowerCore_sanitizeContext_(context);
  if (String(actionKey || "") === "MODULE_01_PLACEHOLDER") {
    edsPowerModulePlaceholder_();
  }
  return {
    status: "placeholder",
    action: "open_module",
    action_key: typeof actionKey === "string" ? actionKey : "",
    core_version: EDSPowerCore_VERSION,
    terminal_id_present: !!safeContext.terminal_id
  };
}

function EDSPowerCore_callApi(request) {
  return {
    status: "not_implemented_in_foundation_skeleton",
    request_type: request && typeof request === "object" ? "object" : "none",
    core_version: EDSPowerCore_VERSION
  };
}

function EDSPowerCore_fetchMenuEnvelope_(context) {
  const scriptProps = PropertiesService.getScriptProperties();
  const baseUrlPropertyName = typeof MODULE01_AUTH_BASE_URL_PROPERTY === "string"
    ? MODULE01_AUTH_BASE_URL_PROPERTY
    : "MODULE01_API_BASE_URL";
  const baseUrl = String(scriptProps.getProperty(baseUrlPropertyName) || "").trim();
  if (!baseUrl) {
    throw {
      code: "EDS_POWER_MENU_BASE_URL_MISSING",
      message: "API base URL is missing for dynamic menu refresh."
    };
  }
  const endpointUrl = baseUrl.replace(/\/+$/, "") + EDS_POWER_DYNAMIC_MENU_ENDPOINT_PATH;
  const headers = {};
  const sessionToken = EDSPowerCore_resolveSessionToken_();
  if (sessionToken) {
    headers.Authorization = "Bearer " + sessionToken;
  }
  const response = UrlFetchApp.fetch(endpointUrl, {
    method: "get",
    headers: headers,
    muteHttpExceptions: true
  });
  let envelope = null;
  try {
    envelope = JSON.parse(response.getContentText());
  } catch (_error) {
    throw new Error("EDS_POWER_MENU_INVALID_JSON");
  }
  if (!envelope || typeof envelope !== "object") {
    throw new Error("EDS_POWER_MENU_INVALID_ENVELOPE");
  }
  if (!envelope.data || !Array.isArray(envelope.data.menus)) {
    throw new Error("EDS_POWER_MENU_ITEMS_MISSING");
  }
  return {
    http_status: response.getResponseCode(),
    base_url_present: true,
    endpoint_path: EDS_POWER_DYNAMIC_MENU_ENDPOINT_PATH,
    envelope: envelope
  };
}

function EDSPowerCore_resolveSessionToken_() {
  if (typeof module01AuthGetSession_ !== "function") {
    return "";
  }
  const session = module01AuthGetSession_();
  const token = session && typeof session.session_token === "string"
    ? String(session.session_token).trim()
    : "";
  return token || "";
}

function EDSPowerCore_renderDynamicMenu_(menus) {
  const ui = SpreadsheetApp.getUi();
  const visibleMenus = menus
    .filter(function (item) {
      return item && typeof item === "object" && String(item.visibility || "") === EDS_POWER_VISIBLE_STATUS;
    })
    .sort(function (a, b) {
      return Number(a.sort_order || 0) - Number(b.sort_order || 0);
    });

  const menu = ui.createMenu(EDS_POWER_BOOTSTRAP_MENU_TITLE);
  let rendered = 0;
  visibleMenus.forEach(function (item) {
    const callbackName = EDSPowerCore_resolveMenuCallback_(item);
    if (!callbackName) {
      return;
    }
    const label = EDSPowerCore_resolveMenuLabel_(item);
    if (item.enabled === true) {
      menu.addItem(label, callbackName);
      rendered += 1;
      return;
    }
    if (String(item.action_type || "") === "PLACEHOLDER_DISABLED") {
      menu.addItem(label, callbackName);
      rendered += 1;
    }
  });
  menu.addToUi();
  return rendered;
}

function EDSPowerCore_resolveMenuLabel_(item) {
  const fallback = "EDS Power Action";
  const label = item && typeof item.menu_label === "string" ? item.menu_label.trim() : "";
  return label || fallback;
}

function EDSPowerCore_resolveMenuCallback_(item) {
  if (!item || typeof item !== "object") {
    return "";
  }
  const actionType = String(item.action_type || "").trim().toUpperCase();
  const actionKey = String(item.action_key || "").trim().toUpperCase();
  const normalizedAction = actionType || actionKey;
  if (!EDS_POWER_MENU_ALLOWED_ACTIONS[normalizedAction]) {
    return "";
  }
  if (normalizedAction === "REFRESH_MENU") {
    return "edsPowerRefreshMenu";
  }
  if (normalizedAction === "SESSION_STATUS") {
    return typeof runModule01AuthenticatedSessionStatusCheck === "function"
      ? "runModule01AuthenticatedSessionStatusCheck"
      : "edsPowerSessionStatusPlaceholder_";
  }
  if (normalizedAction === "LOGOUT") {
    return "edsPowerLogout";
  }
  if (normalizedAction === "PLACEHOLDER_DISABLED") {
    return "edsPowerModulePlaceholder_";
  }
  return "";
}

function EDSPowerCore_renderStaticFallbackMenu_() {
  SpreadsheetApp.getUi()
    .createMenu(EDS_POWER_BOOTSTRAP_MENU_TITLE)
    .addItem("⚠ Setup Required", "edsPowerFallbackSetupRequired_")
    .addItem("Refresh Setup Check", "edsPowerRefreshSetupCheck_")
    .addToUi();
}

function edsPowerFallbackSetupRequired_() {
  SpreadsheetApp.getUi().alert("Setup required: set MODULE01_API_BASE_URL in Script Properties.");
}

function edsPowerRefreshSetupCheck_() {
  EDSPowerCore_refreshMenu(EDSPowerCore_sanitizeContext_({}));
}

function edsPowerModulePlaceholder_() {
  SpreadsheetApp.getUi().alert("Module 01 is not active in this mock menu slice.");
}

function edsPowerSessionStatusPlaceholder_() {
  SpreadsheetApp.getUi().alert("Session status action is unavailable.");
}

function EDSPowerCore_showError(error, context) {
  const ui = SpreadsheetApp.getUi();
  const safeContext = EDSPowerCore_sanitizeContext_(context);
  const message = error && typeof error.message === "string"
    ? error.message
    : "EDSPowerCore error";
  ui.alert("EDSPowerCore Error", message, ui.ButtonSet.OK);
  return {
    status: "error_displayed",
    core_version: EDSPowerCore_VERSION,
    terminal_id_present: !!safeContext.terminal_id
  };
}

function EDSPowerCore_showFallback(message, context) {
  const ui = SpreadsheetApp.getUi();
  const safeContext = EDSPowerCore_sanitizeContext_(context);
  const fallbackMessage = typeof message === "string" && message
    ? message
    : "EDS Power fallback mode: core unavailable or terminal setup incomplete.";
  ui.alert("EDS Power Fallback", fallbackMessage, ui.ButtonSet.OK);
  return {
    status: "fallback_shown",
    core_version: EDSPowerCore_VERSION,
    terminal_id_present: !!safeContext.terminal_id
  };
}

function EDSPowerCore_sanitizeContext_(context) {
  const ctx = context && typeof context === "object" ? context : {};
  return {
    terminal_id: typeof ctx.terminal_id === "string" ? ctx.terminal_id : "",
    terminal_id_mode: typeof ctx.terminal_id_mode === "string" ? ctx.terminal_id_mode : "",
    spreadsheet_id: typeof ctx.spreadsheet_id === "string" ? ctx.spreadsheet_id : "",
    active_sheet_name: typeof ctx.active_sheet_name === "string" ? ctx.active_sheet_name : "",
    client_type: "GAS",
    core_version: EDSPowerCore_VERSION,
    bootstrap_version: typeof ctx.bootstrap_version === "string" ? ctx.bootstrap_version : "",
    user_session_present: ctx.user_session_present === true
  };
}
