# conda install scikit-learn
import scipy
import numpy
import datetime as dt
from sklearn import linear_model
from sklearn.metrics import roc_auc_score
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import StratifiedKFold
from sklearn import svm, preprocessing
from loadSPYData import last_day_of_month, is_ld
from loadTickers import daterange, START_DATE
from get_pages import file_dt


def date_from_str(datestring):
    #YYYY/MM/DD
    y,m,d = datestring.split('/')
    y,m,d = int(y),int(m),int(d)
    return dt.datetime(y,m,d)

def lastday(datestring):
    date = date_from_str(datestring)
    return is_ld(date)

def load_features():
    f = open('full_features.csv', 'r')
    lines = f.readlines()
    f.close()

    features = []
    for line in lines:
        line = line.strip()
        features.append(line.split(','))
    return features


def load_label():
    f = open('label.csv', 'r')
    lines = f.readlines()
    f.close()

    label = {}
    for line in lines[1:]:
        line = line.strip().split(',')
        date = line[0]
        price = line[1]
        label[date] = price

    return label


def load():
    return load_features(), load_label()


def create_input(features):
    # don't want to inlude date
    features=features[1:]
    SKIP = 1
    WIDTH = len(features[0])
    X = scipy.zeros((len(features), WIDTH))
    for i in range(len(features)):
        for j in range(SKIP, WIDTH):
                X[i, j-SKIP] = features[i][j]
    return X


def create_baseline(features, feature='SPY_subj'):
    col = features[1].index(feature)
    features=features[1:]
    X = scipy.zeros((len(features), 1))
    for i in range(len(features)):
        X[i,0] = features[i][col]
    return X


def get_prices(datestring, label):
    date = date_from_str(datestring)
    y,m = date.year,date.month
    y2,m2 = y,m
    if m==12:
        m2=0
        y2+=1
    price1,price2 = 0,0
    for date in daterange(dt.datetime(y,m,1),dt.datetime(y2,m2+1,1)):
        dat = file_dt(date)
        if dat in label:
            if price1==0:
                price1=label[dat]
            price2=label[dat]
    return price1,price2

def create_output(features, label):
    features=features[1:]
    LENGTH = len(features)
    Y = scipy.zeros(LENGTH)
    i,price1,price2 = 0,0,0
    for i in range(0, LENGTH):
        date=features[i][0]
        price1,price2 = get_prices(date,label)
        if price2 > price1: # if price increased over a month
            Y[i] = 1
    print 'Number of price increases', int(sum(Y))
    return Y


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
    print clf.__class__.__name__, aucs
    return numpy.mean(aucs)


def main():
    features, label = load()

    X = create_input(features)
    Y = create_output(features, label)

    baseline = create_baseline(features) # SPY_subj

    clfs = [linear_model.SGDClassifier(loss='log'),
            GaussianNB(),
            RandomForestClassifier(n_estimators=10, max_depth=10),
            svm.SVC(kernel="linear", C=1.0, probability = True)]

    print """
    BASELINE
    ########
    ########
    """

    for clf in clfs:
        print test_classifier(clf, baseline, Y)
        print

    print """
    REAL RUN
    ########
    ########
    """

    for clf in clfs:
        print test_classifier(clf, X, Y)
        print

    X = preprocessing.scale(X)
    baseline = preprocessing.scale(baseline)

    print """

    
    BASELINE -- PREPROCESSED
    ########
    ########
    """

    for clf in clfs:
        print test_classifier(clf, baseline, Y)
        print

    print """
    REAL RUN -- PREPROCESSED
    ########
    ########
    """

    for clf in clfs:
        print test_classifier(clf, X, Y)
        print


if __name__ == '__main__':
    main()
