#! python3

from keysAuthentication import *

import tweepy

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.text)

result = api.user_timeline(1268410636553371648, since_id=(1273063704528072707))
for tweet in result:
    print("NEW LOOOP")
    print(tweet.text, tweet.id)
    tweet.retweet()
print(result.since_id)