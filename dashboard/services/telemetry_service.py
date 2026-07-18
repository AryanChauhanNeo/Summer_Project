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

    # ------------------------------------------------------------
    # Backend has no telemetry yet
    # ------------------------------------------------------------
    if (
        not isinstance(data, dict)
        or "navigation" not in data
        or "sensors" not in data
        or "system_status" not in data
    ):
        return {
            "timestamp": "No Data",
            "x": 0,
            "y": 0,
            "destination_x": 0,
            "destination_y": 0,
            "battery": 0,
            "temperature": 0,
            "speed": 0,
            "is_moving": False,
            "obstacle_detected": False,
            "distance_to_target": 0,
            "state": "WAITING FOR MEMBER 1",
            "raw": data,
        }

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
    """Return battery color."""

    if pct >= 75:
        return "#22c55e"

    if pct >= 40:
        return "#facc15"

    return "#ef4444"


def temp_color(temp: float) -> str:
    """Return temperature color."""

    if temp < 45:
        return "#60a5fa"

    if temp < 60:
        return "#facc15"

    return "#ef4444"