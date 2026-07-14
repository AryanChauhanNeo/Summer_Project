"""
models/telemetry.py
====================
Pydantic schema for telemetry data produced by Member 1's
Rover Simulator (rover state, battery, temperature, position).

This is the single source of truth for the telemetry JSON shape.
FastAPI uses it to validate incoming POST bodies and to document
the API automatically in Swagger (/docs).
"""

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, field_validator


class SystemStatus(BaseModel):
    """Current operational state of the rover."""

    state: str = Field(
        ...,
        description="Current rover state, e.g. IDLE, MOVING, CHARGING, STOPPED, ERROR.",
        examples=["MOVING"],
    )
    speed_kmh: float = Field(
        ...,
        ge=0,
        description="Current speed of the rover in kilometres per hour.",
        examples=[2.0],
    )


class NavigationSnapshot(BaseModel):
    """Lightweight position snapshot embedded inside telemetry."""

    current_position: List[float] = Field(
        ...,
        min_length=2,
        max_length=2,
        description="Current [x, y] grid position of the rover.",
        examples=[[4, 7]],
    )
    destination: List[float] = Field(
        ...,
        min_length=2,
        max_length=2,
        description="Target [x, y] grid position the rover is heading to.",
        examples=[[9, 9]],
    )


class Sensors(BaseModel):
    """Raw sensor readings from the rover."""

    battery_level_percent: float = Field(
        ...,
        ge=0,
        le=100,
        description="Remaining battery charge, as a percentage.",
        examples=[85.5],
    )
    temperature_celsius: float = Field(
        ...,
        description="Ambient/onboard temperature in Celsius.",
        examples=[-62.3],
    )
    obstacle_detected: bool = Field(
        ...,
        description="Whether the rover's sensors currently detect an obstacle.",
        examples=[False],
    )


class TelemetryData(BaseModel):
    """
    Full telemetry payload sent by Member 1 via `POST /telemetry`
    and served back to Member 2 / the dashboard via `GET /telemetry`.
    """

    timestamp: datetime = Field(
        ...,
        description="ISO-8601 UTC timestamp of the reading.",
        examples=["2026-06-01T11:39:38Z"],
    )
    system_status: SystemStatus
    navigation: NavigationSnapshot
    sensors: Sensors

    @field_validator("timestamp")
    @classmethod
    def _ensure_timezone_aware(cls, value: datetime) -> datetime:
        """Guarantee every stored timestamp carries timezone info."""
        if value.tzinfo is None:
            raise ValueError("timestamp must include timezone info, e.g. suffix 'Z' or '+00:00'.")
        return value

    class Config:
        json_schema_extra = {
            "example": {
                "timestamp": "2026-06-01T11:39:38Z",
                "system_status": {"state": "MOVING", "speed_kmh": 2.0},
                "navigation": {"current_position": [4, 7], "destination": [9, 9]},
                "sensors": {
                    "battery_level_percent": 85.5,
                    "temperature_celsius": -62.3,
                    "obstacle_detected": False,
                },
            }
        }


class TelemetryResponse(BaseModel):
    """Standard response envelope returned after a successful POST."""

    message: str
    data: TelemetryData
