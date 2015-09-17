import os

from pymongo import MongoClient


mongo_uri = os.environ['MONGOHQ_URL']
mongo_database_str = mongo_uri.split('/')[-1]
client = MongoClient(mongo_uri)
db = client[mongo_database_str]
users_collection = db['users']


def authorize(email):
    user_found = users_collection.find_one({'email': email})
    if not user_found:
        return False
    elif user_found['email'] != email:
        return False
    return True

