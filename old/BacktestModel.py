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
from pyti.relative_strength_index import relative_strength_index as rsi
from pyti.on_balance_volume import on_balance_volume as obv

class TradingModel:
    def __init__(self):

        self.df = self.getData()


    def getData(self):
        #get url to data from kraken api
        data = pd.read_csv("Kraken_BTCUSD_1h.csv")

        #creat pandas df
        col_names = ['time','symbol','open','high','low','close','volume','volume usd', 'sma20', 'sma40', 'rsi', 'obv']
        df = pd.DataFrame(data, columns = col_names)
        print df        #turn df into floats
        for col in col_names:
            df[col] = df[col].astype(float)
        #add techinical indicatiors to the df
        #df['time'] = [datetime.fromtimestamp(x) for x in df['time']]
        df['sma20'] = sma(df['close'].tolist(), 20)
        df['sma40'] = sma(df['close'].tolist(), 40)
        df['rsi'] = rsi(df['close'].tolist(), 14)
        df['obv'] = obv(df['close'].tolist(), df['volume'].tolist())

        return df

    def strategy(self):
        df = self.df


        buy_signals = []
        sell_signals = []
        pre_act = 'sell'

        #obv_average = df['obv'].sum()/dflength
        std_obv = np.std(df['obv'])
        #print obv_average
        print std_obv


        #check for buy points
        for i in range(1, len(df['close'])):
            if df['obv'][i] < 0 and df['low'][i] > df['sma20'][i]:
                buy_signals.append([df['time'][i], df['low'][i]])
                pre_act = 'buy'

        #check for sell points
            if df['obv'][i] >= 0 + std_obv and df['rsi'][i] > 65:
                sell_signals.append([df['time'][i], df['high'][i]])
                pre_act = 'sell'

        self.plotData(buy_signals = buy_signals, sell_signals = sell_signals)


    def plotData(self, buy_signals = False, sell_signals = False):
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
            name = "SMA 40",
            line = dict(color = ('rgba(255, 207, 102, 50)')))
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
        #limit errors when a buy/sell signals doesn't exist
        if buy_signals:
            fig.append_trace(buys, row=1, col=1)
        if sell_signals:
            fig.append_trace(sells, row=1, col=1)

        fig.append_trace(rsi, row=2, col=1)

        fig.append_trace(obv, row=3, col=1)

        #adjust layout
        fig.update_layout(title_text="Backtest of BTC", xaxis_rangeslider_visible=False)
        #save plot to html file for later use
        plot(fig, filename= 'backtest.html')

        #copyfile('chart.html', '/var/www/html/')
def Main():
	symbol = "XETHZUSD"
	model = TradingModel()
	model.strategy()

if __name__ == '__main__':
    Main()
