#!/usr/bin/python
import pandas as pd
import numpy as np
#import pprint
from PlotData import PlotData
from MakeTrade import MakeTrade
from OrderLog import OrderLog
class Strategy:
    def __init__(self, df, pair):
        self.df = df
        self.pair = pair

    def run(self):
        df = self.df
        pair = self.pair
        dflength = len(df)
        buy_signals = []
        sell_signals = []
        pre_act = 'sell'
        balance = 0
        #deal with time and get
        orders = OrderLog()

        #calculations to help make accurate predictions
        high = df['high'].max()
        low = df['low'].min()

        close_average = df['close'].sum()/dflength
        std_close = np.std(df['close'])

        obv_average = df['obv'].sum()/dflength
        std_obv = np.std(df['obv'])

        #check for buy points
        for i in range(1, len(df['close'])):
            #calculate hull slope
            try:
                hull_slope = df['hma20'][i] - df['hma20'][i-1]
            except:
                hull_slope = 0
            if  pre_act == 'sell':
                #mean deviation strategy
                if df['low'][i] < df['sma40'][i] - std_close*1 and df['rsi'][i] < 30:
                    buy_signals.append([df['time'][i], df['low'][i]])
                    balance = balance - df['low'][i]
                    pre_act = 'buy'
                    if(i == len(df['close']) -1):
                        orders.record(pair,'Buy',str(df['time'][i]), df['close'][i]) #record a buy
                #mommentum strategy
                elif df['obv'][i] < obv_average - std_obv and df['rsi'][i] < 25 and i > len(df['close']/2): #dont do momentum buy with no data
                        buy_signals.append([df['time'][i], df['low'][i]])
                        balance = balance - df['low'][i]
                        pre_act = 'buy'
                        if(i == len(df['close']) -1):
                            orders.record(pair,'Buy',str(df['time'][i]), df['close'][i]) #record a buy

        #check for sell points
            elif  pre_act == 'buy':
                #greater than 1.5% take profit
                if df['high'][i] > 1.01 * buy_signals[-1][1] and df['rsi'][i] > 70:
                    sell_signals.append([df['time'][i], df['high'][i]])
                    pre_act = 'sell'
                    balance = balance + df['high'][i]
                    if(i == len(df['close']) -1):
                        orders.record(pair,'Sell',str(df['time'][i]), df['close'][i])
                #if greater than 1 standard deviation above sma40 line take profit
                elif df['high'][i] > df['sma40'][i] + std_close *1:
                    sell_signals.append([df['time'][i], df['high'][i]])
                    pre_act = 'sell'
                    balance = balance + df['high'][i]
                    if(i == len(df['close']) -1):
                        orders.record(pair,'Sell',str(df['time'][i]), df['close'][i])
                #stop loss at -1%
                elif df['low'][i] < buy_signals[-1][1]*.99:
                        sell_signals.append([df['time'][i], df['high'][i]])
                        pre_act = 'sell'
                        balance = balance + df['close'][i]
                        if(i == len(df['close']) -1):
                            orders.record(pair,'Sell',str(df['time'][i]), df['close'][i])
        # return all buys/ sells
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
        graph = PlotData(df, pair, buy_signals = buy_signals, sell_signals = sell_signals)
        graph.graph()
