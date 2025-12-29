import feedparser
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def get_sentiment_label(score):
    if score >= 0.4:
        return "Bullish"
    elif score <= -0.4:
        return "Bearish"
    else:
        return "Neutral"


def composite_sentiment(stock_name):
    feeds = [
        f"https://news.google.com/rss/search?q={stock_name}+stock",
        f"https://www.reddit.com/search.rss?q={stock_name}"
    ]

    scores = []

    for url in feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries[:10]:
            text = entry.get("title", "") + " " + entry.get("summary", "")
            scores.append(analyzer.polarity_scores(text)["compound"])

    if not scores:
        return 0.0, "Neutral"

    avg = sum(scores) / len(scores)
    return round(avg, 2), get_sentiment_label(avg)
