from loadTickers import *
from googlenews import *

search_terms = tickers+companies

#print get_url(query=tickers[0],month=1,day=1,year=2015)
#URLS = [goog_url(query=term,month=1,day=1,year=2015) for term in search_terms]

#print get_content(URLS[0])

# for url in URLS:
#     print get_content(url)

# print search_terms

URLS = []
def date_fun():
    f = open('urls.csv','wb')
    writer = csv.writer(f)
    writer.writerow(["date"]+search_terms)
    # Date handling
    for date in daterange(START_DATE,END_DATE):
        month,day,year = date.month,date.day,date.year
        #if date.weekday() < 5: # is a weekday
        app = []
        for term in search_terms:
            url = goog_url(query=term,month=month,day=day,year=year)
            # content = get_content(url)
            # perform sentiment analysis on content
            app.append(url)
            #URLS.append(url)
        writer.writerow([date]+app)
    f.close()
