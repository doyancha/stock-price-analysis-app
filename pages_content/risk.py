import pandas as pd
import streamlit as st

from utils.charts import risk_return_scatter, rolling_vol_chart, sharpe_bar_chart, volatility_bar_chart
from utils.data import NAME_MAP, TICKERS, compute_features, compute_sharpe, compute_volatility, load_data


def _boxed_toggle_selector(label, options, default, format_func=str, key="risk_selector"):
    st.markdown(f"##### {label}")
    box = st.container(border=True)
    selected = []
    default_set = set(default)
    cols = box.columns(min(len(options), 4))
    for i, option in enumerate(options):
        with cols[i % len(cols)]:
            checked = st.toggle(format_func(option), value=option in default_set, key=f"{key}_{option}")
            if checked:
                selected.append(option)
    return selected


def render():
    df = compute_features(load_data())
    vol_df = compute_volatility(df)
    sharpe_df = compute_sharpe(df)

    st.markdown(
        """
    <div class="hero">
        <div class="hero-eyebrow">Risk Profile</div>
        <h1>Risk &amp; <span>Volatility</span></h1>
        <p class="hero-sub">
            Measure each stock through volatility, Sharpe Ratio, and risk-versus-return positioning
            to build a more balanced view of upside and downside characteristics.
        </p>
        <div class="hero-badges">
            <span class="hero-badge red">Volatility</span>
            <span class="hero-badge purple">Sharpe Ratio</span>
            <span class="hero-badge cyan">Risk-Return</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    highest_vol = vol_df.loc[vol_df["volatility"].idxmax()]
    lowest_vol = vol_df.loc[vol_df["volatility"].idxmin()]
    best_sharpe = sharpe_df.loc[sharpe_df["sharpe_annual"].idxmax()]
    worst_sharpe = sharpe_df.loc[sharpe_df["sharpe_annual"].idxmin()]

    with c1:
        st.markdown(f'<div class="kpi-card red"><div class="kpi-icon">VOL</div><div class="kpi-label">Highest Volatility</div><div class="kpi-value" style="font-size:1rem">{highest_vol["company"]}</div><div class="kpi-delta">sigma = {highest_vol["volatility"]:.4f}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="kpi-card green"><div class="kpi-icon">STAB</div><div class="kpi-label">Lowest Volatility</div><div class="kpi-value" style="font-size:1rem">{lowest_vol["company"]}</div><div class="kpi-delta">sigma = {lowest_vol["volatility"]:.4f}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="kpi-card cyan"><div class="kpi-icon">SHRP</div><div class="kpi-label">Best Sharpe</div><div class="kpi-value" style="font-size:1rem">{best_sharpe["company"]}</div><div class="kpi-delta">Annualised Sharpe = {best_sharpe["sharpe_annual"]:.2f}</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="kpi-card amber"><div class="kpi-icon">WEAK</div><div class="kpi-label">Weakest Sharpe</div><div class="kpi-value" style="font-size:1rem">{worst_sharpe["company"]}</div><div class="kpi-delta">Annualised Sharpe = {worst_sharpe["sharpe_annual"]:.2f}</div></div>', unsafe_allow_html=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown('<div class="chart-card"><div class="chart-title">Volatility Comparison</div><div class="chart-sub">Standard deviation of daily returns across the aligned period</div>', unsafe_allow_html=True)
        st.plotly_chart(volatility_bar_chart(vol_df), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    with col_r:
        st.markdown('<div class="chart-card"><div class="chart-title">Annualised Sharpe Ratio</div><div class="chart-sub">Risk-adjusted return using rf = 0 and sqrt(252) annualisation</div>', unsafe_allow_html=True)
        st.plotly_chart(sharpe_bar_chart(sharpe_df), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="chart-card"><div class="chart-title">Risk vs Risk-Adjusted Return</div><div class="chart-sub">Volatility on the x-axis and Sharpe Ratio on the y-axis</div>', unsafe_allow_html=True)
    st.plotly_chart(risk_return_scatter(vol_df, sharpe_df), use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    window_choice = st.select_slider("Rolling window (days)", options=[10, 20, 30, 60, 90], value=30)
    tickers_sel = _boxed_toggle_selector("Select stocks", TICKERS, default=TICKERS, format_func=lambda x: NAME_MAP[x], key="rvol")
    if not tickers_sel:
        tickers_sel = TICKERS
    st.markdown('<div class="chart-card"><div class="chart-title">Rolling Volatility</div><div class="chart-sub">Moving standard deviation of returns for the selected stocks and window</div>', unsafe_allow_html=True)
    st.plotly_chart(rolling_vol_chart(df, tickers_sel, window_choice), use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(
            """
        <div class="insight-box red">
            <div class="insight-box-label">Risk Interpretation</div>
            <p>
            Higher volatility means wider daily price swings and a rougher return path. Lower-volatility
            names often provide smoother behaviour, but that does not automatically mean better performance.
            </p>
        </div>""",
            unsafe_allow_html=True,
        )
    with col_b:
        st.markdown(
            """
        <div class="insight-box purple">
            <div class="insight-box-label">Sharpe Ratio Context</div>
            <p>
            The Sharpe Ratio compares average return to volatility. A higher value indicates better
            compensation for the amount of risk taken, making it useful for ranking stocks on a
            risk-adjusted basis rather than a pure return basis.
            </p>
        </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("#### Full Risk Metrics Table")
    merged = vol_df.merge(sharpe_df[["ticker", "mean", "std", "sharpe_daily", "sharpe_annual"]], on="ticker")
    merged = merged.rename(
        columns={
            "company": "Company",
            "volatility": "Volatility (sigma)",
            "mean": "Mean Daily Return (%)",
            "sharpe_daily": "Daily Sharpe",
            "sharpe_annual": "Annualised Sharpe",
        }
    )
    display_cols = ["Company", "Volatility (sigma)", "Mean Daily Return (%)", "Daily Sharpe", "Annualised Sharpe"]
    st.dataframe(merged[display_cols].sort_values("Annualised Sharpe", ascending=False).round(4), use_container_width=True, hide_index=True)
