import tweepy
from tweepy.auth import OAuthHandler
from .models import Tweet
from django.conf import settings

auth = OAuthHandler(settings.TWITTER_API_KEY, settings.TWITTER_API_KEY_SECRET)
auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)
trends_result = api.get_place_trends(23424848)[:5]

def user_tweets():
    user_tweets = api.home_timeline(count=50)
    return user_tweets

list_tag = ["bitcoin","btc","ethereum","eth","Binance","bnb","Cardano","ada","Litecoin","ltc","crypto","nft","Metaverse"]
def save_to_db():
    original_tweets = user_tweets()
    for tweets in original_tweets:
        if any(word in tweets.text for word in list_tag):
            if not Tweet.objects.filter(tweet_id=tweets.id):
                new_tweet = Tweet.objects.create(tweet_id = tweets.id, tweet_name = tweets.user.name, tweet_text = tweets.text, published_date = tweets.created_at)
                new_tweet.save()

