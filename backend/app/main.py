"""
app/main.py
===========
Application entrypoint for the Smart Mars Rover Monitoring &
Navigation Simulator backend.

Run locally with:
    uvicorn app.main:app --reload

The app is intentionally deployment-agnostic: HOST, PORT, and
CORS_ORIGINS all come from environment variables (see app/config.py
and .env.example), so the exact same code runs locally today and on
Render / Railway later without any changes.
"""

import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from routes import navigation, telemetry
from utils.logging_config import configure_logging

configure_logging()
log = logging.getLogger("mars_rover.main")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Shared backend for the Smart Mars Rover Monitoring & Navigation "
        "Simulator team project.\n\n"
        "- **Member 1** (Rover Simulator) publishes telemetry via `POST /telemetry`.\n"
        "- **Member 2** (AI Navigation) publishes route plans via `POST /navigation`.\n"
        "- **Member 3** (Dashboard) reads both via `GET /telemetry` and `GET /navigation`.\n\n"
        "Interactive documentation is available below (Swagger UI) and at `/redoc` (ReDoc)."
    ),
    contact={"name": "Smart Mars Rover Simulator Team"},
)

# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------
# The three team members work from different cities/machines and the
# Streamlit dashboard runs on yet another origin, so CORS must be open
# enough for development. CORS_ORIGINS is environment-driven — restrict
# it via the CORS_ORIGINS_RAW env var before going to production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(telemetry.router)
app.include_router(navigation.router)


# ---------------------------------------------------------------------------
# Root & health-check endpoints
# ---------------------------------------------------------------------------
@app.get("/", tags=["Meta"], summary="API root / info")
def read_root() -> dict:
    """Basic info endpoint — useful for a quick sanity check that the API is up."""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "docs": "/docs",
        "endpoints": {
            "telemetry": {"POST": "/telemetry", "GET": "/telemetry"},
            "navigation": {"POST": "/navigation", "GET": "/navigation"},
        },
    }


@app.get("/health", tags=["Meta"], summary="Health check")
def health_check() -> dict:
    """Used for uptime checks / Render & Railway health probes."""
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Global exception handlers
# ---------------------------------------------------------------------------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Returns a clean, consistent 422 response when incoming JSON doesn't
    match the expected schema (e.g. Member 1 sends a malformed telemetry
    payload), instead of FastAPI's default verbose trace.
    """
    log.warning("Validation error on %s %s: %s", request.method, request.url.path, exc.errors())
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": "Request validation failed. Check the payload against the expected schema.",
            "errors": exc.errors(),
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Last-resort safety net so an unexpected bug never leaks a raw traceback to clients."""
    log.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "An unexpected server error occurred."},
    )


@app.on_event("startup")
async def on_startup() -> None:
    log.info("%s v%s starting up in '%s' mode", settings.APP_NAME, settings.APP_VERSION, settings.ENVIRONMENT)
