import json
import requests
from sentiment import getSentiment, countPos, countNeg
from loadTickers import positive_words, negative_words


# NYT API vars
APPLICATION = "SentimentML"
API_KEY = "46ad1d95c0f01e124f481eba9d6771d2:10:73701170"
base = "http://api.nytimes.com/svc/search/v2/articlesearch"

field_list = "lead_paragraph,headline,abstract,snippet,keywords"

params = {
'fq':'google',
'begin_date': '20120101',
'end_date':'20120101',
#'news_desk' : blah,
'fl':field_list,
'api-key':API_KEY
}
r2 = requests.get(base+".json",params)
print r2.url
parsed = json.loads(r2.content)
resp = parsed['response']
doc = resp['docs'][0]
for p in doc:
    print 
    print p
    var = doc[p]
    if p == "headline":
        var = var['main']
    if p == "keywords":
        var = [e['value'] for e in var]
        var = " ".join(var)
    print "countNeg", countNeg(var,negative_words)
    print "countPos", countPos(var,positive_words)
    print "sentiment", getSentiment(var,negative_words,positive_words)


lead_paragraph = doc["lead_paragraph"]
headline = doc["headline"]
abstract = doc["abstract"]
snippet = doc["snippet"]
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
