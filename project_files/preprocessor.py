import re

def preprocess(tweet_text):
    """
    This functions cleans all the tweets.
    It first extracts all the #hashtags and @mentions,
    then make sure the tweets does not contain http links,
    also removes punctuations
    """

    remove_hashtags = re.compile(r'\w*#\w*')
    remove_mentions = re.compile(r'\w*@\w*')
    remove_links = re.compile(r'http[^\s]+')
    remove_special_chars = re.compile(r'[\x21-\x2f\x3a-\x40\x5b-\x60\x7b-\x7e]')

    if len(tweet_text) > 1:
        hashtags = re.findall(r'\B#\w+', tweet_text)
        mentions = re.findall(r'\B@\w+', tweet_text)

        tweet = remove_hashtags.sub('', tweet_text)
        tweet = remove_mentions.sub('', tweet)
        tweet = remove_links.sub('', tweet)
        tweet = remove_special_chars.sub('', tweet)

        if "#sarcasm" in hashtags:
            hashtags.remove("#sarcasm")

        return {
            "text": tweet.strip(),
            "hashtags": hashtags,
            "mentions": mentions
        }
