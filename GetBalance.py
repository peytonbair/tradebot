#class to get account balance
import krakenex

class GetBalance:
    def __init__(self):
        pass
    # currnecy | buy/sell | market,limit,etc | price, for limit orders | volume, or amount of currency
    def get(self):
        k = krakenex.API()
        k.load_key('key/kraken.key')

        print k.query_private('TradesHistory')

bal = GetBalance()
bal.get()
