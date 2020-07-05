#! python3

from keysAuthentication import *

import requests
import urllib3

import tweepy
from time import sleep

# "new" authenticaiotn
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

users = ["1268410636553371648"]

def does_have_value(jsonObject, keyvalue):
    try:
        jsonObject[keyvalue]
        return True
    except KeyError:
        return False 

# --- USING THE STREAMING METHOD --- 
# class for the stream 
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        tweet = Tweet(status)
        try:
            tweet.retweet()
            print(status.text)
            print(tweet.isPureRetweet)
        except tweepy.TweepError as error:
            print(error.reason)

    def on_error(self, status_code):
        print(status_code)
        return False

class Tweet():
    """ A class for all of the tweets to make life easier """
    def __init__(self, statusObj):
        self.id = statusObj.__dict__["_json"]["id"]
        self.isPureRetweet = does_have_value(status._json, "retweeted_status") # a pure retweet is a retweet with no comment

    def retweet(self):
        api.retweet(self.id)

#creating and initialising the stream
myStreamListener = MyStreamListener()

myStream = tweepy.Stream(auth= auth, listener=myStreamListener)

# starting the stream
myStream.filter(follow=users)

