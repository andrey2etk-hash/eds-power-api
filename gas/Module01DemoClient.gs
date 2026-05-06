const MODULE01_DEMO_SHEET_NAME = "MODULE_01_DEMO";
const MODULE01_DEMO_ENDPOINT_PATH = "/api/demo/module-01/kzo/run";
const MODULE01_DEMO_CONTROL_RANGE_A1 = "A1:H9";
const MODULE01_DEMO_STATUS_RANGE_A1 = "A12:D16";
const MODULE01_DEMO_FLOW_RANGE_A1 = "A19:E25";
const MODULE01_DEMO_NODE_RANGE_A1 = "A28:H40";
const MODULE01_DEMO_FASTENER_RANGE_A1 = "A43:I55";
const MODULE01_DEMO_KIT_RANGE_A1 = "A58:H70";
const MODULE01_DEMO_TRACE_RANGE_A1 = "A73:H85";
const MODULE01_DEMO_SUMMARY_RANGE_A1 = "A88:H96";
const MODULE01_DEMO_ERROR_RANGE_A1 = "A99:H108";
const MODULE01_DEMO_RESULT_RANGES_TO_CLEAR = [
  MODULE01_DEMO_STATUS_RANGE_A1,
  MODULE01_DEMO_FLOW_RANGE_A1,
  MODULE01_DEMO_NODE_RANGE_A1,
  MODULE01_DEMO_FASTENER_RANGE_A1,
  MODULE01_DEMO_KIT_RANGE_A1,
  MODULE01_DEMO_TRACE_RANGE_A1,
  MODULE01_DEMO_SUMMARY_RANGE_A1,
  MODULE01_DEMO_ERROR_RANGE_A1
];

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu("EDS Power Demo")
    .addItem("Run Module 01 Demo", "runModule01Demo")
    .addItem("Clear Module 01 Demo Output", "clearModule01DemoOutput")
    .addToUi();
  if (typeof module01AuthOnOpen_ === "function") {
    module01AuthOnOpen_();
  }
}

function runModule01Demo() {
  const sheet = ensureModule01DemoSheet_();
  clearModule01DemoOutput();
  setModule01RunStatus_(sheet, "RUNNING...");
  setModule01LastRunTime_(sheet, new Date().toISOString());

  const endpointUrl = buildModule01DemoEndpointUrl_(sheet);
  if (!endpointUrl) {
    writeModule01TransportError_(new Error("API URL is required in cell B2."));
    return;
  }

  const requestEnvelope = buildModule01DemoRequest_();
  setModule01LastRequestId_(sheet, requestEnvelope.request_id);

  const options = {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(requestEnvelope),
    muteHttpExceptions: true
  };

  try {
    const response = UrlFetchApp.fetch(endpointUrl, options);
    const httpStatus = response.getResponseCode();
    validateDemoHeader_(response);

    const responseText = response.getContentText();
    let envelope;
    try {
      envelope = JSON.parse(responseText);
    } catch (_jsonError) {
      throw new Error("Invalid JSON response from Demo API.");
    }

    if (!envelope || typeof envelope !== "object" || !envelope.status) {
      throw new Error("Invalid response envelope from Demo API.");
    }

    if (envelope.status === "error") {
      clearModule01EngineeringBlocks_(sheet);
      writeModule01Error_(envelope);
      setModule01RunStatus_(sheet, "ERROR");
      return;
    }

    if (envelope.status === "success" && httpStatus >= 200 && httpStatus < 300) {
      validateModule01SuccessEnvelope_(envelope, requestEnvelope.request_id);
      writeModule01Success_(envelope);
      setModule01RunStatus_(sheet, "PASS");
      return;
    }

    if (httpStatus < 200 || httpStatus >= 300) {
      throw new Error("Demo API returned non-success HTTP status: " + String(httpStatus));
    }

    throw new Error("Unsupported envelope.status in Demo API response.");
  } catch (error) {
    clearModule01EngineeringBlocks_(sheet);
    writeModule01TransportError_(error);
    setModule01RunStatus_(sheet, "TRANSPORT_ERROR");
  }
}

