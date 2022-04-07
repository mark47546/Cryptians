from textwrap import indent
import tweepy
import time
from tweepy.auth import OAuthHandler
from tweepy.streaming import Stream
from .models import Tweet
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

auth = OAuthHandler("W2mDDh5w4BHZblR9tGiTOiHG0", "F9IPLi9VBWNTjDz2X6HVgQWVE4zQIdjTqEKOIsVuprj8VQB8WH")
auth.set_access_token("1507008482481868820-zfm9W8VhFSbXzYtkgTKS8w0zOFfO4O", "3RXm3LJ0oS9E4yuqByvwNFAlEmisjNUe43fXfTialHyn6")
api = tweepy.API(auth, wait_on_rate_limit=True)
trends_result = api.get_place_trends(23424848)[:5]


def user_tweets():
    user_tweets = api.user_timeline(count=50)
    return user_tweets

def save_to_db():
    original_tweets = user_tweets()
    for original_tweet in original_tweets:
        if not original_tweet.retweeted:
            if not Tweet.objects.filter(tweet_id=original_tweet.id):
                new_tweet = Tweet(tweet_id = original_tweet.id, tweet_text = original_tweet.text, published_date = original_tweet.created_at, is_active = True)
                new_tweet.save()

def set_inactive(pk):
    Tweet.objects.filter(tweet_id = pk).update(is_active = False)

def set_active(pk):
    Tweet.objects.filter(tweet_id = pk).update(is_active = True)

class MyStreamListener(Stream):
    def on_status(self, status):
        print(status.user.screen_name + "tweeted: " + status.text)
        tweets_name = status.user.screen_name
        status_text = status.text
        created_at = status.created_at 
        return tweets_name, status_text, created_at

    def on_error(self, status_code):
        if status_code == 420:
            return False  

def stream_tweets():
    runtime = 10
    myStreamListener = MyStreamListener("W2mDDh5w4BHZblR9tGiTOiHG0", 
                                        "F9IPLi9VBWNTjDz2X6HVgQWVE4zQIdjTqEKOIsVuprj8VQB8WH",
                                        "1507008482481868820-zfm9W8VhFSbXzYtkgTKS8w0zOFfO4O", 
                                        "3RXm3LJ0oS9E4yuqByvwNFAlEmisjNUe43fXfTialHyn6")
    myStreamListener.filter(track = ['Bitcoin'], languages=["en"]).order_by('created_at')[:10]
    time.sleep(runtime)
    myStreamListener.disconnect()
    # return MyStreamListener.tweets_name, MyStreamListener.status_text

# 

