import pandas as pd
import numpy as np

def SMA(series, n):
    return series.rolling(n).mean()

def RSI(series, n=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    rs = gain.rolling(n).mean() / loss.rolling(n).mean()
    return 100 - (100 / (1 + rs))

def ATR(df, n=14):
    tr = pd.concat([
        df["High"] - df["Low"],
        abs(df["High"] - df["Close"].shift()),
        abs(df["Low"] - df["Close"].shift())
    ], axis=1).max(axis=1)
    return tr.rolling(n).mean()
