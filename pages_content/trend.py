import pandas as pd
import streamlit as st

from utils.charts import ma_overlay_chart, price_trend_chart
from utils.data import NAME_MAP, TICKERS, aligned_period, compute_features, load_data


def _box_multiselect(label, options, default, format_func=str, key="box_select"):
    if hasattr(st, "pills"):
        return st.pills(label, options, default=default, format_func=format_func, selection_mode="multi", key=key)

    st.markdown(f"##### {label}")
    container = st.container(border=True)
    selected = []
    cols = container.columns(2)
    default_set = set(default)
    for i, option in enumerate(options):
        with cols[i % 2]:
            checked = st.checkbox(format_func(option), value=option in default_set, key=f"{key}_{option}")
            if checked:
                selected.append(option)
    return selected


def render():
    df = compute_features(load_data())
    aligned_period(df)

    st.markdown(
        """
    <div class="hero">
        <div class="hero-eyebrow">Price Trends</div>
        <h1>Trend <span>Analysis</span></h1>
        <p class="hero-sub">
            Explore historical closing-price trends and moving-average overlays to understand
            directional momentum and trend structure across the selected stocks.
        </p>
        <div class="hero-badges">
            <span class="hero-badge cyan">MA 10-200</span>
            <span class="hero-badge purple">Interactive</span>
            <span class="hero-badge green">Multi-Stock</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col_a, col_b, col_c = st.columns([2, 2, 3])
    with col_a:
        selected_tickers = _box_multiselect("Select stocks", TICKERS, default=TICKERS, format_func=lambda x: NAME_MAP[x], key="trend_tickers")
    with col_b:
        ma_options = _box_multiselect("Moving averages", [10, 20, 50, 100, 200], default=[50, 200], format_func=lambda x: f"MA {x}", key="trend_ma")
    with col_c:
        date_range = st.date_input("Date range", value=(df["date"].min(), df["date"].max()), min_value=df["date"].min(), max_value=df["date"].max())

    if not selected_tickers:
        st.warning("Please select at least one stock.")
        return

    try:
        d_start, d_end = date_range
    except Exception:
        d_start, d_end = df["date"].min(), df["date"].max()

    df_f = df[(df["date"] >= pd.Timestamp(d_start)) & (df["date"] <= pd.Timestamp(d_end))]

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="chart-card"><div class="chart-title">Multi-Stock Price Comparison</div><div class="chart-sub">Closing-price comparison across the selected date range</div>',
        unsafe_allow_html=True,
    )
    st.plotly_chart(price_trend_chart(df_f, selected_tickers), use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("#### Moving Average Breakdown by Stock")
    tabs = st.tabs([NAME_MAP[t] for t in selected_tickers])
    for i, t in enumerate(selected_tickers):
        with tabs[i]:
            st.plotly_chart(ma_overlay_chart(df_f, t, ma_options or [50]), use_container_width=True, config={"displayModeBar": False})
            sub = df_f[df_f["name"] == t].sort_values("date")
            if len(sub):
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Latest Close", f"${sub['close'].iloc[-1]:.2f}")
                c2.metric("Period High", f"${sub['high'].max():.2f}")
                c3.metric("Period Low", f"${sub['low'].min():.2f}")
                period_ret = (sub["close"].iloc[-1] / sub["close"].iloc[0] - 1) * 100
                c4.metric("Period Return", f"{period_ret:+.1f}%")

    st.markdown(
        """
    <div class="insight-box cyan">
        <div class="insight-box-label">Analyst Takeaway</div>
        <p>
        Shorter moving averages react quickly to recent price changes, while longer averages provide
        structural context for the broader trend. When the short-term average remains above the long-term
        average, the price trend is generally stronger; when it falls below, momentum is typically weaker.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )
