from textblob import TextBlob

class TweetClient:
    def __init__(self):
        return

    def list_tweets(self, search_data):
        tweets = []
        for data in search_data['statuses']:
            tweets.append(data)
        text = [x['text'] for x in tweets]
        return text

    def analyze_tweets(self, clean_text):
        analysis = TextBlob(clean_text)
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
