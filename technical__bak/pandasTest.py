#pandasTest.py
import pandas as pd
import pandas_datareader.data as web
import datetime
import numpy as np



data = [(2,3,4,5,5),(1,3,4,5,5),(4,5,5,2,8)]
df = pd.DataFrame(data)

print type(df), '\n'
print df, '\n'

print df[1][2:], '\n'
print df[2], '\n'
print df[:][3:], '\n'






        # df_VIX = pd.read_csv(ticker+  '.csv', names=['Date', 'VIX'])
        # df_features.append(df_VIX)
