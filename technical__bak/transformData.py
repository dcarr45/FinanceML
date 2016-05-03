#transformData.py
import pandas_datareader.data as web
import datetime
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt
import csv

#(year, month, day)
start = datetime.datetime(2000, 1, 1)
end = datetime.datetime(2016, 3, 20)

#trading days ahead to predict
time_horizon = 30

def loadTickers():
    filename = 'tickers.csv'
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    tickers = []
    for line in lines[1:]:
        line = line.strip()
        tickers.append(line)
    print tickers
    return tickers

def loadRawData(tickers):
    for ticker in tickers:
        df = web.DataReader(ticker, 'yahoo', start, end)
        df.to_csv(ticker+ ".csv", sep = ',')

def getPrices(ticker):
    # csv format
    # Date,	Open, High,	Low, Close, Volume, Adj Close
    f = open(ticker + '.csv', 'r')
    lines = f.readlines()
    f.close()

    prices = []
    for line in lines[1:]:
        line = line.strip()
        line = line.split(',')
        line = [line[0], line[-1]]
        prices.append(line)
    return prices

def priceToPercentChange(prices):
    for day in range(1:len(prices)):
        prices[day][1] = percentChange(prices[day-1][1], prices[day][1])


de



# # 30 day volatility
# # adjusted close: time series of array
def volCalc(ticker, prices, lagTime):
        if '^' in ticker:
            vol = prices[30:]
            f = open(ticker + '.csv', 'wb')
            # writer = csv.writer(f)
            # writer.writerows(prices)
        else:
            vol = []
            for i in range(lagTime,len(prices)):
                delta = 0
                for day in range(1,lagTime):
                    delta += abs(percentChange(prices[i-day][1], prices[i-day-1][1]))
                #print delta
                sigma30 = 100.0 * delta/lagTime
                line = [prices[i][0], prices[i][1], sigma30]
                vol.append(line)
                delta = 0
            f = open('vol_' + ticker + '.csv', 'wb')
        writer = csv.writer(f)
        writer.writerows(vol)

def percentChange(p0,p1):
    p0 = float(p0)
    p1 = float(p1)
    return (p1-p0)/p0


def RSICalc(ticker,prices, n=14):
    date = zip(*prices)[0]
    p = zip(*prices)[1]
    price = [float(i) for i in p]

    deltas = np.diff(price)
    seed = deltas[:n+1]
    up  = seed[seed >= 0].sum()/n
    down = -seed[seed < 0].sum()/n
    RS = up/down
    RSI = np.zeros_like(price)
    RSI[:n] = 100. - 100./(1.+ RS)

    for i in range(time_horizon, len(price)):
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
    RSI = zip(date[30:],RSI[30:])
    f = open('RSI_' + ticker + '.csv', 'wb')
    writer = csv.writer(f)
    writer.writerows(RSI)


### load and transform data
tickers = loadTickers()
### write to csv
loadRawData(tickers)
for ticker in tickers:
    prices = getPrices(ticker)
    volCalc(ticker, prices, time_horizon)
    if '^' in ticker:
        continue
    RSICalc(ticker, prices, time_horizon)
