"""
components/alerts_panel.py
==========================
Bottom-right panel: alert cards + critical/warning summary counts.
Mirrors alerts-panel.tsx.
"""

import streamlit as st
from services.api_client import fetch_alerts


def render_alerts_panel(extra_alerts: list | None = None) -> None:
    alerts = fetch_alerts()

    # Merge live alerts generated during the session
    if extra_alerts:
        alerts = list(alerts) + list(extra_alerts)

    n_critical = sum(1 for a in alerts if a.get("type") == "critical")
    n_warning  = sum(1 for a in alerts if a.get("type") == "warning")

    st.markdown(
        '<div class="panel-title">⚡ Alerts &amp; Warnings</div>',
        unsafe_allow_html=True,
    )

    if not alerts:
        st.markdown(
            '<p style="color:#999;font-size:0.82rem;text-align:center;padding:2rem 0;">'
            "All systems nominal</p>",
            unsafe_allow_html=True,
        )
    else:
        for alert in alerts:
            atype = alert.get("type", "warning")
            msg   = alert.get("message", "")
            sub   = alert.get("subsystem", "")
            ts    = alert.get("timestamp", "")

            if atype == "critical":
                card_cls  = "alert-card alert-critical"
                icon      = "🔴"
                type_html = '<span class="alert-type-critical">CRITICAL</span>'
            else:
                card_cls  = "alert-card alert-warning"
                icon      = "🟡"
                type_html = '<span class="alert-type-warning">WARNING</span>'

            sub_html = f'<span style="font-size:0.62rem;color:#555;margin-left:6px;">[{sub}]</span>' if sub else ""
            st.markdown(
                f"""
                <div class="{card_cls}">
                    <span class="alert-icon">{icon}</span>
                    <div>
                        {type_html}{sub_html}
                        <div class="alert-msg">{msg}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Summary counts
    st.markdown('<hr class="section-sep"/>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f"""<div class="stat-block">
                <div class="stat-label">Critical</div>
                <div class="stat-value" style="color:#ef4444;">{n_critical}</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""<div class="stat-block">
                <div class="stat-label">Warnings</div>
                <div class="stat-value" style="color:#facc15;">{n_warning}</div>
            </div>""",
            unsafe_allow_html=True,
        )
