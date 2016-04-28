import pandas_datareader.data as web
import datetime
import csv


#(year, month, day)
start = datetime.datetime(2000, 1, 1)
end = datetime.datetime(2016, 3, 20)

def loadTickers():
    filename = 'tickers.csv'
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    tickers = []
    for line in lines[1:5]:
        line = line.strip()
        tickers.append(line)
    return tickers

def loadRawData():
    tickers =loadTickers()
    for ticker in tickers:
        df = web.DataReader(ticker, 'yahoo', start, end)
        df.to_csv(ticker+ ".csv", sep = ',')
    return tickers
