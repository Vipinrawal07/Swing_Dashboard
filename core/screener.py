from core.indicators import SMA, RSI, ATR

def swing_screen(df, index_df):
    df["SMA50"] = SMA(df["Close"], 50)
    df["SMA200"] = SMA(df["Close"], 200)
    df["RSI"] = RSI(df["Close"])
    df["ATR"] = ATR(df)
    df["AvgVolume"] = df["Volume"].rolling(20).mean()

    df["StockRet"] = df["Close"].pct_change(30)
    df["IndexRet"] = index_df["Close"].pct_change(30)
    df["RS"] = df["StockRet"] - df["IndexRet"]

    df["Signal"] = (
        (df["Close"] > df["SMA200"]) &
        (df["SMA50"] > df["SMA200"]) &
        (df["RSI"].between(40, 55)) &
        (abs(df["Close"] - df["SMA50"]) / df["SMA50"] < 0.1) &
        (df["RS"] > 0.05)
    )
    return df
