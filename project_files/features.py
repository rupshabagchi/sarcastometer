import nltk
from textblob import TextBlob

from preprocessor import preprocess
from sentiment import LoadSentiWordNet
from tweets import get_tweets_for_feature_extraction


sentiment_helper = LoadSentiWordNet()


def get_topic_sentiment_nltk(topic_keywords):
    topic_max_distance = [0]
    topic_min_distance = [0]
    topic_sarcastic = False

    for topic_keyword in topic_keywords:
        tweets = get_tweets_for_feature_extraction(topic_keyword, 3)

        tweets_positive = [0]
        tweets_negative = [0]
        tweets_sarcastic = False
        for tweet in tweets:
            processed_tweet = preprocess(tweet["text"])
            processed_text = processed_tweet["text"]

            tokens = nltk.word_tokenize(processed_text)
            tokens = [(t.lower()) for t in tokens]

            mean_sentiment = sentiment_helper.score_sentence(tokens)
            positive_sentence_sentiment = mean_sentiment[0]
            negative_sentence_sentiment = mean_sentiment[1]

            tweets_positive.append(positive_sentence_sentiment)
            tweets_negative.append(negative_sentence_sentiment)
            tweets_sarcastic = ("#sarcasm" in processed_tweet["hashtags"]) or tweets_sarcastic

        topic_max_distance.append(max(tweets_positive) - min(tweets_positive))
        topic_min_distance.append(max(tweets_negative) - min(tweets_negative))
        topic_sarcastic = topic_sarcastic or tweets_sarcastic

    return sum(topic_max_distance) / (len(topic_keywords) or 1), sum(topic_min_distance) / (len(topic_keywords) or 1), int(topic_sarcastic)


def get_features_from_text_blob(tweet):

    # is tweet sarcastic
    is_sarcastic = int("#sarcasm" in tweet["text"])

    # preprocess tweet content
    processed_tweet = preprocess(tweet["text"])
    processed_text = processed_tweet["text"]

    blob_text = TextBlob(processed_text)

    # measure sentiment features of tweet
    sentence_polarity = blob_text.sentiment.polarity
    sentence_subjectivity = blob_text.sentiment.subjectivity

    # calculate word based polarity to capture extreme expressions
    polarities = []
    for word in processed_text.split(" "):
        blob_word = TextBlob(word)
        polarities.append(blob_word.sentiment.polarity)

    maximum_word_polarity = max(polarities)
    minimum_word_polarity = min(polarities)

    # measure how extreme the most expressive is with respect to whole sentence
    polarity_distance_max = maximum_word_polarity - sentence_polarity
    polarity_distance_min = abs(minimum_word_polarity - sentence_polarity)

    # extract topic based sentiment values; combined polarity, subjectivity and any sarcasm clue
    topic_keywords = blob_text.noun_phrases + processed_tweet["hashtags"] + processed_tweet["mentions"]
    topic_polarity, topic_subjectivity, topic_sarcasm = get_topic_sentiment(topic_keywords)

    return ["{0:.2f}".format(sentence_polarity),
            "{0:.2f}".format(sentence_subjectivity),
            "{0:.2f}".format(maximum_word_polarity),
            "{0:.2f}".format(polarity_distance_max),
            "{0:.2f}".format(polarity_distance_min),
            "{0:.2f}".format(topic_polarity),
            "{0:.2f}".format(topic_subjectivity),
            topic_sarcasm,
            is_sarcastic]


def get_features_from_nltk(tweet):

    # is tweet sarcastic
    is_sarcastic = int("#sarcasm" in tweet["text"])

    processed_tweet = preprocess(tweet["text"])
    processed_text = processed_tweet["text"]

    tokens = nltk.word_tokenize(processed_text)
    tokens = [(t.lower()) for t in tokens]

    mean_sentiment = sentiment_helper.score_sentence(tokens)
    positive_sentence_sentiment = mean_sentiment[0]
    negative_sentence_sentiment = mean_sentiment[1]
    sentence_sentiment = mean_sentiment[0] - mean_sentiment[1]

    word_sentiments = []
    for word in processed_text.split(" "):
        if len(word) > 0:
            word_sentiment = sentiment_helper.score_word(word.lower())
            word_sentiments.append(word_sentiment)

    maximum_word_polarity = max([x[0] for x in word_sentiments])
    minimum_word_polarity = max([x[1] for x in word_sentiments])

    polarity_distance_max = maximum_word_polarity - sentence_sentiment
    polarity_distance_min = abs(minimum_word_polarity - sentence_sentiment)

    blob_text = TextBlob(processed_text)
    topic_keywords = blob_text.noun_phrases + processed_tweet["hashtags"] + processed_tweet["mentions"]
    topic_positive, topic_negative, topic_sarcasm = get_topic_sentiment_nltk(topic_keywords)

    return ["{0:.2f}".format(positive_sentence_sentiment),
            "{0:.2f}".format(negative_sentence_sentiment),
            "{0:.2f}".format(sentence_sentiment),
            "{0:.2f}".format(maximum_word_polarity),
            "{0:.2f}".format(minimum_word_polarity),
            "{0:.2f}".format(polarity_distance_max),
            "{0:.2f}".format(polarity_distance_min),
            "{0:.2f}".format(topic_positive),
            "{0:.2f}".format(topic_negative),
            topic_sarcasm,
            is_sarcastic]
