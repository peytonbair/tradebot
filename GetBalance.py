#!/usr/bin/python
#class to get account balance
import krakenex

class GetBalance:
    def __init__(self):
        self.k = krakenex.API()
        self.k.load_key('key/kraken.key')
    # currnecy | buy/sell | market,limit,etc | price, for limit orders | volume, or amount of currency
    def balance(self, pair):
        data = self.k.query_private('Balance')
        balance = data['result']['Z'+pair] # Get the balance of a certain currency
        return balance
    def trades(self):
        data = self.k.query_private('TradesHistory')
        trades = data['result']
        return trades
    def OpenPositions(self):
        data = self.k.query_private('OpenPositions')
        positions = data['result']
        return positions
bal = GetBalance()

#print bal.balance('USD')
#print bal.trades()
#print bal.OpenPositions()
