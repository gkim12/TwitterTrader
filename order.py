class Order:
    
    ''' 
    Creates order with certain price and quantity (ticker defined in trader portfolio) 
    '''
    def __init__(self, price, quantity):
        self.price = price
        self.quantity = quantity
    
    ''' 
    Buys quantity for a price and adjusts average price and quantity 
    '''
    def buy(self, price, quantity):
        self.adjust(price, quantity)
        return self.price * quantity
    
    ''' 
    Sells quantity for a price and adjusts average price and quantity 
    '''
    def sell(self, price, quantity):
        self.adjust(price, -1 * quantity)
        return -1 * self.price * quantity
    
    ''' 
    Recalculates average price for ticker and updates quantity 
    '''
    def adjust(self, new_price, quantity):
        self.price = ((self.price * self.quantity) + (new_price * quantity)) / (self.quantity + quantity)
        self.quantity += quantity
        