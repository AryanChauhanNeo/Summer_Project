"""
api_client.py
=============
HTTP client for connecting to the FastAPI backend.

Backend Endpoints:
    GET /telemetry
    GET /navigation
    GET /terrain

Set:
    BACKEND_API_URL=http://localhost:8000

or

    BACKEND_API_URL=https://your-render-backend.onrender.com
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict

import requests

log = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent / "data"

BACKEND_API_URL = os.getenv("BACKEND_API_URL")

REQUEST_TIMEOUT = 5


# ---------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------

def _load_json(filename: str) -> Any:
    """Load fallback JSON."""
    path = DATA_DIR / filename

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _get(endpoint: str, fallback_file: str):
    """Fetch data from backend or fallback JSON."""

    if not BACKEND_API_URL:
        return _load_json(fallback_file)

    try:
        response = requests.get(
            f"{BACKEND_API_URL}{endpoint}",
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        return response.json()

    except Exception as exc:
        log.warning(
            "Backend unavailable (%s). Using %s",
            exc,
            fallback_file,
        )

        return _load_json(fallback_file)


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------

def fetch_telemetry() -> Dict[str, Any]:
    return _get("/telemetry", "telemetry.json")


def fetch_navigation() -> Dict[str, Any]:
    return _get("/navigation", "telemetry.json")


def fetch_terrain() -> Dict[str, Any]:
    return _get("/terrain", "terrain.json")


def fetch_alerts():
    return _load_json("alerts.json")


def fetch_logs():
    return _load_json("logs.json")