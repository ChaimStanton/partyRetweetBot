#! python3

from tinydb import TinyDB, Query

db = TinyDB("db/libDemKEYS.json")

consumer_key = db.all()[0]["consumer_key"]
consumer_secret = db.all()[1]["consumer_secret"]
access_token = db.all()[2]["access_token"]
access_token_secret = db.all()[3]["access_token_secret"]