function clearModule01DemoOutput() {
  const sheet = ensureModule01DemoSheet_();
  ensureModule01DemoLayout_(sheet);
  MODULE01_DEMO_RESULT_RANGES_TO_CLEAR.forEach(function(rangeA1) {
    sheet.getRange(rangeA1).clearContent();
  });
  setModule01RunStatus_(sheet, "");
}

function buildModule01DemoRequest_() {
  return {
    request_id: generateUuidV4_(),
    client_type: "GAS_DEMO",
    mode: "MODULE_01_DEMO",
    product_type: "KZO",
    demo_id: "MODULE_01_KZO_DEMO_001",
    requested_output_blocks: [
      "demo_status",
      "status_flow",
      "node_results",
      "fastener_decisions",
      "kit_issue_lines",
      "traceability",
      "boundary_note",
      "management_summary",
      "registry_versions"
    ],
    operator_context: {
      source: "GOOGLE_SHEETS",
      sheet_name: MODULE01_DEMO_SHEET_NAME
    }
  };
}

function generateUuidV4_() {
  return Utilities.getUuid().toLowerCase();
}

function validateDemoHeader_(httpResponse) {
  const headers = httpResponse.getAllHeaders() || {};
  const demoModeValue =
    headers["X-EDS-Power-Mode"] ||
    headers["x-eds-power-mode"] ||
    headers["X-Eds-Power-Mode"] ||
    null;
  if (demoModeValue !== "DEMO") {
    throw new Error("Invalid demo mode response header. Expected X-EDS-Power-Mode=DEMO.");
  }
}

function writeModule01Success_(envelope) {
  const sheet = ensureModule01DemoSheet_();
  ensureModule01DemoLayout_(sheet);
  clearModule01EngineeringBlocks_(sheet);
  clearModule01ErrorBlock_(sheet);

  const data = envelope.data || {};
  const metadata = envelope.metadata || {};
  setModule01LastRequestId_(sheet, metadata.request_id || "");
  setModule01LastRunTime_(sheet, metadata.generated_at || new Date().toISOString());

  writeRowsWithHeader_(
    sheet,
    MODULE01_DEMO_STATUS_RANGE_A1,
    ["Field", "Value"],
    [
      ["status", envelope.status],
      ["demo_status", data.demo_status || ""],
      ["demo_id", data.demo_id || ""],
      ["demo_version", metadata.demo_version || ""]
    ]
  );

  const statusFlowRows = objectToRows_(data.status_flow || {}, "step", "status");
  writeRowsWithHeader_(sheet, MODULE01_DEMO_FLOW_RANGE_A1, ["Step", "Status"], statusFlowRows);

  const nodeRows = buildNodeResultsRows_(data.node_results || {});
  writeRowsWithHeader_(
    sheet,
    MODULE01_DEMO_NODE_RANGE_A1,
    [
      "Node",
      "Total Busbar Length, mm",
      "Joint Stacks",
      "Selected Bolts",
      "Slice Status",
      "Reserved1",
      "Reserved2",
      "Reserved3"
    ],
    nodeRows
  );

  const fastenerRows = (data.fastener_decisions || []).map(function(row) {
    return [
      row.node || "",
      row.connection_group || "",
      row.required_bolt_length_mm != null ? row.required_bolt_length_mm : "",
      row.candidate_bolt || "",
      row.candidate_length_mm != null ? row.candidate_length_mm : "",
      row.decision || "",
      row.selected_bolt || "",
      row.reason || "",
      row.registry_version || ""
    ];
  });
  writeRowsWithHeader_(
    sheet,
    MODULE01_DEMO_FASTENER_RANGE_A1,
    [
      "Node",
      "Connection Group",
      "Required Bolt Length, mm",
      "Candidate Bolt",
      "Candidate Length, mm",
      "Decision",
      "Selected Bolt",
      "Reason",
      "Registry Version"
    ],
    fastenerRows
  );

  const kitRows = (data.kit_issue_lines || []).map(function(line) {
    return [
      line.item_id || "",
      line.display_name || "",
      line.item_type || "",
      line.total_quantity != null ? line.total_quantity : "",
      line.unit || "",
      line.registry_version || "",
      safeJoin_(line.source_node_ids),
      safeJoin_(line.traceability_refs)
    ];
  });
  writeRowsWithHeader_(
    sheet,
    MODULE01_DEMO_KIT_RANGE_A1,
    [
      "Item ID",
      "Display Name",
      "Item Type",
      "Total Quantity",
      "Unit",
      "Registry Version",
      "Source Node IDs",
      "Traceability Refs"
    ],
    kitRows
  );

  const traceRows = buildTraceabilityRows_(data);
  writeRowsWithHeader_(
    sheet,
    MODULE01_DEMO_TRACE_RANGE_A1,
    [
      "Item ID",
      "Source Node IDs",
      "Source Line IDs",
      "Traceability Refs",
      "Registry Version",
      "",
      "",
      ""
    ],
    traceRows
  );

  const summaryRows = [
    ["Boundary Note", data.boundary_note || ""],
    ["Management Summary", data.management_summary || ""],
    ["Visible Note", "Production-preparation kit issue only - not final ERP BOM."]
  ];
  writeRowsWithHeader_(
    sheet,
    MODULE01_DEMO_SUMMARY_RANGE_A1,
    ["Field", "Value", "", "", "", "", "", ""],
    summaryRows
  );
}

