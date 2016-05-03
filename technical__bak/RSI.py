

import pandas_datareader.data as web
import datetime
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt
import csv

time_horizon= 30

def getPrices(ticker):
    # csv format
    f = open(ticker + '.csv', 'r')
    lines = f.readlines()
    f.close()
    prices = []
    for line in lines[1:]:
        line = line.strip()
        line = line.split(',')
        line = [line[0], line[-1]]
        prices.append(line)
    dates = zip(*prices)[0]
    p = zip(*prices)[1]
    d = [float(i) for i in p]
    return d


def RSICalc(ticker,prices, n=14):

    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up  = seed[seed >= 0].sum()/n
    down = -seed[seed < 0].sum()/n
    RS = up/down
    RSI = np.zeros_like(prices)
    RSI[:n] = 100. - 100./(1.+ RS)

    for i in range(time_horizon, len(prices)):
        delta = deltas[i-1]
        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta
        up = (up * (n-1) + upval)/n
        down = (down * (n-1) + downval)/n
        RS = up/down
        RSI[i] = 100. - 100./(1.+ RS)
    return RSI

    #print RSI

ticker = 'AAPL'
p = getPrices(ticker)
t = RSICalc(ticker,p, n=14)

print len(p)
print len(t)
