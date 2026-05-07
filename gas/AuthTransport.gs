const MODULE01_AUTH_ENDPOINT_PATH = "/api/module01/auth/login";
const MODULE01_AUTH_SESSION_STATUS_ENDPOINT_PATH = "/api/module01/auth/session/status";
const MODULE01_SIDEBAR_CONTEXT_ENDPOINT_PATH = "/api/module01/sidebar/context";
const MODULE01_CREATE_CALCULATION_ENDPOINT_PATH = "/api/module01/calculations/create";
const MODULE01_AUTH_BASE_URL_PROPERTY = "MODULE01_API_BASE_URL";

function module01AuthRedactUrl_(url) {
  const raw = String(url || "").trim();
  if (!raw) {
    return "";
  }
  const qIndex = raw.indexOf("?");
  return qIndex >= 0 ? raw.substring(0, qIndex) : raw;
}

function module01AuthResolveLoginUrl_() {
  const scriptProps = PropertiesService.getScriptProperties();
  const baseUrl = String(scriptProps.getProperty(MODULE01_AUTH_BASE_URL_PROPERTY) || "").trim();
  const apiBaseUrlPresent = !!baseUrl;
  if (!baseUrl) {
    throw {
      code: "AUTH_TRANSPORT_BASE_URL_MISSING",
      message: "API base URL is missing.",
      api_base_url_present: false,
      endpoint_path: MODULE01_AUTH_ENDPOINT_PATH,
      endpoint_url_redacted: ""
    };
  }
  return {
    endpointUrl: baseUrl.replace(/\/+$/, "") + MODULE01_AUTH_ENDPOINT_PATH,
    apiBaseUrlPresent: apiBaseUrlPresent
  };
}

function module01AuthResolveSessionStatusUrl_() {
  const scriptProps = PropertiesService.getScriptProperties();
  const baseUrl = String(scriptProps.getProperty(MODULE01_AUTH_BASE_URL_PROPERTY) || "").trim();
  if (!baseUrl) {
    throw {
      code: "AUTH_TRANSPORT_BASE_URL_MISSING",
      message: "API base URL is missing.",
      api_base_url_present: false,
      endpoint_path: MODULE01_AUTH_SESSION_STATUS_ENDPOINT_PATH,
      endpoint_url_redacted: ""
    };
  }
  return baseUrl.replace(/\/+$/, "") + MODULE01_AUTH_SESSION_STATUS_ENDPOINT_PATH;
}

function module01AuthResolveSidebarContextUrl_() {
  const scriptProps = PropertiesService.getScriptProperties();
  const baseUrl = String(scriptProps.getProperty(MODULE01_AUTH_BASE_URL_PROPERTY) || "").trim();
  if (!baseUrl) {
    throw {
      code: "AUTH_TRANSPORT_BASE_URL_MISSING",
      message: "API base URL is missing.",
      api_base_url_present: false,
      endpoint_path: MODULE01_SIDEBAR_CONTEXT_ENDPOINT_PATH,
      endpoint_url_redacted: ""
    };
  }
  return baseUrl.replace(/\/+$/, "") + MODULE01_SIDEBAR_CONTEXT_ENDPOINT_PATH;
}

function module01AuthLoginTransport_(email, password, spreadsheetId) {
  const resolved = module01AuthResolveLoginUrl_();
  const endpointUrl = resolved.endpointUrl;
  const endpointUrlRedacted = module01AuthRedactUrl_(endpointUrl);
  const apiBaseUrlPresent = !!resolved.apiBaseUrlPresent;
  const payload = {
    email: String(email || "").trim(),
    password: String(password || ""),
    spreadsheet_id: String(spreadsheetId || "").trim()
  };

  let response;
  try {
    response = UrlFetchApp.fetch(endpointUrl, {
      method: "post",
      contentType: "application/json",
      payload: JSON.stringify(payload),
      muteHttpExceptions: true
    });
  } catch (error) {
    throw {
      code: "AUTH_TRANSPORT_FETCH_FAILED",
      message: String((error && error.message) || error || "Unknown transport error."),
      api_base_url_present: apiBaseUrlPresent,
      endpoint_path: MODULE01_AUTH_ENDPOINT_PATH,
      endpoint_url_redacted: endpointUrlRedacted
    };
  }

  const responseText = response.getContentText();
  let envelope = null;
  try {
    envelope = JSON.parse(responseText);
  } catch (error) {
    throw {
      code: "AUTH_TRANSPORT_INVALID_JSON",
      message: String((error && error.message) || "Invalid JSON response."),
      api_base_url_present: apiBaseUrlPresent,
      endpoint_path: MODULE01_AUTH_ENDPOINT_PATH,
      endpoint_url_redacted: endpointUrlRedacted
    };
  }
  if (!envelope || typeof envelope !== "object") {
    throw {
      code: "AUTH_TRANSPORT_INVALID_ENVELOPE",
      message: "Invalid response envelope.",
      api_base_url_present: apiBaseUrlPresent,
      endpoint_path: MODULE01_AUTH_ENDPOINT_PATH,
      endpoint_url_redacted: endpointUrlRedacted
    };
  }
  return {
    http_status: response.getResponseCode(),
    envelope: envelope
  };
}

