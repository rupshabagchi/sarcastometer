import csv

import pymongo

from features import get_features_from_nltk
from settings import MONGODB_CONNECTION

connection = pymongo.MongoClient(MONGODB_CONNECTION)
database = connection.sarcasm_data

with open('tweet_features_nltk.csv', 'w', newline='') as csvfile:
    for x in range(10000):
        print(x)
        tweet = database.tweets.find_one({"data_class_indicator": x})
        feature_list = get_features_from_nltk(tweet)
        tweetwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        tweetwriter.writerow(feature_list)
