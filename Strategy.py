#!/usr/bin/python
import pandas as pd
import numpy as np
import time
import datetime
#import pprint
from PlotData import PlotData
from MakeTrade import MakeTrade
from OrderLog import OrderLog
from ReadJson import ReadJson
from GetBalance import GetBalance
class Strategy:
    def __init__(self, df, pair):
        self.df = df
        self.pair = pair
        bal = GetBalance()
        self.balance = bal.balance('USD')
    def output(self, graph):
        df = self.df
        pair = self.pair
        balance = self.balance
        dflength = len(df)
        buy_signals = self.buy_signals
        sell_signals = self.sell_signals
        # return all buys/ sells
        print datetime.datetime.now()
        print (" ---")
        for i in range(len(buy_signals)):
            try:
                print " | Buy:"
                print(" | " + str(buy_signals[i]))
                print " | Sell:"
                print(" | " + str(sell_signals[i]))
            except:
                print " | Waiting sell..."
        print " ---"
        print "Profit: " + str(balance)
        print "Close: " + str(df['close'][len(df['close'])-1])
        #remove when sending to raspberry pi or server
        if graph:
            graph = PlotData(df, pair, buy_signals = buy_signals, sell_signals = sell_signals)
            graph.graph()

    def live(self):
        df = self.df
        pair = self.pair
        dflength = len(df)
        self.buy_signals = []
        self.sell_signals = []
        #create a json reader object
        reader = ReadJson('logs/orders.json')
        pre_act = reader.last_action()
        pre_price = reader.last_price()
        print pre_price

        orders = OrderLog()
        #orders.record("btc", 'buy', '12/12/20', '8900')
        i = len(df['time'])-1
        #calculations to help make accurate predictions
        high = df['high'].max()
        low = df['low'].min()

        close_average = df['close'].sum()/dflength
        std_close = np.std(df['close'])

        obv_average = df['obv'].sum()/dflength
        std_obv = np.std(df['obv'])

        #actual strategy
        if  pre_act == 'sell':
            #mean deviation strategy
            if df['low'][i] < df['sma40'][i] - std_close*1.5 and df['rsi'][i] < 30:

                orders.record(pair, 'buy', str(df['time'][i]), str(df['close'][i]))
            #mommentum strategy
            elif df['obv'][i] < obv_average - std_obv and df['rsi'][i] < 25 and i > len(df['close']/3): #dont do momentum buy with no data

                orders.record(pair, 'buy', str(df['time'][i]), str(df['close'][i]))

        #check for sell points
        elif  pre_act == 'buy':
            #greater than 1.5% take profit
            if df['high'][i] > 1.02 * pre_price and df['rsi'][i] > 70:

                orders.record(pair, 'sell', str(df['time'][i]), str(df['close'][i]))

            #if greater than 1.5 standard deviation above sma40 line take profit
        elif df['high'][i] > df['sma40'][i] + std_close *1.5:

                orders.record(pair, 'sell', str(df['time'][i]), str(df['close'][i]))

            #stop loss at -1%
        elif df['low'][i] < pre_price*.99:

                orders.record(pair, 'sell', str(df['time'][i]), str(df['close'][i]))

        self.balance = 0

    def run(self):
        df = self.df
        pair = self.pair
        dflength = len(df)
        self.buy_signals = []
        self.sell_signals = []
        pre_act = 'sell'
        balance = 0

        #deal with time and get
        orders = OrderLog()
        #orders.record("btc", 'buy', '12/12/20', '8900')

        #calculations to help make accurate predictions
        high = df['high'].max()
        low = df['low'].min()

        close_average = df['close'].sum()/dflength
        std_close = np.std(df['close'])

        obv_average = df['obv'].sum()/dflength
        std_obv = np.std(df['obv'])

        #check for buy points on all data to test the strat

        for i in range(1, len(df['close'])):
            if  pre_act == 'sell':
                #mean deviation strategy
                if df['low'][i] < df['sma40'][i] - std_close*1 and df['rsi'][i] < 30:
                    self.buy_signals.append([df['time'][i], df['low'][i]])
                    balance = balance - df['low'][i]
                    pre_act = 'buy'


                #mommentum strategy
                elif df['obv'][i] < obv_average - std_obv and df['rsi'][i] < 25 and i > len(df['close']/3): #dont do momentum buy with no data
                        self.buy_signals.append([df['time'][i], df['low'][i]])
                        balance = balance - df['low'][i]
                        pre_act = 'buy'

        #check for sell points
            elif  pre_act == 'buy':
                #greater than 1.5% take profit
                if df['high'][i] > 1.01 * self.buy_signals[-1][1] and df['rsi'][i] > 70:
                    self.sell_signals.append([df['time'][i], df['high'][i]])
                    pre_act = 'sell'
                    balance = balance + df['high'][i]

                #if greater than 1 standard deviation above sma40 line take profit
                elif df['high'][i] > df['sma40'][i] + std_close *1:
                    self.sell_signals.append([df['time'][i], df['high'][i]])
                    pre_act = 'sell'
                    balance = balance + df['high'][i]

                #stop loss at -1%
            elif df['low'][i] < self.buy_signals[-1][1]*.99:
                        self.sell_signals.append([df['time'][i], df['high'][i]])
                        pre_act = 'sell'
                        balance = balance + df['close'][i]

        self.balance = balance
