#aggregate.py
from transformData import *
import pandas as pd
import pandas_datareader.data as web
import datetime
import numpy as np


def aggregateInput():
    tickers = loadTickers()

    df_features = []
    for ticker in tickers:
        if '^' in ticker:
            df_VIX = pd.read_csv(ticker+  '.csv', names=['Date', 'VIX'])
            df_features.append(df_VIX)
        else:

            vol_df = pd.read_csv('vol_' + ticker + '.csv', names=['Date', ticker + '_Price',  ticker + '_Vol'])
            RSI_df = pd.read_csv('RSI_' + ticker + '.csv', names=['Date', ticker + '_RSI'])
            df_features.append(vol_df)
            df_features.append(RSI_df)

    df_raw_feature = reduce(lambda left,right: pd.merge(left,right,on='Date'), df_features)
    df_raw_feature.set_index('Date')


    df_raw_feature.to_csv('feature_matrix.csv', sep = ',')
    # return df_raw_feature

#
# def createOutput(df_raw_feature):
#     #create a 30 day lag in the returns
#     filename = 'feature_matrix.csv'
#     f = open(filename, 'r')
#     lines = f.readlines()
#     f.close()
#     tickers = []
#     for line in lines[1:]:
#         line = line.strip()
#         tickers.append(line)
#     print tickers
#     return tickers


aggregateInput()
