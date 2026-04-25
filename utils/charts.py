"""
Reusable Plotly chart builders with a consistent dark-theme design system.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from utils.data import COLORS, NAME_MAP, TICKERS, TICKER_COLORS

# ── Theme defaults ────────────────────────────────────────────────────────────
LAYOUT_DEFAULTS = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#94a3b8", size=12),
    margin=dict(l=20, r=20, t=50, b=20),
    legend=dict(
        bgcolor="rgba(15,30,61,0.8)",
        bordercolor="#1e3058",
        borderwidth=1,
        font=dict(size=11),
    ),
    xaxis=dict(
        gridcolor="rgba(30,48,88,0.6)",
        zerolinecolor="rgba(30,48,88,0.6)",
        tickfont=dict(size=10),
    ),
    yaxis=dict(
        gridcolor="rgba(30,48,88,0.6)",
        zerolinecolor="rgba(30,48,88,0.6)",
        tickfont=dict(size=10),
    ),
)


def _base_fig(**kwargs) -> go.Figure:
    fig = go.Figure()
    layout = {**LAYOUT_DEFAULTS, **kwargs}
    fig.update_layout(**layout)
    return fig


# ── Price trend (multi-stock line chart) ──────────────────────────────────────
def price_trend_chart(df: pd.DataFrame, tickers: list, title: str = "Closing Price Trend") -> go.Figure:
    fig = _base_fig(title=dict(text=title, font=dict(size=15, color="#e2e8f0"), x=0))
    for t in tickers:
        sub = df[df["name"] == t].sort_values("date")
        fig.add_trace(go.Scatter(
            x=sub["date"], y=sub["close"],
            name=NAME_MAP[t],
            mode="lines",
            line=dict(color=TICKER_COLORS[t], width=2),
            hovertemplate=f"<b>{NAME_MAP[t]}</b><br>Date: %{{x|%b %d, %Y}}<br>Close: $%{{y:.2f}}<extra></extra>",
        ))
    fig.update_layout(hovermode="x unified", height=400)
    return fig


# ── Moving average overlay ────────────────────────────────────────────────────
def ma_overlay_chart(df: pd.DataFrame, ticker: str, ma_windows: list) -> go.Figure:
    sub = df[df["name"] == ticker].sort_values("date")
    name = NAME_MAP[ticker]
    color = TICKER_COLORS[ticker]

    fig = _base_fig(
        title=dict(text=f"{name} — Moving Average Analysis", font=dict(size=15, color="#e2e8f0"), x=0)
    )
    fig.add_trace(go.Scatter(
        x=sub["date"], y=sub["close"],
        name="Close Price",
        line=dict(color=color, width=2),
        opacity=0.9,
    ))

    ma_colors = ["#f87171", "#fbbf24", "#34d399", "#a78bfa", "#38bdf8"]
    for i, w in enumerate(ma_windows):
        col_name = f"ma_{w}"
        if col_name in sub.columns:
            fig.add_trace(go.Scatter(
                x=sub["date"], y=sub[col_name],
                name=f"MA {w}",
                line=dict(color=ma_colors[i % len(ma_colors)], width=1.4, dash="dot"),
                opacity=0.85,
            ))
    fig.update_layout(hovermode="x unified", height=420)
    return fig


# ── Daily returns line ────────────────────────────────────────────────────────
def daily_return_chart(df: pd.DataFrame, tickers: list) -> go.Figure:
    fig = _base_fig(title=dict(text="Daily Return (%)", font=dict(size=15, color="#e2e8f0"), x=0))
    for t in tickers:
        sub = df[df["name"] == t].sort_values("date").dropna(subset=["daily_return"])
        fig.add_trace(go.Scatter(
            x=sub["date"], y=sub["daily_return"].clip(-10, 10),
            name=NAME_MAP[t],
            mode="lines",
            line=dict(color=TICKER_COLORS[t], width=1.2),
            opacity=0.85,
        ))
    fig.update_layout(height=380)
    return fig


# ── Return distribution histogram ────────────────────────────────────────────
def return_dist_chart(df: pd.DataFrame, tickers: list) -> go.Figure:
    fig = _base_fig(title=dict(text="Return Distribution", font=dict(size=15, color="#e2e8f0"), x=0))
    for t in tickers:
        sub = df[df["name"] == t].dropna(subset=["daily_return"])
        fig.add_trace(go.Histogram(
            x=sub["daily_return"].clip(-8, 8),
            name=NAME_MAP[t],
            marker_color=TICKER_COLORS[t],
            opacity=0.65,
            nbinsx=60,
        ))
    fig.update_layout(barmode="overlay", height=380)
    return fig


# ── Volatility bar chart ──────────────────────────────────────────────────────
def volatility_bar_chart(vol_df: pd.DataFrame) -> go.Figure:
    fig = _base_fig(title=dict(text="Volatility — Std Dev of Daily Returns", font=dict(size=15, color="#e2e8f0"), x=0))
    vol_sorted = vol_df.sort_values("volatility", ascending=False)
    fig.add_trace(go.Bar(
        x=vol_sorted["company"],
        y=vol_sorted["volatility"],
        marker_color=[COLORS[c] for c in vol_sorted["company"]],
        text=[f"{v:.4f}" for v in vol_sorted["volatility"]],
        textposition="outside",
        textfont=dict(size=11, color="#94a3b8"),
    ))
    fig.update_layout(height=380, showlegend=False)
    return fig


# ── Sharpe ratio bar chart ────────────────────────────────────────────────────
def sharpe_bar_chart(sharpe_df: pd.DataFrame) -> go.Figure:
    fig = _base_fig(title=dict(text="Annualised Sharpe Ratio (rf = 0)", font=dict(size=15, color="#e2e8f0"), x=0))
    s = sharpe_df.sort_values("sharpe_annual", ascending=False)
    fig.add_trace(go.Bar(
        x=s["company"],
        y=s["sharpe_annual"],
        marker_color=[COLORS[c] for c in s["company"]],
        text=[f"{v:.2f}" for v in s["sharpe_annual"]],
        textposition="outside",
        textfont=dict(size=11, color="#94a3b8"),
    ))
    fig.update_layout(height=380, showlegend=False)
    return fig


# ── Risk vs Return scatter ────────────────────────────────────────────────────
def risk_return_scatter(vol_df: pd.DataFrame, sharpe_df: pd.DataFrame) -> go.Figure:
    merged = vol_df.merge(sharpe_df[["ticker", "sharpe_annual"]], on="ticker")
    fig = _base_fig(title=dict(text="Risk vs Risk-Adjusted Return", font=dict(size=15, color="#e2e8f0"), x=0))
    for _, row in merged.iterrows():
        color = COLORS.get(row["company"], "#94a3b8")
        fig.add_trace(go.Scatter(
            x=[row["volatility"]],
            y=[row["sharpe_annual"]],
            mode="markers+text",
            name=row["company"],
            marker=dict(size=18, color=color, opacity=0.9, line=dict(color="white", width=1.5)),
            text=[row["company"]],
            textposition="top center",
            textfont=dict(size=10, color="#e2e8f0"),
        ))
    fig.update_layout(height=420, xaxis_title="Volatility (σ)", yaxis_title="Annualised Sharpe Ratio")
    return fig


# ── Correlation heatmap ───────────────────────────────────────────────────────
def corr_heatmap(corr_matrix: pd.DataFrame, title: str) -> go.Figure:
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=list(corr_matrix.columns),
        y=list(corr_matrix.index),
        colorscale=[
            [0.0, "#0b1630"], [0.3, "#1e3a5f"],
            [0.5, "#1d4ed8"], [0.75, "#38bdf8"],
            [1.0, "#00e5ff"],
        ],
        zmin=-1, zmax=1,
        text=[[f"{v:.2f}" for v in row] for row in corr_matrix.values],
        texttemplate="%{text}",
        textfont=dict(size=12, color="white"),
        hovertemplate="<b>%{y} vs %{x}</b><br>Correlation: %{z:.3f}<extra></extra>",
    ))
    layout = {**LAYOUT_DEFAULTS}
    layout["title"] = dict(text=title, font=dict(size=15, color="#e2e8f0"), x=0)
    layout["height"] = 420
    fig.update_layout(**layout)
    return fig


# ── Buy/Sell signal chart ─────────────────────────────────────────────────────
def signal_chart(sig_df: pd.DataFrame, ticker: str) -> go.Figure:
    name = NAME_MAP[ticker]
    color = TICKER_COLORS[ticker]
    buy  = sig_df[sig_df["position"] == 1]
    sell = sig_df[sig_df["position"] == -1]

    fig = _base_fig(title=dict(text=f"{name} — MA Crossover Signal", font=dict(size=15, color="#e2e8f0"), x=0))

    fig.add_trace(go.Scatter(x=sig_df["date"], y=sig_df["close"],
        name="Close", line=dict(color=color, width=2)))
    fig.add_trace(go.Scatter(x=sig_df["date"], y=sig_df["ma_short"],
        name="MA Short", line=dict(color="#fbbf24", width=1.4, dash="dot")))
    fig.add_trace(go.Scatter(x=sig_df["date"], y=sig_df["ma_long"],
        name="MA Long", line=dict(color="#f87171", width=1.4, dash="dash")))

    if len(buy):
        fig.add_trace(go.Scatter(x=buy["date"], y=buy["close"],
            mode="markers", name="Buy Signal",
            marker=dict(symbol="triangle-up", size=12, color="#34d399",
                        line=dict(color="white", width=1))))
    if len(sell):
        fig.add_trace(go.Scatter(x=sell["date"], y=sell["close"],
            mode="markers", name="Sell Signal",
            marker=dict(symbol="triangle-down", size=12, color="#f87171",
                        line=dict(color="white", width=1))))

    fig.update_layout(hovermode="x unified", height=450)
    return fig


# ── Backtest cumulative return chart ─────────────────────────────────────────
def backtest_chart(bt: dict) -> go.Figure:
    d = bt["data"].reset_index()
    fig = _base_fig(title=dict(
        text=f"{bt['company']} — MA{bt['ma_window']} Strategy vs Buy & Hold",
        font=dict(size=15, color="#e2e8f0"), x=0))
    fig.add_trace(go.Scatter(x=d["date"], y=d["cum_market"],
        name="Buy & Hold", line=dict(color="#00e5ff", width=2)))
    fig.add_trace(go.Scatter(x=d["date"], y=d["cum_strategy"],
        name=f"MA{bt['ma_window']} Strategy", line=dict(color="#a78bfa", width=2, dash="dot")))
    fig.update_layout(hovermode="x unified", height=420)
    return fig


# ── Pairwise scatter (return % correlation) ───────────────────────────────────
def pairwise_scatter(pivot_close: pd.DataFrame) -> go.Figure:
    """Overlay scatter for each pair of companies' daily returns."""
    rets = pivot_close.pct_change().dropna() * 100
    cols = list(rets.columns)
    pairs = [(cols[i], cols[j]) for i in range(len(cols)) for j in range(i+1, len(cols))]

    fig = _base_fig(title=dict(text="Pairwise Daily Return Scatter", font=dict(size=15, color="#e2e8f0"), x=0))
    for (a, b) in pairs:
        fig.add_trace(go.Scatter(
            x=rets[a], y=rets[b],
            mode="markers",
            name=f"{a} vs {b}",
            marker=dict(size=4, opacity=0.5, color=COLORS.get(a, "#94a3b8")),
            hovertemplate=f"<b>{a}</b>: %{{x:.2f}}%<br><b>{b}</b>: %{{y:.2f}}%<extra></extra>",
        ))
    fig.update_layout(height=440, xaxis_title="Return %", yaxis_title="Return %")
    return fig


