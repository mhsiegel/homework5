from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data # file that contains OAuth credentials
import nltk

## SI 206 - HW
## COMMENT WITH:
## Your section day/time: 002/2 pm
## Any names of people you worked with on this assignment: Tori Engler, Michelle Phillips

#usage should be python3 hw5_twitter.py <username> <num_tweets>
username = sys.argv[1]
num_tweets = sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)
#Code for OAuth ends

CACHE_FNAME = 'twitter_cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}
data = open(CACHE_FNAME, 'w')

def get_tweets(username, num_tweets):
    user_url = 'https://api.twitter.com/1.1/search/tweets.json?q={}&count={}'.format(username, num_tweets)
    if user_url in CACHE_DICTION:
        print('checking cache...')
        json_data = CACHE_DICTION[user_url]
    else:
        print('fetching data...')
        request = requests.get(user_url, auth = auth)
        json_data = json.loads(request.text)
        write_file = open('tweet.json', 'w')
        write_file.write(json.dumps(json_data, indent = 4))
        write_file.close()
        write_file = open(CACHE_FNAME, 'w')
        CACHE_DICTION[user_url] = json_data
        write_file.write(json.dumps(CACHE_DICTION))
        write_file.close()
    tweets = ''
    for x in json_data['statuses']:
        tweets += x['text']
    tokens = nltk.word_tokenize(tweets)
    freqDist = nltk.FreqDist(token for token in tokens if token.isalpha() and "https" not in token and 'http' not in token and 'RT' not in token)
    for word, frequency in freqDist.most_common(5):
        print(word + " " + str(frequency))
    return CACHE_DICTION[user_url]
get_tweets(username, num_tweets)

if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()
