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

def param_maker(query,date1,date2):
    ret = {'fl':field_list,'api-key':API_KEY}
    ret['fq'] = query
    ret['begin_date'] = date1
    ret['end_date'] = date2
    return ret


def doc_sentiment(params):
    r = requests.get(base+".json",params)
    parsed = json.loads(r.content)
    resp = parsed['response']
    docs = resp['docs']
    ret = 0
    for doc in docs:
        sentiment = 0
        for p in doc:
            var = doc[p]
            if var is not None:
                if p == "headline":
                    var = var['main']
                if p == "keywords":
                    var = [e['value'] for e in var]
                    var = " ".join(var)
                sentiment+= getSentiment(var)
        ret+=sentiment
    return ret

if __name__ == '__main__':
    print doc_sentiment(params)
