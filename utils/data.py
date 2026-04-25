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
COMBINED_DATA_FILE = BASE_DIR / "data" / "stock_prices.csv"
STOOQ_URL = "https://stooq.com/q/d/l/?s={symbol}.us&i=d"


def _load_combined_csv() -> pd.DataFrame | None:
    if not COMBINED_DATA_FILE.exists():
        return None

    df = pd.read_csv(COMBINED_DATA_FILE)
    df.columns = df.columns.str.strip().str.lower()
    return df


def _load_local_csv(ticker: str) -> pd.DataFrame | None:
    fpath = DATA_DIR / f"{ticker}_data.csv"
    if not fpath.exists():
        return None

    df = pd.read_csv(fpath)
    df.columns = df.columns.str.strip().str.lower()
    return df


def _load_remote_history(ticker: str) -> pd.DataFrame:
    url = STOOQ_URL.format(symbol=ticker.lower())
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip().str.lower()

    if df.empty:
        raise ValueError(f"No rows returned for {ticker}")

    df["date"] = pd.to_datetime(df["date"])
    cutoff = pd.Timestamp.today().normalize() - pd.DateOffset(years=5)
    return df[df["date"] >= cutoff].copy()


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    """Load ticker data from the packaged dataset, local CSVs, or online history."""
    combined_csv = _load_combined_csv()
    required_cols = {"date", "open", "high", "low", "close", "volume"}

    if combined_csv is not None:
        missing = (required_cols | {"name"}) - set(combined_csv.columns)
        if missing:
            st.error(f"Combined dataset is missing required columns: {missing}")
            st.stop()
            raise RuntimeError(f"Combined dataset is missing required columns: {missing}")

        combined_csv["date"] = pd.to_datetime(combined_csv["date"])
        combined_csv = combined_csv[combined_csv["name"].isin(TICKERS)].copy()
        combined_csv["company"] = combined_csv["name"].map(NAME_MAP)
        return combined_csv.sort_values(["name", "date"]).reset_index(drop=True)

    frames = []
    for ticker in TICKERS:
        df = _load_local_csv(ticker)
        if df is None:
            try:
                df = _load_remote_history(ticker)
            except Exception as exc:
                message = (
                    f"Could not load {ticker} stock history from local CSVs or Stooq. "
                    f"Details: {exc}"
                )
                st.error(message)
                st.stop()
                raise RuntimeError(message) from exc

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
