"""
navigation_service.py
=====================

Converts backend navigation response into the format expected
by the Mission Control Dashboard.
"""

import math
from typing import Any, Dict

from services.api_client import fetch_navigation

DESTINATION = (250.0, 210.0)


def get_navigation_data(rover_x: float, rover_y: float) -> Dict[str, Any]:
    """
    Returns navigation data for the dashboard.
    Falls back to a simple route if the backend is unavailable.
    """

    try:
        data = fetch_navigation()

        route = [tuple(point) for point in data.get("route", [])]

        if route:
            rover = route[0]
            destination = route[-1]
        else:
            rover = (rover_x, rover_y)
            destination = DESTINATION
            route = [rover, destination]

        obstacles = [
            (x, y, 4)        # give every obstacle a radius for Plotly drawing
            for x, y in data.get("obstacles", [])
        ]

        return {
            "rover": rover,
            "destination": destination,
            "planned_route": route,
            "obstacles": obstacles,
            "craters": [],
            "rocks": [],
            "mountains": [],
            "distance_to_target": data.get("distance_remaining", 0.0),
            "heading": data.get("heading", "--"),
            "estimated_time_sec": data.get("estimated_time_sec", 0),
        }

    except Exception:
        # Backend unavailable -> simple fallback

        dist = math.sqrt(
            (rover_x - DESTINATION[0]) ** 2 +
            (rover_y - DESTINATION[1]) ** 2
        )

        return {
            "rover": (rover_x, rover_y),
            "destination": DESTINATION,
            "planned_route": [
                (rover_x, rover_y),
                DESTINATION,
            ],
            "obstacles": [],
            "craters": [],
            "rocks": [],
            "mountains": [],
            "distance_to_target": round(dist, 1),
            "heading": "--",
            "estimated_time_sec": 0,
        }