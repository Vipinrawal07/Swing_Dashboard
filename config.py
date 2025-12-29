START_DATE = "2019-01-01"
INDEX_SYMBOL = "^NSEI"

SECTORS = {
    "IT": ["TCS", "INFY", "WIPRO"],
    "BANKING": ["HDFCBANK", "ICICIBANK", "SBIN"],
    "METALS": ["TATASTEEL", "HINDALCO", "HINDZINC"],
    "ENERGY": ["RELIANCE", "ONGC", "BPCL"],
    "PHARMA": ["SUNPHARMA", "DRREDDY", "CIPLA"]
}

ATR_MULT = 2
RR_RATIO = 2.5

SENTIMENT_WEIGHTS = {
    "twitter": 0.4,
    "reddit": 0.3,
    "news": 0.3
}
