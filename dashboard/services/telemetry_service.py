"""
telemetry_service.py
====================

Converts backend telemetry response into the format expected by the
Mission Control Dashboard.
"""

from math import sqrt
from typing import Any, Dict

from services.api_client import fetch_telemetry


def get_telemetry() -> Dict[str, Any]:
    """
    Fetch telemetry from backend and convert it to the format
    expected by the dashboard.
    """

    data = fetch_telemetry()

    navigation = data["navigation"]
    sensors = data["sensors"]
    system = data["system_status"]

    x = navigation["current_position"][0]
    y = navigation["current_position"][1]

    destination_x = navigation["destination"][0]
    destination_y = navigation["destination"][1]

    distance = sqrt(
        (destination_x - x) ** 2 +
        (destination_y - y) ** 2
    )

    return {
    "timestamp": data["timestamp"],

    "x": x,
    "y": y,

    "destination_x": destination_x,
    "destination_y": destination_y,

    "battery": sensors["battery_level_percent"],

    "temperature": sensors["temperature_celsius"],

    "speed": system["speed_kmh"],

    "is_moving": system["state"].upper() == "MOVING",

    "obstacle_detected": sensors["obstacle_detected"],

    "distance_to_target": round(distance, 2),

    "state": system["state"],

    "raw": data,
    }


def battery_color(pct: float) -> str:
    if pct > 60:
        return "#4ade80"
    if pct > 30:
        return "#facc15"
    return "#ef4444"


def temp_color(temp: float) -> str:
    if temp < 45:
        return "#60a5fa"
    if temp < 55:
        return "#facc15"
    return "#ef4444"