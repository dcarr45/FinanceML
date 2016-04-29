#aggregate.py
from transformData import *
import pandas as pd
import pandas_datareader.data as web
import datetime
import numpy as np

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

#stock_dfs = pd.merge(vol_df,RSI_df, on = 'Date')
# stock_dfs.append(vol_df)
# stock_dfs.append(RSI_df)
# df_features.join(stock_dfs, on = 'Date')

print type(df_features)
print len(df_features)

df_final_feature = reduce(lambda left,right: pd.merge(left,right,on='Date'), df_features)

print df_final_feature
