try:
    import snscrape.modules.twitter as sntwitter
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    analyzer = SentimentIntensityAnalyzer()
except:
    sntwitter = None

def twitter_sentiment(query):
    if not sntwitter:
        return 0  # fallback safely

    scores = []
    for i, tweet in enumerate(
        sntwitter.TwitterSearchScraper(query).get_items()
    ):
        if i >= 30:
            break
        scores.append(
            analyzer.polarity_scores(tweet.content)["compound"]
        )

    return sum(scores) / len(scores) if scores else 0
