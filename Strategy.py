#!/usr/bin/python
import pandas as pd
import numpy as np
from PlotData import PlotData

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

        #calculations to help make accurate predictions
        high = df['high'].max()
        low = df['low'].min()

        close_average = df['close'].sum()/dflength
        std_close = np.std(df['close'])

        obv_average = df['obv'].sum()/dflength
        std_obv = np.std(df['obv'])

        #check for buy points
        for i in range(1, len(df['close'])):
            try:
                hull_slope = df['hma20'][i] - df['hma20'][i-1]
            except:
                hull_slope = 0
            if  pre_act == 'sell':
                #mean deviation strategy
                if df['low'][i] < df['sma40'][i] - std_close and df['rsi'][i] < 30:
                    buy_signals.append([df['time'][i], df['low'][i]])
                    balance = balance - df['low'][i]
                    pre_act = 'buy'
                #mommentum strategy
            elif df['obv'][i] < obv_average - std_obv and df['rsi'][i] < 25:
                    buy_signals.append([df['time'][i], df['low'][i]])
                    balance = balance - df['low'][i]
                    pre_act = 'buy'

        #check for sell points
            elif  pre_act == 'buy':
                if df['high'][i] > 1.01 * buy_signals[-1][1] and df['rsi'][i] > 70:
                    sell_signals.append([df['time'][i], df['high'][i]])
                    pre_act = 'sell'
                    balance = balance + df['high'][i]
                #stop loss at -1%
                elif df['low'][i] < buy_signals[-1][1]*.99:
                        sell_signals.append([df['time'][i], df['high'][i]])
                        pre_act = 'sell'
                        balance = balance + df['close'][i]

        print balance
        graph = PlotData(df, pair, buy_signals = buy_signals, sell_signals = sell_signals)
        graph.graph()
