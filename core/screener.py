import pandas as pd
import numpy as np

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def compute_atr(df, period=14):
    tr = pd.concat([
        df["High"] - df["Low"],
        (df["High"] - df["Close"].shift()).abs(),
        (df["Low"] - df["Close"].shift()).abs()
    ], axis=1).max(axis=1)
    return tr.rolling(period).mean()


def swing_screen(df):
    if df is None or df.empty or len(df) < 250:
        return None

    df = df.copy()

    df["SMA50"] = df["Close"].rolling(50).mean()
    df["SMA200"] = df["Close"].rolling(200).mean()
    df["RSI"] = compute_rsi(df["Close"])
    df["ATR"] = compute_atr(df)
    df["ATR_pct"] = df["ATR"] / df["Close"]
    df["Vol_Avg"] = df["Volume"].rolling(20).mean()

    latest = df.iloc[-1]

    trend = latest["Close"] > latest["SMA200"]
    institutional = latest["SMA50"] > latest["SMA200"]
    momentum_reset = 40 <= latest["RSI"] <= 65
    liquidity = latest["Volume"] > latest["Vol_Avg"]
    risk_ok = latest["ATR_pct"] < 0.05

    score = (
        25 * trend +
        25 * institutional +
        20 * momentum_reset +
        15 * liquidity +
        15 * risk_ok
    )

    return {
        "Close": round(latest["Close"], 2),
        "RSI": round(latest["RSI"], 1),
        "SMA50": round(latest["SMA50"], 2),
        "SMA200": round(latest["SMA200"], 2),
        "ATR_pct": round(latest["ATR_pct"] * 100, 2),
        "SwingScore": score
    }
