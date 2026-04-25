import numpy as np
import streamlit as st

from utils.data import compute_features, compute_kpis, compute_sharpe, compute_volatility, get_pivot_close, load_data


def render():
    df = compute_features(load_data())
    kpis = compute_kpis(df)
    vol_df = compute_volatility(df)
    sharpe_df = compute_sharpe(df)
    pivot = get_pivot_close(df)
    total_ret = (pivot.iloc[-1] / pivot.iloc[0] - 1) * 100

    best_ret_company = total_ret.idxmax()
    best_ret_val = total_ret.max()
    best_sharpe_row = sharpe_df.loc[sharpe_df["sharpe_annual"].idxmax()]
    highest_vol_row = vol_df.loc[vol_df["volatility"].idxmax()]
    lowest_vol_row = vol_df.loc[vol_df["volatility"].idxmin()]

    ret_corr = pivot.pct_change().dropna().corr()
    mask = ~np.eye(len(ret_corr), dtype=bool)
    flat = ret_corr.where(mask)
    weakest_pair = flat.stack().idxmin()
    weakest_corr = float(flat.loc[weakest_pair])

    st.markdown(
        """
    <div class="hero">
        <div class="hero-eyebrow">Analytical Conclusions</div>
        <h1>Key <span>Insights</span></h1>
        <p class="hero-sub">
            Consolidated findings from the full multi-stock analysis, framed as decision-support
            context for stakeholders rather than trading advice.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    findings = [
        ("Top Total Return", f"{best_ret_company} delivered the strongest cumulative return at {best_ret_val:+.1f}%, outperforming the group average of {kpis['avg_return']:+.1f}%."),
        ("Best Risk-Adjusted Performance", f"{best_sharpe_row['company']} achieved the highest annualised Sharpe Ratio at {best_sharpe_row['sharpe_annual']:.2f}, indicating the strongest return per unit of risk."),
        ("Highest Volatility Stock", f"{highest_vol_row['company']} had the largest daily return standard deviation at {highest_vol_row['volatility']:.4f}, making it the most risk-intensive holding in this universe."),
        ("Lowest Volatility Stock", f"{lowest_vol_row['company']} was the most stable stock in the group, offering lower volatility with a more defensive return profile."),
        ("Best Diversification Pair", f"{weakest_pair[0]} and {weakest_pair[1]} showed the weakest return correlation at {weakest_corr:.3f}, giving them the strongest diversification potential within this set."),
        ("Equal-Weight Portfolio", "An equal-weight portfolio across all four names would still be highly concentrated in large-cap technology, but it would capture some limited diversification benefit within the sector."),
    ]

    col1, col2 = st.columns(2)
    for i, (title, desc) in enumerate(findings):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(
                f"""
            <div class="finding-card" style="margin-bottom:16px">
                <div class="finding-num">0{i+1}</div>
                <h4>{title}</h4>
                <p>{desc}</p>
            </div>""",
                unsafe_allow_html=True,
            )

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("#### Decision-Support Takeaways by Stakeholder Type")

    tabs = st.tabs(["Growth-Focused", "Risk-Aware", "Diversification-Seeking"])
    with tabs[0]:
        st.markdown(
            f"""
        <div class="insight-box green">
            <div class="insight-box-label">Growth-Focused Stakeholder</div>
            <p>
            Prioritise <strong>{best_ret_company}</strong> for strongest total return, but validate that choice
            against volatility and signal context before calling it a leadership position.
            </p>
        </div>""",
            unsafe_allow_html=True,
        )
    with tabs[1]:
        st.markdown(
            f"""
        <div class="insight-box cyan">
            <div class="insight-box-label">Risk-Aware Stakeholder</div>
            <p>
            Focus on <strong>{lowest_vol_row['company']}</strong> for relative stability and compare its risk
            profile with its Sharpe Ratio before treating it as a defensive anchor.
            </p>
        </div>""",
            unsafe_allow_html=True,
        )
    with tabs[2]:
        st.markdown(
            f"""
        <div class="insight-box purple">
            <div class="insight-box-label">Diversification-Seeking Stakeholder</div>
            <p>
            The pairing of <strong>{weakest_pair[0]} and {weakest_pair[1]}</strong> offers the most independent
            return behaviour in this dataset, though true diversification would still require sector expansion.
            </p>
        </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    st.markdown("#### Analytical Limitations & Future Improvements")
    col1, col2 = st.columns(2)
    limitations = [
        "All four stocks are from the US technology sector, so the universe lacks cross-sector diversification.",
        "Dividend and split-adjusted total return is not modelled.",
        "The analysis uses daily data only and does not capture intraday volatility behaviour.",
        "Moving-average signals are backward-looking and do not forecast future price direction.",
    ]
    improvements = [
        "Add a benchmark such as SPY or QQQ for relative-performance context.",
        "Blend price analysis with a small set of fundamental indicators.",
        "Expand the ticker universe across sectors.",
        "Introduce out-of-sample or walk-forward testing for the strategy layer.",
    ]
    with col1:
        st.markdown("##### Known Limitations")
        for item in limitations:
            st.markdown(f"<div style='font-size:0.83rem;color:#94a3b8;padding:6px 0;border-bottom:1px solid #1e3058'>- {item}</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("##### Future Improvements")
        for item in improvements:
            st.markdown(f"<div style='font-size:0.83rem;color:#94a3b8;padding:6px 0;border-bottom:1px solid #1e3058'>- {item}</div>", unsafe_allow_html=True)
