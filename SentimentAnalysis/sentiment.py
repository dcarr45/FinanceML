from loadTickers import *
from googlenews import goog_url, fmt
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

## TODO: fix issue with nltk.
## imports do not work. throws ValueError: numpy.dtype has the wrong size, try recompiling


def cleanText(text):
    """
    removes punctuation, stopwords and returns lowercase text in a list of single words
    """
    text = text.lower()

    text = BeautifulSoup(text, 'html.parser').get_text()

    tokenizer = RegexpTokenizer(r'\w+')
    text = tokenizer.tokenize(text)

    clean = [word for word in text if word not in stopwords.words('english')]

    return clean


def countPos(cleantext):
    """
    counts positive words in cleantext
    """
    if type(cleantext) == type("str"):
        cleantext = cleanText(cleantext)
    pos = [word for word in cleantext if word in positive_words]
    return len(pos)


def countNeg(cleantext):
    """
    counts negative words in cleantext
    """ 
    if type(cleantext) == type("str"):
        cleantext = cleanText(cleantext)
    negs = [word for word in cleantext if word in negative_words]
    return len(negs)


def getSentiment(text):
    """
    counts negative and positive words in cleantext and returns a score accordingly
    """
    cleantext = cleanText(text)
    return (countPos(cleantext) - countNeg(cleantext))


# soup = BeautifulSoup(html_doc, 'html.parser')
#
# #print soup.prettify()
# descriptions = soup.find_all('div', class_="st")
# link_titles = soup.find_all('a')

# terms = {}
# for line in [e.get_text() for e in descriptions+link_titles]:
#     for word in line.split():
#         if word in terms:
#             terms[word] += 1
#         else:
#             terms[word] = 1
# for term in terms:
#     print terms[term], term

# for line in [e.get_text() for e in descriptions+link_titles]:
#     ct = cleanText(line)
#     cp = countPos(ct, positive_words)
#     cn =  countNeg(ct, negative_words)
#     sent = getSentiment(ct, negative_words, positive_words)
#     print sent, ct

# for link in soup.find_all('a'):
#     print link.get_text()

#print soup.title
# for link in soup.find_all('a'):
#     print(link.get('href'))


# for url in URLS:
#     print get_content(url)

# print search_terms

# 1/1/2000 - 2/1/20000
# 2
# 3
# 4
# 5
# 6
# 7
# 8
# 9
# 10
# 11 - 12
