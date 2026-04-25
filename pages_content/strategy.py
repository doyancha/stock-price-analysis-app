import pandas as pd
import streamlit as st

from utils.charts import backtest_chart
from utils.data import NAME_MAP, TICKERS, backtest_ma, compute_features, load_data


def render():
    df = compute_features(load_data())

    st.markdown(
        """
    <div class="hero">
        <div class="hero-eyebrow">Backtesting</div>
        <h1>Strategy &amp; <span>Backtesting</span></h1>
        <p class="hero-sub">
            Evaluate the historical performance of a simple moving-average strategy against
            a passive buy-and-hold baseline across multiple lookback windows.
        </p>
        <div class="hero-badges">
            <span class="hero-badge purple">MA Strategy</span>
            <span class="hero-badge cyan">Buy & Hold</span>
            <span class="hero-badge amber">Cumulative Return</span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class="disclaimer">
    <strong>Backtesting Disclaimer:</strong> These results are based on historical data only and do not
    include transaction costs, taxes, slippage, or position-sizing rules. They are intended for
    educational evaluation rather than real-world trading decisions.
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        ticker = st.selectbox("Select stock", TICKERS, format_func=lambda x: NAME_MAP[x], key="bt_ticker")
    with col_b:
        ma_window = st.select_slider("MA window", options=[10, 20, 50, 100, 200], value=50)

    bt = backtest_ma(df, ticker, ma_window)

    c1, c2, c3 = st.columns(3)
    mkt_ret = (bt["market_return"] - 1) * 100
    strat_ret = (bt["strat_return"] - 1) * 100
    alpha = strat_ret - mkt_ret
    with c1:
        st.markdown(f'<div class="kpi-card cyan"><div class="kpi-icon">B&H</div><div class="kpi-label">Buy & Hold Return</div><div class="kpi-value">{mkt_ret:+.1f}%</div><div class="kpi-delta">Passive baseline</div></div>', unsafe_allow_html=True)
    with c2:
        accent = "green" if strat_ret >= mkt_ret else "red"
        st.markdown(f'<div class="kpi-card {accent}"><div class="kpi-icon">MA</div><div class="kpi-label">MA{ma_window} Strategy Return</div><div class="kpi-value">{strat_ret:+.1f}%</div><div class="kpi-delta">Rule-based strategy</div></div>', unsafe_allow_html=True)
    with c3:
        alpha_accent = "green" if alpha >= 0 else "red"
        st.markdown(f'<div class="kpi-card {alpha_accent}"><div class="kpi-icon">ALPHA</div><div class="kpi-label">Strategy Alpha</div><div class="kpi-value">{alpha:+.1f}%</div><div class="kpi-delta">Versus buy and hold</div></div>', unsafe_allow_html=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown('<div class="chart-card"><div class="chart-title">Cumulative Return - Strategy vs Buy & Hold</div><div class="chart-sub">Direct comparison of active rule-based performance against the passive baseline</div>', unsafe_allow_html=True)
    st.plotly_chart(backtest_chart(bt), use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("#### MA Window Performance Comparison")
    rows = []
    for w in [10, 20, 50, 100, 200]:
        b = backtest_ma(df, ticker, w)
        rows.append(
            {
                "MA Window": f"MA {w}",
                "Strategy Return (%)": round((b["strat_return"] - 1) * 100, 2),
                "Buy & Hold Return (%)": round((b["market_return"] - 1) * 100, 2),
                "Alpha (%)": round(((b["strat_return"] - 1) - (b["market_return"] - 1)) * 100, 2),
            }
        )
    tbl = pd.DataFrame(rows).sort_values("Strategy Return (%)", ascending=False)
    st.dataframe(tbl, use_container_width=True, hide_index=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("#### Planned Strategy Enhancements")
    col1, col2, col3 = st.columns(3)
    cards = [
        ("Benchmark Overlay", "Compare strategy performance with SPY or QQQ for market-relative context."),
        ("Drawdown Analysis", "Track peak-to-trough declines and recovery time across different windows."),
        ("Position Sizing", "Introduce sizing rules such as fixed-fraction or volatility-adjusted exposure."),
    ]
    for col, (title, desc) in zip([col1, col2, col3], cards):
        with col:
            st.markdown(f'<div class="roadmap-card"><div class="roadmap-tag">Planned</div><h4>{title}</h4><p>{desc}</p></div>', unsafe_allow_html=True)

    st.markdown(
        """
    <div class="insight-box purple">
        <div class="insight-box-label">Strategy Limitations</div>
        <p>
        This backtest uses a simple price-versus-moving-average rule with no stop loss, no rebalancing,
        no cost model, and no multi-asset portfolio context. A production-grade strategy review would
        require out-of-sample testing, walk-forward validation, and execution assumptions.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )
