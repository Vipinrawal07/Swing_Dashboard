def swing_screen(df, index_df=None):
    # Ensure required columns exist
    required_cols = ["Close", "Volume"]
    for col in required_cols:
        if col not in df.columns:
            return df

    # Technical indicators
    df["SMA50"] = df["Close"].rolling(50).mean()
    df["SMA200"] = df["Close"].rolling(200).mean()
    df["RSI"] = compute_rsi(df["Close"])

    # Drop rows where indicators are not ready
    df = df.dropna(subset=["SMA50", "SMA200", "RSI"])

    # Safety check
    if df.empty:
        return df

    # Swing conditions
    df["SwingSignal"] = (
        (df["Close"] > df["SMA200"]) &
        (df["SMA50"] > df["SMA200"]) &
        (df["RSI"] > 40) &
        (df["RSI"] < 70)
    )

    return df
