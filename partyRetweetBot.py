#! usr/bin/python3

import tweepy
from time import sleep

from tinydb import TinyDB

import sys

keysString = sys.argv[1]
mpDBstr = sys.argv[2]

def does_have_value(jsonObject, keyvalue):
    """This is a generic function just to see if a json object exists used to determine if somehting is a retweet"""
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
            print("quote retweet:      ", tweet.isQuoteRetweet) # a retweet with a comment
            print("pure retweet:       ", tweet.isPureRetweet) # i.e. a pure retweet with no comment
            print("comment tweet:      ", tweet.isComment) # a retweet that is a retweet of a comment
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


# getting authentication from database
# keysString = "db/libDemKEYS.json"
db = TinyDB(keysString)

consumer_key = db.all()[0]["consumer_key"]
consumer_secret = db.all()[1]["consumer_secret"]
access_token = db.all()[2]["access_token"]
access_token_secret = db.all()[3]["access_token_secret"]


# "new" authenticaiotn
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# mpDBstr = "db/libDem.json"
db = TinyDB(mpDBstr) # get the database 

mps = []

for mp in db: # iterates through the database and adds the idstring to a list
   mps.append(mp["id_str"])

for mp in mps: 
    api.create_friendship(mp) # follows each mp

# creating and initializing the stream
myStreamListener = MyStreamListener()

myStream = tweepy.Stream(auth=auth, listener=myStreamListener)

# starting the stream
myStream.filter(follow=mps)
