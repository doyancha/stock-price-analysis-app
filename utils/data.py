"""
Shared data loading, preprocessing, and analytics helpers.
All functions are cached with st.cache_data for performance.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

TICKERS = ["AAPL", "AMZN", "GOOG", "MSFT"]
NAME_MAP = {
    "AAPL": "Apple",
    "AMZN": "Amazon",
    "GOOG": "Google",
    "MSFT": "Microsoft",
}
COLORS = {
    "Apple": "#00e5ff",
    "Amazon": "#a78bfa",
    "Google": "#34d399",
    "Microsoft": "#fbbf24",
}
TICKER_COLORS = {ticker: COLORS[NAME_MAP[ticker]] for ticker in TICKERS}

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "individual_stocks_5yr"


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    """Load all ticker CSVs and return a unified long-form dataframe."""
    frames = []
    required_cols = {"date", "open", "high", "low", "close", "volume"}

    for ticker in TICKERS:
        fpath = DATA_DIR / f"{ticker}_data.csv"
        if not fpath.exists():
            st.error(
                f"Data file not found: `{fpath}`. "
                "Please keep the `individual_stocks_5yr/` folder next to `app.py`."
            )
            st.stop()

        df = pd.read_csv(fpath)
        df.columns = df.columns.str.strip().str.lower()

        if "name" not in df.columns:
            df["name"] = ticker
        df["name"] = ticker

        missing = required_cols - set(df.columns)
        if missing:
            st.warning(f"Columns missing for {ticker}: {missing}. Some metrics may be unavailable.")

        frames.append(df)

    combined = pd.concat(frames, ignore_index=True)
    combined["date"] = pd.to_datetime(combined["date"])
    combined = combined.sort_values(["name", "date"]).reset_index(drop=True)
    combined["company"] = combined["name"].map(NAME_MAP)
    return combined


@st.cache_data(show_spinner=False)
def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute daily returns and moving averages per ticker."""
    df = df.copy()
    df["daily_return"] = df.groupby("name")["close"].pct_change() * 100
    for window in [10, 20, 50, 100, 200]:
        df[f"ma_{window}"] = df.groupby("name")["close"].transform(lambda s: s.rolling(window).mean())
    return df


@st.cache_data(show_spinner=False)
def get_pivot_close(df: pd.DataFrame) -> pd.DataFrame:
    """Return a wide pivot of closing prices with one column per ticker."""
    pivot = df.pivot_table(index="date", columns="name", values="close", aggfunc="first")
    pivot = pivot.dropna()
    pivot.columns.name = None
    return pivot.rename(columns=NAME_MAP)


@st.cache_data(show_spinner=False)
def aligned_period(df: pd.DataFrame):
    """Return the common start and end date across all tickers."""
    grouped = df.groupby("name")["date"]
    return grouped.min().max(), grouped.max().min()


@st.cache_data(show_spinner=False)
def compute_volatility(df: pd.DataFrame) -> pd.DataFrame:
    start, end = aligned_period(df)
    subset = df[(df["date"] >= start) & (df["date"] <= end)].dropna(subset=["daily_return"])
    vol = (
        subset.groupby("name")["daily_return"]
        .std()
        .reset_index()
        .rename(columns={"name": "ticker", "daily_return": "volatility"})
    )
    vol["company"] = vol["ticker"].map(NAME_MAP)
    return vol


@st.cache_data(show_spinner=False)
def compute_sharpe(df: pd.DataFrame) -> pd.DataFrame:
    start, end = aligned_period(df)
    subset = df[(df["date"] >= start) & (df["date"] <= end)].dropna(subset=["daily_return"])
    agg = subset.groupby("name")["daily_return"].agg(["mean", "std"]).reset_index()
    agg["sharpe_daily"] = agg["mean"] / agg["std"]
    agg["sharpe_annual"] = agg["sharpe_daily"] * np.sqrt(252)
    agg = agg.rename(columns={"name": "ticker"})
    agg["company"] = agg["ticker"].map(NAME_MAP)
    return agg


