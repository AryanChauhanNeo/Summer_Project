"""
api_client.py
=============
HTTP client for connecting to the FastAPI backend.

Backend:
https://mars-rover-backend.onrender.com
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict

import requests

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

DATA_DIR = Path(__file__).parent.parent / "data"

# LIVE RENDER BACKEND
BACKEND_API_URL = "https://mars-rover-backend.onrender.com"

REQUEST_TIMEOUT = 10

# ---------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------


def _load_json(filename: str) -> Any:
    """
    Load local fallback JSON if backend is unavailable.
    """
    path = DATA_DIR / filename

    if not path.exists():
        return {}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _get(endpoint: str, fallback_file: str):
    """
    Fetch data from Render backend.
    Falls back to local JSON only if backend is unreachable.
    """

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
    return _get("/navigation", "navigation.json")


def fetch_terrain() -> Dict[str, Any]:
    return _get("/terrain", "terrain.json")


def fetch_alerts():
    return _load_json("alerts.json")


def fetch_logs():
    return _load_json("logs.json")