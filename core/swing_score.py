def normalize(v, lo, hi):
    return max(0, min(1, (v - lo) / (hi - lo)))

def swing_score(row, sentiment):
    score = 0

    score += 25 if row["SMA50"] > row["SMA200"] else 0
    score += normalize(row["RS"], 0, 0.15) * 25

    pullback = abs(row["Close"] - row["SMA50"]) / row["SMA50"]
    score += normalize(0.12 - pullback, 0, 0.12) * 20

    score += 15 if row["Volume"] < row["AvgVolume"] else 0
    score += normalize(sentiment, -0.2, 0.4) * 15

    return round(score, 1)
