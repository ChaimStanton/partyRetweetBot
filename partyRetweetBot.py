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

"""
# Auth 1 authenticaton
try:
    redirect_url = auth.get_authorization_url()
except tweepy.TweepError:
    print('Error! Failed to get request token.')

print("go to this link", redirect_url)

verifier = int(input('Verifier:'))


s = requests.Session()
# s.set("a")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
token = s.get(redirect_url)
s.delete(redirect_url)
# auth.request_token = { 'oauth_token' : token,
#                          'oauth_token_secret' : verifier }

auth.request_token = {
      'oauth_token': s.get(token.url),
      'oauth_token_secret': verifier
}

# try:
auth.get_access_token(str(verifier))
print("yay")
# except tweepy.TweepError:
#     print('Error! Failed to get access token.')
"""

users = ["1268410636553371648"]

# --- USING THE STREAMING METHOD --- 
# class for the stream 
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        # status.retweet()
        try:
            api.retweet(status.__dict__["_json"]["id"])
            print(status.text)
            print(status._json["retweeted_status"])
        except tweepy.TweepError as error:
            print(error.reason)

    def on_error(self, status_code):
        print(status_code)
        return False

#creating and initialising the stream
myStreamListener = MyStreamListener()
# myStream = tweepy.Stream(auth= api.auth, listener=myStreamListener)

myStream = tweepy.Stream(auth= auth, listener=myStreamListener)


# starting the stream
myStream.filter(follow=users)

