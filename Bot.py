#!/usr/bin/python
import time
import os
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
        strat.output()


def main():
    pair = 'XXBTZUSD'
    interval = 1
    tradebot = Bot(pair, interval)
    tradebot.run()
def graphic():
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
    print "__________________________"
    print ""
if __name__ == '__main__':
    #initial display items
    starttime=time.time()
    os.system('clear')
    graphic()
    #continuos run items
    while True:
      os.system('clear')
      graphic()
      main()
      time.sleep(60.0 - ((time.time() - starttime) % 60.0))
