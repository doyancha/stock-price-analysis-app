import base64
from pathlib import Path

import streamlit as st


def _profile_data_uri() -> str:
    profile_path = Path(__file__).resolve().parents[1] / "assets" / "profile.jpg"
    encoded = base64.b64encode(profile_path.read_bytes()).decode("ascii")
    return f"data:image/jpeg;base64,{encoded}"


def render():
    profile_data_uri = _profile_data_uri()

    st.markdown(
        """
    <div class="hero">
        <div class="hero-eyebrow">About This Project</div>
        <h1>Project <span>Overview</span></h1>
        <p class="hero-sub">
            A portfolio-grade financial analytics case study built to demonstrate
            professional-level data analysis, visualisation, and decision-support thinking.
        </p>
        <div class="hero-badges">
            <span class="hero-badge cyan">Python</span>
            <span class="hero-badge purple">Streamlit</span>
            <span class="hero-badge green">Plotly</span>
            <span class="hero-badge amber">Pandas</span>
            <span class="hero-badge red">NumPy</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col_l, col_r = st.columns([2, 3], vertical_alignment="top")
    with col_l:
        st.markdown(
            f"""
        <div class="about-panel center">
            <img class="profile-photo" src="{profile_data_uri}" alt="Mir Shahadut Hossain profile photo">
            <div style="font-family:'Space Grotesk',sans-serif;font-size:1.15rem;font-weight:700;color:#e2e8f0;margin-bottom:4px">Mir Shahadut Hossain</div>
            <div style="font-size:0.78rem;color:#64748b;margin-bottom:16px;font-family:'JetBrains Mono',monospace">Data Analyst</div>
            <div class="btn-row" style="justify-content:center">
                <a class="glow-btn cyan" href="https://github.com/doyancha" target="_blank" rel="noopener noreferrer">GitHub</a>
                <a class="glow-btn purple" href="https://www.linkedin.com/in/mir-shahadut-hossain/" target="_blank" rel="noopener noreferrer">LinkedIn</a>
            </div>
            <div class="btn-row" style="justify-content:center;margin-top:8px">
                <a class="glow-btn green" href="mailto:your.email@example.com">Email</a>
                <a class="glow-btn green" href="https://github.com/doyancha" target="_blank" rel="noopener noreferrer">Repository</a>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col_r:
        st.markdown(
            """
        <div class="about-panel">
            <div class="about-panel-title">Project Purpose</div>
            <p class="about-panel-text">
            This project was designed as a comprehensive financial data analytics case study,
            demonstrating the end-to-end workflow of a data analyst working with structured
            time-series financial data - from raw CSV ingestion through preprocessing, exploratory
            analysis, visualisation, statistical modelling, and insight generation.
            </p>
            <div class="about-panel-title" style="margin-top:4px;margin-bottom:10px">Analytical Scope</div>
            <div class="about-panel-list">
            • Multi-stock historical price trend analysis<br>
            • Moving average computation and crossover signal detection<br>
            • Daily return calculation and distribution analysis<br>
            • Volatility quantification and Sharpe ratio analysis<br>
            • Closing price and return-level correlation mapping<br>
            • MA-crossover buy/sell signal backtesting vs. buy-and-hold baseline
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    st.markdown("#### Methodology Summary")
    steps = [
        ("01", "Data Collection", "Five years of daily OHLCV data for AAPL, AMZN, GOOG, and MSFT loaded from individual CSV files."),
        ("02", "Preprocessing", "Date parsing, column normalisation, sort ordering, and deduplication applied per ticker."),
        ("03", "Feature Engineering", "Daily returns (pct_change), rolling moving averages (MA10-MA200), and signal columns computed per ticker with no cross-ticker leakage."),
        ("04", "Alignment", "All comparative metrics are restricted to the common overlapping date range across all tickers for fairness."),
        ("05", "Statistical Analysis", "Volatility (sigma), Sharpe Ratio (daily and annualised), total and cumulative return, and Pearson correlation are computed analytically."),
        ("06", "Signal Generation", "MA-crossover logic (Golden Cross / Death Cross) is applied to detect structural trend shifts."),
        ("07", "Backtesting", "MA-based strategy is compared against passive buy-and-hold using cumulative return arithmetic without cost modelling."),
    ]
    cols = st.columns(2)
    for i, (num, title, desc) in enumerate(steps):
        with cols[i % 2]:
            st.markdown(
                f"""
            <div style="display:flex;gap:12px;margin-bottom:14px;padding:14px;background:var(--card);border:1px solid var(--border);border-radius:10px">
                <div style="font-family:'JetBrains Mono',monospace;font-size:1.1rem;font-weight:700;color:var(--border);min-width:28px">{num}</div>
                <div>
                    <div style="font-size:0.88rem;font-weight:600;color:#e2e8f0;margin-bottom:3px">{title}</div>
                    <div style="font-size:0.78rem;color:#64748b;line-height:1.5">{desc}</div>
                </div>
            </div>""",
                unsafe_allow_html=True,
            )

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    st.markdown("#### Technology Stack")
    tech = [
        ("Python 3.10+", "https://docs.python.org/", "Core language"),
        ("Streamlit", "https://docs.streamlit.io/", "Dashboard framework"),
        ("Plotly", "https://plotly.com/python/", "Interactive visualisations"),
        ("Pandas", "https://pandas.pydata.org/docs/", "Data manipulation"),
        ("NumPy", "https://numpy.org/doc/stable/", "Numerical computation"),
        ("Pathlib", "https://docs.python.org/3/library/pathlib.html", "Portable file paths"),
    ]
    pills = " ".join(
        [
            f'<a class="tech-pill" href="{url}" target="_blank" rel="noopener noreferrer" title="{desc}">{label}</a>'
            for label, url, desc in tech
        ]
    )
    st.markdown(f"<div style='margin:8px 0'>{pills}</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    with st.expander("Project Architecture"):
        st.code(
            """
stock_dashboard/
|-- app.py                    # Entry point - routing and layout
|-- utils/
|   |-- styles.py             # Global CSS design system
|   |-- sidebar.py            # Sidebar navigation and contact card
|   |-- data.py               # Cached data loading and analytics helpers
|   `-- charts.py             # Reusable Plotly chart builders
|-- pages_content/
|   |-- home.py               # Home dashboard
|   |-- dataset.py            # Dataset Overview
|   |-- trend.py              # Trend Analysis
|   |-- returns.py            # Return Analysis
|   |-- risk.py               # Risk and Volatility
|   |-- correlation.py        # Correlation Analysis
|   |-- signals.py            # Signal Explorer
|   |-- strategy.py           # Strategy and Backtesting
|   |-- insights.py           # Key Insights
|   `-- about.py              # About Project
`-- individual_stocks_5yr/
    |-- AAPL_data.csv
    |-- AMZN_data.csv
    |-- GOOG_data.csv
    `-- MSFT_data.csv
            """.strip(),
            language="text",
        )

    st.markdown(
        """
    <div class="insight-box cyan">
        <div class="insight-box-label">Reproducibility Note</div>
        <p>
        All data loading uses <code>pathlib.Path</code> for OS-portable relative paths.
        Place the <code>individual_stocks_5yr/</code> folder in the same directory as
        <code>app.py</code> and run <code>streamlit run app.py</code>.
        No absolute paths or environment-specific configurations are required.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )
