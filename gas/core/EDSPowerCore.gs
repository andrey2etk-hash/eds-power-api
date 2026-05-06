const EDS_POWER_CORE_VERSION = "foundation-skeleton-v1";
const EDS_POWER_BOOTSTRAP_MENU_TITLE = "EDS Power Terminal";

function EDSPowerCore_onTerminalOpen(context) {
  const safeContext = EDSPowerCore_sanitizeContext_(context);
  const ui = SpreadsheetApp.getUi();
  ui.createMenu(EDS_POWER_BOOTSTRAP_MENU_TITLE)
    .addItem("Refresh EDS Power Menu", "edsPowerRefreshMenu")
    .addItem("Login (Skeleton)", "edsPowerLogin")
    .addItem("Logout (Skeleton)", "edsPowerLogout")
    .addToUi();
  return {
    status: "ok",
    core_version: EDS_POWER_CORE_VERSION,
    core_reachable: true,
    terminal_id_present: !!safeContext.terminal_id,
    spreadsheet_id_present: !!safeContext.spreadsheet_id
  };
}

function EDSPowerCore_refreshMenu(context) {
  return EDSPowerCore_onTerminalOpen(context);
}

function EDSPowerCore_login(context) {
  const safeContext = EDSPowerCore_sanitizeContext_(context);
  return {
    status: "placeholder",
    action: "login",
    core_version: EDS_POWER_CORE_VERSION,
    terminal_id_present: !!safeContext.terminal_id
  };
}

function EDSPowerCore_logout(context) {
  const safeContext = EDSPowerCore_sanitizeContext_(context);
  return {
    status: "placeholder",
    action: "logout",
    core_version: EDS_POWER_CORE_VERSION,
    terminal_id_present: !!safeContext.terminal_id
  };
}

function EDSPowerCore_getSessionStatus(context) {
  const safeContext = EDSPowerCore_sanitizeContext_(context);
  return {
    status: "placeholder",
    action: "session_status",
    core_version: EDS_POWER_CORE_VERSION,
    user_session_present: !!safeContext.user_session_present
  };
}

function EDSPowerCore_openModule(actionKey, context) {
  const safeContext = EDSPowerCore_sanitizeContext_(context);
  return {
    status: "placeholder",
    action: "open_module",
    action_key: typeof actionKey === "string" ? actionKey : "",
    core_version: EDS_POWER_CORE_VERSION,
    terminal_id_present: !!safeContext.terminal_id
  };
}

function EDSPowerCore_callApi(request) {
  return {
    status: "not_implemented_in_foundation_skeleton",
    request_type: request && typeof request === "object" ? "object" : "none",
    core_version: EDS_POWER_CORE_VERSION
  };
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
    core_version: EDS_POWER_CORE_VERSION,
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
    core_version: EDS_POWER_CORE_VERSION,
    terminal_id_present: !!safeContext.terminal_id
  };
}

function EDSPowerCore_sanitizeContext_(context) {
  const ctx = context && typeof context === "object" ? context : {};
  return {
    terminal_id: typeof ctx.terminal_id === "string" ? ctx.terminal_id : "",
    spreadsheet_id: typeof ctx.spreadsheet_id === "string" ? ctx.spreadsheet_id : "",
    active_sheet_name: typeof ctx.active_sheet_name === "string" ? ctx.active_sheet_name : "",
    client_type: "GAS",
    core_version: EDS_POWER_CORE_VERSION,
    bootstrap_version: typeof ctx.bootstrap_version === "string" ? ctx.bootstrap_version : "",
    user_session_present: ctx.user_session_present === true
  };
}
