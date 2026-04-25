import numpy as np
import streamlit as st

from utils.charts import corr_heatmap, pairwise_scatter
from utils.data import compute_features, get_pivot_close, load_data


def render():
    df = compute_features(load_data())
    pivot = get_pivot_close(df)
    rets = pivot.pct_change().dropna()

    st.markdown(
        """
    <div class="hero">
        <div class="hero-eyebrow">Co-Movement</div>
        <h1>Correlation <span>Analysis</span></h1>
        <p class="hero-sub">
            Map stock relationships at both the closing-price and daily-return level to understand
            co-movement, concentration risk, and diversification potential.
        </p>
        <div class="hero-badges">
            <span class="hero-badge cyan">Price Correlation</span>
            <span class="hero-badge green">Return Correlation</span>
            <span class="hero-badge amber">Pairwise Scatter</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    ret_corr = rets.corr()
    mask = ~np.eye(len(ret_corr), dtype=bool)
    flat = ret_corr.where(mask)
    strongest_idx = flat.stack().idxmax()
    weakest_idx = flat.stack().idxmin()
    avg_corr = float(flat.stack().mean())

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f'<div class="kpi-card cyan"><div class="kpi-icon">PAIR</div><div class="kpi-label">Strongest Pair</div><div class="kpi-value" style="font-size:0.95rem">{strongest_idx[0]} / {strongest_idx[1]}</div><div class="kpi-delta">rho = {float(flat.loc[strongest_idx]):.3f}</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div class="kpi-card green"><div class="kpi-icon">DIVERSE</div><div class="kpi-label">Weakest Pair</div><div class="kpi-value" style="font-size:0.95rem">{weakest_idx[0]} / {weakest_idx[1]}</div><div class="kpi-delta">rho = {float(flat.loc[weakest_idx]):.3f}</div></div>',
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f'<div class="kpi-card amber"><div class="kpi-icon">AVG</div><div class="kpi-label">Avg Pairwise Corr</div><div class="kpi-value">{avg_corr:.3f}</div><div class="kpi-delta">Return-level average</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown(
            '<div class="chart-card"><div class="chart-title">Closing Price Correlation</div><div class="chart-sub">Level-based view that is less useful for risk decisions</div>',
            unsafe_allow_html=True,
        )
        price_corr = pivot.corr()
        st.plotly_chart(corr_heatmap(price_corr, "Closing Price Correlation Matrix"), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    with col_r:
        st.markdown(
            '<div class="chart-card"><div class="chart-title">Daily Return Correlation</div><div class="chart-sub">Preferred measure for diversification and portfolio construction</div>',
            unsafe_allow_html=True,
        )
        st.plotly_chart(corr_heatmap(ret_corr, "Daily Return Correlation Matrix"), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
    <div class="insight-box amber">
        <div class="insight-box-label">Why Return Correlation Matters More</div>
        <p>
        Price-level correlation is often elevated among growth stocks that trend upward together over time.
        Return-level correlation removes that broad trend effect and focuses on day-to-day movement.
        For diversification decisions, return correlation provides the more actionable signal.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="chart-card"><div class="chart-title">Pairwise Daily Return Scatter</div><div class="chart-sub">Each point is one trading day; tighter clouds indicate stronger correlation</div>',
        unsafe_allow_html=True,
    )
    st.plotly_chart(pairwise_scatter(pivot), use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("Full Correlation Tables"):
        tab1, tab2 = st.tabs(["Return Correlation", "Price Correlation"])
        with tab1:
            st.dataframe(ret_corr.round(4), use_container_width=True)
        with tab2:
            st.dataframe(price_corr.round(4), use_container_width=True)

    st.markdown(
        """
    <div class="insight-box green">
        <div class="insight-box-label">Diversification Insight</div>
        <p>
        When pairwise return correlation is high, stocks tend to rise and fall together, which limits
        diversification benefit during drawdowns. The weakest pair in this universe offers the best
        relative diversification potential, though sector concentration remains high.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )
