import base64
from pathlib import Path

import streamlit as st

NAV_PAGES = [
    "Home",
    "Dataset Overview",
    "Trend Analysis",
    "Return Analysis",
    "Risk & Volatility",
    "Correlation Analysis",
    "Signal Explorer",
    "Strategy & Backtesting",
    "Key Insights",
    "About Project",
]


def _profile_data_uri() -> str:
    profile_path = Path(__file__).resolve().parents[1] / "assets" / "profile.jpg"
    encoded = base64.b64encode(profile_path.read_bytes()).decode("ascii")
    return f"data:image/jpeg;base64,{encoded}"


def render_sidebar() -> str:
    profile_data_uri = _profile_data_uri()

    with st.sidebar:
        st.markdown(
            """
        <div class="sb-project-card">
            <div class="sb-project-badge">Analytics Dashboard</div>
            <div class="sb-project-title">EquityLens</div>
            <div class="sb-project-tag">Multi-Stock Price Analysis &amp; Decision-Support Tool</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown("<div class='nav-section-label'>Navigation</div>", unsafe_allow_html=True)

        selected_label = st.radio(
            "nav",
            NAV_PAGES,
            label_visibility="collapsed",
        )
        selected_page = selected_label

        st.markdown("<div style='flex:1'></div>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color:#1e3058;margin:14px 0'>", unsafe_allow_html=True)

        st.markdown(
            f"""
        <div class="sb-contact-card">
            <div class="sb-contact-title">Contact</div>
            <div class="sb-contact-head">
                <img class="sb-contact-photo" src="{profile_data_uri}" alt="Mir Shahadut Hossain">
                <div class="sb-contact-meta">
                    <div class="sb-contact-name">Mir Shahadut Hossain</div>
                    <div class="sb-contact-role">Data Analyst</div>
                    <div class="sb-contact-status">
                        <span class="sb-contact-status-dot"></span>
                        Open to Connect
                    </div>
                </div>
            </div>
            <div class="sb-contact-grid">
                <a class="sb-contact-link github" href="https://github.com/doyancha" target="_blank" rel="noopener noreferrer">
                    <span class="sb-contact-link-main"><span class="sb-contact-icon">GH</span> GitHub</span>
                    <span class="sb-contact-arrow">›</span>
                </a>
                <a class="sb-contact-link linkedin" href="https://www.linkedin.com/in/mir-shahadut-hossain/" target="_blank" rel="noopener noreferrer">
                    <span class="sb-contact-link-main"><span class="sb-contact-icon">in</span> LinkedIn</span>
                    <span class="sb-contact-arrow">›</span>
                </a>
                <a class="sb-contact-link email" href="mailto:your.email@example.com">
                    <span class="sb-contact-link-main"><span class="sb-contact-icon">@</span> Email</span>
                    <span class="sb-contact-arrow">›</span>
                </a>
                <a class="sb-contact-link repo" href="https://github.com/doyancha" target="_blank" rel="noopener noreferrer">
                    <span class="sb-contact-link-main"><span class="sb-contact-icon">[]</span> Repository</span>
                    <span class="sb-contact-arrow">›</span>
                </a>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
        <div style="font-size:0.62rem;color:#334155;text-align:center;padding:6px 0 2px;font-family:'JetBrains Mono',monospace;">
        Built by Mir Shahadut Hossain
        </div>
        """,
            unsafe_allow_html=True,
        )

    return selected_page
