import feedparser
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def reddit_sentiment(q):
    feed = feedparser.parse(f"https://www.reddit.com/search.rss?q={q}")
    scores = [analyzer.polarity_scores(e.title)["compound"] for e in feed.entries[:30]]
    return sum(scores)/len(scores) if scores else 0
