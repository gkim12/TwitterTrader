from trader import Trader
from tweets import TwitterHandler
import nltk
import math
import pprint
nltk.download('averaged_perceptron_tagger')
from nltk import tokenize

'''
Follow approach detailed here:
http://www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/

To do:
- create naive bayes classifier of tweets
-- preprocess the data
--- match each tweet to time series data (did stock go up or down after tweet)
--- depending on up or down, add tweet to positive or negative tweet list
--- tokenize the tweets
--- remove insignificant words (<2 word-length)
--- convert all words to lowercase
--- merge pos/neg lists to singular list of tuples (list of text, pos/neg)
--- asdf
'''

class PolarityLexicon:
    
    def __init__(self):
        self.handler = TwitterHandler()
        self.tokenizer = tokenize.casual.TweetTokenizer(preserve_case=False)
        self.freq_dict = {}
    
    '''
    Splits tweets by words and tags with pos or neg. Adds all to list and returns
    '''
    def split_tweets(self, pos_tweets, neg_tweets):
        tweets = []
        for (tweet, sentiment) in pos_tweets + neg_tweets:
            filtered_words = [word.lower() for word in tweet.split() if len(word) >= 3]
            tweets.append((filtered_words, sentiment))
        return tweets

    '''
    Takes list of tagged individuals words and generates frequency dict of words in all tweets
    '''
    def get_word_features(self, tweets):
        freq_dict = {}
        for (tweet, _) in tweets:
            for word in tweet:
                if word not in freq_dict:
                    freq_dict[word] = 0
                freq_dict[word] += 1
        self.freq_dict = freq_dict
        return freq_dict
    
    def extract_features(self, document):
        doc_set = set(document)
        features = {}
        for word in self.freq_dict:
            features['contains(%s)' % word] = (word in doc_set)
        return features
    
# <------------------- SAMPLE FOR NOW ------------------->    
pos_tweets = [('I love this car', 'positive'),
              ('This view is amazing', 'positive'),
              ('I feel great this morning', 'positive'),
              ('I am so excited about the concert', 'positive'),
              ('He is my best friend', 'positive')]
neg_tweets = [('I do not like this car', 'negative'),
              ('This view is horrible', 'negative'),
              ('I feel tired this morning', 'negative'),
              ('I am not looking forward to the concert', 'negative'),
              ('He is my enemy', 'negative')]

# Create training data
p = PolarityLexicon()
tweets = p.split_tweets(pos_tweets, neg_tweets)
p.get_word_features(tweets)
training_data = []

for (tweet, sentiment) in tweets:
    training_data.append((p.extract_features(tweet), sentiment))

classifier = nltk.NaiveBayesClassifier.train(training_data)
pprint.pprint(classifier._feature_probdist)

