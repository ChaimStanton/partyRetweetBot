#! python3

from keysAuthentication import *

import tweepy
from time import sleep


def does_have_value(jsonObject, keyvalue):
    try:
        jsonObject[keyvalue]
        return True
    except KeyError:
        return False


class MyStreamListener(tweepy.StreamListener):
    """This is a class for the stream """
    def on_status(self, status):
        tweet = Tweet(status)
        try:
            tweet.retweet()
            print(status.text)
            print("pure retweet:", tweet.isPureRetweet)
            print("pure tweet: ", tweet.isPureTweet)
            print("quote retweet:", tweet.isQuoteRetweet)
            
        except tweepy.TweepError as error:
            print(error.reason)

    def on_error(self, status_code):
        print(status_code)
        return False


class Tweet():
    """ A class for all of the tweets to make life easier """
    def __init__(self, statusObj):
        self.id = statusObj.__dict__["_json"]["id"]
        self.isPureRetweet = does_have_value(statusObj._json, "retweeted_status")
        # a pure retweet is a retweet with no comment
        self.isQuoteRetweet = does_have_value(statusObj._json, "quoted_status")
        # a quoted tweet is one that has a comment AND a retweet 
        if self.isQuoteRetweet == False and self.isPureRetweet == False:
            self.isPureTweet = True 
        else:
            self.isPureTweet = False 
        # a pure tweet is a completley not retweeted tweet and original

    def retweet(self):
        api.retweet(self.id)


# "new" authenticaiotn
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

users = ["1268410636553371648"]

# creating and initializing the stream
myStreamListener = MyStreamListener()

myStream = tweepy.Stream(auth=auth, listener=myStreamListener)

# starting the stream
myStream.filter(follow=users)
