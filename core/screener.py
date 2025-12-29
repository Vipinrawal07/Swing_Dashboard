import pandas as pd
import numpy as np


def compute_rsi(close, period=14):
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def compute_atr(high, low, close, period=14):
    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low - close.shift()).abs()
    ], axis=1).max(axis=1)

    return tr.rolling(period).mean()


def swing_screen(df):
    # -------- HARD SAFETY GUARDS --------
    if df is None or df.empty:
        return None

    if len(df) < 220:
        return None

    df = df.copy()

    # -------- FORCE SERIES (CRITICAL) --------
    close = df["Close"].squeeze()
    high = df["High"].squeeze()
    low = df["Low"].squeeze()
    volume = df["Volume"].squeeze()

    # -------- INDICATORS --------
    df["SMA50"] = close.rolling(50).mean()
    df["SMA200"] = close.rolling(200).mean()
    df["RSI"] = compute_rsi(close)
    df["ATR"] = compute_atr(high, low, close)
    df["ATR_pct"] = df["ATR"] / close
    df["Vol_Avg"] = volume.rolling(20).mean()

    # -------- BOOLEAN MASK (NO dropna EVER) --------
    valid = (
        df["SMA50"].notna() &
        df["SMA200"].notna() &
        df["RSI"].notna() &
        df["ATR_pct"].notna() &
        df["Vol_Avg"].notna()
    )

    df = df.loc[valid]

    if df.empty:
        return None

    latest = df.iloc[-1]

    # -------- SWING CONDITIONS --------
    trend = latest["Close"] > latest["SMA200"]
    institutional = latest["SMA50"] > latest["SMA200"]
    momentum_reset = 40 <= latest["RSI"] <= 65
    volume_confirm = latest["Volume"] > latest["Vol_Avg"]
    controlled_risk = latest["ATR_pct"] < 0.05

    swing_score = (
        25 * trend +
        25 * institutional +
        20 * momentum_reset +
        15 * volume_confirm +
        15 * controlled_risk
    )

    return {
        "Close": round(float(latest["Close"]), 2),
        "RSI": round(float(latest["RSI"]), 1),
        "SMA50": round(float(latest["SMA50"]), 2),
        "SMA200": round(float(latest["SMA200"]), 2),
        "ATR_pct": round(float(latest["ATR_pct"]) * 100, 2),
        "SwingScore": int(swing_score)
    }
