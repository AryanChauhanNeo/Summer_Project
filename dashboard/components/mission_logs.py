"""
components/mission_logs.py
==========================
Bottom-left panel: scrollable mission log entries + summary stats.
Mirrors mission-logs-panel.tsx.
"""

import datetime
import streamlit as st
from services.api_client import fetch_logs


_LEVEL_COLOR = {
    "INFO": "#00bfff",
    "WARN": "#facc15",
    "ERROR": "#ef4444",
    "DEBUG": "#999",
}


def render_mission_logs(extra_entries: list | None = None) -> None:
    logs = fetch_logs()

    # Optionally merge live-generated entries (from session state)
    if extra_entries:
        logs = logs + extra_entries

    last_update = datetime.datetime.now().strftime("%H:%M:%S")

    st.markdown(
        '<div class="panel-title">📋 Mission Logs</div>',
        unsafe_allow_html=True,
    )

    # Scrollable log list
    log_html = '<div class="log-scroll">'
    for entry in logs:
        ts   = entry.get("timestamp", "")
        msg  = entry.get("message", "")
        lvl  = entry.get("level", "INFO")
        col  = _LEVEL_COLOR.get(lvl, "#999")
        log_html += (
            f'<div class="log-entry">'
            f'<span style="color:{col};font-weight:700;">[{ts}]</span> {msg}'
            f'</div>'
        )
    log_html += "</div>"
    st.markdown(log_html, unsafe_allow_html=True)

    # Separator + stats
    st.markdown('<hr class="section-sep"/>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f"""<div class="stat-block">
                <div class="stat-label">Total Events</div>
                <div class="stat-value" style="color:#ffaa00;">{len(logs)}</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""<div class="stat-block">
                <div class="stat-label">Last Update</div>
                <div class="stat-value" style="color:#00bfff;font-size:0.95rem;">{last_update}</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """<div class="stat-block">
                <div class="stat-label">Status</div>
                <div class="stat-value" style="color:#4ade80;">Running</div>
            </div>""",
            unsafe_allow_html=True,
        )
