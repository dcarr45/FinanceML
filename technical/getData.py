#getData.py
import os
import pandas as pd
import pandas_datareader.data as web
import datetime
import numpy as np
import csv

#Set Time Frame
#(year, month, day)
PREDICTED ='SPY'
START_DATE = datetime.datetime(2000, 1, 1)
END_DATE = datetime.datetime(2016, 3, 20)
lagTime = 30
rawDataDirectory = 'historical_data'

def loadTickers():
    filename = 'tickers.csv'
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    stockTickers = []
    indexTickers = []
    for line in lines[1:]:
        line = line.strip()
        if '^' in line:
            indexTickers.append(line)
        else:
            stockTickers.append(line)
    print stockTickers, indexTickers
    return stockTickers, indexTickers

def getHistoricalData(ticker):
        df = web.DataReader(ticker, 'yahoo', START_DATE, END_DATE)
        # Date (index), Open, High, Low, Close, Volume, Adj Close
        filename = ticker + '.csv'
        df.to_csv(filename, sep = ',')


def getDateAndPrice(ticker):
    # csv format
    # Date,	Open, High,	Low, Close, Volume, Adj Close
    f = open(ticker + '.csv', 'r')
    lines = f.readlines()
    f.close()
    dates = []
    prices = []
    for line in lines[1:]:
        line = line.strip()
        line = line.split(',')
        date, price = line[0], float(line[1])
        dates.append(date)
        prices.append(price)
    return dates, prices

def calcDailyPercentChange(prices):
    df_prices = pd.DataFrame(np.array(prices)) \
        .pct_change() \
        .as_matrix()
    deltaPrice = [x[0] for x in df_prices]
    return np.array(deltaPrice)

def calc30DayVol(percentChange):
    vol = np.zeros_like(percentChange)
    length = len(percentChange)

    #calc 30 day historical vol for rolling window
    for day in range(lagTime,length):
        delta = 0.
        for i in range(1,lagTime+1):
            delta += abs(percentChange[day-i])
        sigma30 = 100 * delta/lagTime
        vol[day] = sigma30
    return vol


def calcRSI(prices, n=14):
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up  = seed[seed >= 0].sum()/n
    down = -seed[seed < 0].sum()/n
    RS = up/down
    RSI = np.zeros_like(prices)
    RSI[:n] = 100. - 100./(1.+ RS)

    for i in range(lagTime, len(prices)):
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

def combineTechnicalIndicators(ticker):
    dates, prices = getDateAndPrice(ticker)
    np_dates = np.chararray(len(dates), itemsize=len(dates[0]))
    for day in range(len(dates)):
        np_dates[day] = dates[day]

    percentChange = calcDailyPercentChange(prices)
    vol = calc30DayVol(percentChange)
    RSI = calcRSI(prices)


    if ticker == PREDICTED:
        np_prices = np.array(prices)
        label = np.zeros_like(np_prices)

    #create label for price of SPY
        for x in range(len(np_prices[:-lagTime])):
            print x
            if np_prices[x] < np_prices[x + lagTime]:
                label[x] = 1
            else:
                label[x] = 0
        features = np.column_stack((np_dates,  percentChange, vol, RSI, label))
        headers = ['date', 'return_'+ ticker, 'vol_'+ ticker, 'RSI_'+ ticker, 'label']
    else:
        features = np.column_stack((np_dates, percentChange, vol, RSI))
        headers = ['date', 'return_'+ ticker, 'vol_'+ ticker, 'RSI_'+ ticker]

    df_features = pd.DataFrame(features, columns=headers)
    # print df_features[25:35]
    return df_features


def joinFeatures(tickers):
    df_list = []
    for ticker in tickers:
        getHistoricalData(ticker)
        print ticker + ' data acquired.'
        df_list.append(combineTechnicalIndicators(ticker))
        print ticker + ' transformations made.'


    feature_matrix = reduce(lambda left,right: pd.merge(left,right,on='date'), df_list)
    feature_matrix.drop(feature_matrix.index[:lagTime+1], inplace=True)
    feature_matrix.drop(feature_matrix.index[-lagTime:], inplace=True)

    # print feature_matrix
    return feature_matrix




def main():

    wd = os.getcwd()
    if not os.path.exists(rawDataDirectory):
        os.makedirs(rawDataDirectory)

    stockTickers, indexTickers = loadTickers()

    os.chdir(wd + '/' + rawDataDirectory)

    # ticker ='AAPL'
    # getHistoricalData(ticker)

    feature_matrix = joinFeatures(stockTickers)

    os.chdir(wd)
    feature_matrix.set_index('date')
    feature_matrix.to_csv('feature_matrix.csv', sep = ',')


    # print type(dates)
    # print type(dates[1])
    # print type(prices)
    # print type(percentChange)
    # print type(vol)
    # print type(RSI)
    #
    # print len(dates)
    # print len(prices)
    # print len(percentChange)
    # print len(vol)
    # print len(RSI)

    # print dates
    # print prices
    # print percentChange[0:50]
    # print vol[0:50]
    # print RSI[0:50]

if __name__ == '__main__':
    main()
