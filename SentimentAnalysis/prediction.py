# conda install scikit-learn
import scipy
import numpy
from sklearn import linear_model
from sklearn.metrics import roc_auc_score
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import StratifiedKFold
from loadSPYData import last_day_of_month, is_ld

def load_features():
    f = open('full_features.csv', 'r')
    lines = f.readlines()
    f.close()

    features = []
    for line in lines:
        line = line.strip()
        if line[0] == '#':
            continue
        features.append(line.split(','))
    return features


def load_label():
    f = open('label.csv', 'r')
    lines = f.readlines()
    f.close()

    label = {}
    for line in lines:
        line = line.strip().split(',')
        if line[0] == '#':
            continue
        date = line[0]
        price = line[1]
        label[date] = price

    return label


def load():
    return load_features(), load_label()


def create_input(features):
    # don't want to inlude date
    SKIP = 1
    WIDTH = len(features[0])
    X = scipy.zeros((len(features), WIDTH))
    for i in range(0, len(features)):
        for j in range(SKIP, WIDTH):
                X[i, j-SKIP] = features[i][j]
    return X[:-1] # have to chop off last month


def create_output(features, label):
    LENGTH = len(features)-1
    Y = scipy.zeros(LENGTH)
    i,price1,price2 = 0,0,0
    for date in label:
        if price1==0: price1 = label[date] # set price1 if first price of month
        if is_ld(date) and i < LENGTH: # if is last day of month
            price2 = label[date]
            Y[i] = 1 if price1 > price2 else 0
            i+=1
            price1=0
    # for i in range(0, len(label)-1):
    #     price1 = label[i][1]
    #     price2 = label[i+1][1]
    #     if price2 > price1: # if price increased over a month
    #         Y[i] = 1
    print 'Number of price increases', sum(Y), LENTH, i
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
    print clf.__class__.__name__
    print aucs, numpy.mean(aucs)


def main():
    features, label = load()
    X = create_input(feature)
    Y = create_output(features, label)

    clf = linear_model.SGDClassifier(loss='log')
    test_classifier(clf, X, Y)

    clf = GaussianNB()
    test_classifier(clf, X, Y)

    clf = RandomForestClassifier(n_estimators=10, max_depth=10)
    test_classifier(clf, X, Y)


if __name__ == '__main__':
    main()
