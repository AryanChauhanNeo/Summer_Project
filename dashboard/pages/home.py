"""
pages/home.py
=============
Landing / home page.  Displays mission overview and a Launch button
that navigates to the live dashboard view.
"""

import streamlit as st


def render() -> None:
    st.markdown(
        """
        <div style="text-align:center;padding:3rem 1rem 2rem;">
            <div style="font-size:0.8rem;letter-spacing:0.22em;color:#999;
                        text-transform:uppercase;margin-bottom:0.5rem;">
                NASA / ESA Joint Operation
            </div>
            <div style="font-size:2.8rem;font-weight:900;color:#ffaa00;
                        letter-spacing:0.07em;text-transform:uppercase;line-height:1.1;">
                MARS ROVER<br>MISSION CONTROL
            </div>
            <div style="font-size:0.85rem;color:#999;letter-spacing:0.14em;
                        text-transform:uppercase;margin-top:0.75rem;">
                Perseverance Class &mdash; Expedition 2026
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Mission facts grid
    cols = st.columns(4, gap="small")
    facts = [
        ("🚀", "Mission",   "Expedition 2026"),
        ("📍", "Location",  "Jezero Crater"),
        ("🔋", "Power",     "RTG + Solar"),
        ("📡", "Link",      "DSN Active"),
    ]
    for col, (icon, label, val) in zip(cols, facts):
        with col:
            st.markdown(
                f"""
                <div style="background:#1e2130;border:1px solid #282e40;
                             border-radius:0.5rem;padding:1rem;text-align:center;">
                    <div style="font-size:1.6rem;">{icon}</div>
                    <div style="font-size:0.62rem;text-transform:uppercase;
                                letter-spacing:0.14em;color:#999;margin-top:0.3rem;">
                        {label}
                    </div>
                    <div style="font-size:0.92rem;font-weight:700;color:#f2f2f2;
                                margin-top:0.25rem;">
                        {val}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div style='margin:2rem 0 1rem;text-align:center;'>", unsafe_allow_html=True)
    if st.button("🛰  Launch Mission Dashboard", use_container_width=False):
        st.session_state["page"] = "dashboard"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div style="margin-top:2rem;background:#1e2130;border:1px solid #282e40;
                     border-radius:0.5rem;padding:1.25rem 1.5rem;">
            <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;
                        letter-spacing:0.14em;color:#00bfff;margin-bottom:0.75rem;">
                System Overview
            </div>
            <ul style="color:#999;font-size:0.8rem;line-height:1.9;margin:0;padding-left:1.1rem;">
                <li>Live telemetry: coordinates, battery, temperature, speed</li>
                <li>Plotly terrain map with rover position, route &amp; obstacles</li>
                <li>Real-time mission log feed with timestamped entries</li>
                <li>Alert system: warning and critical severity levels</li>
                <li>API-ready: connect Rover Simulator &amp; Navigation Engine via FastAPI</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
