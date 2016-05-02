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
