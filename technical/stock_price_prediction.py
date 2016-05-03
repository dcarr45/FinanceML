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

    baseline = np.array(data_df['return_SPY'].values).T



    print baseline[-5:]
    print X[-5:]
    # print y[-5:]
    baseline = preprocessing.scale(baseline).T
    X = preprocessing.scale(X)

    return X , baseline, y

def test_classifier(clf, X, Y):
    folds = StratifiedKFold(Y, 2)
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
    print baseline[-5:]
    print type(X)
    print type(baseline)
    print type(Y)

    print X[0].size
    print baseline[0].size
    print Y[0].size

    print type(X[0])
    print type(baseline[0])
    print type(Y[0])

    clf = svm.SVC(kernel="linear", C=1.0, probability = True)
    print 'Baseline: '
    test_classifier(clf, baseline, Y )
    print 'Model: '
    test_classifier(clf, X, Y)

    # clf = linear_model.SGDClassifier(loss='log')
    # test_classifier(clf, X, Y)
    #
    # clf = KNeighborsClassifier()
    # test_classifier(clf, X, Y)
    #
    # clf = GaussianNB()
    # test_classifier(clf, X, Y)
    #
    # clf = RandomForestClassifier(n_estimators=10, max_depth=10)
    # test_classifier(clf, X, Y)
    #
    # clf = svm.SVC(kernel="linear", C=1.0, probability = True)
    # print 'Baseline: '
    # test_classifier(clf, baseline, Y )
    # print 'Model: '
    # test_classifier(clf, X, Y)






    #SVC_Means=[]
    #for day in range(100):
    #    SVC_Means.append(test_classifier(clf, X, Y))

    #print SVC_Means




if __name__ == '__main__':
    main()
