#!/usr/bin/python
# When using cronjob @reboot on raspberry pi add a delay to allow for the pi to create an internet connection
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
        strat.run() #run test the entire day and live goes live
        strat.output(True)
def main():
    pair = 'XETHZUSD'
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
    #time.sleep(60) #add when running live
    #continuos run items
    while True:
      try: #hopefully eliminate internet issues
          os.system('clear')
          graphic()
          main()
          time.sleep(60.0 - ((time.time() - starttime) % 60.0))
      except Exception as e:
          time.sleep(60.0 - ((time.time() - starttime) % 60.0))
          print(e)
