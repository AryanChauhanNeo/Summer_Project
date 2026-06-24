"""
components/telemetry_panel.py
=============================
Left-column telemetry cards: coordinates, battery, temperature,
system status – mirrors telemetry-panel.tsx faithfully.
"""

import streamlit as st
from services.telemetry_service import battery_color, temp_color


def _tel_card(label: str, value: str, unit: str = "", color: str = "#f2f2f2",
              icon: str = "") -> None:
    icon_html = f'<span style="float:right;font-size:0.9rem;color:{color};">{icon}</span>' if icon else ""
    st.markdown(
        f"""
        <div class="tel-card">
            <div class="tel-label">{label}{icon_html}</div>
            <div class="tel-value" style="color:{color};">{value}</div>
            {f'<div class="tel-unit">{unit}</div>' if unit else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )


def _battery_card(battery: float) -> None:
    color = battery_color(battery)
    fill_pct = max(0, min(100, battery))
    st.markdown(
        f"""
        <div class="tel-card">
            <div class="tel-label">
                Battery
                <span style="float:right;font-size:0.9rem;color:{color};">⚡</span>
            </div>
            <div class="tel-value" style="color:{color};">{battery:.1f}%</div>
            <div class="battery-track">
                <div class="battery-fill"
                     style="width:{fill_pct}%;background:{color};"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _status_card(is_moving: bool, signal: float) -> None:
    dot_class  = "dot-active" if is_moving else "dot-idle"
    motion_lbl = "Moving"     if is_moving else "Stationary"
    sig_color  = "#4ade80" if signal > 70 else ("#facc15" if signal > 40 else "#ef4444")
    st.markdown(
        f"""
        <div class="tel-card">
            <div class="tel-label">System Status</div>
            <div style="margin-top:0.4rem;">
                <div style="display:flex;align-items:center;margin-bottom:0.35rem;">
                    <span class="status-dot {dot_class}"></span>
                    <span style="font-size:0.82rem;">{motion_lbl}</span>
                </div>
                <div style="display:flex;align-items:center;margin-bottom:0.35rem;">
                    <span class="status-dot dot-active"></span>
                    <span style="font-size:0.82rem;">Navigation Active</span>
                </div>
                <div style="display:flex;align-items:center;">
                    <span class="status-dot" style="background:{sig_color};box-shadow:0 0 6px {sig_color};"></span>
                    <span style="font-size:0.82rem;">Signal&nbsp;
                        <span style="color:{sig_color};font-family:monospace;">{signal:.0f}%</span>
                    </span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_telemetry_panel(telemetry: dict) -> None:
    st.markdown(
        '<div class="panel-title">📡 Telemetry Data</div>',
        unsafe_allow_html=True,
    )

    _tel_card("X Coordinate", f"{telemetry['x']:.1f}", "meters", "#f2f2f2", "📍")
    _tel_card("Y Coordinate", f"{telemetry['y']:.1f}", "meters", "#f2f2f2", "📍")
    _battery_card(telemetry["battery"])
    _tel_card(
        "Temperature",
        f"{telemetry['temperature']:.1f}°C",
        "Rover chassis",
        temp_color(telemetry["temperature"]),
        "🌡",
    )
    _tel_card(
        "Speed",
        f"{telemetry.get('speed', 0.0):.3f}",
        "m/s",
        "#00bfff" if telemetry.get("is_moving") else "#999",
        "🔄",
    )
    _status_card(telemetry.get("is_moving", False), telemetry.get("signal_strength", 87))
