import time

import pymongo
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream, API, Cursor, TweepError

from settings import MONGODB_CONNECTION, TWITTER_CREDENTIALS

connection = pymongo.MongoClient(MONGODB_CONNECTION)
database = connection.sarcasm_data

"""
These handle Twitter authetification and the connection to Twitter API.
Keys taken from settings which is not publically available within this project.
To get your owns please visit: https://apps.twitter.com
"""
auth = OAuthHandler(TWITTER_CREDENTIALS.get("consumer_key"),
                    TWITTER_CREDENTIALS.get("consumer_secret"))
auth.set_access_token(TWITTER_CREDENTIALS.get("access_token"),
                      TWITTER_CREDENTIALS.get("access_token_secret"))

class TwitterStreamListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status.text)

    def on_status(self, status):
        print(data)
        return True

def get_sarcasm_tweets_by_stream():
    listener = TwitterStreamListener()
    stream = Stream(auth, listener)

    stream.filter(track=["#sarcasm"])

def get_tweets_by_cursor(query):
    api = API(auth)
    query = query + " -RT"
    cursor = Cursor(api.search, q=query, lang="en").items(5000)
    while True:
        try:
            tweet = cursor.next()
            print(tweet._json)
            database.tweets.insert(tweet._json)
        except TweepError:
            time.sleep(60 * 15)
            continue
        except StopIteration:
            break

def get_tweets_for_feature_extraction(query, count):
    api = API(auth)
    query = query + " -RT"
    cursor = Cursor(api.search, q=query, lang="en").items(count)
    tweets = []
    while True:
        try:
            tweet = cursor.next()
            tweets.append(tweet._json)
        except TweepError as e:
            print(e)
            time.sleep(60 * 5)
            continue
        except StopIteration:
            break
    return tweets

if __name__ == "__main__":
    # to collect initial data
    get_tweets_by_cursor("#sarcasm")
    time.sleep(60 * 15)
    get_tweets_by_cursor("#")
