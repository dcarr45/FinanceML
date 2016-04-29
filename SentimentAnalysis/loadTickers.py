#loadTickers.py
import datetime
import csv
import requests
import webbrowser

def loadTickers():
    filename = 'tickers.csv'
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    tickers = [line.strip().replace('^','').replace('-','.') for line in lines[1:]]
    #print tickers
    return tickers

def get_content(url):
    response = requests.get(url)
    return response.content

def get_companies():
    mw = 'http://www.marketwatch.com/investing/stock/{ticker}'
    urls = [mw.format(ticker=t) for t in tickers]
    #webbrowser.open_new_tab(urls[0])
    #get_content(urls[0])
    # c = get_content(urls[0])
    # f = open('mwtest.html','w')
    # f.write(c)
    # f.close()
    ret = []
    for url in urls:
        content = get_content(url)
        ret.append(content.split('<meta property="og:title" content="')[1].split('"')[0])
    return ret

def loadCompanies()

#(year, month, day)
start = datetime.datetime(2000, 1, 1)
end = datetime.datetime(2016, 3, 20)

tickers = loadTickers()
companies = loadCompanies()

def maxwrite():
    f = open('vol_' + ticker + '.csv', 'w')
    writer = csv.writer(f)
    writer.writerows(vol)
