#!/usr/bin/python
import pandas as pd
import requests
import json
from datetime import datetime
from pyti.smoothed_moving_average import smoothed_moving_average as sma
from pyti.exponential_moving_average import exponential_moving_average as ema
from pyti.hull_moving_average import hull_moving_average as hma
from pyti.relative_strength_index import relative_strength_index as rsi
from pyti.on_balance_volume import on_balance_volume as obv

class GetData:
    def __init__(self, pair, interval):
        self.pair = pair
        self.interval = interval

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
        df['sma40'] = sma(df['close'].tolist(), 40)
        df['hma20'] = hma(df['close'].tolist(), 20)
        df['rsi'] = rsi(df['close'].tolist(), 10)
        df['obv'] = obv(df['close'].tolist(), df['volume'].tolist())

        return df
