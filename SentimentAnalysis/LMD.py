import csv

inf = open('LoughranMcDonald_MasterDictionary_2014.csv', 'r')
lines = inf.readlines()
lines = [line.split(",") for line in lines]
lines = [[line[0],line[7],line[8]] for line in lines if line[7]!='0' or line[8]!='0']

def make_neg():
    negfile = open('LoughranMcDonald_Negative.csv', "w")
    negatives = [line[0] for line in lines if line[1]!='0']
    writer = csv.writer(negfile)
    for word in negatives[1:]:
        writer.writerow([word])
    negfile.close()

def make_pos():
    posfile = open('LoughranMcDonald_Positive.csv', "w")
    positives = [line[0] for line in lines if line[2]!='0']
    writer = csv.writer(posfile)
    for word in positives[1:]:
        writer.writerow([word])
    posfile.close()

make_neg()
make_pos()
inf.close()
