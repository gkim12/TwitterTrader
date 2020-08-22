import tweepy

class TwitterHandler:

    '''
    Creates new Twitter handler
    '''
    def __init__(self):
        consumer_key = 'ubovhm4kltShXATK5fU2ilwQP'
        consumer_secret = 'TCe3TCtqqt3NdMlFQYXGcVexeykwjfxOyCl7KFoLjOVBnDnCCh'
        access_token = '974409907242848256-qjfTgftQri1PxBBHZsH0VEMLXf9bnL7'
        access_token_secret = 'aPHPm6VFaQPSSI5ZXCyFf5SPjQifqm52MMBY64ZSx7SEb'
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)


    '''
    Get latest tweets from user via id
    twitter_handle: @realDonaldTrump => realDonaldTrump
    since: return tweets that occured after given tweet ID
    cnt: how many tweets to return
    keywords: list of words to look for in tweets

    returns: list of Status objects (latest tweet objects)
    '''
    def get_latest_tweets(self, twitter_handle, cnt=10, keywords=[]):
        tweets = self.api.user_timeline(screen_name=twitter_handle, count=cnt)
        temp = []
        filtered_tweets = []
        for tweet in tweets:
            if tweet.text[:2] != 'RT':
                filtered_tweets.append(tweet)
        if keywords:
            for tweet in filtered_tweets:
                if any(word in tweet.text for word in keywords):
                    temp.append(tweet)
            filtered_tweets = temp
        return filtered_tweets

#th = TwitterHandler()

#'''Get latest tweet ID (avoiding recurrence)'''
#latest_trump_tweet = th.api.user_timeline(screen_name='realDonaldTrump', count=1)
#latest_ID = latest_trump_tweet[0].id_str
#print(latest_ID)

#'''After some time, get Trump tweets that occured after latest tweet'''
#since_tweets = th.api.user_timeline(
 #   screen_name='realDonaldTrump', since_id=latest_ID)
#for tweet in since_tweets:
 #   print(tweet.text)

#tweets = th.get_latest_tweets('realDonaldTrump', 20)
#for tweet in tweets:
 #   print(tweet.text)
