/**
 * Module 01 sidebar shell — transport + show sidebar only (no business logic).
 */

function edsPowerOpenModule01Sidebar() {
  const html = HtmlService.createHtmlOutputFromFile("Module01Sidebar");
  html.setTitle("Module 01 — Розрахунки");
  SpreadsheetApp.getUi().showSidebar(html);
}

/**
 * Called from sidebar HTML via google.script.run — returns safe summary for UI.
 */
function module01SidebarServerGetContext() {
  return module01SidebarBuildSafeContext_();
}

function module01SidebarBuildSafeContext_() {
  var token = "";
  if (typeof module01AuthGetSession_ === "function") {
    var s = module01AuthGetSession_();
    token = s && typeof s.session_token === "string" ? String(s.session_token).trim() : "";
  }
  if (!token) {
    return {
      ok: false,
      code: "AUTH_MISSING_TOKEN",
      message: "Потрібна авторизація. Увійдіть через EDS Power / Module 01 Auth."
    };
  }

  try {
    var tr = module01SidebarContextTransport_(token);
    var httpStatus = typeof tr.http_status === "number" ? tr.http_status : 0;
    var envelope = tr.envelope || {};

    if (httpStatus >= 500) {
      return {
        ok: false,
        code: "MODULE01_BACKEND_UNAVAILABLE",
        message: "Сервер тимчасово недоступний. Спробуйте пізніше.",
        http_status: httpStatus
      };
    }

    var envStatus = typeof envelope.status === "string" ? envelope.status : "";
    if (envStatus === "auth_error") {
      var ae = envelope.error && typeof envelope.error === "object" ? envelope.error : {};
      var ac = typeof ae.error_code === "string" ? ae.error_code : "AUTH_INVALID_TOKEN";
      var am =
        typeof ae.message === "string" && ae.message
          ? ae.message
          : "Помилка авторизації.";
      if (ac === "AUTH_SESSION_EXPIRED") {
        am = "Сесію закінчено. Увійдіть знову.";
      }
      if (ac === "AUTH_MISSING_TOKEN") {
        am = "Токен відсутній. Увійдіть знову.";
      }
      return {ok: false, code: ac, message: am, http_status: httpStatus};
    }

    if (envStatus === "error") {
      var ee = envelope.error && typeof envelope.error === "object" ? envelope.error : {};
      var ec = typeof ee.error_code === "string" ? ee.error_code : "MODULE01_SIDEBAR_CONTEXT_UNAVAILABLE";
      var em =
        typeof ee.message === "string" && ee.message
          ? ee.message
          : "Не вдалося завантажити контекст бічної панелі.";
      return {ok: false, code: ec, message: em, http_status: httpStatus};
    }

    if (envStatus !== "success" || !envelope.data || !envelope.data.sidebar) {
      return {
        ok: false,
        code: "MODULE01_SIDEBAR_CONTEXT_UNAVAILABLE",
        message: "Некоректна відповідь сервера.",
        http_status: httpStatus
      };
    }

    return {ok: true, envelope: envelope, http_status: httpStatus};
  } catch (error) {
    var err = error && typeof error === "object" ? error : {};
    var c = typeof err.code === "string" ? err.code : "SIDEBAR_TRANSPORT_ERROR";
    return {
      ok: false,
      code: c,
      message: "Не вдалося зв'язатися з API. Перевірте MODULE01_API_BASE_URL.",
      transport: true
    };
  }
}