function writeModule01Error_(errorEnvelope) {
  const sheet = ensureModule01DemoSheet_();
  ensureModule01DemoLayout_(sheet);
  clearModule01ErrorBlock_(sheet);

  const errorObj = errorEnvelope.error || {};
  const metadata = errorEnvelope.metadata || {};
  writeRowsWithHeader_(
    sheet,
    MODULE01_DEMO_ERROR_RANGE_A1,
    ["Field", "Value"],
    [
      ["status", "error"],
      ["error_code", errorObj.error_code || ""],
      ["message", errorObj.message || ""],
      ["source_field", errorObj.source_field || ""],
      ["notes", safeJoin_(errorObj.notes)],
      ["request_id", metadata.request_id || ""]
    ]
  );
}

function writeModule01TransportError_(err) {
  const sheet = ensureModule01DemoSheet_();
  ensureModule01DemoLayout_(sheet);
  clearModule01ErrorBlock_(sheet);
  writeRowsWithHeader_(
    sheet,
    MODULE01_DEMO_ERROR_RANGE_A1,
    ["Field", "Value"],
    [
      ["status", "TRANSPORT_ERROR"],
      ["message", err && err.message ? String(err.message) : String(err)],
      ["timestamp", new Date().toISOString()]
    ]
  );
}

function ensureModule01DemoSheet_() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  if (!spreadsheet) {
    throw new Error("Active spreadsheet is required.");
  }
  const existing = spreadsheet.getSheetByName(MODULE01_DEMO_SHEET_NAME);
  const sheet = existing || spreadsheet.insertSheet(MODULE01_DEMO_SHEET_NAME);
  ensureModule01DemoLayout_(sheet);
  return sheet;
}

function ensureModule01DemoLayout_(sheet) {
  if (sheet.getRange("A1").getValue() !== "MODULE_01_DEMO - Thin Client") {
    sheet.getRange(MODULE01_DEMO_CONTROL_RANGE_A1).setValues([
      ["MODULE_01_DEMO - Thin Client", "", "", "", "", "", "", ""],
      ["API URL", "", "", "", "", "", "", ""],
      ["Demo ID", "MODULE_01_KZO_DEMO_001", "", "", "", "", "", ""],
      ["Client Type", "GAS_DEMO", "", "", "", "", "", ""],
      ["Mode", "MODULE_01_DEMO", "", "", "", "", "", ""],
      ["Product Type", "KZO", "", "", "", "", "", ""],
      ["Run Status", "", "", "", "", "", "", ""],
      ["Last Request ID", "", "", "", "", "", "", ""],
      ["Last Run Time", "", "", "", "", "", "", ""]
    ]);
    sheet.getRange("A1:H1").setFontWeight("bold");
    sheet.getRange("A2:A9").setFontWeight("bold");
    sheet.getRange("B2").setNote("Set API base URL or full endpoint URL.");
  }
}

function buildModule01DemoEndpointUrl_(sheet) {
  const raw = String(sheet.getRange("B2").getValue() || "").trim();
  if (!raw) {
    return "";
  }
  if (raw.indexOf(MODULE01_DEMO_ENDPOINT_PATH) >= 0) {
    return raw;
  }
  return raw.replace(/\/+$/, "") + MODULE01_DEMO_ENDPOINT_PATH;
}

