#! python3

from keysAuthentication import *

import tweepy
from time import sleep


def does_have_value(jsonObject, keyvalue):
    try:
        jsonObject[keyvalue] # see if it exists
        if jsonObject[keyvalue] == None:
            return False 
        return True
    except KeyError:
        return False


class MyStreamListener(tweepy.StreamListener):
    """This is a class for the stream """
    def on_status(self, status):
        print("\nNEW TWEET")
        tweet = Tweet(status)
        try:
            if tweet.isComment == True or tweet.isPureRetweet == True:
                print("NOT RETWETED ")
            else:
                tweet.retweet()
                print("THIS WAS RETWEETED")
            
            print("text                ", status.text)
            print("quote retweet:      ", tweet.isQuoteRetweet)
            print("pure retweet:       ", tweet.isPureRetweet)
            print("comment tweet:      ", tweet.isComment)
            print()

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
        self.isComment = does_have_value(statusObj._json, "in_reply_to_status_id")

    def retweet(self):
        api.retweet(self.id)


# "new" authenticaiotn
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

users = ["1268410636553371648", "1279585853942239243"]

for user in users:
    api.create_friendship(user)

# creating and initializing the stream
myStreamListener = MyStreamListener()

myStream = tweepy.Stream(auth=auth, listener=myStreamListener)

# starting the stream
myStream.filter(follow=users)
