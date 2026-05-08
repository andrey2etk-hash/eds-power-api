const EDS_POWER_BOOTSTRAP_VERSION = "foundation-skeleton-v1";
const EDS_POWER_TERMINAL_ID_PROPERTY = "EDS_POWER_TERMINAL_ID";

function onOpen() {
  const context = buildEDSPowerTerminalContext_();

  if (!context.terminal_id) {
    addEDSPowerEmergencyFallbackMenu_();
    edsPowerShowFallbackError("Terminal setup required: terminal_id is missing in ScriptProperties.");
    return;
  }

  if (typeof EDSPowerCore_onTerminalOpen !== "function") {
    addEDSPowerEmergencyFallbackMenu_();
    edsPowerShowFallbackError("EDSPowerCore unavailable. Running in fallback mode.");
    return;
  }

  try {
    EDSPowerCore_onTerminalOpen(context);
    edsPowerTryAutoOpenModule01Sidebar_(context);
  } catch (error) {
    addEDSPowerEmergencyFallbackMenu_();
    edsPowerShowFallbackError("EDSPowerCore failed on open. Check configuration.");
    if (typeof EDSPowerCore_showError === "function") {
      EDSPowerCore_showError(error, context);
    }
  }
}

/**
 * After successful menu init: open Module 01 sidebar if session cookie exists (non-authoritative UI hint).
 */
function edsPowerTryAutoOpenModule01Sidebar_(context) {
  const ctx = context && typeof context === "object" ? context : buildEDSPowerTerminalContext_();
  if (ctx.user_session_present !== true) {
    return;
  }
  try {
    edsPowerOpenModule01Sidebar();
  } catch (_e) {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    if (ss) {
      ss.toast(
        "Не вдалося відкрити бічну панель автоматично. Меню: EDS Power → Відкрити бокову панель.",
        "EDS Power",
        8
      );
    }
  }
}

function edsPowerRefreshMenu() {
  const context = buildEDSPowerTerminalContext_();
  return EDSPowerCore_refreshMenu(context);
}

function edsPowerLogin() {
  const context = buildEDSPowerTerminalContext_();
  return EDSPowerCore_login(context);
}

function edsPowerLogout() {
  const context = buildEDSPowerTerminalContext_();
  return EDSPowerCore_logout(context);
}

function edsPowerOpenModule(actionKey) {
  const context = buildEDSPowerTerminalContext_();
  return EDSPowerCore_openModule(actionKey || "", context);
}

function edsPowerShowFallbackError(message) {
  const context = buildEDSPowerTerminalContext_();
  if (typeof EDSPowerCore_showFallback === "function") {
    return EDSPowerCore_showFallback(message, context);
  }
  SpreadsheetApp.getUi().alert("EDS Power Fallback", String(message || "Fallback mode."), SpreadsheetApp.getUi().ButtonSet.OK);
  return {
    status: "fallback_local_only",
    bootstrap_version: EDS_POWER_BOOTSTRAP_VERSION
  };
}

function buildEDSPowerTerminalContext_() {
  const scriptProperties = PropertiesService.getScriptProperties();
  const terminalIdRaw = scriptProperties.getProperty(EDS_POWER_TERMINAL_ID_PROPERTY) || "";
  const terminalId = String(terminalIdRaw || "").trim() || "TERMINAL_TEMPLATE";
  const terminalIdMode = terminalId === "TERMINAL_TEMPLATE" ? "template_marker" : "assigned";
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const activeSheet = spreadsheet ? spreadsheet.getActiveSheet() : null;
  const sessionData = typeof module01AuthGetSession_ === "function" ? module01AuthGetSession_() : null;
  const expired =
    sessionData &&
    typeof module01AuthIsExpired_ === "function" &&
    module01AuthIsExpired_(sessionData);
  const hasSession = !!sessionData && !expired;
  return {
    terminal_id: terminalId,
    terminal_id_mode: terminalIdMode,
    spreadsheet_id: spreadsheet ? spreadsheet.getId() : "",
    active_sheet_name: activeSheet ? activeSheet.getName() : "",
    client_type: "GAS",
    bootstrap_version: EDS_POWER_BOOTSTRAP_VERSION,
    core_version: typeof EDSPowerCore_VERSION === "string" ? EDSPowerCore_VERSION : "unknown",
    user_session_present: hasSession === true
  };
}

function runEDSPowerTerminalFoundationHandshakeTest() {
  const context = buildEDSPowerTerminalContext_();
  const result = typeof EDSPowerCore_onTerminalOpen === "function"
    ? EDSPowerCore_onTerminalOpen(context)
    : { status: "core_unavailable", core_reachable: false };
  const safeOutput = {
    terminal_id_present: !!context.terminal_id,
    terminal_id: context.terminal_id,
    terminal_id_mode: context.terminal_id_mode,
    spreadsheet_id_present: !!context.spreadsheet_id,
    core_reachable: result && result.core_reachable === true,
    bootstrap_version: context.bootstrap_version,
    core_version: context.core_version,
    status: result && typeof result.status === "string" ? result.status : "unknown",
    no_token_logged: true,
    no_business_logic: true
  };
  Logger.log(JSON.stringify(safeOutput));
  return safeOutput;
}

function addEDSPowerEmergencyFallbackMenu_() {
  const ui = SpreadsheetApp.getUi();
  const ctx = typeof buildEDSPowerTerminalContext_ === "function" ? buildEDSPowerTerminalContext_() : {};
  const hasSession = ctx.user_session_present === true;
  const menu = ui.createMenu("EDS Power");
  if (hasSession) {
    menu.addItem("Перевірити сесію", "runModule01AuthenticatedSessionStatusCheck");
  } else {
    menu.addItem("Авторизуватись", "module01AuthLogin");
  }
  menu.addItem("Відкрити бокову панель", "edsPowerOpenModule01Sidebar");
  menu.addItem("Оновити меню", "edsPowerRefreshMenu");
  menu.addItem("Module 01 — Розрахунки", "edsPowerOpenModule01Sidebar");
  if (hasSession) {
    menu.addItem("Вийти", "module01AuthLogout");
  }
  menu.addSeparator();
  menu.addItem("⚠ Показати повідомлення про налаштування", "edsPowerShowFallbackSetupRequired_");
  menu.addToUi();
}

function edsPowerShowFallbackSetupRequired_() {
  edsPowerShowFallbackError("EDS Power terminal setup required.");
}
