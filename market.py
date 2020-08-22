from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import numpy as np
import statistics
import json
from pprint import pprint
import datetime
import pytz
from tweets import TwitterHandler

class MarketTracker:

	def __init__(self):
		# Your key here
		key = 'XNEKGC3CKSICNHK3'
		ts = TimeSeries(key)
		data, meta = ts.get_intraday(symbol='SPY',interval='60min', outputsize='full')
		self.averages = {}
		self.deltas = {}
		for time in data:
			self.averages[time] = (float(data[time]['1. open']) + float(data[time]['4. close'])) / 2
			self.deltas[time] = float(data[time]['4. close']) - float(data[time]['1. open'])
			print(self.deltas[time])

		self.normalized_deltas = {}
		mean = sum(list(self.deltas.values())) / len(list(self.deltas.values()))
		std = statistics.stdev(list(self.deltas.values()))
		for time in self.deltas:
			self.normalized_deltas[time] = (self.deltas[time] - mean)/(10*std)
			print(time + '  ' + str(self.normalized_deltas[time]) + '  ' + str(self.deltas[time]))
		print(std)
		self.month_to_str = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}

	def assign_tweets(self):
		positive_tweets = {}
		negative_tweets = {}

		tweets = TwitterHandler().get_latest_tweets("@realDonaldTrump", cnt=10)
		for tweet in tweets:
			tweetTime = tweet.created_at
			#tokens = tweetTime.split(' ')

			#changedTime = datetime.datetime(int(tokens[5]), self.month_to_str[tokens[1]], int(tokens[2], int(tokens[3][:2]), int(tokens[3][3:5]), tzinfo=pytz.timezone('US/Eastern')))
			print(tweetTime)

			




tracker = MarketTracker()
tracker.assign_tweets()