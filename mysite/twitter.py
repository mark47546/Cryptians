from textwrap import indent
import tweepy
import time
from tweepy.auth import OAuthHandler
from tweepy.streaming import Stream
from .models import Tweet
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

twitter_keys = {
        'consumer_key':        'W2mDDh5w4BHZblR9tGiTOiHG0',
        'consumer_secret':     'F9IPLi9VBWNTjDz2X6HVgQWVE4zQIdjTqEKOIsVuprj8VQB8WH',
        'access_token_key':    '1507008482481868820-zfm9W8VhFSbXzYtkgTKS8w0zOFfO4O',
        'access_token_secret': '3RXm3LJ0oS9E4yuqByvwNFAlEmisjNUe43fXfTialHyn6'
    }

auth = OAuthHandler(twitter_keys['consumer_key'], twitter_keys['consumer_secret'])
auth.set_access_token(twitter_keys['access_token_key'], twitter_keys['access_token_secret'])
api = tweepy.API(auth, wait_on_rate_limit=True)
trends_result = api.get_place_trends(23424848)[:5]

def user_tweets():
    user_tweets = api.user_timeline(count=50)
    return user_tweets


def set_inactive(pk):
    Tweet.objects.filter(tweet_id = pk).update(is_active = False)

def set_active(pk):
    Tweet.objects.filter(tweet_id = pk).update(is_active = True)

class MyStreamListener(Stream):
    def on_status(self, status):
        # print(status.user.screen_name + "tweeted: " + status.text)
        tweets_name = status.user.screen_name
        status_text = status.text
        created_at = status.created_at 
        # print(created_at)
        return tweets_name, status_text, created_at

    def on_error(self, status_code):
        if status_code == 420:
            return False  

def stream_tweets():
    runtime = 10
    myStreamListener = MyStreamListener(twitter_keys['consumer_key'], 
                                        twitter_keys['consumer_secret'],
                                        twitter_keys['access_token_key'], 
                                        twitter_keys['access_token_secret'])
    myStreamListener.filter(track = ['Bitcoin'], languages=["en"])
    time.sleep(runtime)
    myStreamListener.disconnect()
    # print(myStreamListener.created_at)
    # return myStreamListener.tweets_name, myStreamListener.status_text, myStreamListener.created_at

def save_to_db():
    original_tweets = user_tweets()
    for original_tweet in original_tweets:
        if not original_tweet.retweeted:
            if not Tweet.objects.filter(tweet_id=original_tweet.id):
                new_tweet = Tweet(tweet_id = original_tweet.id, tweet_text = original_tweet.text, published_date = original_tweet.created_at, is_active = True)
                new_tweet.save()
    stream_tweets_list = stream_tweets()
    # for stream_tweet_lists in stream_tweets_list:
    #     new_data = Tweet(tweets_name = stream_tweet_lists.status.user.screen_name, status_text = stream_tweet_lists.status.text, created_at = stream_tweet_lists.status.created_at)
    #     new_data.save()

