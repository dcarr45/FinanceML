#getData.py
import os
import pandas as pd
import pandas_datareader.data as web
import datetime
import numpy as np
import csv
from get_pages import file_dt

#Set Time Frame
#(year, month, day)
ticker ='SPY'
START_DATE = datetime.datetime(2000, 1, 1)
END_DATE = datetime.datetime.today() #(2016, 3, 20)

def last_day_of_month(date):
    if date.month == 12:
        return date.replace(day=31)
    return date.replace(month=date.month+1, day=1) - datetime.timedelta(days=1)

def is_ld(date):
    ld = last_day_of_month(date)
    return date == ld

def getHistoricalData():
        return web.DataReader(ticker, 'yahoo', START_DATE, END_DATE)


def getDateAndPrice():
    # df format
    # Date,	Open, High,	Low, Close, Volume, Adj Close
    df = getHistoricalData()['Adj Close']
    dates = df.index.values
    dates = [pd.to_datetime(ts) for ts in dates]
    prices = df.values
    return dates, prices


def main():
    d, p = getDateAndPrice()
    return [[file_dt(d[i]),p[i]] for i in range(len(d))]# if is_ld(d[i])]

if __name__ == '__main__':
    f = open('label.csv','wb')
    writer = csv.writer(f)
    writer.writerow(['#Date','SPY_adj_close'])
    for row in main():
        writer.writerow(row)
    f.close()
