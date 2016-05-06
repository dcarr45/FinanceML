#addTimeDelay.py
import pandas as pd
import pandas_datareader.data as web
import datetime
import numpy as np
import scipy as sp
import csv
from pprint import pprint

#Date SPY_Price SPY_Vol SPY_RSI VIX AAPL_Price ... T_Vol T_RSI

def getFeatures():
    filename = 'feature_matrix.csv'
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    rawFeatures = []
    #dont need to include titles, schema above
    for line in lines[1:]:
        line = line.strip()
        # assuming date is not significant
        rawFeatures.append(line.split(',')[1:])
    return rawFeatures

def getTimeDelay(rawFeatures):
    #create a 30day-future price
    # pprint(features)
    #grab 30:n features and add as feature
    truncated = rawFeatures[30:]
    delay = [float(x[0]) for x in truncated]
    features = rawFeatures[:-30]

    return features,delay

def getInput(features):
    # don't want to cinlude playerID, sting, team, league year in predicition
    LENGTH = len(features)
    WIDTH = len(features[0])
    X = sp.zeros((LENGTH, WIDTH))
    for i in range(0, LENGTH):
        for j in range(WIDTH):
                X[i, j] = features[i][j]
    return X


def create_output(features, all_stars):
    Y = scipy.zeros(len(features))
    for i in range(0, len(features)):
        player = features[i][0]
        year = features[i][1]
        if (player, year) in all_stars:
            Y[i] = 1
    print 'Number of all stars', sum(Y)
    return Y




rawFeatures = getFeatures()
features, delay = getTimeDelay(rawFeatures)
print getInput(features)

    #
    #     batting.append(line.split(','))
    # return batting
    #
    # return features


#
#
# def truncateFeatures(features):
#     for i in range(len(features)):
#         features[i] = features[i][:-29]
#     X = features
#     return X
#
# def getOutput(features,delay):
#     Y = sp.zeros(len(features))
#     Y[0] = 0
#     for i in range(1,len(features)):
#         if features[2][i] < delay[i]:
#             Y[i] = 1
#     return Y
#
#
# features = loadFeatures()
# delay = getTimeDelay(features)
# X = truncateFeatures(features)
# Y = getOutput(X,delay)
#
# pprint(X)
# pprint(Y)
