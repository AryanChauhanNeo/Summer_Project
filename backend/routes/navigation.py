"""
routes/navigation.py
=====================
Endpoints for Member 2 (AI Navigation Engine) to publish the planned
route, and for the dashboard to read the latest navigation data.

    POST /navigation   -> Member 2 pushes a new route/plan
    GET  /navigation    -> Anyone reads the latest route/plan
"""

import logging

from fastapi import APIRouter, HTTPException, status

from models.navigation import NavigationData, NavigationResponse
from services.storage import storage

log = logging.getLogger("mars_rover.navigation")

router = APIRouter(prefix="/navigation", tags=["Navigation"])


@router.post(
    "",
    response_model=NavigationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Publish the latest navigation plan",
    description=(
        "Called by Member 2's AI Navigation Engine after running A* "
        "pathfinding and obstacle detection. Overwrites whatever "
        "navigation data was stored previously."
    ),
)
def post_navigation(payload: NavigationData) -> NavigationResponse:
    try:
        storage.save_navigation(payload)
        log.info("Navigation updated: heading=%s eta_sec=%s",
                  payload.heading, payload.estimated_time_sec)
        return NavigationResponse(message="Navigation data received successfully.", data=payload)
    except Exception as exc:  # defensive: pydantic already validated `payload`
        log.exception("Failed to store navigation data")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to store navigation data: {exc}",
        ) from exc


@router.get(
    "",
    response_model=NavigationData,
    status_code=status.HTTP_200_OK,
    summary="Get the latest navigation plan",
    description=(
        "Called by the Streamlit dashboard to read the most recently "
        "published route, obstacles, heading, and ETA."
    ),
    responses={
        404: {"description": "No navigation data has been published yet."},
    },
)
def get_navigation() -> NavigationData:
    latest = storage.get_latest_navigation()
    if latest is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No navigation data available yet. Has Member 2's engine posted a route?",
        )
    return latest
