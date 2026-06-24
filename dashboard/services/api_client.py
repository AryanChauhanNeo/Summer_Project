"""
api_client.py
=============
HTTP client for connecting to external FastAPI backends.

Future integration points:
  Member 1 – Rover Simulator  →  FastAPI  →  /api/telemetry
  Member 2 – Navigation Engine →  FastAPI  →  /api/navigation

When backends are ready, set environment variables:
  ROVER_API_URL     e.g. http://localhost:8000
  NAV_API_URL       e.g. http://localhost:8001

If the URLs are not set, the client falls back to local JSON files
so the dashboard continues to work in standalone / demo mode.
"""

import os
import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

import requests

log = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent / "data"
ROVER_API_URL: Optional[str] = os.getenv("ROVER_API_URL")
NAV_API_URL: Optional[str] = os.getenv("NAV_API_URL")
REQUEST_TIMEOUT = 5  # seconds


# ---------------------------------------------------------------------------
# Low-level helpers
# ---------------------------------------------------------------------------

def _get(url: str, fallback_file: str) -> Dict[str, Any]:
    """GET *url* and return parsed JSON, or load *fallback_file* on failure."""
    try:
        resp = requests.get(url, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:
        log.warning("API unreachable (%s) – using local fallback: %s", url, exc)
        return _load_json(fallback_file)


def _load_json(filename: str) -> Any:
    path = DATA_DIR / filename
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def fetch_telemetry() -> Dict[str, Any]:
    """Return latest rover telemetry from the Rover Simulator API or local JSON."""
    if ROVER_API_URL:
        return _get(f"{ROVER_API_URL}/api/telemetry", "telemetry.json")
    return _load_json("telemetry.json")


def fetch_navigation() -> Dict[str, Any]:
    """Return navigation / route data from the Navigation Engine API or local JSON."""
    if NAV_API_URL:
        return _get(f"{NAV_API_URL}/api/navigation", "telemetry.json")
    return _load_json("telemetry.json")


def fetch_alerts() -> list:
    """Return active alerts from the Rover API or local JSON."""
    if ROVER_API_URL:
        data = _get(f"{ROVER_API_URL}/api/alerts", "alerts.json")
        return data if isinstance(data, list) else data.get("alerts", [])
    return _load_json("alerts.json")


def fetch_logs() -> list:
    """Return mission log entries from the Rover API or local JSON."""
    if ROVER_API_URL:
        data = _get(f"{ROVER_API_URL}/api/logs", "logs.json")
        return data if isinstance(data, list) else data.get("logs", [])
    return _load_json("logs.json")
