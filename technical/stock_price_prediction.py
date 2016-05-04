#stock_price_prediction.py

import pandas as pd
import pandas_datareader.data as web
import datetime
import numpy as np
import scipy as sp
import csv
from pprint import pprint
from sklearn import linear_model
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import roc_auc_score
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import StratifiedKFold
from sklearn import svm, preprocessing

TIME_HORIZON = 30

def loadData():

    data_df = pd.DataFrame.from_csv('feature_matrix.csv')
    # print data_df[-5:]

    #load feature headers
    filename = 'features.csv'
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    FEATURES = []
    for line in lines[1:]:
        line = line.strip()
        FEATURES.append(line)

    #load label headers
    LABEL = 'label'

    #create input
    X = np.array(data_df[FEATURES].values)
    #create output
    y = np.array(data_df[LABEL].values)
    #create baseline
    baseline = np.array(data_df['return_SPY'].values)

    #normalize each feature around 0
    #single features require reshape
    baseline = preprocessing.scale(baseline).reshape(-1,1)
    X = preprocessing.scale(X)

    return X , baseline, y

def test_classifier(clf, X, Y):
    folds = StratifiedKFold(Y, 5)
    aucs = []
    for train, test in folds:
        # Sizes
        # print X[train].shape, Y[train].shape
        # print X[test].shape, len(prediction)

        clf.fit(X[train], Y[train])
        prediction = clf.predict_proba(X[test])
        aucs.append(roc_auc_score(Y[test], prediction[:, 1]))
    print clf.__class__.__name__, aucs, np.mean(aucs)
    return np.mean(aucs)


def main():

    X, baseline, Y = loadData()

    clf = RandomForestClassifier(n_estimators=10, max_depth=10)
    print 'Random Forest Baseline Mean AUC: '
    test_classifier(clf, baseline, Y )
    print 'Random Forest Model Mean AUC: '
    test_classifier(clf, X, Y)


    clf = svm.SVC(kernel="linear", C=1.0, probability = True)
    print 'SVM Baseline Mean AUC: '
    test_classifier(clf, baseline, Y )
    print 'SVM Model Mean AUC: '
    test_classifier(clf, X, Y)



if __name__ == '__main__':
    main()
