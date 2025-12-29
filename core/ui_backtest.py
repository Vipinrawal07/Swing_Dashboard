def run_backtest(df, hold=60):
    trades = []

    for i in range(200, len(df)):
        if df["Signal"].iloc[i]:
            entry = df["Close"].iloc[i]
            stop = entry - 2 * df["ATR"].iloc[i]
            target = entry + (entry - stop) * 2.5

            for j in range(i+1, min(i+hold, len(df))):
                if df["Low"].iloc[j] <= stop:
                    trades.append(-1)
                    break
                if df["High"].iloc[j] >= target:
                    trades.append(1)
                    break

    if not trades:
        return {"Trades": 0}

    wins = trades.count(1)
    return {
        "Trades": len(trades),
        "Win Rate %": round(wins / len(trades) * 100, 1),
        "Expectancy": round((wins*2.5 - (len(trades)-wins)) / len(trades), 2)
    }
