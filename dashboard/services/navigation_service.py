"""
navigation_service.py
=====================
Provides terrain, route, and obstacle data for the Navigation panel.

All coordinates are in the rover's local metric frame (metres).
The destination is fixed; the planned route is a multi-waypoint path
that avoids known obstacles.
"""

import os
import random
from typing import List, Dict, Any, Tuple

from services.api_client import fetch_navigation

_USE_LIVE_API = bool(os.getenv("NAV_API_URL"))

# Fixed destination in metric coordinates
DESTINATION: Tuple[float, float] = (250.0, 210.0)

# Static obstacle list (x, y, radius_m)
OBSTACLES: List[Tuple[float, float, float]] = [
    (160, 270, 12),
    (200, 230, 8),
    (100, 300, 10),
    (230, 310, 15),
    (270, 160, 9),
]

# Pre-computed waypoint route (avoids obstacles)
PLANNED_ROUTE: List[Tuple[float, float]] = [
    (125, 240),
    (145, 260),
    (170, 255),
    (190, 245),
    (210, 230),
    (225, 220),
    (250, 210),
]

# Crater features (cx, cy, radius)
CRATERS: List[Tuple[float, float, float]] = [
    (80,  300, 22),
    (300, 340, 16),
    (175, 170, 12),
]

# Rock clusters (cx, cy)
ROCKS: List[Tuple[float, float]] = [
    (280, 280), (285, 275), (275, 285),
    (90,  200), (95,  207),
]

# Mountain ridge points for polygon fill
MOUNTAIN_POLYGONS: List[List[Tuple[float, float]]] = [
    [(50, 165), (100, 130), (150, 165)],
    [(220, 185), (270, 155), (315, 185)],
]


def get_navigation_data(rover_x: float, rover_y: float) -> Dict[str, Any]:
    """Return complete navigation payload for the terrain panel."""
    if _USE_LIVE_API:
        raw = fetch_navigation()
        return raw

    import math
    dist = math.sqrt((rover_x - DESTINATION[0]) ** 2 + (rover_y - DESTINATION[1]) ** 2)

    return {
        "rover": (rover_x, rover_y),
        "destination": DESTINATION,
        "planned_route": PLANNED_ROUTE,
        "obstacles": OBSTACLES,
        "craters": CRATERS,
        "rocks": ROCKS,
        "mountains": MOUNTAIN_POLYGONS,
        "distance_to_target": round(dist, 1),
    }
