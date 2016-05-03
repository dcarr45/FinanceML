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

        df = web.DataReader(ticker, 'yahoo', START_DATE, END_DATE)
        # Date (index), Open, High, Low, Close, Volume, Adj Close
        #process data ahead of time
        #df = df.ix[:,[-1]]
        # filename = ticker + '.csv'
        # df.to_csv(filename, sep = ',')
        return df.as_matrix()

def getDateAndPrice(ticker):
    # csv format
    # Date,	Open, High,	Low, Close, Volume, Adj Close
    # f = open(ticker + '.csv', 'r')
    # lines = f.readlines()
    # f.close()
    lines = getHistoricalData()
    dates = []
    prices = []
    for line in lines[1:]:
        line = line.strip()
        line = line.split(',')
        date, price = line[0], float(line[1])
        dates.append(date)
        prices.append(price)
    return dates, prices


def main():
    getHistoricalData()
    dates, prices = getDateAndPrice(ticker)


if __name__ == '__main__':
    main()
