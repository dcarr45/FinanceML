import json
import requests
from sentiment import getSentiment, countPos, countNeg, cleanText
from loadTickers import positive_words, negative_words


# NYT API vars
APPLICATION = "SentimentML"
API_KEY = "46ad1d95c0f01e124f481eba9d6771d2:10:73701170"
base = "http://api.nytimes.com/svc/search/v2/articlesearch"

field_list = "lead_paragraph,headline,abstract,snippet,keywords"

params = {
'fq':'google',
'begin_date': '20120101',
'end_date':'20130101',
#'news_desk' : blah,
'fl':field_list,
'api-key':API_KEY
}

def sentiment(params):
    r = requests.get(base+".json",params)
    parsed = json.loads(r2.content)
    resp = parsed['response']
    docs = resp['docs']
    ret = 0
    for doc in docs:
        sentiment = 0
        for p in doc:
            print
            print p
            var = doc[p]
            if p == "headline":
                var = var['main']
            if p == "keywords":
                var = [e['value'] for e in var]
                var = " ".join(var)
            print cleanText(var)
            sentiment+= getSentiment(var)
        ret+=sentiment
    return ret



# lead_paragraph = doc["lead_paragraph"]
# headline = doc["headline"]
# abstract = doc["abstract"]
# snippet = doc["snippet"]
# keywords = doc["keywords"]


#
# docs
# facets
# meta

# lead_paragraph
# headline
# abstract
# snippet
# keywords

# var = "[{u'value': u'Dictionaries', u'is_major': u'Y', u'rank': u'1', u'name': u'subject'}, {u'value': u'McKean, Erin', u'is_major': u'N', u'rank': u'2', u'name': u'persons'}, {u'value': u'Computers and the Internet', u'is_major': u'N', u'rank': u'3', u'name': u'subject'}, {u'value': u'English Language', u'is_major': u'N', u'rank': u'4', u'name': u'subject'}]"
# print " ".join(var.split("'")[1::2])

if __name__ == '__main__':
    sentiment(params)
