import time
from MakeTrade import MakeTrade
from GetData import GetData
from Strategy import Strategy

class Bot:
    def __init__(self, pair, interval):
        self.pair = pair
        self.interval = interval
        self.df = GetData(pair, interval)
        self.df = self.df.getData()

    def run(self):
        pair = self.pair
        interval = self.interval
        df = self.df
        print df
        strat = Strategy(df, pair)
        strat.run()


def main():
    pair = 'XETHZUSD'
    interval = 1
    tradebot = Bot(pair, interval)
    tradebot.run()
if __name__ == '__main__':
    starttime=time.time()
    while True:
      print "tick"
      main()
      time.sleep(60.0 - ((time.time() - starttime) % 60.0))
