"""
components/navigation_panel.py
==============================
Centre panel: Mars terrain visualisation (Plotly) + navigation stats.
Mirrors navigation-panel.tsx: grid, rover, destination, route, obstacles.
"""

import math
import numpy as np
import plotly.graph_objects as go
import streamlit as st

from services.navigation_service import get_navigation_data

# ── Design tokens ──────────────────────────────────────────────────────────
BG          = "#10131a"
GRID_COLOR  = "rgba(0,191,255,0.08)"
PRIMARY     = "#00bfff"
SECONDARY   = "#7c22e0"
ACCENT      = "#ffaa00"
DANGER      = "#ef4444"
MUTED       = "#3a4060"
ROVER_COLOR = "#00bfff"
DEST_COLOR  = ACCENT
ROUTE_COLOR = "rgba(0,191,255,0.55)"

# Axis bounds
X_MIN, X_MAX = 30, 340
Y_MIN, Y_MAX = 80, 400


def _terrain_figure(nav: dict) -> go.Figure:
    rover_x, rover_y   = nav["rover"]
    dest_x,  dest_y    = nav["destination"]
    route               = nav["planned_route"]
    obstacles           = nav["obstacles"]
    craters             = nav["craters"]
    rocks               = nav["rocks"]
    mountains           = nav["mountains"]

    fig = go.Figure()

    # ── Terrain dust / gradient via filled contour background ──────────────
    xg = np.linspace(X_MIN, X_MAX, 80)
    yg = np.linspace(Y_MIN, Y_MAX, 80)
    XX, YY = np.meshgrid(xg, yg)
    # Subtle elevation noise for atmosphere
    ZZ = (
        0.3 * np.sin(XX / 55) * np.cos(YY / 65)
        + 0.2 * np.cos(XX / 30 + 1) * np.sin(YY / 40)
        + 0.1 * np.random.default_rng(42).standard_normal((80, 80))
    )
    fig.add_trace(go.Contour(
        x=xg, y=yg, z=ZZ,
        showscale=False,
        colorscale=[
            [0.0,  "rgba(12,16,28,1)"],
            [0.35, "rgba(18,22,38,1)"],
            [0.65, "rgba(22,28,48,1)"],
            [1.0,  "rgba(28,34,58,1)"],
        ],
        contours=dict(start=-1, end=1, size=0.25, showlines=False),
        hoverinfo="skip",
        name="terrain",
    ))

    # ── Mountain polygons ──────────────────────────────────────────────────
    for pts in mountains:
        xs = [p[0] for p in pts] + [pts[0][0]]
        ys = [p[1] for p in pts] + [pts[0][1]]
        fig.add_trace(go.Scatter(
            x=xs, y=ys,
            fill="toself",
            fillcolor="rgba(124,34,224,0.12)",
            line=dict(color="rgba(124,34,224,0.5)", width=1.5),
            mode="lines",
            hoverinfo="skip",
            name="terrain-ridge",
            showlegend=False,
        ))

    # ── Craters ───────────────────────────────────────────────────────────
    for (cx, cy, cr) in craters:
        theta = np.linspace(0, 2 * math.pi, 60)
        fig.add_trace(go.Scatter(
            x=[cx + cr * math.cos(t) for t in theta],
            y=[cy + cr * math.sin(t) for t in theta],
            mode="lines",
            line=dict(color="rgba(239,68,68,0.35)", width=1.5, dash="dot"),
            fill="toself",
            fillcolor="rgba(239,68,68,0.04)",
            hoverinfo="skip",
            showlegend=False,
        ))

    # ── Rock clusters ──────────────────────────────────────────────────────
    fig.add_trace(go.Scatter(
        x=[r[0] for r in rocks],
        y=[r[1] for r in rocks],
        mode="markers",
        marker=dict(symbol="square", size=6, color="#555", line=dict(color="#777", width=1)),
        hoverinfo="skip",
        showlegend=False,
    ))

    # ── Obstacles ─────────────────────────────────────────────────────────
    for (ox, oy, orad) in obstacles:
        theta = np.linspace(0, 2 * math.pi, 40)
        fig.add_trace(go.Scatter(
            x=[ox + orad * math.cos(t) for t in theta],
            y=[oy + orad * math.sin(t) for t in theta],
            mode="lines",
            line=dict(color="rgba(250,204,21,0.5)", width=1.5),
            fill="toself",
            fillcolor="rgba(250,204,21,0.06)",
            hovertemplate=f"<b>Obstacle</b><br>({ox:.0f}, {oy:.0f})<extra></extra>",
            showlegend=False,
        ))

    # ── Planned route ──────────────────────────────────────────────────────
    route_xs = [p[0] for p in route]
    route_ys = [p[1] for p in route]
    fig.add_trace(go.Scatter(
        x=route_xs, y=route_ys,
        mode="lines",
        line=dict(color=ROUTE_COLOR, width=2, dash="dash"),
        hoverinfo="skip",
        showlegend=False,
    ))

    # Waypoint markers
    fig.add_trace(go.Scatter(
        x=route_xs[1:-1], y=route_ys[1:-1],
        mode="markers",
        marker=dict(symbol="circle-open", size=7, color=ROUTE_COLOR,
                    line=dict(color=ROUTE_COLOR, width=1.5)),
        hovertemplate="<b>Waypoint</b><br>(%{x:.0f}, %{y:.0f})<extra></extra>",
        showlegend=False,
    ))

    # ── Destination marker ─────────────────────────────────────────────────
    theta = np.linspace(0, 2 * math.pi, 60)
    for r, op in [(14, 0.8), (9, 0.5), (4, 0.3)]:
        fig.add_trace(go.Scatter(
            x=[dest_x + r * math.cos(t) for t in theta],
            y=[dest_y + r * math.sin(t) for t in theta],
            mode="lines",
            line=dict(color=DEST_COLOR, width=1.5 if r == 14 else 1),
            fill="none",
            hoverinfo="skip" if r != 14 else None,
            hovertemplate="<b>Destination</b><br>(%{x:.0f}, %{y:.0f})<extra></extra>" if r == 14 else None,
            showlegend=False,
            opacity=op,
        ))
    # Cross-hair on destination
    for dx, dy in [(-10, 0), (10, 0), (0, -10), (0, 10)]:
        fig.add_trace(go.Scatter(
            x=[dest_x, dest_x + dx],
            y=[dest_y, dest_y + dy],
            mode="lines",
            line=dict(color=DEST_COLOR, width=1.5),
            hoverinfo="skip",
            showlegend=False,
        ))
    fig.add_trace(go.Scatter(
        x=[dest_x], y=[dest_y],
        mode="markers+text",
        marker=dict(symbol="star", size=10, color=DEST_COLOR),
        text=["TARGET"],
        textposition="top right",
        textfont=dict(color=DEST_COLOR, size=9, family="Courier New"),
        hovertemplate="<b>Destination</b><br>(%{x:.0f}, %{y:.0f})<extra></extra>",
        showlegend=False,
    ))

    # ── Rover position ─────────────────────────────────────────────────────
    # Outer pulse ring
    theta = np.linspace(0, 2 * math.pi, 60)
    for r, op in [(16, 0.2), (10, 0.4)]:
        fig.add_trace(go.Scatter(
            x=[rover_x + r * math.cos(t) for t in theta],
            y=[rover_y + r * math.sin(t) for t in theta],
            mode="lines",
            line=dict(color=ROVER_COLOR, width=1),
            fill="toself",
            fillcolor=f"rgba(0,191,255,{op * 0.3})",
            hoverinfo="skip",
            showlegend=False,
        ))
    fig.add_trace(go.Scatter(
        x=[rover_x], y=[rover_y],
        mode="markers+text",
        marker=dict(symbol="circle", size=12, color=ROVER_COLOR,
                    line=dict(color="white", width=1.5)),
        text=["ROVER"],
        textposition="bottom right",
        textfont=dict(color=ROVER_COLOR, size=9, family="Courier New"),
        hovertemplate="<b>Rover</b><br>(%{x:.1f}, %{y:.1f})<extra></extra>",
        showlegend=False,
    ))

    # ── Layout ─────────────────────────────────────────────────────────────
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=BG,
        margin=dict(l=0, r=0, t=0, b=0),
        height=420,
        xaxis=dict(
            range=[X_MIN, X_MAX],
            showgrid=True,
            gridcolor=GRID_COLOR,
            gridwidth=1,
            dtick=40,
            tickfont=dict(color="#444", size=9, family="Courier New"),
            zeroline=False,
            color="#444",
            linecolor="#282e40",
            title=dict(text="X (metres)", font=dict(color="#555", size=9)),
        ),
        yaxis=dict(
            range=[Y_MIN, Y_MAX],
            showgrid=True,
            gridcolor=GRID_COLOR,
            gridwidth=1,
            dtick=40,
            tickfont=dict(color="#444", size=9, family="Courier New"),
            zeroline=False,
            color="#444",
            linecolor="#282e40",
            title=dict(text="Y (metres)", font=dict(color="#555", size=9)),
        ),
        hoverlabel=dict(
            bgcolor="#1e2130",
            bordercolor="#282e40",
            font=dict(color="#f2f2f2", family="Courier New"),
        ),
    )
    return fig


def render_navigation_panel(telemetry: dict) -> None:
    nav = get_navigation_data(telemetry["x"], telemetry["y"])

    st.markdown(
        '<div class="panel-title">🗺 Navigation &amp; Terrain</div>',
        unsafe_allow_html=True,
    )

    fig = _terrain_figure(nav)
    st.plotly_chart(fig, use_container_width=True, config=dict(displayModeBar=False))

    # ── Stats row ──────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    dist = nav["distance_to_target"]
    hdg = nav.get("heading", "--")
    spd  = telemetry.get("speed", 0.0)

    with c1:
        st.markdown(
            f"""<div class="stat-block">
                <div class="stat-label">Distance to Target</div>
                <div class="stat-value" style="color:#00bfff;">{dist:.1f} m</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""<div class="stat-block">
                <div class="stat-label">Heading</div>
                <div class="stat-value" style="color:#7c22e0;">{hdg}°</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with c3:
        color = "#4ade80" if telemetry.get("is_moving") else "#999"
        st.markdown(
            f"""<div class="stat-block">
                <div class="stat-label">Speed</div>
                <div class="stat-value" style="color:{color};">{spd:.3f} m/s</div>
            </div>""",
            unsafe_allow_html=True,
        )
