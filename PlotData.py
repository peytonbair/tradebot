#!/usr/bin/python
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot
from plotly.subplots import make_subplots

class PlotData:
    def __init__(self, df, pair, buy_signals = False, sell_signals = False):
        self.df = df
        self.pair = pair
        self.buy_signals = buy_signals
        self.sell_signals = sell_signals
    def graph(self):
        df = self.df
        pair = self.pair
        buy_signals = self.buy_signals
        sell_signals = self.sell_signals
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
