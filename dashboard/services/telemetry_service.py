"""
telemetry_service.py
====================
Provides live-simulated rover telemetry for the dashboard.

Wraps api_client.fetch_telemetry() and applies a lightweight
random-walk simulation on top of the base values so the UI
appears live even without a backend.  When ROVER_API_URL is set,
the simulation is bypassed and real data is used directly.
"""

import os
import math
import random
import time
from typing import Dict, Any

from services.api_client import fetch_telemetry

_USE_LIVE_API = bool(os.getenv("ROVER_API_URL"))


def _clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def get_telemetry(seed: float | None = None) -> Dict[str, Any]:
    """
    Return a telemetry dict.

    In standalone mode a reproducible random-walk is applied around
    the base JSON values using *seed* (defaults to current time so
    each Streamlit rerun produces slightly different numbers).
    """
    base = fetch_telemetry()

    if _USE_LIVE_API:
        return base

    rng = random.Random(seed if seed is not None else time.time())

    x = _clamp(base["x"] + rng.uniform(-5, 5), 50, 300)
    y = _clamp(base["y"] + rng.uniform(-5, 5), 100, 380)
    battery = _clamp(base["battery"] - rng.uniform(0, 0.4), 20, 100)
    temperature = _clamp(base["temperature"] + rng.uniform(-1, 1), 20, 65)
    is_moving = rng.random() > 0.45
    heading = (base.get("heading", 245) + rng.randint(-3, 3)) % 360
    speed = round(rng.uniform(0.05, 0.22), 3) if is_moving else 0.0
    signal_strength = _clamp(base.get("signal_strength", 87) + rng.uniform(-2, 2), 0, 100)

    # Distance to fixed destination (250, 250)
    dist = math.sqrt((x - 250) ** 2 + (y - 250) ** 2)

    return {
        **base,
        "x": round(x, 1),
        "y": round(y, 1),
        "battery": round(battery, 1),
        "temperature": round(temperature, 1),
        "is_moving": is_moving,
        "heading": heading,
        "speed": speed,
        "signal_strength": round(signal_strength, 1),
        "distance_to_target": round(dist, 1),
    }


def battery_color(pct: float) -> str:
    if pct > 60:
        return "#4ade80"   # green-400
    if pct > 30:
        return "#facc15"   # yellow-400
    return "#ef4444"        # red-500


def temp_color(temp: float) -> str:
    if temp < 45:
        return "#60a5fa"   # blue-400
    if temp < 55:
        return "#facc15"   # yellow-400
    return "#ef4444"        # red-500
