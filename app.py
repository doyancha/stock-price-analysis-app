"""
EquityLens — Premium Stock Analytics Dashboard
Author: Mir Shahadut Hossain
GitHub: https://github.com/doyancha
LinkedIn: https://www.linkedin.com/in/mir-shahadut-hossain/
"""

import streamlit as st
from pathlib import Path

# ── Page config (must be first Streamlit call) ──────────────────────────────
st.set_page_config(
    page_title="EquityLens | Stock Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Shared CSS ────────────────────────────────────────────────────────────────
from utils.styles import inject_css
inject_css()

# ── Sidebar ──────────────────────────────────────────────────────────────────
from utils.sidebar import render_sidebar
page = render_sidebar()

# ── Page routing ─────────────────────────────────────────────────────────────
if page == "Home":
    from pages_content import home; home.render()
elif page == "Dataset Overview":
    from pages_content import dataset; dataset.render()
elif page == "Trend Analysis":
    from pages_content import trend; trend.render()
elif page == "Return Analysis":
    from pages_content import returns; returns.render()
elif page == "Risk & Volatility":
    from pages_content import risk; risk.render()
elif page == "Correlation Analysis":
    from pages_content import correlation; correlation.render()
elif page == "Signal Explorer":
    from pages_content import signals; signals.render()
elif page == "Strategy & Backtesting":
    from pages_content import strategy; strategy.render()
elif page == "Key Insights":
    from pages_content import insights; insights.render()
elif page == "About Project":
    from pages_content import about; about.render()
