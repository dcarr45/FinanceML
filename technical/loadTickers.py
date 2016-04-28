#loadTickers.py


def loadTickers():
    filename = 'tickers.csv'
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    tickers = []

    for line in lines[1:]:
        line = line.strip()
        tickers.append(line)


    print tickers

loadTickers()
