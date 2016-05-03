#transformData.py
import pandas_datareader.data as web
import datetime
import numpy as np

def loadTickers():
    filename = 'tickers.csv'
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    tickers = []
    for line in lines[1:]:
        line = line.strip()
        tickers.append(line)
    return tickers

def loadRawData(tickers):
    for ticker in tickers:
        df = web.DataReader(ticker, 'yahoo', start, end)
        df.to_csv(ticker+ ".csv", sep = ',')


#trading days ahead to predict
time_horizon = 30

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

# # 30 day volatility
# # adjusted close: time series of array
def volCalc(ticker, prices, lagTime):
        if '^' in ticker:
            vol = prices
            f = open(ticker + '.csv', 'wb')
            # writer = csv.writer(f)
            # writer.writerows(prices)
        else:
            vol = []
            for i in range(lagTime,len(prices)):
                delta = 0
                for day in range(1,lagTime):
                    delta += percentChange(prices[i-day][1], prices[i-day-1][1])
                #print delta
                sigma30 = 100.0 * delta/lagTime
                line = [prices[i][0], prices[i][1], sigma30]
                vol.append(line)
                delta = 0
            f = open('vol' + ticker + '.csv', 'wb')
        writer = csv.writer(f)
        writer.writerows(vol)

def percentChange(p0,p1):
    p0 = float(p0)
    p1 = float(p1)
    return abs(p1-p0)/p0



def RSICalc(ticker,prices, n=14):
    delta = np.diff(prices)
    seed = deltas[:n+1]
    up  = seed[seed >= 0].sum()/n
    down = -seed[seed < 0].sum()/n
    RS = up/down
    RSI = np.zeros_like(prices)
    RSI = 100. - 100./(1.+ RS)

    for i in range(time_horizon, len(prices)):
        delta = delta[i-1]
        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = delta
        up = (up * (n-1) + upval)/n
        down = (down * (n-1) + downval)/n

        RS = up/down
        RSI[i] = 100. - 100./(1.+ RS)
    return RSI





#     f = open('vol' + ticker + '.csv', 'wb')
# writer = csv.writer(f)
# writer.writerows(vol)




tickers = loadTickers()
loadRawData(tickers)
for ticker in tickers:
    prices = getPrices(ticker)
    volCalc(ticker, prices, time_horizon)
    RSI(ticker, prices, time_horizon)
