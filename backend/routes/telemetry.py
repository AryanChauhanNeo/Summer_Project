"""
routes/telemetry.py
====================
Endpoints for Member 1 (Rover Simulator) to publish telemetry, and for
Member 2 / the dashboard to read the latest telemetry.

    POST /telemetry   -> Member 1 pushes a new reading
    GET  /telemetry    -> Anyone reads the latest reading
"""

import logging

from fastapi import APIRouter, HTTPException, status

from models.telemetry import TelemetryData, TelemetryResponse
from services.storage import storage

log = logging.getLogger("mars_rover.telemetry")

router = APIRouter(prefix="/telemetry", tags=["Telemetry"])


@router.post(
    "",
    response_model=TelemetryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Publish the latest rover telemetry",
    description=(
        "Called by Member 1's Rover Simulator every simulation tick to "
        "push the rover's current state, position, and sensor readings. "
        "Overwrites whatever telemetry was stored previously."
    ),
)
def post_telemetry(payload: TelemetryData) -> TelemetryResponse:
    try:
        storage.save_telemetry(payload)
        log.info("Telemetry updated: state=%s position=%s",
                  payload.system_status.state, payload.navigation.current_position)
        return TelemetryResponse(message="Telemetry received successfully.", data=payload)
    except Exception as exc:  # defensive: pydantic already validated `payload`
        log.exception("Failed to store telemetry")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to store telemetry: {exc}",
        ) from exc


@router.get(
    "",
    response_model=TelemetryData,
    status_code=status.HTTP_200_OK,
    summary="Get the latest rover telemetry",
    description=(
        "Called by Member 2's Navigation Engine and the Streamlit dashboard "
        "to read the most recently published telemetry reading."
    ),
    responses={
        404: {"description": "No telemetry has been published yet."},
    },
)
def get_telemetry() -> TelemetryData:
    latest = storage.get_latest_telemetry()
    if latest is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No telemetry data available yet. Has Member 1's simulator posted any data?",
        )
    return latest
