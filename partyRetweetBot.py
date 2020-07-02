#! python3

from keysAuthentication import *

import tweepy
from time import sleep

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

since_id = 1273073579786211330

while True:
    print ("NEW WHILE")
    result = api.user_timeline(1268410636553371648, since_id=(since_id))
    for tweet in result:
        print("NEW FOR")
        print(tweet.text, tweet.id)
        # tweet.retweet()
    since_id = result.since_id
    sleep(5)