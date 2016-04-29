#loadTickers.py
import datetime
import csv
import requests
import webbrowser

def loadTickers():
    f = open('tickers.csv', 'r')
    lines = f.readlines()
    f.close()
    tickers = [line.strip().replace('^','').replace('-','.') for line in lines[1:]]
    #print tickers
    return tickers

def get_content(url):
    response = requests.get(url)
    return response.content

def get_companies_from_tickers():
    mw = 'http://www.marketwatch.com/investing/stock/{ticker}'
    urls = [mw.format(ticker=t) for t in tickers]

    f = open('companies.csv','wb')
    writer = csv.writer(f)

    for url in urls:
        content = get_content(url) \
            .split('<meta property="og:title" content="')[1] \
            .split('"')[0]
        writer.writerow([content])
    f.close()

def loadCompanies():
    f = open('companies.csv', 'r')
    lines = f.readlines()
    f.close()
    return [line.strip() for line in lines]


#(year, month, day)
start = datetime.datetime(2000, 1, 1)
end = datetime.datetime(2016, 3, 20)

tickers = loadTickers()
companies = loadCompanies()

if __name__ == '__main__':
    get_companies_from_tickers()
