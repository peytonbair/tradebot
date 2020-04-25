#!/usr/bin/python
import time
import datetime
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
        strat = Strategy(df, pair)
        strat.run()


def main():
    pair = 'XETHZUSD'
    interval = 1
    tradebot = Bot(pair, interval)
    tradebot.run()
if __name__ == '__main__':
    #initial display items
    starttime=time.time()
    print "       _"
    print "      | |"
    print "      | |"
    print " _____| |___ _____ _ ___"
    print "|  _  |  _  |  _  | |  _\\"
    print "| |_| | |_| | |_| | | |"
    print "| ____|_____|_| |_|_|_|"
    print "| |"
    print "| |      TRADEBOT"
    print "|_|"
    print "____________________________"
    print ""
    #continuos run items
    while True:
      print "Time: " + str(datetime.datetime.now())
      main()
      time.sleep(60.0 - ((time.time() - starttime) % 60.0))
