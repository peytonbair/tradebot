#!/usr/bin/python
#class to make orders to kraken
import krakenex

class MakeTrade:
    def __init__(self):
        pass
    # currnecy | buy/sell | market,limit,etc | price, for limit orders | volume, or amount of currency
    def order(self, pair, type, ordertype, volume):
        k = krakenex.API()
        k.load_key('key/kraken.key')

        k.query_private('AddOrder', {'pair': pair,
                                     'type': type,
                                     'ordertype': ordertype,
                                     'volume': volume})
        return 'done'
order = MakeTrade()
#order.order('XETHZUSD', 'buy', 'market', .5)
