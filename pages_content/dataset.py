import pandas as pd
import streamlit as st

from utils.data import NAME_MAP, TICKERS, compute_features, load_data


def render():
    df_raw = load_data()
    df = compute_features(df_raw)

    st.markdown(
        """
    <div class="hero">
        <div class="hero-eyebrow">Data Layer</div>
        <h1>Dataset <span>Overview</span></h1>
        <p class="hero-sub">
            Structural inspection of the underlying dataset covering coverage, quality,
            schema, and preprocessing before any analytical layer is applied.
        </p>
        <div class="hero-badges">
            <span class="hero-badge cyan">Long-form Format</span>
            <span class="hero-badge green">4 Tickers</span>
            <span class="hero-badge amber">5 Years</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    coverage = (
        df.groupby("name")
        .agg(
            rows=("close", "size"),
            start=("date", "min"),
            end=("date", "max"),
            missing_close=("close", lambda s: int(s.isna().sum())),
        )
        .sort_index()
        .reset_index()
    )
    coverage["company"] = coverage["name"].map(NAME_MAP)

    c1, c2, c3, c4 = st.columns(4)
    total_rows = len(df)
    date_min = df["date"].min().strftime("%b %d, %Y")
    date_max = df["date"].max().strftime("%b %d, %Y")
    missing_pct = df["close"].isna().mean() * 100

    with c1:
        st.markdown(
            f'<div class="kpi-card cyan"><div class="kpi-icon">Rows</div><div class="kpi-label">Total Rows</div><div class="kpi-value" style="font-size:1rem">{total_rows:,}</div><div class="kpi-delta">All tickers combined</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div class="kpi-card purple"><div class="kpi-icon">Date</div><div class="kpi-label">Earliest Date</div><div class="kpi-value" style="font-size:1rem">{date_min}</div></div>',
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f'<div class="kpi-card green"><div class="kpi-icon">Date</div><div class="kpi-label">Latest Date</div><div class="kpi-value" style="font-size:1rem">{date_max}</div></div>',
            unsafe_allow_html=True,
        )
    with c4:
        quality_label = "Clean" if missing_pct < 0.5 else f"{missing_pct:.1f}% missing"
        st.markdown(
            f'<div class="kpi-card amber"><div class="kpi-icon">Scan</div><div class="kpi-label">Data Quality</div><div class="kpi-value" style="font-size:1rem">{quality_label}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    st.markdown("#### Per-Ticker Coverage")
    display_cov = coverage[["company", "rows", "start", "end", "missing_close"]].copy()
    display_cov.columns = ["Company", "Trading Days", "Start", "End", "Missing Close"]
    display_cov["Start"] = display_cov["Start"].dt.strftime("%Y-%m-%d")
    display_cov["End"] = display_cov["End"].dt.strftime("%Y-%m-%d")
    st.dataframe(display_cov, use_container_width=True, hide_index=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    st.markdown("#### Schema & Data Dictionary")
    schema = {
        "Column": ["date", "open", "high", "low", "close", "volume", "name", "company"],
        "Type": ["Date", "Float", "Float", "Float", "Float", "Integer", "String", "String"],
        "Description": [
            "Trading session date (daily frequency)",
            "Opening price of the session",
            "Intraday high price",
            "Intraday low price",
            "Session closing price - primary analysis metric",
            "Total share volume traded",
            "Ticker symbol (AAPL / AMZN / GOOG / MSFT)",
            "Full company display name",
        ],
    }
    st.dataframe(pd.DataFrame(schema), use_container_width=True, hide_index=True)

    with st.expander("Raw Data Preview (first 200 rows)"):
        cols_show = [
            c
            for c in ["date", "open", "high", "low", "close", "volume", "name", "company"]
            if c in df.columns
        ]
        st.dataframe(df[cols_show].head(200), use_container_width=True, hide_index=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("#### Preprocessing Summary")
    st.markdown(
        """
    <div class="insight-box green">
        <div class="insight-box-label">Steps Applied</div>
        <p>
        1. <strong>Date parsing</strong> - all date strings converted to <code>datetime64</code>.<br>
        2. <strong>Column normalisation</strong> - lowercase strip applied to all headers.<br>
        3. <strong>Ticker tagging</strong> - <code>name</code> column enforced for each file.<br>
        4. <strong>Sort order</strong> - sorted by <code>[name, date]</code> ascending.<br>
        5. <strong>Moving averages</strong> - MA10 / MA20 / MA50 / MA100 / MA200 computed
           per ticker with <code>groupby().transform()</code>.<br>
        6. <strong>Daily returns</strong> - computed as <code>pct_change() * 100</code> per ticker.<br>
        7. <strong>Overlapping window</strong> - comparison metrics use the common date range
           shared by all tickers.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("#### Descriptive Statistics by Ticker")
    ticker_choice = st.selectbox("Select ticker", options=TICKERS, format_func=lambda x: NAME_MAP[x])
    desc = df[df["name"] == ticker_choice][["open", "high", "low", "close", "volume"]].describe().T.round(2)
    st.dataframe(desc, use_container_width=True)
