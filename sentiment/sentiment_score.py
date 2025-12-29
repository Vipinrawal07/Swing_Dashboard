from config import SENTIMENT_WEIGHTS
from sentiment.twitter_sentiment import twitter_sentiment
from sentiment.reddit_sentiment import reddit_sentiment
from sentiment.news_sentiment import news_sentiment

def composite_sentiment(asset):
    t = twitter_sentiment(asset)
    r = reddit_sentiment(asset)
    n = news_sentiment(asset)
    score = (
        t*SENTIMENT_WEIGHTS["twitter"] +
        r*SENTIMENT_WEIGHTS["reddit"] +
        n*SENTIMENT_WEIGHTS["news"]
    )
    return round(score,3), t, r, n
