import tweepy
from tweepy.auth import OAuthHandler
from .models import Tweet

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
    user_tweets = api.home_timeline(count=50)
    return user_tweets

list_tag = ["bitcoin","btc","ethereum","eth","Binance","bnb","Cardano","ada","Litecoin","ltc","crypto","nft","Metaverse"]
def save_to_db():
    original_tweets = user_tweets()
    for tweets in original_tweets:
        if any(word in tweets.text for word in list_tag):
            if not Tweet.objects.filter(tweet_id=tweets.id):
                new_tweet = Tweet.objects.create(tweet_id = tweets.id, tweets_name = tweets.user.name, tweet_text = tweets.text, published_date = tweets.created_at)
                new_tweet.save()

