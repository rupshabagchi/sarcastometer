import random

import pymongo

from settings import MONGODB_CONNECTION

connection = pymongo.MongoClient(MONGODB_CONNECTION)
database = connection.sarcasm_data

"""
This script is needed after data collected with tweets.py
Since we're first collecting sarsactic tweets then normal ones; they
are insert into db in that order.
This ensure that they have a property which can be used as they are
shuffled when we split collection as training, cv and test data.
"""

class_indicator = [i for i in range(10000)]
random.shuffle(class_indicator)

try:
    cursor = database.tweets.find()
    index = 0
    for doc in cursor:
        indicator = class_indicator[index]
        index = index + 1
        query = {"_id": doc["_id"]}
        update = {"$set": {"data_class_indicator": indicator }}
        database.tweets.update_one(query, update)
except Exception as e:
    print("Exception: ", type(e), e)
