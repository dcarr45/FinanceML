from loadTickers import *
from googlenews import *

#(year, month, day)

search_terms = tickers+companies

#print get_url(query=tickers[0],month=1,day=1,year=2015)
URLS = [goog_url(query=term,month=1,day=1,year=2015) for term in search_terms]

print get_content(URLS[0])

# for url in URLS:
#     print get_content(url)

print search_terms
