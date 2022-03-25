import tweepy
from tweepy.auth import OAuthHandler
from .models import Tweet
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def user_tweets():
    auth = OAuthHandler("W2mDDh5w4BHZblR9tGiTOiHG0", "F9IPLi9VBWNTjDz2X6HVgQWVE4zQIdjTqEKOIsVuprj8VQB8WH")
    auth.set_access_token("1507008482481868820-zfm9W8VhFSbXzYtkgTKS8w0zOFfO4O", "3RXm3LJ0oS9E4yuqByvwNFAlEmisjNUe43fXfTialHyn6")
    api = tweepy.API(auth)
    # trends_result = api.trend_place(1225448)[:10]
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


