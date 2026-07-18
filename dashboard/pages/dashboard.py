"""
pages/dashboard.py
==================
Main dashboard page: assembles all panels in the 3-column layout
that mirrors mars-dashboard.tsx.
"""

import time
import random
import datetime
import streamlit as st

from components.header          import render_header
from components.telemetry_panel import render_telemetry_panel
from components.navigation_panel import render_navigation_panel
from components.mission_logs    import render_mission_logs
from components.alerts_panel    import render_alerts_panel
from services.telemetry_service import get_telemetry


# ── Log messages used for live simulation ─────────────────────────────────
_LOG_POOL = [
    "Rover repositioning in progress",
    "Terrain scan complete – sector clear",
    "Navigation recalibration",
    "System diagnostics running",
    "Obstacle avoidance protocol active",
    "Solar panel output stabilised",
    "Camera array calibrated",
    "Sample analysis complete",
    "Dust storm advisory updated",
    "Motor torque nominal",
]

_ALERT_POOL = [
    {"type": "warning",  "message": "High dust storm detected ahead",           "subsystem": "ENVIRONMENT"},
    {"type": "critical", "message": "Battery approaching critical threshold 20%","subsystem": "POWER"},
    {"type": "warning",  "message": "Motor performance degrading – check drives","subsystem": "MECHANICAL"},
    {"type": "warning",  "message": "Solar output reduced – cloud cover detected","subsystem": "POWER"},
]


def _init_session() -> None:
    if "extra_logs" not in st.session_state:
        st.session_state.extra_logs   = []
    if "extra_alerts" not in st.session_state:
        st.session_state.extra_alerts = []
    if "last_tick" not in st.session_state:
        st.session_state.last_tick    = time.time()
    if "tick_seed" not in st.session_state:
        st.session_state.tick_seed    = time.time()


def _simulate_tick() -> None:
    """Advance the simulation: maybe add a log entry or alert."""
    now = time.time()
    if now - st.session_state.last_tick < 3:
        return

    st.session_state.last_tick  = now
    st.session_state.tick_seed  = now  # new seed → new telemetry values

    rng = random.Random(now)

    if rng.random() > 0.55:
        ts  = datetime.datetime.now().strftime("%H:%M:%S")
        msg = rng.choice(_LOG_POOL)
        st.session_state.extra_logs.append(
            {"timestamp": ts, "message": msg, "level": "INFO"}
        )
        # Keep the live log buffer bounded
        if len(st.session_state.extra_logs) > 12:
            st.session_state.extra_logs = st.session_state.extra_logs[-12:]

    if rng.random() > 0.80:
        st.session_state.extra_alerts.append(rng.choice(_ALERT_POOL))
        if len(st.session_state.extra_alerts) > 4:
            st.session_state.extra_alerts = st.session_state.extra_alerts[-4:]


def render() -> None:
    _init_session()
    _simulate_tick()

    telemetry = get_telemetry()

    render_header(mission_active=True)

    # ── Top row: Telemetry (1/3) + Navigation (2/3) ───────────────────────
    left, right = st.columns([1, 2], gap="medium")

    with left:
        render_telemetry_panel(telemetry)

    with right:
        render_navigation_panel(telemetry)

    st.markdown("<div style='margin-top:1.25rem;'></div>", unsafe_allow_html=True)

    # ── Bottom row: Mission Logs + Alerts ─────────────────────────────────
    bl, br = st.columns(2, gap="medium")

    with bl:
        render_mission_logs(extra_entries=st.session_state.extra_logs)

    with br:
        render_alerts_panel(extra_alerts=st.session_state.extra_alerts)

    # ── Auto-refresh every 3 seconds ──────────────────────────────────────
    time.sleep(0.05)   # tiny yield so the rerun isn't instant
    st.rerun()
