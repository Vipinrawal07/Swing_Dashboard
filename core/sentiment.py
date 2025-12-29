import requests
import feedparser
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

# Reddit via Pushshift (free; limited but works)
def reddit_sentiment_score(ticker, size=50):
    """
    Fetch recent Reddit comments containing the ticker from Pushshift public API.
    Returns average compound sentiment score.
    """
    query = ticker.replace(".NS", "").upper()
    url = f"https://api.pushshift.io/reddit/comment/search/?q={query}&size={size}"
    try:
        res = requests.get(url, timeout=10).json()
        comments = [c.get("body", "") for c in res.get("data", [])]
    except Exception:
        comments = []

    if not comments:
        return 0.0

    scores = [analyzer.polarity_scores(c)["compound"] for c in comments]
    return sum(scores) / len(scores) if scores else 0.0


# Google News RSS sentiment
def news_sentiment_score(ticker, size=10):
    """
    Fetch recent news headlines via Google News RSS for the ticker keyword.
    Returns average sentiment score.
    """
    query = ticker.replace(".NS", "").upper()
    # Google News RSS search
    url = f"https://news.google.com/rss/search?q={query}%20stock"
    try:
        feed = feedparser.parse(url)
        entries = feed.entries[:size]
    except Exception:
        entries = []

    if not entries:
        return 0.0

    scores = []
    for entry in entries:
        text = entry.get("title", "") + " " + entry.get("summary", "")
        scores.append(analyzer.polarity_scores(text)["compound"])
    return sum(scores) / len(scores) if scores else 0.0


def composite_sentiment(ticker: str):
    """
    Returns:
      - combined sentiment score (-1 to +1)
      - label: "Bullish", "Neutral", "Bearish"
    """
    reddit_score = reddit_sentiment_score(ticker)
    news_score = news_sentiment_score(ticker)

    # Simple equal weighting of sources
    combined = (reddit_score + news_score) / 2

    # Label logic
    if combined >= 0.2:
        label = "Bullish"
    elif combined <= -0.2:
        label = "Bearish"
    else:
        label = "Neutral"

    return round(combined, 3), label
