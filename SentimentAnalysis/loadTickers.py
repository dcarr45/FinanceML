#loadTickers.py
import datetime
import csv
import requests
import webbrowser
import datetime
#from googlenews import goog_url, fmt

#(year, month, day)
START_DATE = datetime.datetime(2000, 1, 1)
END_DATE = datetime.datetime(2016, 3, 20)


def loadTickers():
    f = open('tickers.csv', 'r')
    lines = f.readlines()
    f.close()
    tickers = [line.strip().replace('^','').replace('-','.') for line in lines[1:]]
    #print tickers
    return tickers

def loadTerms():
    f = open('search_terms.csv', 'r')
    lines = f.readlines()
    f.close()
    terms = lines[0].split(",")
    return terms

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


def loadPositive():
    """
    loading positive dictionary
    """
    myfile = open('LoughranMcDonald_Positive.csv', "r")
    positives = myfile.readlines()
    positive = [pos.strip().lower() for pos in positives]
    return positive


def loadNegative():
    """
    loading negative dictionary
    """
    myfile = open('LoughranMcDonald_Negative.csv', "r")
    negatives = myfile.readlines()
    negative = [neg.strip().lower() for neg in negatives]
    return negative


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

def last_day_of_month(date):
    if date.month == 12:
        return date.replace(day=31)
    return date.replace(month=date.month+1, day=1) - datetime.timedelta(days=1)

def load_urls():
    f = open('urls.csv','wb')
    writer = csv.writer(f)
    writer.writerow(["date"]+search_terms)
    # Date handling
    for date in daterange(START_DATE,END_DATE):
        month,day,year = date.month,date.day,date.year
        if day == 1:
            # monthly
            month2 = 1 if month == 12 else month+1
            year = year if month2 == month else year+1
            app = []
            for term in search_terms:
                url = goog_url(query=fmt(term),month1=month,
                    month2=month2,day=day,year=year)
                # perform sentiment analysis on content
                app.append(url)
            writer.writerow([date]+app)
    f.close()

#(year, month, day)
start = datetime.datetime(2000, 1, 1)
end = datetime.datetime(2016, 3, 20)

terms = loadTerms()
tickers = loadTickers()
companies = loadCompanies()
search_terms = tickers+companies
positive_words = loadPositive()
negative_words = loadNegative()


if __name__ == '__main__':
    #get_companies_from_tickers()
    # for date in daterange(START_DATE,datetime.datetime(2000, 1, 20)):
    #     month,day,year = date.month,date.day,date.year
    #     if date.weekday() <5: print month, day, year
    # print negative_words[:10]
    print search_terms
    print [term.split()[0] for term in terms]
