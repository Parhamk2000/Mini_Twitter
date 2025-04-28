from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["twitter_db"]

users_col = db["users"]
tweets_col = db["tweets"]