function setModule01RunStatus_(sheet, statusText) {
  sheet.getRange("B7").setValue(statusText || "");
}

function setModule01LastRequestId_(sheet, requestId) {
  sheet.getRange("B8").setValue(requestId || "");
}

function setModule01LastRunTime_(sheet, timestampIso) {
  sheet.getRange("B9").setValue(timestampIso || "");
}

function clearModule01EngineeringBlocks_(sheet) {
  [
    MODULE01_DEMO_STATUS_RANGE_A1,
    MODULE01_DEMO_FLOW_RANGE_A1,
    MODULE01_DEMO_NODE_RANGE_A1,
    MODULE01_DEMO_FASTENER_RANGE_A1,
    MODULE01_DEMO_KIT_RANGE_A1,
    MODULE01_DEMO_TRACE_RANGE_A1,
    MODULE01_DEMO_SUMMARY_RANGE_A1
  ].forEach(function(rangeA1) {
    sheet.getRange(rangeA1).clearContent();
  });
}

function clearModule01ErrorBlock_(sheet) {
  sheet.getRange(MODULE01_DEMO_ERROR_RANGE_A1).clearContent();
}

function writeRowsWithHeader_(sheet, rangeA1, headerRow, rows) {
  const range = sheet.getRange(rangeA1);
  const rowCount = range.getNumRows();
  const colCount = range.getNumColumns();
  const output = [];
  output.push(fillRow_(headerRow, colCount));
  (rows || []).forEach(function(row) {
    if (output.length < rowCount) {
      output.push(fillRow_(row, colCount));
    }
  });
  while (output.length < rowCount) {
    output.push(fillRow_([], colCount));
  }
  range.setValues(output);
  sheet.getRange(range.getRow(), range.getColumn(), 1, colCount).setFontWeight("bold");
}

function fillRow_(values, width) {
  const out = [];
  let i;
  for (i = 0; i < width; i += 1) {
    out.push(values && values[i] !== undefined ? values[i] : "");
  }
  return out;
}

function objectToRows_(obj, keyHeader, valueHeader) {
  const keys = Object.keys(obj || {});
  return keys.map(function(key) {
    return [key, obj[key]];
  });
}

function safeJoin_(value) {
  if (!value) {
    return "";
  }
  if (Array.isArray(value)) {
    return value.join(", ");
  }
  return String(value);
}

function buildNodeResultsRows_(nodeResults) {
  return Object.keys(nodeResults || {}).map(function(nodeId) {
    const block = nodeResults[nodeId] || {};
    return [
      nodeId,
      block.total_busbar_length_mm != null ? block.total_busbar_length_mm : "",
      block.joint_stacks ? JSON.stringify(block.joint_stacks) : "",
      block.selected_bolts ? JSON.stringify(block.selected_bolts) : "",
      block.status || "",
      "",
      "",
      ""
    ];
  });
}

function buildTraceabilityRows_(data) {
  const lines = data.kit_issue_lines || [];
  if (lines.length > 0) {
    return lines.map(function(line) {
      return [
        line.item_id || "",
        safeJoin_(line.source_node_ids),
        safeJoin_(line.source_line_ids),
        safeJoin_(line.traceability_refs),
        line.registry_version || "",
        "",
        "",
        ""
      ];
    });
  }
  const trace = data.traceability || {};
  return [[
    "",
    safeJoin_(trace.source_node_ids),
    safeJoin_(trace.source_line_ids),
    safeJoin_(trace.traceability_refs),
    "",
    "",
    "",
    ""
  ]];
}

function validateModule01SuccessEnvelope_(envelope, sentRequestId) {
  const metadata = envelope.metadata || {};
  if (metadata.request_id !== sentRequestId) {
    throw new Error("Response request_id does not match sent request_id.");
  }
  if (metadata.client_type !== "GAS_DEMO") {
    throw new Error("Response client_type is invalid for demo flow.");
  }
  if (metadata.demo_version !== "demo_v1") {
    throw new Error("Response demo_version is invalid for demo flow.");
  }
}
