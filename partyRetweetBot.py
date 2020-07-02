#! python3

from keysAuthentication import *

import tweepy
from time import sleep

# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)

# api = tweepy.API(auth)

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

api=tweepy.API(auth)


# since_id = 1273073579786211330
# since_id = 1

users = ["1268410636553371648"]

# --- USING THE STREAMING METHOD --- 
# class for the stream 
class MyStreamListner(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)
        status.retweet()

#creating and initialising the stream
myStreamListner = MyStreamListner()
myStream = tweepy.Stream(auth= auth, listener=myStreamListner)

# starting the stream
myStream.filter(follow=users)


# --- USING THE OLD FASHIONED METHOD ---
# # Below is using the old fashioned method
# with open("since_id.txt", "r") as txtFile:
#     since_id = int(txtFile.read())

# while True:
#     print ("NEW loop for program")
#     for user in users:
#         result = api.user_timeline(user, since_id=(since_id))
#         for tweet in result:
#             print("NEW for loop for the result")
#             print(tweet.text, tweet.id) # this prints it out for debugging purposes
#             # tweet.retweet()
#         if result.since_id == None: #bc if nothing gets tweeted then it returns none
#             pass 
#         else:
#             since_id = result.since_id
#             with open("since_id.txt", "w") as txtFile:
#                 txtFile.write(str(since_id))
#         sleep(5)