import pandas as pd
import plotly.express as px
import streamlit as st

from utils.charts import cumulative_return_chart, daily_return_chart, return_dist_chart
from utils.data import NAME_MAP, TICKERS, aligned_period, compute_features, get_pivot_close, load_data


def _box_multiselect(label, options, default, format_func=str, key="box_select"):
    if hasattr(st, "pills"):
        return st.pills(
            label,
            options,
            default=default,
            format_func=format_func,
            selection_mode="multi",
            key=key,
        )

    st.markdown(f"##### {label}")
    container = st.container(border=True)
    selected = []
    cols = container.columns(2)
    default_set = set(default)
    for i, option in enumerate(options):
        with cols[i % 2]:
            checked = st.checkbox(
                format_func(option),
                value=option in default_set,
                key=f"{key}_{option}",
            )
            if checked:
                selected.append(option)
    return selected


def render():
    df = compute_features(load_data())
    start, end = aligned_period(df)

    st.markdown(
        """
    <div class="hero">
        <div class="hero-eyebrow">Performance</div>
        <h1>Return <span>Analysis</span></h1>
        <p class="hero-sub">
            Examine daily return behaviour, distribution characteristics, and cumulative
            performance across all stocks over the aligned comparison period.
        </p>
        <div class="hero-badges">
            <span class="hero-badge cyan">Daily Returns</span>
            <span class="hero-badge purple">Distributions</span>
            <span class="hero-badge green">Cumulative</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    aligned = df[(df["date"] >= start) & (df["date"] <= end)].dropna(subset=["daily_return"])
    pivot = get_pivot_close(df)
    total_returns = (pivot.iloc[-1] / pivot.iloc[0] - 1) * 100

    c1, c2, c3, c4 = st.columns(4)
    cols = [c1, c2, c3, c4]
    accents = ["cyan", "purple", "green", "amber"]
    for i, t in enumerate(TICKERS):
        company = NAME_MAP[t]
        tr = total_returns.get(company, 0)
        avg_daily = aligned[aligned["name"] == t]["daily_return"].mean()
        with cols[i]:
            sign = "up" if tr >= 0 else "down"
            icon = "UP" if tr >= 0 else "DN"
            st.markdown(
                f"""
            <div class="kpi-card {accents[i]}">
                <div class="kpi-icon">{icon}</div>
                <div class="kpi-label">{company}</div>
                <div class="kpi-value">{tr:+.1f}%</div>
                <div class="kpi-delta {sign}">Avg daily: {avg_daily:+.3f}%</div>
            </div>""",
                unsafe_allow_html=True,
            )

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Daily Returns", "Distribution", "Cumulative"])

    with tab1:
        selected = _box_multiselect(
            "Filter stocks",
            TICKERS,
            default=TICKERS,
            format_func=lambda x: NAME_MAP[x],
            key="ret_sel",
        )
        if not selected:
            selected = TICKERS

        st.markdown(
            '<div class="chart-card"><div class="chart-title">Daily Return Timeline</div><div class="chart-sub">Aligned-period day-by-day return movement across selected stocks</div>',
            unsafe_allow_html=True,
        )
        st.plotly_chart(
            daily_return_chart(df, selected),
            use_container_width=True,
            config={"displayModeBar": False},
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            """
        <div class="insight-box green">
            <div class="insight-box-label">What This Means</div>
            <p>
            Daily return values oscillate around zero. Clusters of large swings indicate periods
            of elevated market stress, major news flow, or abrupt repricing. A sustained drift
            above zero supports a constructive return profile, while persistent downside pressure
            signals a weaker momentum regime.
            </p>
        </div>""",
            unsafe_allow_html=True,
        )

        st.markdown("#### Best vs Worst Trading Days")
        day_stock = st.selectbox(
            "Select stock",
            selected,
            format_func=lambda x: NAME_MAP[x],
            key="ret_best_worst_day",
        )
        day_sub = (
            aligned[aligned["name"] == day_stock]
            .sort_values("date")
            .dropna(subset=["daily_return"])
            .copy()
        )
        if len(day_sub):
            best_day = day_sub.loc[day_sub["daily_return"].idxmax()]
            worst_day = day_sub.loc[day_sub["daily_return"].idxmin()]
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(
                    f"""
                <div class="kpi-card green">
                    <div class="kpi-label">Best Trading Day</div>
                    <div class="kpi-value" style="font-size:1rem">{best_day['daily_return']:+.2f}%</div>
                    <div class="kpi-delta">{best_day['date'].strftime('%b %d, %Y')}</div>
                </div>""",
                    unsafe_allow_html=True,
                )
            with c2:
                st.markdown(
                    f"""
                <div class="kpi-card red">
                    <div class="kpi-label">Worst Trading Day</div>
                    <div class="kpi-value" style="font-size:1rem">{worst_day['daily_return']:+.2f}%</div>
                    <div class="kpi-delta">{worst_day['date'].strftime('%b %d, %Y')}</div>
                </div>""",
                    unsafe_allow_html=True,
                )

    with tab2:
        col_l, col_r = st.columns(2)
        with col_l:
            st.markdown(
                '<div class="chart-card"><div class="chart-title">Return Distribution</div><div class="chart-sub">Spread and skew of daily returns across the full comparison window</div>',
                unsafe_allow_html=True,
            )
            st.plotly_chart(
                return_dist_chart(df, TICKERS),
                use_container_width=True,
                config={"displayModeBar": False},
            )
            st.markdown("</div>", unsafe_allow_html=True)
        with col_r:
            st.markdown("##### Summary Statistics (Aligned Period)")
            stats = aligned.groupby("name")["daily_return"].describe().round(4).rename(index=NAME_MAP)
            st.dataframe(stats, use_container_width=True)

        st.markdown(
            """
        <div class="insight-box purple">
            <div class="insight-box-label">Distribution Insight</div>
            <p>
            A tighter distribution indicates more stable daily returns, while a wider one points to
            greater unpredictability. Skewness helps identify directional asymmetry and kurtosis
            highlights whether extreme tail events appear more frequently than in a normal shape.
            </p>
        </div>""",
            unsafe_allow_html=True,
        )

        st.markdown("#### Distribution Diagnostics")
        dist_stock = st.selectbox(
            "Select stock",
            TICKERS,
            format_func=lambda x: NAME_MAP[x],
            key="ret_dist_diag",
        )
        dist_sub = aligned[aligned["name"] == dist_stock]["daily_return"].dropna()
        if len(dist_sub):
            q1 = dist_sub.quantile(0.25)
            q3 = dist_sub.quantile(0.75)
            iqr = q3 - q1
            outliers = ((dist_sub < q1 - 1.5 * iqr) | (dist_sub > q3 + 1.5 * iqr)).sum()
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(
                    f"""
                <div class="kpi-card purple">
                    <div class="kpi-label">Skewness</div>
                    <div class="kpi-value" style="font-size:1rem">{dist_sub.skew():+.2f}</div>
                    <div class="kpi-delta">Asymmetry of returns</div>
                </div>""",
                    unsafe_allow_html=True,
                )
            with c2:
                st.markdown(
                    f"""
                <div class="kpi-card cyan">
                    <div class="kpi-label">Kurtosis</div>
                    <div class="kpi-value" style="font-size:1rem">{dist_sub.kurt():+.2f}</div>
                    <div class="kpi-delta">Tail heaviness</div>
                </div>""",
                    unsafe_allow_html=True,
                )
            with c3:
                st.markdown(
                    f"""
                <div class="kpi-card amber">
                    <div class="kpi-label">Outlier Days</div>
                    <div class="kpi-value" style="font-size:1rem">{int(outliers)}</div>
                    <div class="kpi-delta">1.5 x IQR rule</div>
                </div>""",
                    unsafe_allow_html=True,
                )

    with tab3:
        st.markdown(
            '<div class="chart-card"><div class="chart-title">Cumulative Indexed Return</div><div class="chart-sub">Normalised performance path with a common base of 100</div>',
            unsafe_allow_html=True,
        )
        st.plotly_chart(
            cumulative_return_chart(pivot),
            use_container_width=True,
            config={"displayModeBar": False},
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            """
        <div class="insight-box amber">
            <div class="insight-box-label">Cumulative Return Insight</div>
            <p>
            Normalising all stocks to a base index of 100 allows clean relative-performance comparison.
            The steepest ending path corresponds to the strongest compounded result, while periods of
            divergence help identify leadership shifts and relative underperformance.
            </p>
        </div>""",
            unsafe_allow_html=True,
        )

        st.markdown("#### Best vs Worst Monthly Returns")
        sel2 = st.selectbox("Select stock", TICKERS, format_func=lambda x: NAME_MAP[x], key="ret_monthly")
        sub = df[df["name"] == sel2].sort_values("date").copy()
        sub["month"] = sub["date"].dt.to_period("M")
        monthly = sub.groupby("month")["close"].last().pct_change() * 100
        monthly = monthly.dropna().sort_values()
        mfig = px.bar(
            x=[str(m) for m in monthly.index],
            y=monthly.values,
            color=monthly.values,
            color_continuous_scale=["#f87171", "#1e3058", "#34d399"],
            labels={"x": "Month", "y": "Return (%)"},
        )
        mfig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8"),
            margin=dict(l=20, r=20, t=30, b=20),
            coloraxis_showscale=False,
            height=320,
        )
        st.plotly_chart(mfig, use_container_width=True, config={"displayModeBar": False})
