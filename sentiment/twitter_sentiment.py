import snscrape.modules.twitter as sntwitter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def twitter_sentiment(q):
    scores = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(q).get_items()):
        if i > 50: break
        scores.append(analyzer.polarity_scores(tweet.content)["compound"])
    return sum(scores)/len(scores) if scores else 0
