import feedparser
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def news_sentiment(q):
    feed = feedparser.parse(f"https://news.google.com/rss/search?q={q}+India+stock")
    scores = [analyzer.polarity_scores(e.title)["compound"] for e in feed.entries[:30]]
    return sum(scores)/len(scores) if scores else 0
