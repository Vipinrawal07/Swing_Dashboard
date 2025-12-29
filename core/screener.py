import pandas as pd

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def swing_screen(df, index_df=None):
    if df is None or df.empty:
        return pd.DataFrame()

    if "Close" not in df.columns:
        return pd.DataFrame()

    # Indicators
    df = df.copy()
    df["SMA50"] = df["Close"].rolling(50).mean()
    df["SMA200"] = df["Close"].rolling(200).mean()
    df["RSI"] = compute_rsi(df["Close"])

    # Boolean mask (this auto-handles NaNs safely)
    mask = (
        (df["Close"] > df["SMA200"]) &
        (df["SMA50"] > df["SMA200"]) &
        (df["RSI"] > 40) &
        (df["RSI"] < 70)
    )

    df["SwingSignal"] = mask.fillna(False)

    return df
