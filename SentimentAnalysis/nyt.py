import json
import requests

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
for p in resp['docs'][0]:
    print p, ":",resp['docs'][1][p]
#
# docs
# facets
# meta

# lead_paragraph
# headline
# abstract
# snippet
# keywords
