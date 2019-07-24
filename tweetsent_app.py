import base64
import requests
import re
import os
from dotenv import load_dotenv
from tweet_client import TweetClient


def clean_tweets(text):
    return ' '.join(re.sub(r"[^a-z0-9]", " ", text.lower()).split(" "))


if __name__ == "__main__":
    keyword = input("Enter keyword(s): ")
    language = 'en'
    return_type = 'recent'

    load_dotenv()
    client_key = os.getenv("KEY")
    client_secret = os.getenv("SECRET_KEY")
    key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')
    b64_encoded_key = base64.b64encode(key_secret)
    b64_encoded_key = b64_encoded_key.decode('ascii')

    base_url = 'https://api.twitter.com/'
    auth_url = '{}oauth2/token'.format(base_url)

    auth_headers = {'Authorization': 'Basic {}'.format(b64_encoded_key),
                    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}

    auth_data = {'grant_type': 'client_credentials'}

    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)

    access_token = auth_resp.json()['access_token']

    search_headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }

    search_params = {
        'q': '{}-filter:retweets'.format(keyword),
        'lang': language,
        'return-type': return_type,
        'count': 100  # default value is 100
    }

    search_url = '{}1.1/search/tweets.json'.format(base_url)

    search_resp = requests.get(search_url, headers=search_headers, params=search_params)
    search_data = search_resp.json()

    tweet_client = TweetClient()

    tweet_list = tweet_client.list_tweets(search_data)

    clean_text = [clean_tweets(tweet) for tweet in tweet_list]

    sentiment = [tweet_client.analyze_tweets(clean_tweet) for clean_tweet in clean_text]

    print("Sentiment analysis on '{}' based on {} tweets".format(keyword, return_type))
    postweets = [s for s in sentiment if s == 'positive']
    print("Positive: {} %".format(100 * len(postweets) / len(sentiment)))
    negtweets = [s for s in sentiment if s == 'negative']
    print("Negative: {} %".format(100 * len(negtweets) / len(sentiment)))
    print("Neutral: {} %".format(100 * (len(sentiment) - len(negtweets) - len(postweets)) / len(sentiment)))
