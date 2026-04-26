from time import perf_counter
from typing import Any
from uuid import uuid4

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


KZO_REQUIRED_FIELDS = (
    "object_number",
    "product_type",
    "logic_version",
    "voltage_class",
    "busbar_current",
    "configuration_type",
    "quantity_total",
    "cell_distribution",
    "status",
)

KZO_VOLTAGE_CLASSES = {"VC_06", "VC_10", "VC_20", "VC_35"}
KZO_CONFIGURATION_TYPES = {"CFG_SINGLE_BUS", "CFG_SINGLE_BUS_SECTION"}
KZO_CELL_TYPES = {
    "CELL_INCOMER",
    "CELL_OUTGOING",
    "CELL_PT",
    "CELL_BUS_SECTION",
}
KZO_OBJECT_STATUSES = {
    "DRAFT",
    "VALIDATED",
    "LOCKED",
    "SENT_TO_NEXT_MODULE",
    "ARCHIVED",
    "ERROR",
}


def _response_metadata(meta: dict[str, Any] | None, logic_version: str | None, started_at: float) -> dict[str, Any]:
    return {
        "request_id": (meta or {}).get("request_id") or str(uuid4()),
        "api_version": "0.1.0",
        "logic_version": logic_version,
        "execution_time_ms": int((perf_counter() - started_at) * 1000),
    }


def _validation_error(
    *,
    message: str,
    source_field: str,
    error_code: str,
    meta: dict[str, Any] | None,
    logic_version: str | None,
    started_at: float,
) -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content={
            "status": "validation_error",
            "data": None,
            "error": {
                "error_code": error_code,
                "message": message,
                "source_field": source_field,
                "module": "CALC_CONFIGURATOR",
                "action": "prepare_calculation",
            },
            "metadata": _response_metadata(meta, logic_version, started_at),
        },
    )


def _validate_kzo_payload(payload: dict[str, Any]) -> tuple[dict[str, Any] | None, tuple[str, str, str] | None]:
    for field in KZO_REQUIRED_FIELDS:
        if field not in payload or payload[field] is None:
            return None, (
                "KZO_REQUIRED_FIELD_MISSING",
                f"Required field {field} is missing",
                field,
            )

    if payload["product_type"] != "KZO":
        return None, ("KZO_UNSUPPORTED_CONFIGURATION", "Only KZO product_type is supported", "product_type")

    if payload["voltage_class"] not in KZO_VOLTAGE_CLASSES:
        return None, ("KZO_INVALID_VOLTAGE_CLASS", "Invalid voltage_class", "voltage_class")

    if payload["configuration_type"] not in KZO_CONFIGURATION_TYPES:
        return None, ("KZO_UNSUPPORTED_CONFIGURATION", "Unsupported configuration_type", "configuration_type")

    if payload["status"] not in KZO_OBJECT_STATUSES:
        return None, ("KZO_UNSUPPORTED_CONFIGURATION", "Unsupported object status", "status")

    if not isinstance(payload["quantity_total"], int) or payload["quantity_total"] <= 0:
        return None, ("KZO_CELL_QUANTITY_MISMATCH", "quantity_total must be a positive integer", "quantity_total")

    cell_distribution = payload["cell_distribution"]
    if not isinstance(cell_distribution, dict):
        return None, ("KZO_CELL_QUANTITY_MISMATCH", "cell_distribution must be an object", "cell_distribution")

    for cell_type, quantity in cell_distribution.items():
        if cell_type not in KZO_CELL_TYPES:
            return None, ("KZO_UNSUPPORTED_CONFIGURATION", "Unsupported cell_type", "cell_distribution")
        if not isinstance(quantity, int) or quantity < 0:
            return None, ("KZO_CELL_QUANTITY_MISMATCH", "Cell quantities must be non-negative integers", "cell_distribution")

    if sum(cell_distribution.values()) != payload["quantity_total"]:
        return None, (
            "KZO_CELL_QUANTITY_MISMATCH",
            "Cell distribution sum must match quantity_total",
            "cell_distribution",
        )

    normalized_payload = {field: payload[field] for field in KZO_REQUIRED_FIELDS}
    normalized_payload["status"] = "VALIDATED"
    normalized_payload["breaker_type"] = payload.get("breaker_type")
    normalized_payload["notes"] = payload.get("notes")

    return normalized_payload, None


@app.get("/")
def root():
    return {"message": "EDS Power API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/calc/prepare_calculation")
def prepare_calculation(request: dict[str, Any]):
    started_at = perf_counter()
    meta = request.get("meta") if isinstance(request.get("meta"), dict) else None
    payload = request.get("payload") if isinstance(request.get("payload"), dict) else None
    logic_version = payload.get("logic_version") if payload else None

    for field in ("meta", "module", "action", "payload"):
        if field not in request:
            return _validation_error(
                message=f"Required envelope field {field} is missing",
                source_field=field,
                error_code="KZO_REQUIRED_FIELD_MISSING",
                meta=meta,
                logic_version=logic_version,
                started_at=started_at,
            )

    if request["module"] != "CALC_CONFIGURATOR":
        return _validation_error(
            message="module must be CALC_CONFIGURATOR",
            source_field="module",
            error_code="KZO_UNSUPPORTED_CONFIGURATION",
            meta=meta,
            logic_version=logic_version,
            started_at=started_at,
        )

    if request["action"] != "prepare_calculation":
        return _validation_error(
            message="action must be prepare_calculation",
            source_field="action",
            error_code="KZO_UNSUPPORTED_CONFIGURATION",
            meta=meta,
            logic_version=logic_version,
            started_at=started_at,
        )

    if payload is None:
        return _validation_error(
            message="payload must be an object",
            source_field="payload",
            error_code="KZO_REQUIRED_FIELD_MISSING",
            meta=meta,
            logic_version=logic_version,
            started_at=started_at,
        )

    normalized_payload, error = _validate_kzo_payload(payload)
    if error:
        error_code, message, source_field = error
        return _validation_error(
            message=message,
            source_field=source_field,
            error_code=error_code,
            meta=meta,
            logic_version=logic_version,
            started_at=started_at,
        )

    cell_type_summary = {
        cell_type: normalized_payload["cell_distribution"][cell_type]
        for cell_type in sorted(normalized_payload["cell_distribution"])
    }

    return {
        "status": "success",
        "data": {
            "validation_status": "VALIDATED",
            "logic_version": normalized_payload["logic_version"],
            "status": normalized_payload["status"],
            "normalized_payload": normalized_payload,
            "basic_result_summary": {
                "summary_version": "KZO_MVP_V1",
                "product_type": normalized_payload["product_type"],
                "logic_version": normalized_payload["logic_version"],
                "voltage_class": normalized_payload["voltage_class"],
                "busbar_current": normalized_payload["busbar_current"],
                "configuration_type": normalized_payload["configuration_type"],
                "quantity_total": normalized_payload["quantity_total"],
                "cell_type_summary": cell_type_summary,
                "validation_status": "VALIDATED",
            },
        },
        "error": None,
        "metadata": _response_metadata(meta, normalized_payload["logic_version"], started_at),
    }
