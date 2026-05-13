"""Module 01 — Calculation Items API V1 (add + list). No product/engine/GAS. Bounded slice."""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from typing import Any
from uuid import UUID

try:
    from supabase import Client
except ImportError:  # pragma: no cover
    Client = Any  # type: ignore[misc, assignment]

from services.module01_calculations_service import _is_unique_violation, _table_fetch_single

ALLOWED_ITEM_KINDS = frozenset({"CONTAINER", "PRODUCT", "SERVICE", "MANUAL", "CUSTOM"})

# STRICT_REJECT (DOC_CASCADE_VERIFIED_STRICT_REJECT_LOCKED): these item_type values are child-only
# and must not be created with parent_item_id null. Legacy aliases KZO / SHCHO map to KZO_CELL / SHOS_CABINET.
_CHILD_ONLY_ITEM_TYPES = frozenset(
    {
        "KZO_CELL",
        "SHOS_CABINET",
        "SERVICE_ITEM",
        "KZO",
        "SHCHO",
    }
)

Q4 = Decimal("0.0001")


def _is_uuid_str(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        UUID(value.strip())
    except ValueError:
        return False
    return True


def is_child_only_item_type(item_type: str) -> bool:
    """True if item_type (case-insensitive) is a child-only canonical or legacy alias."""
    if not isinstance(item_type, str) or not item_type.strip():
        return False
    return item_type.strip().upper() in _CHILD_ONLY_ITEM_TYPES


def parent_required_for_child_item_message(item_type: str) -> str:
    """Human-readable STRICT_REJECT message; source_field is always parent_item_id on API."""
    key = item_type.strip().upper() if isinstance(item_type, str) else ""
    if key in ("SHOS_CABINET", "SHCHO"):
        return "SHOS_CABINET cannot be created as root. Select or create parent product first."
    if key == "SERVICE_ITEM":
        return "SERVICE_ITEM cannot be created as root. Select or create parent product first."
    return "KZO_CELL cannot be created as root. Select or create parent product first."


def _dec_quantity(value: Any) -> Decimal | None:
    if value is None:
        return None
    try:
        d = Decimal(str(value))
    except Exception:  # noqa: BLE001
        return None
    return d


def validate_items_add_payload(body: Any) -> tuple[dict[str, Any] | None, str | None, str | None]:
    """Return (normalized, error_code, source_field)."""
    if not isinstance(body, dict):
        return None, "ITEM_CREATE_FAILED", None
    cid = body.get("calculation_id")
    vid = body.get("calculation_version_id")
    if not _is_uuid_str(cid) or not _is_uuid_str(vid):
        return None, "ITEM_CREATE_FAILED", None
    pid_raw = body.get("parent_item_id")
    parent_item_id: str | None
    if pid_raw is None or (isinstance(pid_raw, str) and not pid_raw.strip()):
        parent_item_id = None
    else:
        if not _is_uuid_str(pid_raw):
            return None, "ITEM_CREATE_FAILED", "parent_item_id"
        parent_item_id = str(pid_raw).strip()

    kind = body.get("item_kind")
    if not isinstance(kind, str) or not kind.strip():
        return None, "ITEM_INVALID_KIND", "item_kind"
    kind_s = kind.strip()
    if kind_s not in ALLOWED_ITEM_KINDS:
        return None, "ITEM_INVALID_KIND", "item_kind"

    itype = body.get("item_type")
    name = body.get("item_name")
    if not isinstance(itype, str) or not itype.strip():
        return None, "ITEM_CREATE_FAILED", "item_type"
    if not isinstance(name, str) or not name.strip():
        return None, "ITEM_CREATE_FAILED", "item_name"

    lq = _dec_quantity(body.get("local_quantity"))
    if lq is None or lq <= 0:
        return None, "ITEM_INVALID_QUANTITY", "local_quantity"

    payload_json = body.get("payload_json")
    if payload_json is None:
        pj: dict[str, Any] = {}
    elif isinstance(payload_json, dict):
        pj = payload_json
    else:
        return None, "ITEM_CREATE_FAILED", "payload_json"

    return (
        {
            "calculation_id": str(cid).strip(),
            "calculation_version_id": str(vid).strip(),
            "parent_item_id": parent_item_id,
            "item_kind": kind_s,
            "item_type": itype.strip(),
            "item_name": name.strip(),
            "local_quantity": lq,
            "payload_json": pj,
        },
        None,
        None,
    )


def _max_sibling_sort_order(client: Client, *, version_id: str, parent_item_id: str | None) -> int | None:
    q = client.table("module01_calculation_items").select("sort_order")
    q = q.eq("calculation_version_id", version_id)
    if parent_item_id is None:
        q = q.is_("parent_item_id", "null")
    else:
        q = q.eq("parent_item_id", parent_item_id)
    result = q.order("sort_order", desc=True).limit(1).execute()
    rows = getattr(result, "data", None)
    if not isinstance(rows, list) or not rows or not isinstance(rows[0], dict):
        return None
    so = rows[0].get("sort_order")
    if isinstance(so, bool):
        return None
    if isinstance(so, int):
        return so
    if isinstance(so, float):
        return int(so)
    return None


def _count_siblings(client: Client, *, version_id: str, parent_item_id: str | None) -> int:
    q = client.table("module01_calculation_items").select("id")
    q = q.eq("calculation_version_id", version_id)
    if parent_item_id is None:
        q = q.is_("parent_item_id", "null")
    else:
        q = q.eq("parent_item_id", parent_item_id)
    result = q.execute()
    rows = getattr(result, "data", None)
    if not isinstance(rows, list):
        return 0
    return len(rows)


def _sort_items_tree_preorder(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    children_map: dict[str | None, list[dict[str, Any]]] = {}
    for r in items:
        if not isinstance(r, dict):
            continue
        pid = r.get("parent_item_id")
        pk: str | None = str(pid) if isinstance(pid, str) else None
        children_map.setdefault(pk, []).append(r)
    for key in children_map:
        children_map[key].sort(key=lambda x: (int(x.get("sort_order") or 0), str(x.get("id") or "")))
    out: list[dict[str, Any]] = []

    def walk(parent_key: str | None) -> None:
        for node in children_map.get(parent_key, []):
            out.append(node)
            nid = node.get("id")
            if isinstance(nid, str):
                walk(nid)

    walk(None)
    return out


def _to_float(n: Any) -> float:
    if isinstance(n, Decimal):
        return float(n)
    if isinstance(n, (int, float)):
        return float(n)
    try:
        return float(str(n))
    except Exception:  # noqa: BLE001
        return 0.0


def _normalize_item_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": row.get("id"),
        "calculation_id": row.get("calculation_id"),
        "calculation_version_id": row.get("calculation_version_id"),
        "parent_item_id": row.get("parent_item_id"),
        "item_kind": row.get("item_kind"),
        "item_type": row.get("item_type"),
        "item_name": row.get("item_name"),
        "local_quantity": _to_float(row.get("local_quantity")),
        "total_quantity": _to_float(row.get("total_quantity")),
        "item_status": row.get("item_status"),
        "sort_order": row.get("sort_order"),
        "display_index": row.get("display_index"),
        "payload_json": row.get("payload_json") if isinstance(row.get("payload_json"), dict) else {},
        "result_summary_json": row.get("result_summary_json")
        if isinstance(row.get("result_summary_json"), dict)
        else {},
        "created_at": row.get("created_at"),
        "updated_at": row.get("updated_at"),
    }


def add_calculation_item_v1(
    *,
    client: Client,
    user_id: str,
    normalized: dict[str, Any],
) -> tuple[dict[str, Any] | None, str | None, str | None]:
    """
    Append one item to a DRAFT version. PostgREST: read max sort then insert (no DB txn).
    Returns (data, error_code, source_field).
    """
    calculation_id = normalized["calculation_id"]
    version_id = normalized["calculation_version_id"]
    parent_item_id = normalized["parent_item_id"]

    calc = _table_fetch_single(
        client,
        "module01_calculations",
        select="id,created_by_user_id",
        filters={"id": calculation_id},
    )
    if calc is None or str(calc.get("created_by_user_id") or "") != user_id:
        return None, "CALCULATION_NOT_FOUND", None

    ver = _table_fetch_single(
        client,
        "module01_calculation_versions",
        select="id,calculation_id,status",
        filters={"id": version_id},
    )
    if ver is None or str(ver.get("calculation_id") or "") != calculation_id:
        return None, "CALCULATION_VERSION_NOT_FOUND", None
    if str(ver.get("status") or "").upper() != "DRAFT":
        return None, "VERSION_NOT_DRAFT", None

    if parent_item_id is None and is_child_only_item_type(str(normalized.get("item_type") or "")):
        return None, "PARENT_REQUIRED_FOR_CHILD_ITEM", "parent_item_id"

    local_q: Decimal = normalized["local_quantity"]
    total_q: Decimal
    parent_row: dict[str, Any] | None = None

    if parent_item_id is None:
        total_q = local_q.quantize(Q4, rounding=ROUND_HALF_UP)
    else:
        parent_row = _table_fetch_single(
            client,
            "module01_calculation_items",
            select="id,calculation_id,calculation_version_id,parent_item_id,item_kind,total_quantity,display_index",
            filters={"id": parent_item_id},
        )
        if parent_row is None:
            return None, "ITEM_PARENT_NOT_FOUND", "parent_item_id"
        if str(parent_row.get("calculation_id") or "") != calculation_id:
            return None, "ITEM_PARENT_VERSION_MISMATCH", "parent_item_id"
        if str(parent_row.get("calculation_version_id") or "") != version_id:
            return None, "ITEM_PARENT_VERSION_MISMATCH", "parent_item_id"
        if parent_row.get("parent_item_id") is not None:
            return None, "ITEM_DEPTH_LIMIT_EXCEEDED", "parent_item_id"
        if str(parent_row.get("item_kind") or "") != "CONTAINER":
            return None, "ITEM_PARENT_NOT_CONTAINER", "parent_item_id"
        ptot = _dec_quantity(parent_row.get("total_quantity"))
        if ptot is None or ptot <= 0:
            return None, "ITEM_CREATE_FAILED", "parent_item_id"
        total_q = (ptot * local_q).quantize(Q4, rounding=ROUND_HALF_UP)

    max_sort = _max_sibling_sort_order(client, version_id=version_id, parent_item_id=parent_item_id)
    next_sort = (max_sort + 1) if isinstance(max_sort, int) else 100

    sibling_count_before = _count_siblings(client, version_id=version_id, parent_item_id=parent_item_id)
    ordinal = sibling_count_before + 1
    if parent_item_id is None:
        display_index = str(ordinal)
    else:
        if parent_row is None:
            return None, "ITEM_PARENT_NOT_FOUND", "parent_item_id"
        pdi = parent_row.get("display_index")
        if not isinstance(pdi, str) or not pdi.strip():
            return None, "ITEM_CREATE_FAILED", "parent_item_id"
        display_index = f"{pdi.strip()}.{ordinal}"

    insert_payload: dict[str, Any] = {
        "calculation_id": calculation_id,
        "calculation_version_id": version_id,
        "parent_item_id": parent_item_id,
        "item_kind": normalized["item_kind"],
        "item_type": normalized["item_type"],
        "item_name": normalized["item_name"],
        "local_quantity": float(local_q),
        "total_quantity": float(total_q),
        "item_status": "DRAFT",
        "payload_json": normalized["payload_json"],
        "result_summary_json": {},
        "sort_order": next_sort,
        "display_index": display_index,
    }

    try:
        ins = client.table("module01_calculation_items").insert(insert_payload).execute()
    except Exception as exc:  # noqa: BLE001
        if _is_unique_violation(exc):
            return None, "ITEM_SORT_CONFLICT", None
        return None, "ITEM_CREATE_FAILED", None

    rows = getattr(ins, "data", None)
    if not isinstance(rows, list) or not rows or not isinstance(rows[0], dict):
        return None, "ITEM_CREATE_FAILED", None
    created = rows[0]
    return {"item": _normalize_item_row(created)}, None, None


def list_calculation_items_v1(
    *,
    client: Client,
    user_id: str,
    calculation_id: str,
    version_id: str,
) -> tuple[list[dict[str, Any]] | None, str | None]:
    calc = _table_fetch_single(
        client,
        "module01_calculations",
        select="id,created_by_user_id",
        filters={"id": calculation_id},
    )
    if calc is None or str(calc.get("created_by_user_id") or "") != user_id:
        return None, "CALCULATION_NOT_FOUND"

    ver = _table_fetch_single(
        client,
        "module01_calculation_versions",
        select="id,calculation_id",
        filters={"id": version_id},
    )
    if ver is None or str(ver.get("calculation_id") or "") != calculation_id:
        return None, "CALCULATION_VERSION_NOT_FOUND"

    try:
        res = (
            client.table("module01_calculation_items")
            .select(
                "id,calculation_id,calculation_version_id,parent_item_id,"
                "item_kind,item_type,item_name,local_quantity,total_quantity,item_status,"
                "sort_order,display_index,payload_json,result_summary_json,created_at,updated_at"
            )
            .eq("calculation_version_id", version_id)
            .execute()
        )
    except Exception:  # noqa: BLE001
        return None, "ITEM_CREATE_FAILED"

    rows = getattr(res, "data", None)
    if not isinstance(rows, list):
        return None, "ITEM_CREATE_FAILED"
    dict_rows = [r for r in rows if isinstance(r, dict)]
    ordered = _sort_items_tree_preorder(dict_rows)
    return [_normalize_item_row(r) for r in ordered], None
