import streamlit as st

from utils.charts import cumulative_return_chart, price_trend_chart
from utils.data import NAME_MAP, TICKERS, compute_features, compute_kpis, load_data


def get_pivot_close(df):
    from utils.data import get_pivot_close as _gpc

    return _gpc(df)


def render():
    df = compute_features(load_data())
    kpis = compute_kpis(df)

    st.markdown(
        """
    <div class="hero">
        <div class="hero-eyebrow">Equity Research Platform</div>
        <h1>EquityLens <span>Analytics</span></h1>
        <p class="hero-sub">
            A portfolio-grade multi-stock analytics dashboard covering trend analysis,
            return profiling, risk measurement, correlation mapping, and signal exploration
            across AAPL, AMZN, GOOG, and MSFT.
        </p>
        <div class="hero-badges">
            <span class="hero-badge cyan">5-Year Dataset</span>
            <span class="hero-badge purple">4 Tech Stocks</span>
            <span class="hero-badge green">Interactive Analysis</span>
            <span class="hero-badge amber">Decision Support</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"""
        <div class="kpi-card cyan">
            <div class="kpi-icon">DATA</div>
            <div class="kpi-label">Stocks Analysed</div>
            <div class="kpi-value">{kpis['n_stocks']}</div>
            <div class="kpi-delta">AAPL | AMZN | GOOG | MSFT</div>
        </div>""",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
        <div class="kpi-card purple">
            <div class="kpi-icon">TIME</div>
            <div class="kpi-label">Analysis Period</div>
            <div class="kpi-value" style="font-size:1.1rem">{kpis['date_range']}</div>
            <div class="kpi-delta">Overlapping comparison window</div>
        </div>""",
            unsafe_allow_html=True,
        )
    with c3:
        sign = "up" if kpis["avg_return"] >= 0 else "down"
        arrow = "UP" if kpis["avg_return"] >= 0 else "DN"
        st.markdown(
            f"""
        <div class="kpi-card green">
            <div class="kpi-icon">RET</div>
            <div class="kpi-label">Avg Period Return</div>
            <div class="kpi-value">{kpis['avg_return']:+.1f}%</div>
            <div class="kpi-delta {sign}">{arrow} Portfolio average</div>
        </div>""",
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f"""
        <div class="kpi-card amber">
            <div class="kpi-icon">RISK</div>
            <div class="kpi-label">Best Sharpe Ratio</div>
            <div class="kpi-value" style="font-size:1rem">{kpis['best_sharpe_stock']}</div>
            <div class="kpi-delta">Annualised, rf = 0</div>
        </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"""
        <div class="kpi-card green">
            <div class="kpi-icon">TOP</div>
            <div class="kpi-label">Highest Return</div>
            <div class="kpi-value" style="font-size:1rem">{kpis['best_return_stock']}</div>
            <div class="kpi-delta up">UP Top performer</div>
        </div>""",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
        <div class="kpi-card red">
            <div class="kpi-icon">LOW</div>
            <div class="kpi-label">Lowest Return</div>
            <div class="kpi-value" style="font-size:1rem">{kpis['worst_return_stock']}</div>
            <div class="kpi-delta down">DN Relative underperformer</div>
        </div>""",
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""
        <div class="kpi-card red">
            <div class="kpi-icon">VOL</div>
            <div class="kpi-label">Highest Volatility</div>
            <div class="kpi-value" style="font-size:1rem">{kpis['highest_vol_stock']}</div>
            <div class="kpi-delta">Highest daily sigma</div>
        </div>""",
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f"""
        <div class="kpi-card cyan">
            <div class="kpi-icon">CORR</div>
            <div class="kpi-label">Strongest Corr Pair</div>
            <div class="kpi-value" style="font-size:0.95rem">{kpis['strongest_corr_pair']}</div>
            <div class="kpi-delta">Return-level correlation</div>
        </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    col_l, col_r = st.columns([3, 2])
    with col_l:
        st.markdown(
            '<div class="chart-card"><div class="chart-title">Price History - All Stocks</div><div class="chart-sub">Daily closing price across the full dataset range</div>',
            unsafe_allow_html=True,
        )
        st.plotly_chart(price_trend_chart(df, TICKERS), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with col_r:
        pivot = get_pivot_close(df)
        st.markdown(
            '<div class="chart-card"><div class="chart-title">Cumulative Return (Indexed = 100)</div><div class="chart-sub">Normalised performance comparison</div>',
            unsafe_allow_html=True,
        )
        st.plotly_chart(cumulative_return_chart(pivot), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
    <div class="insight-box cyan">
        <div class="insight-box-label">Executive Summary</div>
        <p>
        This dashboard analyses five years of daily closing price data for Apple, Amazon,
        Google, and Microsoft. The workflow covers trend identification, return behaviour,
        volatility measurement, correlation analysis, and moving-average signal exploration.
        All comparative metrics use the overlapping date window to keep stock-to-stock analysis fair.
        <strong>This tool is for educational and analytical use only and is not financial advice.</strong>
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### What This Dashboard Covers")
    cols = st.columns(3)
    features = [
        ("TREND", "Trend Analysis", "Price history with configurable moving averages from MA10 to MA200."),
        ("RET", "Return Analysis", "Daily returns, distribution behaviour, and cross-stock performance ranking."),
        ("RISK", "Risk & Volatility", "Volatility, rolling risk, and Sharpe-ratio comparison."),
        ("CORR", "Correlation", "Closing-price and return-level heatmaps plus pairwise scatter analysis."),
        ("SIG", "Signal Explorer", "Golden Cross and Death Cross style moving-average signal tracking."),
        ("BT", "Backtesting", "Simple MA strategy evaluation against a buy-and-hold baseline."),
    ]
    for i, (tag, title, desc) in enumerate(features):
        with cols[i % 3]:
            st.markdown(
                f"""
            <div class="kpi-card" style="margin-bottom:14px">
                <div style="font-size:1rem;margin-bottom:6px;font-family:'JetBrains Mono',monospace;color:#38bdf8">{tag}</div>
                <div style="font-size:0.85rem;font-weight:600;color:#e2e8f0;margin-bottom:4px">{title}</div>
                <div style="font-size:0.78rem;color:#64748b;line-height:1.5">{desc}</div>
            </div>""",
                unsafe_allow_html=True,
            )

    st.markdown(
        """
    <div class="disclaimer">
    <strong>Disclaimer:</strong> All content on this dashboard is strictly for educational and portfolio
    demonstration purposes. Nothing presented here should be treated as a recommendation to buy or sell
    any security. Past performance does not guarantee future results.
    </div>
    """,
        unsafe_allow_html=True,
    )
