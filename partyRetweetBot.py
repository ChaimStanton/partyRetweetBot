#! python3

import tweepy
from time import sleep

from tinydb import TinyDB

import sys

import logging

filehandler = logging.FileHandler("db/logs/logs.log", mode="a")
streamhandler = logging.StreamHandler()

logging.basicConfig(format="%(levelname)s : %(msg)s : %(asctime)s : %(name)s ", 
                    level="NOTSET", handlers =(filehandler, streamhandler))
# : %(pathname)s : %(lineno)s was in format 


logging.info("\n \n Start of program")

keysString = sys.argv[1]
mpDBstr = sys.argv[2]


def does_have_value(jsonObject, keyvalue):
    """This is a generic function just to see if a json object exists used to determine if somehting is a retweet"""
    try:
        jsonObject[keyvalue]  # see if it exists
        if jsonObject[keyvalue] is None:
            return False
        return True
    except KeyError:
        return False


class MyStreamListener(tweepy.StreamListener):
    """This is a class for the stream """
    def on_status(self, status): # when a tweet is recived
        tweet = Tweet(status)
        try:
            if tweet.isComment or tweet.isPureRetweet:
                logging.info("NOT RETWEETED " + str(tweet))
                pass
            else:
                tweet.retweet()
                logging.info("RETWEETED " + str(tweet))

        except tweepy.TweepError as error:
            print(error.reason)

    def on_error(self, status_code):
        print(status_code)
        return False


class Tweet():
    """ A class for all of the tweets to make life easier """
    def __init__(self, statusObj):
        self.id = statusObj.__dict__["_json"]["id"]
        self.text = statusObj.text

        #TODO clarify tweet boolean catogories with better comments above 

        
        self.isPureRetweet = does_have_value(statusObj._json, "retweeted_status")
        # a pure retweet is a retweet with no comment

        self.isQuoteRetweet = does_have_value(statusObj._json, "quoted_status")
        # a quoted tweet is one that has a comment AND a retweet

        self.isComment = does_have_value(statusObj._json, "in_reply_to_status_id")

    def retweet(self):
        api.retweet(self.id)

    def __str__(self):
        return "text : " + self.text + " - isQuoteRetweet : " + str(self.isQuoteRetweet) + " - pure retweet : " + str(self.isPureRetweet) + " - comment tweet : " + str(self.isComment)


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
db = TinyDB(mpDBstr)  # get the database 

mps = []

for mp in db:  # iterates through the database and adds the idstring to a list
    mps.append(mp["id_str"])

try:
    for mp in mps:
        api.create_friendship(mp)  # follows each mp
except tweepy.error.TweepError:
    print("already followed")

# creating and initializing the stream
myStreamListener = MyStreamListener()

myStream = tweepy.Stream(auth=auth, listener=myStreamListener)

logging.info("starting stream")

try:
    myStream.filter(follow=mps)

except:
    logging.exception("Error with the stream")