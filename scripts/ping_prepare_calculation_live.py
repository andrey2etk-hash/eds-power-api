#!/usr/bin/env python3
"""
Local smoke probe: POST live Render prepare_calculation (KZO canonical vector).

Usage (from repo root):
  python scripts/ping_prepare_calculation_live.py

Optional:
  python scripts/ping_prepare_calculation_live.py --url https://other-host/api/calc/prepare_calculation

No third-party deps (stdlib only).
"""
from __future__ import annotations

import argparse
import json
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_URL = "https://eds-power-api.onrender.com/api/calc/prepare_calculation"

CANONICAL_BODY = {
    "meta": {"request_id": "local-ping-prepare_calculation"},
    "module": "CALC_CONFIGURATOR",
    "action": "prepare_calculation",
    "payload": {
        "object_number": "7445-B",
        "product_type": "KZO",
        "logic_version": "KZO_MVP_V1",
        "voltage_class": "VC_10",
        "busbar_current": 1250,
        "configuration_type": "CFG_SINGLE_BUS_SECTION",
        "quantity_total": 22,
        "cell_distribution": {
            "CELL_INCOMER": 2,
            "CELL_OUTGOING": 16,
            "CELL_PT": 2,
            "CELL_BUS_SECTION": 2,
        },
        "status": "DRAFT",
    },
}


def main() -> int:
    parser = argparse.ArgumentParser(description="POST prepare_calculation to live API (stdlib only).")
    parser.add_argument(
        "--url",
        default=DEFAULT_URL,
        help=f"Full endpoint URL (default: {DEFAULT_URL})",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Print pretty JSON response (can be large).",
    )
    args = parser.parse_args()

    raw = json.dumps(CANONICAL_BODY).encode("utf-8")
    req = Request(
        args.url,
        data=raw,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(req, timeout=120) as resp:
            http_code = resp.status
            text = resp.read().decode("utf-8")
    except HTTPError as e:
        sys.stderr.write(f"HTTP error: {e.code} {e.reason}\n")
        if e.fp:
            sys.stderr.write(e.fp.read().decode("utf-8", errors="replace")[:4000])
        return 2
    except URLError as e:
        sys.stderr.write(f"Request failed: {e.reason}\n")
        return 2

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        sys.stdout.write(text[:2000])
        sys.stderr.write("\nResponse was not JSON.\n")
        return 2

    if args.pretty:
        print(json.dumps(parsed, indent=2, ensure_ascii=False))
    else:
        status = parsed.get("status")
        data = parsed.get("data") or {}
        print(f"HTTP {http_code} | envelope status: {status!r}")
        if isinstance(data, dict):
            checks = []
            keys = ("structural_composition_summary", "physical_summary", "physical_topology_summary",
                    "engineering_class_summary", "engineering_burden_summary")
            for k in keys:
                checks.append((k, k in data and data[k] is not None))
            for name, ok in checks:
                print(f"  data.{name}: {'ok' if ok else 'MISSING'}")
            ebs = data.get("engineering_burden_summary")
            if isinstance(ebs, dict):
                iscope = ebs.get("interpretation_scope")
                print(f"  engineering_burden_summary.interpretation_scope: {iscope!r}")

    ok = parsed.get("status") == "success" and isinstance(parsed.get("data"), dict)
    if ok and parsed["data"].get("engineering_burden_summary"):
        print("Smoke: PASS (success + engineering_burden_summary present)")
        return 0
    sys.stderr.write("Smoke: FAIL (missing success/data or engineering_burden_summary).\n")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
