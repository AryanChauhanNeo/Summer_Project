"""
services/storage.py
====================
In-memory storage layer for the latest telemetry and navigation
readings.

Why a class instead of two bare global variables?
---------------------------------------------------
Wrapping the storage behind a small interface (`get_latest_telemetry`,
`save_telemetry`, `get_latest_navigation`, `save_navigation`) means the
routes never talk to "a dictionary in memory" directly. Later, when the
team wants to move to MongoDB or PostgreSQL, only THIS file needs to
change — a new class implementing the same methods (e.g. reading /
writing from Mongo instead of a Python dict) can be swapped in without
touching routes/, models/, or app/main.py at all.

Thread-safety
-------------
FastAPI can serve multiple requests concurrently (e.g. under Uvicorn's
async event loop, or multiple workers). A simple `threading.Lock` is
used around read/write access so that Member 1 posting telemetry and
the dashboard reading it at the same instant can never corrupt state.
"""

import threading
from typing import Optional

from models.navigation import NavigationData
from models.telemetry import TelemetryData


class InMemoryStorage:
    """
    Keeps only the LATEST telemetry and navigation reading in memory.

    This intentionally does not keep history — the project spec only
    requires "latest telemetry" / "latest navigation". If history is
    needed later, extend this class with a list-based log or swap it
    for a database-backed implementation with the same method names.
    """

    def __init__(self) -> None:
        self._telemetry: Optional[TelemetryData] = None
        self._navigation: Optional[NavigationData] = None
        self._lock = threading.Lock()

    # ── Telemetry ────────────────────────────────────────────────────
    def save_telemetry(self, data: TelemetryData) -> None:
        with self._lock:
            self._telemetry = data

    def get_latest_telemetry(self) -> Optional[TelemetryData]:
        with self._lock:
            return self._telemetry

    # ── Navigation ───────────────────────────────────────────────────
    def save_navigation(self, data: NavigationData) -> None:
        with self._lock:
            self._navigation = data

    def get_latest_navigation(self) -> Optional[NavigationData]:
        with self._lock:
            return self._navigation


# Single shared instance used across the whole app (simple, explicit
# dependency — see routes/telemetry.py and routes/navigation.py).
storage = InMemoryStorage()
