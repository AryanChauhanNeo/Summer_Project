"""
app.py
======
Mars Rover Mission Control Dashboard – Streamlit entry point.

Run with:
    python -m streamlit run app.py
"""

import sys
from pathlib import Path

# Ensure the project root is on the Python path so all imports resolve.
ROOT = Path(__file__).parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

# ── Page config (must be first Streamlit call) ────────────────────────────
st.set_page_config(
    page_title="Mars Rover Mission Control",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Load global CSS ────────────────────────────────────────────────────────
_CSS_PATH = ROOT / "assets" / "styles.css"
with open(_CSS_PATH, "r", encoding="utf-8") as _fh:
    st.markdown(f"<style>{_fh.read()}</style>", unsafe_allow_html=True)

# ── Routing ────────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state["page"] = "home"

# Sidebar navigation (minimal – keeps dashboard full-width)
with st.sidebar:
    st.markdown(
        """
        <div style="font-size:0.7rem;font-weight:700;letter-spacing:0.18em;
                    text-transform:uppercase;color:#00bfff;padding:0.5rem 0 1rem;">
            🚀 MRMCD
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("🏠 Home",      use_container_width=True):
        st.session_state["page"] = "home"
        st.rerun()
    if st.button("📡 Dashboard", use_container_width=True):
        st.session_state["page"] = "dashboard"
        st.rerun()

    st.markdown(
        """
        <div style="margin-top:2rem;font-size:0.62rem;color:#444;
                    letter-spacing:0.1em;text-transform:uppercase;line-height:1.8;">
            Perseverance Class<br>
            Expedition 2026<br>
            Jezero Crater, Mars
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Page dispatch ──────────────────────────────────────────────────────────
page = st.session_state.get("page", "home")

if page == "home":
    from pages.home import render
    render()
elif page == "dashboard":
    from pages.dashboard import render
    render()
else:
    st.error(f"Unknown page: {page!r}")