# ── Cumulative return (normalised) ────────────────────────────────────────────
def cumulative_return_chart(pivot_close: pd.DataFrame) -> go.Figure:
    norm = pivot_close / pivot_close.iloc[0] * 100
    fig = _base_fig(title=dict(text="Cumulative Indexed Return (Base = 100)", font=dict(size=15, color="#e2e8f0"), x=0))
    for col in norm.columns:
        fig.add_trace(go.Scatter(
            x=norm.index, y=norm[col],
            name=col,
            line=dict(color=COLORS.get(col, "#94a3b8"), width=2),
        ))
    fig.update_layout(hovermode="x unified", height=400)
    return fig


# ── Rolling volatility (30-day) ───────────────────────────────────────────────
def rolling_vol_chart(df: pd.DataFrame, tickers: list, window: int = 30) -> go.Figure:
    fig = _base_fig(title=dict(text=f"{window}-Day Rolling Volatility", font=dict(size=15, color="#e2e8f0"), x=0))
    for t in tickers:
        sub = df[df["name"] == t].sort_values("date").dropna(subset=["daily_return"])
        sub = sub.copy()
        sub["rolling_vol"] = sub["daily_return"].rolling(window).std()
        fig.add_trace(go.Scatter(
            x=sub["date"], y=sub["rolling_vol"],
            name=NAME_MAP[t],
            line=dict(color=TICKER_COLORS[t], width=2),
        ))
    fig.update_layout(height=400, yaxis_title="Std Dev (%)")
    return fig