function module01AuthSessionStatusTransport_(sessionToken) {
  const endpointUrl = module01AuthResolveSessionStatusUrl_();
  const token = String(sessionToken || "").trim();
  if (!token) {
    throw new Error("SESSION_TOKEN_MISSING");
  }

  const response = UrlFetchApp.fetch(endpointUrl, {
    method: "get",
    headers: {
      Authorization: "Bearer " + token
    },
    muteHttpExceptions: true
  });

  const responseText = response.getContentText();
  let envelope = null;
  try {
    envelope = JSON.parse(responseText);
  } catch (_error) {
    throw new Error("AUTH_STATUS_INVALID_JSON");
  }
  if (!envelope || typeof envelope !== "object") {
    throw new Error("AUTH_STATUS_INVALID_ENVELOPE");
  }
  return {
    http_status: response.getResponseCode(),
    envelope: envelope
  };
}

function module01AuthResolveCreateCalculationUrl_() {
  const scriptProps = PropertiesService.getScriptProperties();
  const baseUrl = String(scriptProps.getProperty(MODULE01_AUTH_BASE_URL_PROPERTY) || "").trim();
  if (!baseUrl) {
    throw {
      code: "AUTH_TRANSPORT_BASE_URL_MISSING",
      message: "API base URL is missing.",
      api_base_url_present: false,
      endpoint_path: MODULE01_CREATE_CALCULATION_ENDPOINT_PATH,
      endpoint_url_redacted: ""
    };
  }
  return baseUrl.replace(/\/+$/, "") + MODULE01_CREATE_CALCULATION_ENDPOINT_PATH;
}

function module01CreateCalculationTransport_(sessionToken, requestBody) {
  const endpointUrl = module01AuthResolveCreateCalculationUrl_();
  const token = String(sessionToken || "").trim();
  if (!token) {
    throw new Error("SESSION_TOKEN_MISSING");
  }
  const response = UrlFetchApp.fetch(endpointUrl, {
    method: "post",
    contentType: "application/json",
    headers: {
      Authorization: "Bearer " + token
    },
    payload: JSON.stringify(requestBody || {}),
    muteHttpExceptions: true
  });
  const responseText = response.getContentText();
  var envelope = null;
  try {
    envelope = JSON.parse(responseText);
  } catch (_e) {
    throw new Error("CREATE_CALC_INVALID_JSON");
  }
  if (!envelope || typeof envelope !== "object") {
    throw new Error("CREATE_CALC_INVALID_ENVELOPE");
  }
  return {
    http_status: response.getResponseCode(),
    envelope: envelope
  };
}

function module01SidebarContextTransport_(sessionToken) {
  const endpointUrl = module01AuthResolveSidebarContextUrl_();
  const token = String(sessionToken || "").trim();
  if (!token) {
    throw new Error("SESSION_TOKEN_MISSING");
  }

  const response = UrlFetchApp.fetch(endpointUrl, {
    method: "get",
    headers: {
      Authorization: "Bearer " + token
    },
    muteHttpExceptions: true
  });

  const responseText = response.getContentText();
  let envelope = null;
  try {
    envelope = JSON.parse(responseText);
  } catch (_error) {
    throw new Error("SIDEBAR_CONTEXT_INVALID_JSON");
  }
  if (!envelope || typeof envelope !== "object") {
    throw new Error("SIDEBAR_CONTEXT_INVALID_ENVELOPE");
  }
  return {
    http_status: response.getResponseCode(),
    envelope: envelope
  };
}
