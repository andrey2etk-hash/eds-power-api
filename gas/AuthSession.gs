const MODULE01_AUTH_STORAGE = {
  SESSION_TOKEN: "MODULE01_AUTH_SESSION_TOKEN",
  EXPIRES_AT: "MODULE01_AUTH_EXPIRES_AT",
  USER_EMAIL: "MODULE01_AUTH_USER_EMAIL",
  ROLE_CODES: "MODULE01_AUTH_ROLE_CODES"
};

function module01AuthGetSession_() {
  const props = PropertiesService.getUserProperties();
  const token = String(props.getProperty(MODULE01_AUTH_STORAGE.SESSION_TOKEN) || "").trim();
  const expiresAt = String(props.getProperty(MODULE01_AUTH_STORAGE.EXPIRES_AT) || "").trim();
  const userEmail = String(props.getProperty(MODULE01_AUTH_STORAGE.USER_EMAIL) || "").trim();
  const roleCodesRaw = String(props.getProperty(MODULE01_AUTH_STORAGE.ROLE_CODES) || "").trim();

  if (!token) {
    return null;
  }

  let roleCodes = [];
  if (roleCodesRaw) {
    try {
      const parsed = JSON.parse(roleCodesRaw);
      roleCodes = Array.isArray(parsed) ? parsed : [];
    } catch (_error) {
      roleCodes = [];
    }
  }

  return {
    session_token: token,
    expires_at: expiresAt,
    user_email: userEmail,
    role_codes: roleCodes
  };
}

function module01AuthStoreSession_(sessionData) {
  const props = PropertiesService.getUserProperties();
  props.setProperty(MODULE01_AUTH_STORAGE.SESSION_TOKEN, String(sessionData.session_token || "").trim());
  props.setProperty(MODULE01_AUTH_STORAGE.EXPIRES_AT, String(sessionData.expires_at || "").trim());
  props.setProperty(MODULE01_AUTH_STORAGE.USER_EMAIL, String(sessionData.user_email || "").trim());
  props.setProperty(
    MODULE01_AUTH_STORAGE.ROLE_CODES,
    JSON.stringify(Array.isArray(sessionData.role_codes) ? sessionData.role_codes : [])
  );
}

function module01AuthClearSession_() {
  const props = PropertiesService.getUserProperties();
  props.deleteProperty(MODULE01_AUTH_STORAGE.SESSION_TOKEN);
  props.deleteProperty(MODULE01_AUTH_STORAGE.EXPIRES_AT);
  props.deleteProperty(MODULE01_AUTH_STORAGE.USER_EMAIL);
  props.deleteProperty(MODULE01_AUTH_STORAGE.ROLE_CODES);
}

function module01AuthHasSession_() {
  return module01AuthGetSession_() !== null;
}

function module01AuthIsExpired_(sessionData) {
  const raw = String((sessionData && sessionData.expires_at) || "").trim();
  if (!raw) {
    return false;
  }
  const expiresAtMs = Date.parse(raw);
  if (isNaN(expiresAtMs)) {
    return false;
  }
  return Date.now() >= expiresAtMs;
}

function module01AuthBuildBearerHeaders_() {
  const sessionData = module01AuthGetSession_();
  if (!sessionData || !sessionData.session_token) {
    throw new Error("SESSION_MISSING");
  }
  if (module01AuthIsExpired_(sessionData)) {
    throw new Error("SESSION_EXPIRED");
  }
  return {
    Authorization: "Bearer " + sessionData.session_token
  };
}
