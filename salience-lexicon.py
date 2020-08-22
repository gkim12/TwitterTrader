from trader import Trader
from tweets import TwitterHandler
import nltk
import math
import pprint
nltk.download('averaged_perceptron_tagger')
from nltk import tokenize
from collections import defaultdict

class SalienceLexicon:
    
    def __init__(self, num_tweets, handle):
        self.handler = TwitterHandler()
        self.tokenizer = tokenize.casual.TweetTokenizer(preserve_case=False)
        self.handle = handle
        self.idfs = {}
        self.tfs = {}
        self.pageCount = defaultdict(int)
        self.setup(num_tweets)

    def setup(self, num_tweets):
        init_tweets = self.handler.get_latest_tweets(self.handle, num_tweets)
        
        # Tokenize tweets and construct lexicon
        for tweet in init_tweets:
            self.term_freq(nltk.pos_tag(self.tokenizer.tokenize(tweet.text)), tweet.id)
        self.inverse_doc_freq(init_tweets, len(init_tweets))

    '''
    Returns dictionary containing tf of each word in given tweet (document) but also updates
    global tfs_... dictionary accordingly using (key, value) as (tweet id, tf dict)
    '''
    def term_freq(self, document, tweet_id):
        freqs = defaultdict(int)
        for term in document:
            freqs[term] += 1

        max_freq = max(freqs.values())
        tf = {}
        for word in freqs:
            tf[word] = 0.5 + 0.5 * freqs[word] / max_freq
            self.idfs[word] = 1
            self.pageCount[word] += 1

        self.tfs[tweet_id] = tf
        # technically useless
        return tf
    
    def inverse_doc_freq(self, documents, numPages):
        for tweet in documents:
            for word in nltk.pos_tag(self.tokenizer.tokenize(tweet.text)):
                self.idfs[word] = math.log(numPages / self.pageCount[word])         
    
    def tf_idf(self, document, tweet_id):
        tf_idf = {}
        for word in document:
            tf_idf[word] = self.tfs[tweet_id][word] * self.idfs[word]
        return tf_idf
        
p = SalienceLexicon(100, "@realDonaldTrump")

for i, tweet in enumerate(TwitterHandler().get_latest_tweets("@realDonaldTrump", cnt=100)):
    print(str(i) + tweet.text)
    print()
