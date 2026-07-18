import logging

from fastapi import APIRouter, HTTPException, status

from models.terrain import TerrainData, TerrainResponse
from services.storage import storage

log = logging.getLogger("mars_rover.terrain")

router = APIRouter(prefix="/terrain", tags=["Terrain"])


@router.post(
    "",
    response_model=TerrainResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Publish terrain map",
)
def post_terrain(payload: TerrainData):

    try:
        storage.save_terrain(payload)

        log.info("Terrain updated")

        return TerrainResponse(
            message="Terrain received successfully.",
            data=payload,
        )

    except Exception as exc:
        log.exception("Failed to store terrain")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


@router.get(
    "",
    response_model=TerrainData,
    summary="Get latest terrain map",
)
def get_terrain():

    latest = storage.get_latest_terrain()

    if latest is None:
        raise HTTPException(
            status_code=404,
            detail="No terrain data available yet.",
        )

    return latest