# conda install scikit-learn
import scipy
import numpy
from sklearn import linear_model
from sklearn.metrics import roc_auc_score
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import StratifiedKFold


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
        label[(date, price)] = 1

    return label


def load():
    return load_features(), load_allstars()


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
    Y = scipy.zeros(len(label)-1)
    for i in range(0, len(label)-1):
        price1 = label[i][1]
        price2 = label[i+1][1]
        if price2 > price1: # if price increased over a month
            Y[i] = 1
    print 'Number of price increases', sum(Y)
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
    features, all_stars = load()
    X = create_input(batting)
    Y = create_output(batting, all_stars)

    clf = linear_model.SGDClassifier(loss='log')
    test_classifier(clf, X, Y)

    clf = GaussianNB()
    test_classifier(clf, X, Y)

    clf = RandomForestClassifier(n_estimators=10, max_depth=10)
    test_classifier(clf, X, Y)


if __name__ == '__main__':
    main()
