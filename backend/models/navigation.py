"""
models/navigation.py
=====================
Pydantic schema for navigation data produced by Member 2's
AI Navigation Engine (A* route, detected obstacles, ETA, heading).

This is the single source of truth for the navigation JSON shape.
"""

from typing import List

from pydantic import BaseModel, Field


class NavigationData(BaseModel):
    """
    Full navigation payload sent by Member 2 via `POST /navigation`
    and served back to the dashboard via `GET /navigation`.
    """

    route: List[List[float]] = Field(
        ...,
        description="Ordered list of [x, y] waypoints from current position to destination.",
        examples=[[[4, 7], [5, 7], [6, 8], [7, 8], [8, 9], [9, 9]]],
    )
    obstacles: List[List[float]] = Field(
        default_factory=list,
        description="List of [x, y] grid cells currently flagged as obstacles.",
        examples=[[[5, 6], [7, 7], [8, 8]]],
    )
    distance_remaining: float = Field(
        ...,
        ge=0,
        description="Remaining distance to destination, in the simulation's distance unit.",
        examples=[5.4],
    )
    heading: str = Field(
        ...,
        description="Compass heading of travel, e.g. N, NE, E, SE, S, SW, W, NW.",
        examples=["NE"],
    )
    estimated_time_sec: int = Field(
        ...,
        ge=0,
        description="Estimated time remaining to reach the destination, in seconds.",
        examples=[180],
    )

    class Config:
        json_schema_extra = {
            "example": {
                "route": [[4, 7], [5, 7], [6, 8], [7, 8], [8, 9], [9, 9]],
                "obstacles": [[5, 6], [7, 7], [8, 8]],
                "distance_remaining": 5.4,
                "heading": "NE",
                "estimated_time_sec": 180,
            }
        }


class NavigationResponse(BaseModel):
    """Standard response envelope returned after a successful POST."""

    message: str
    data: NavigationData
