# conda install scikit-learn
import scipy
import numpy
from sklearn import linear_model
from sklearn.metrics import roc_auc_score
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import StratifiedKFold


# player,year,stint,teamId,lgID,G,AB,R,H,2B,3B,HR,RBI,SB,CS,BB,SO,IBB,HBP,SH,SF,GIDP
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


# playerID,yearID,gameNum,gameID,teamID,lgID,GP,startingPos
def load_label():
    f = open('label.csv', 'r')
    lines = f.readlines()
    f.close()

    label = {}
    for line in lines:
        line = line.strip().split(',')
        if line[0] == '#':
            continue
        player = line[0]
        year = line[1]
        all_stars[(player, year)] = 1

    return label


def load():
    return load_features(), load_allstars()


def create_input(batting):
    # don't want to cinlude playerID, sting, team, league year in predicition
    SKIP = 5
    WIDTH = len(batting[0]) - SKIP
    X = scipy.zeros((len(batting), WIDTH))
    for i in range(0, len(batting)):
        for j in range(SKIP, WIDTH):
                X[i, j-SKIP] = batting[i][j] if batting[i][j] != '' else 0
    return X


def create_output(batting, all_stars):
    Y = scipy.zeros(len(batting))
    for i in range(0, len(batting)):
        player = batting[i][0]
        year = batting[i][1]
        if (player, year) in all_stars:
            Y[i] = 1
    print 'Number of all stars', sum(Y)
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
