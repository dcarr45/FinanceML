#getData.py
import os
import pandas as pd
import pandas_datareader.data as web
import datetime
import numpy as np
import csv

#Set Time Frame
#(year, month, day)
ticker ='SPY'
START_DATE = datetime.datetime(2000, 1, 1)
END_DATE = datetime.datetime(2016, 3, 20)

def getHistoricalData():
        return web.DataReader(ticker, 'yahoo', START_DATE, END_DATE)


def getDateAndPrice():
    # df format
    # Date,	Open, High,	Low, Close, Volume, Adj Close
    df = getHistoricalData()['Adj Close']
    dates = df.index.values
    dates = [str(pd.to_datetime(ts))[:10] for ts in dates]
    prices = df.values
    return dates, prices


def main():
    d, p = getDateAndPrice(ticker)
    return [[d[i-1],p[i]-1] for i in range(1,len(d))if d[i].split('-')[2]=='01']

if __name__ == '__main__':
    main()
