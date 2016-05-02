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
doc = resp['docs'][1]
# for p in doc:
#     print p, ":",resp['docs'][1][p]
lead_paragraph = doc["lead_paragraph"]
headline = doc["headline"]
abstract = doc["abstract"]
snippet = doc["snippet"]
keywords = doc["keywords"]
print
print "lead_paragraph"
ct = lead_paragraph
cp = countPos(ct, positive_words)
cn =  countNeg(ct, negative_words)
sent = getSentiment(ct, negative_words, positive_words)
print cp, cn, ct
print
print "headline"
ct = headline
cp = countPos(ct, positive_words)
cn =  countNeg(ct, negative_words)
sent = getSentiment(ct, negative_words, positive_words)
print cp, cn, ct
print
print "abstract"
ct = abstract
cp = countPos(ct, positive_words)
cn =  countNeg(ct, negative_words)
sent = getSentiment(ct, negative_words, positive_words)
print cp, cn, ct
print
print "snippet"
ct = snippet
cp = countPos(ct, positive_words)
cn =  countNeg(ct, negative_words)
sent = getSentiment(ct, negative_words, positive_words)
print cp, cn, ct
print
print "keywords"
ct = keywords
cp = countPos(ct, positive_words)
cn =  countNeg(ct, negative_words)
sent = getSentiment(ct, negative_words, positive_words)
print cp, cn, ct
#
# docs
# facets
# meta

# lead_paragraph
# headline
# abstract
# snippet
# keywords

print countPos("good happy", positive_words)

ct = lead_paragraph






ct = headline






ct = abstract






ct = snippet






ct = keywords
