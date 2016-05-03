#loadTickers.py

import pandas_datareader.data as web
import datetime
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt
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
    for line in lines[1:]:
        line = line.strip()
        tickers.append(line)
    print tickers
    return tickers

loadTickers()
