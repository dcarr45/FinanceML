import json, sys
import requests
from sentiment import getSentiment, countPos, countNeg, cleanText
from loadTickers import positive_words, negative_words


# NYT API vars
API_KEY2 = "0fa21861234316c4385d19dfbf33b873:8:73701170"
API_KEY = "46ad1d95c0f01e124f481eba9d6771d2:10:73701170"
base = "http://api.nytimes.com/svc/search/v2/articlesearch"

field_list = "lead_paragraph,headline,abstract,snippet,keywords"

payload = {
'fq':'google',
'begin_date': '20120101',
'end_date':'20130101',
#'news_desk' : blah,
'fl':field_list,
'api-key':API_KEY2
}

def param_maker(query,date1,date2):
    ret = {'fl':field_list,'api-key':API_KEY2}
    ret['fq'] = query
    ret['begin_date'] = date1
    ret['end_date'] = date2
    return ret


def get_json(params):
    r = requests.get(base+".json",params)
    parsed = json.loads(r.content)
    return parsed

def doc_sentiment(params,data):
    print params['begin_date'], params['fq']
    parsed = get_json(params)
    ret = 0
    status = parsed['status']
    if status == "OK":
        resp = parsed['response']
        docs = resp['docs']
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

# TODO
# switch to these forms of sentiment for each search
# polarity = (p - n)/(p + n)
# subjectivity = (n + p_/N)
# pos_refs_per_ref = p/N
# neg_refs_per_ref = n/N
# senti_diffs_per_ref = (p - n)/N

def full_sentiment(data):
    ret = {'p':0,'n':0,'N':0}
    status = parsed['status']
    if status == "OK":
        resp = parsed['response']
        docs = resp['docs']
        for doc in docs:
            p,n,N = 0,0,0
            for page in doc:
                var = doc[page]
                if var is not None:
                    if page == "headline":
                        var = var['main']
                    if page == "keywords":
                        var = [e['value'] for e in var]
                        var = " ".join(var)
                    p += countPos(var)
                    n += countNeg(var)
                    N += len(cleanText(var))
                    ret['p']+=p
                    ret['n']+=n
                    ret['N']+=N
    return ret

if __name__ == '__main__':
    #print payload
    #print doc_sentiment(param_maker("google",'20120101','20130101'))
    #print search_terms
    print get_json(payload)
    #print [term.split()[0] for term in doc_sentiment(payload)]
