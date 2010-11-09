#coding: utf-8
from google.appengine.ext import db
from random import choice
from time import sleep
import tweepy
from flask import Flask
app = Flask(__name__)

JAZZOUT_CONSUMER_KEY = "XXXX"
JAZZOUT_CONSUMER_KEY_SECRET = "XXXX"
JAZZOUT_ACCESS_TOKEN = "XXXX"
JAZZOUT_ACCESS_TOKEN_SECRET = "XXXX"
MY_CONSUMER_KEY = "XXXX"
MY_CONSUMER_KEY_SECRET = "XXXX"
MY_ACCESS_TOKEN = "XXXX"
MY_ACCESS_TOKEN_SECRET = "XXXX"

class CachedData(db.Model):
    """ cached last retweet id
    """
    id = db.IntegerProperty()

@app.route('/post_tweet')
def post_tweet():
    auth = tweepy.OAuthHandler(JAZZOUT_CONSUMER_KEY, JAZZOUT_CONSUMER_KEY_SECRET)
    auth.set_access_token(JAZZOUT_ACCESS_TOKEN, JAZZOUT_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    api.update_status("test")
    return "success post."

def retweet_jazzout(id):
    auth = tweepy.OAuthHandler(JAZZOUT_CONSUMER_KEY, JAZZOUT_CONSUMER_KEY_SECRET)
    auth.set_access_token(JAZZOUT_ACCESS_TOKEN, JAZZOUT_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    try:
        api.retweet(id)
    except tweepy.TweepError:
        pass
    return "success retweet"

@app.route('/search_jazzout')
def search_jazzout():
    auth = tweepy.OAuthHandler(JAZZOUT_CONSUMER_KEY, JAZZOUT_CONSUMER_KEY_SECRET)
    auth.set_access_token(JAZZOUT_ACCESS_TOKEN, JAZZOUT_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    cached_datas = CachedData.all().order('-id').fetch(1)
    if cached_datas:
        cached_data = cached_datas[0]
        #print "cached"
        try:
            search_results = api.search('#jazzout',since_id=cached_data.id)
        except tweepy.TweepError:
            return "search failed"
    else:
        cached_data = CachedData()
        #print "new search"
        try:
            search_results = api.search('#jazzout')
        except tweepy.TweepError:
            return "search failed"
    search_results.reverse()
    #print "--------"
    for tweet in search_results:
        #print "id: %s" % tweet.id
        #print "from_user: %s" % tweet.from_user
        #print "from_user_id: %s" % tweet.from_user_id
        #print "to_user_id: %s" % tweet.to_user_id
        #print tweet.text.encode('utf-8', 'ignore')
        print "retweet %d" % tweet.id
        if not tweet.from_user_id == 136926909:
            retweet_jazzout(tweet.id)
        cached_data.id = tweet.id
        sleep(1)
    cached_data.put()
    return "success search."

@app.route('/yoruho')
def yoruho():
    post = choice(("よるほー", "よるほっ", "もうこんな時間。よるほー", "よるほタイム"))
    auth = tweepy.OAuthHandler(MY_CONSUMER_KEY, MY_CONSUMER_KEY_SECRET)
    auth.set_access_token(MY_ACCESS_TOKEN, MY_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    api.update_status(post)
    return "yoruho success"

if __name__ == '__main__':
    app.run()
