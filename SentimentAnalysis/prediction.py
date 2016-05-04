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
    col = features[0].index(feature)
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

def list_avg(l):
    return sum(l)/float(len(l))

def find_baseline():
        features, label = load()

        Y = create_output(features, label)
        clfs = [linear_model.SGDClassifier(loss='log'),
                GaussianNB(),
                RandomForestClassifier(n_estimators=10, max_depth=10),
                svm.SVC(kernel="linear", C=1.0, probability = True)]

        feat_list = features[0][1:] #skip date
        best_feature = (0,1,None)#(avg_auc,avg_auc_adj,feature)
        best_feature_p = (0,1,None)#(avg_auc,avg_auc_adj,feature)
        for feature in feat_list:
            print "BEGINNING NEW RUN WITH FEATURE:"
            print feature
            print
            baseline = create_baseline(features, feature) # SPY_subj


            print """
            BASELINE
            ########
            ########
            """
            run_auc = []
            best = (0,1,None) #(auc,auc_adj,clf)
            for clf in clfs:
                auc = test_classifier(clf, baseline, Y)
                run_auc.append(auc)
                x = auc - 0.5
                auc_adj = x if x > 0 else -x
                if auc_adj < best[1]:
                    best = (auc,auc_adj,clf.__class__.__name__)
                print auc
                print
            print "THE BEST CLASSIFIER WAS"
            print best[2]
            print "WITH AN AUC OF "
            print best[0]
            raa = list_avg(run_auc)
            x = raa - 0.5
            raa_adj = x if x > 0 else -x
            if raa_adj < best_feature[1]:
                best_feature = (raa,raa_adj,feature)


            baseline = preprocessing.scale(baseline)

            print """

            BASELINE -- PREPROCESSED
            ########
            ########
            """

            run_auc = []
            best = (0,1,None) #(auc,auc_adj,clf)
            for clf in clfs:
                auc = test_classifier(clf, baseline, Y)
                run_auc.append(auc)
                x = auc - 0.5
                auc_adj = x if x > 0 else -x
                if auc_adj < best[1]:
                    best = (auc,auc_adj,clf.__class__.__name__)
                print auc
                print
            print "THE BEST CLASSIFIER WAS"
            print best[2]
            print "WITH AN AUC OF "
            print best[0]
            raa = list_avg(run_auc)
            x = raa - 0.5
            raa_adj = x if x > 0 else -x
            if raa_adj < best_feature_p[1]:
                best_feature_p = (raa,raa_adj,feature)
            print "\n\n\n"

        print """


        THE BEST FEATURE WAS:"""
        print best_feature[2]
        print "WITH AN AVG AUC OF:"
        print best_feature[0]
        print """
        THE BEST PREPROCESSED FEATURE WAS:"""
        print best_feature_p[2]
        print "WITH AN AVG AUC OF:"
        print best_feature_p[0]
        print
        return best_feature[2],best_feature_p[2]

def main():
    features, label = load()

    X = create_input(features)
    Y = create_output(features, label)

    feat_list = features[0][1:] #skip date
    for feature in feat_list:
        baseline = create_baseline(features, feature) # SPY_subj

        clfs = [linear_model.SGDClassifier(loss='log'),
                GaussianNB(),
                RandomForestClassifier(n_estimators=10, max_depth=10),
                svm.SVC(kernel="linear", C=1.0, probability = True)]

        print """
        BASELINE
        ########
        ########
        """
        best = (0,None)
        for clf in clfs:
            tc = test_classifier(clf, baseline, Y)
            if tc > best[0]:
                best = (tc,clf.__class__.__name__)
            print tc
            print

        baseline = preprocessing.scale(baseline)

        print """
        BASELINE -- PREPROCESSED
        ########
        ########
        """

        best = (0,None)
        for clf in clfs:
            tc = test_classifier(clf, baseline, Y)
            if tc > best[0]:
                best = (tc,clf.__class__.__name__)
            print tc
            print

        print """


        REAL RUN
        ########
        ########
        """

        best = (0,None)
        for clf in clfs:
            tc = test_classifier(clf, baseline, Y)
            if tc > best[0]:
                best = (tc,clf.__class__.__name__)
            print tc
            print

        X = preprocessing.scale(X)
        print """
        REAL RUN -- PREPROCESSED
        ########
        ########
        """

        best = (0,None)
        for clf in clfs:
            tc = test_classifier(clf, baseline, Y)
            if tc > best[0]:
                best = (tc,clf.__class__.__name__)
            print tc
            print


if __name__ == '__main__':
    #main()
    find_baseline()
