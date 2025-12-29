def swing_screen(df):
    if df is None or df.empty or len(df) < 220:
        return None

    df = df.copy()

    close = df["Close"].squeeze()
    high = df["High"].squeeze()
    low = df["Low"].squeeze()
    volume = df["Volume"].squeeze()

    df["SMA50"] = close.rolling(50).mean()
    df["SMA200"] = close.rolling(200).mean()
    df["RSI"] = compute_rsi(close)
    df["ATR"] = compute_atr(high, low, close)
    df["ATR_pct"] = df["ATR"] / close
    df["Vol_Avg"] = volume.rolling(20).mean()

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

    # --- Convert all to floats before any comparison ---
    try:
        close_val = float(latest["Close"])
        sma50_val = float(latest["SMA50"])
        sma200_val = float(latest["SMA200"])
        rsi_val = float(latest["RSI"])
        atr_pct_val = float(latest["ATR_pct"])
        vol_val = float(latest["Volume"])
        vol_avg_val = float(latest["Vol_Avg"])
    except:
        return None

    trend = close_val > sma200_val
    institutional = sma50_val > sma200_val
    momentum_reset = 40 <= rsi_val <= 65
    volume_confirm = vol_val > vol_avg_val
    controlled_risk = atr_pct_val < 0.05

    swing_score = (
        25 * trend +
        25 * institutional +
        20 * momentum_reset +
        15 * volume_confirm +
        15 * controlled_risk
    )

    return {
        "Close": round(close_val, 2),
        "RSI": round(rsi_val, 1),
        "SMA50": round(sma50_val, 2),
        "SMA200": round(sma200_val, 2),
        "ATR_pct": round(atr_pct_val * 100, 2),
        "SwingScore": int(swing_score)
    }
