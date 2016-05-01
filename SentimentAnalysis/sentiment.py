from loadTickers import *
from googlenews import *
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

## TODO: fix issue with nltk.
## imports do not work. throws ValueError: numpy.dtype has the wrong size, try recompiling

search_terms = tickers+companies

def cleanText(text):
    """
    removes punctuation, stopwords and returns lowercase text in a list of single words
    """
    text = text.lower()

    text = BeautifulSoup(text).get_text()

    tokenizer = RegexpTokenizer(r'\w+')
    text = tokenizer.tokenize(text)

    clean = [word for word in text if word not in stopwords.words('english')]

    return clean


def countPos(cleantext, positive):
    """
    counts positive words in cleantext
    """
    pos = [word for word in cleantext if word in positive]
    return len(pos)


def countNeg(cleantext, negative):
    """
    counts negative words in cleantext
    """
    negs = [word for word in cleantext if word in negative]
    return len(negs)


def getSentiment(cleantext, negative, positive):
    """
    counts negative and positive words in cleantext and returns a score accordingly
    """
    return (countPos(cleantext, positive) - countNeg(cleantext, negative))



#print get_url(query=tickers[0],month=1,day=1,year=2015)
URLS = [goog_url(query=term,month=1,day=1,year=2015) for term in search_terms]
# print get_content(URLS[0])

#html_doc = get_content('https://www.google.com/#hl=en&gl=us&tbm=nws&authuser=0&q=facebook')
soup = BeautifulSoup(html_doc, 'html.parser')

#print soup.prettify()
descriptions = soup.find_all('div', class_="st")
link_titles = soup.find_all('a')

# terms = {}
# for line in [e.get_text() for e in descriptions+link_titles]:
#     for word in line.split():
#         if word in terms:
#             terms[word] += 1
#         else:
#             terms[word] = 1
# for term in terms:
#     print terms[term], term

for line in [e.get_text() for e in descriptions+link_titles]:
    ct = cleanText(line)
    print countPos(ct, positive_words)
    print countNeg(ct, negative_words)
    print getSentiment(ct, negative_words, positive_words)


# for link in soup.find_all('a'):
#     print link.get_text()

#print soup.title
# for link in soup.find_all('a'):
#     print(link.get('href'))


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
