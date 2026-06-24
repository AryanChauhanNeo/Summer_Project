"""
components/header.py
====================
Renders the MARS ROVER MISSION CONTROL header bar.
"""

import streamlit as st


def render_header(mission_active: bool = True) -> None:
    status_color = "#00bfff" if mission_active else "#ef4444"
    status_text  = "ACTIVE"  if mission_active else "OFFLINE"

    st.markdown(
        f"""
        <div class="mission-header">
            <div>
                <div class="mission-title">MARS ROVER MISSION CONTROL</div>
                <div class="mission-subtitle">Perseverance Class &mdash; Expedition 2026</div>
            </div>
            <div style="text-align:right;">
                <div class="mission-status-label">Mission Status</div>
                <div class="mission-status-value" style="color:{status_color};">{status_text}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
