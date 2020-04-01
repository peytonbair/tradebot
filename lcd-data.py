#!/usr/bin/python
import requests
import json
import time
import Adafruit_CharLCD as LCD

# Raspberry Pi pin setup
lcd_rs = 21
lcd_en = 20
lcd_d4 = 25
lcd_d5 = 24
lcd_d6 = 23
lcd_d7 = 18
lcd_backlight = 0

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

lcd.clear()
lcd.message("Pbair Tradebot")


time.sleep(15)
lcd.clear()

url = 'https://api.kraken.com/0/public/Ticker'

def price(ticker):
    urli = url + '?pair=' + ticker;
    data = requests.get(urli)
    return data.json()['result'][ticker]['a'][0]

while 1:
    try:
        bitcoin = round(float(price('XXBTZUSD')),2)
        eth = round(float(price('XETHZUSD')), 2)
        etc = round(float(price('XETCZUSD')),2)


        for i in range(4):
            lcd.clear()
            lcd.message('BTC: ' + str(bitcoin))
            time.sleep(5)
            lcd.clear()
            lcd.message('ETH: ' + str(eth))
            time.sleep(5)
            lcd.clear()
            lcd.message('ETC: ' + str(etc))
            time.sleep(5)
    except:
        lcd.clear()
        lcd.message('Error')
