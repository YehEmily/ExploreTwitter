import tweepy
import json
import random
import time
import sys

def authenticate():
    f = open('secrets.json')
    data = json.load(f)
    f.close()

    consumer_key = data["api_key"]
    consumer_secret = data["api_secret_key"]
    access_token = data["bearer_token"]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth)
    return api

def get_followers(api, screen_name, count):
    followers = []
    for page in tweepy.Cursor(api.followers_ids, screen_name).pages():
        followers.extend(page)
        time.sleep(60)
    return followers

def get_retweets(api, tweet_id, count):
    retweets = []
    for page in tweepy.Cursor(api.retweeters, id=tweet_id, count=count).pages():
        retweets.extend(page)
        time.sleep(60)
    return retweets

def get_participants(followers, retweets):
    participants = []
    for retweet in retweets:
        participants.append(retweet)
        if retweet in followers:
            participants.append(retweet)
    return participants

def draw_winners(api, num_winners, participants):
    winners = []
    for i in range(num_winners):
        user = api.get_user(participants[random.randint(0, len(participants)-1)])
        winners.append(user.screen_name)
    return winners

if __name__ == "__main__":
    api = authenticate()
    if len(sys.argv) == 3:
        user = sys.argv[1]
        tweet = sys.argv[2]
        followers = get_followers(api, user, 500)
        retweets = get_retweets(api, tweet, 500)
        participants = get_participants(followers, retweets)
        winners = draw_winners(api, 3, participants)
        print("Congratulations!!", winners)
    else:
        print("Too few arguments for ", sys.argv[0], "<twitter username> <tweet ID>")