@st.cache_data(show_spinner=False)
def compute_kpis(df: pd.DataFrame) -> dict:
    """Return high-level KPIs for the home page."""
    start, end = aligned_period(df)
    pivot = get_pivot_close(df)

    if pivot.empty or len(pivot) < 2:
        return {
            "n_stocks": len(TICKERS),
            "date_range": f"{start.strftime('%b %Y')} - {end.strftime('%b %Y')}",
            "avg_return": 0.0,
            "best_return_stock": "N/A",
            "worst_return_stock": "N/A",
            "highest_vol_stock": "N/A",
            "best_sharpe_stock": "N/A",
            "strongest_corr_pair": "N/A",
        }

    total_return = (pivot.iloc[-1] / pivot.iloc[0] - 1) * 100
    best_ticker = total_return.idxmax()
    worst_ticker = total_return.idxmin()

    vol = compute_volatility(df)
    sharpe = compute_sharpe(df)

    best_sharpe_row = sharpe.loc[sharpe["sharpe_annual"].idxmax()]
    highest_vol_row = vol.loc[vol["volatility"].idxmax()]

    strongest_pair = "N/A"
    ret_corr = pivot.pct_change().dropna().corr()
    if ret_corr.shape[0] >= 2:
        off_diag = ret_corr.where(~np.eye(ret_corr.shape[0], dtype=bool))
        stacked = off_diag.stack()
        if not stacked.empty:
            pair = stacked.idxmax()
            strongest_pair = f"{pair[0]} / {pair[1]}"

    return {
        "n_stocks": len(TICKERS),
        "date_range": f"{start.strftime('%b %Y')} - {end.strftime('%b %Y')}",
        "avg_return": float(total_return.mean()),
        "best_return_stock": f"{best_ticker}  ({total_return[best_ticker]:+.1f}%)",
        "worst_return_stock": f"{worst_ticker}  ({total_return[worst_ticker]:+.1f}%)",
        "highest_vol_stock": f"{highest_vol_row['company']}  ({highest_vol_row['volatility']:.3f})",
        "best_sharpe_stock": f"{best_sharpe_row['company']}  ({best_sharpe_row['sharpe_annual']:.2f})",
        "strongest_corr_pair": strongest_pair,
    }


@st.cache_data(show_spinner=False)
def compute_signals(df: pd.DataFrame, ticker: str, short_w: int = 50, long_w: int = 200) -> pd.DataFrame:
    """Generate MA-crossover buy and sell signals for one ticker."""
    d = df[df["name"] == ticker].copy().sort_values("date")
    d["ma_short"] = d["close"].rolling(short_w).mean()
    d["ma_long"] = d["close"].rolling(long_w).mean()
    d["signal"] = 0
    d.loc[d["ma_short"] > d["ma_long"], "signal"] = 1
    d["position"] = d["signal"].diff()
    return d


def backtest_ma(df: pd.DataFrame, ticker: str, ma_window: int) -> dict:
    """Simple price-crossover backtest for one ticker and one MA window."""
    d = df[df["name"] == ticker].copy().sort_values("date").set_index("date")
    d["ma"] = d["close"].rolling(ma_window).mean()
    d["signal"] = (d["close"] > d["ma"]).astype(int)
    d["position"] = d["signal"].shift(1)
    d["ret"] = d["close"].pct_change()
    d["strat_ret"] = d["position"] * d["ret"]
    d["cum_market"] = (1 + d["ret"].fillna(0)).cumprod()
    d["cum_strategy"] = (1 + d["strat_ret"].fillna(0)).cumprod()
    final_mkt = float(d["cum_market"].iloc[-1])
    final_strat = float(d["cum_strategy"].iloc[-1])
    return {
        "ticker": ticker,
        "company": NAME_MAP[ticker],
        "ma_window": ma_window,
        "market_return": final_mkt,
        "strat_return": final_strat,
        "data": d,
    }
