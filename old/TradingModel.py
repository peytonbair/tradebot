#!/usr/bin/python
import pandas as pd
import requests
import json
import numpy as np
from time import sleep
from datetime import datetime
from shutil import copyfile
import plotly.graph_objs as go
from plotly.offline import plot
from plotly.subplots import make_subplots

from pyti.smoothed_moving_average import smoothed_moving_average as sma
from pyti.exponential_moving_average import exponential_moving_average as ema
from pyti.hull_moving_average import hull_moving_average as hma
from pyti.relative_strength_index import relative_strength_index as rsi
from pyti.on_balance_volume import on_balance_volume as obv

class TradingModel:
    def __init__(self, pair, interval):
        self.pair = pair
        self.interval = interval
        self.df = self.getData()


    def getData(self):
        #get url to data from kraken api
        pair = self.pair
        interval = str(self.interval)
        base = 'https://api.kraken.com'
        endpoint = '/0/public/OHLC'
        params = '?pair=' + pair + '&interval=' + interval
        url = base + endpoint + params
        #download the data
        json_string = requests.get(url)
        dictionary = json.loads(json_string.text)
        dict_len = len(dictionary['result'][pair])
        self.dflength = dict_len
        #creat pandas df
        col_names = ['time', 'open', 'high', 'low', 'close', 'volume', 'sma20', 'sma40', 'rsi', 'obv','hma20']
        df = pd.DataFrame(columns = col_names)

        #creat df cause the import stuff would work
        for x in range(dict_len):
            temp = dictionary['result'][pair][x]
            df = df.append({col_names[0]: temp[0], col_names[1]: temp[1], col_names[2]: temp[2], col_names[3]: temp[3], col_names[4]: temp[4], col_names[5]: temp[5]}, ignore_index=True)

        #turn df into floats
        for col in col_names:
            df[col] = df[col].astype(float)
        #add techinical indicatiors to the df
        df['time'] = [datetime.fromtimestamp(x) for x in df['time']]
        df['sma20'] = sma(df['close'].tolist(), 20)
        df['sma40'] = sma(df['close'].tolist(), 50)
        df['hma20'] = hma(df['close'].tolist(), 200)

        df['rsi'] = rsi(df['close'].tolist(), 10)
        df['obv'] = obv(df['close'].tolist(), df['volume'].tolist())

        return df
    def strategy(self):
        df = self.df
        pair = self.pair
        dflength = self.dflength

        buy_signals = []
        sell_signals = []
        pre_act = 'sell'
        balance = 0
        #calculations to help make accurate predictions
        high = df['high'].max()
        low = df['low'].min()

        close_average = df['close'].sum()/dflength
        std_close = np.std(df['close'])
        print std_close

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

        self.plotData(buy_signals = buy_signals, sell_signals = sell_signals)


    def plotData(self, buy_signals = False, sell_signals = False):
        pair = self.pair
        df = self.df
        # plot candlestick chart
        candle = go.Candlestick(
            x = df['time'],
            open = df['open'],
            close = df['close'],
            high = df['high'],
            low = df['low'],
            name = "Price")
        #plot techinical indicatiors
        sma20 = go.Scatter(
            x = df['time'],
            y = df['sma20'],
            name = "SMA 20",
            line = dict(color = ('rgba(102, 207, 255, 50)')))

        sma40 = go.Scatter(
            x = df['time'],
            y = df['sma40'],
            name = "SMA 100",
            line = dict(color = ('rgba(255, 207, 102, 50)')))
        hma20 = go.Scatter(
            x = df['time'],
            y = df['hma20'],
            name = "HMA 20",
            line = dict(color = ('rgba(255, 207, 102, 100)')))
        rsi = go.Scatter(
            x = df['time'],
            y = df['rsi'],
            name = 'RSI 14',
            line = dict(color = ('rgba(0, 102, 255, 50)')))
        obv = go.Scatter(
            x = df['time'],
            y = df['obv'],
            name = 'OBV',
            line = dict(color = ('rgba(204, 51, 255, 50)')))

        if buy_signals:
            buys = go.Scatter(
        		x = [item[0] for item in buy_signals],
        		y = [item[1] for item in buy_signals],
        		name = "Buy Signals",
        		mode = "markers",

			)
        if sell_signals:
            sells = go.Scatter(
				x = [item[0] for item in sell_signals],
				y = [item[1] for item in sell_signals],
				name = "Sell Signals",
				mode = "markers",

                )

        #creat plot
        fig = make_subplots( rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.02)
        #add to the subplots
        fig.append_trace(candle, row=1, col=1)
        fig.append_trace(sma20, row=1, col=1)
        fig.append_trace(sma40, row=1, col=1)
        fig.append_trace(hma20, row=1, col=1)
        #limit errors when a buy/sell signals doesn't exist
        if buy_signals:
            fig.append_trace(buys, row=1, col=1)
        if sell_signals:
            fig.append_trace(sells, row=1, col=1)

        fig.append_trace(rsi, row=2, col=1)

        fig.append_trace(obv, row=3, col=1)

        #adjust layout
        fig.update_layout(title_text="Crypto Data of " + pair, xaxis_rangeslider_visible=False)
        #save plot to html file for later use
        plot(fig, filename= pair + '.html')

        #copyfile('chart.html', '/var/www/html/')
def Main():
	symbol = "XXBTZUSD"
	model = TradingModel(symbol, 1)
	model.strategy()

if __name__ == '__main__':
    Main()
