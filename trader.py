import requests
import json
from order import Order

class Trader:
    
    api_url = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=%s&apikey=%s"
    
    ''' 
    Creates trader with initialized balance and blank portfolio 
    '''
    def __init__(self, balance):
        self.balance = balance
        self.portfolio = {}
        
    ''' 
    Adds funds to balance 
    '''
    def add_funds(self, amount):
        self.balance += amount
        
    ''' 
    Buys quantity of ticker stock with limit price
    Returns true if order successful, false otherwise 
    '''
    def buy(self, ticker, limit_price, quantity):
        total_cost = limit_price * quantity
        price = self.get_price(ticker)
        
        # Check balance
        if total_cost >= self.balance:
            return False

        # Validate price and make order
        if price <= limit_price:
            self.balance -= total_cost
            if ticker in self.portfolio:
                self.portfolio[ticker].buy(limit_price, quantity)
            else:
                self.portfolio[ticker] = Order(limit_price, quantity)
            return True
        return False

    ''' 
    Sells quantity of ticker stock with limit price
    Returns true if order successful, false otherwise 
    '''
    def sell(self, ticker, limit_price, quantity):
        total_gain = limit_price * quantity
        price = self.get_price(ticker)
        
        # Validate price and make order
        if price >= limit_price:
            self.balance += total_gain
            if ticker in self.portfolio:
                self.portfolio[ticker].sell(limit_price, quantity)
                return True
        return False
    
    ''' 
    Gets latest price of ticker 
    '''
    def get_price(self, ticker):
        ticker_url = (self.api_url % (ticker, 'RNQUH4LF70UBW4ZM'))
        return json.loads(requests.get(ticker_url).text)['Global Quote']['05. price']