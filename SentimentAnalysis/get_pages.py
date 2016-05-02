#from sentiment import *
import os, csv
from loadTickers import *
from nyt import param_maker, doc_sentiment

def repl(txt):
    return txt.replace(" ", "_") \
        .replace(".","") \
        .replace("&","")


def file_dt(date):
    month,day,year=date.month,date.day,date.year
    m = month<10
    d = day<10
    month,day,year = str(month),str(day),str(year)
    if m: month = "0"+month
    if d: day = "0"+day
    return year+"/"+month+"/"+day

def search_dt(month,day,year):
    m = month<10
    d = day<10
    month,day,year = str(month),str(day),str(year)
    if m: month = "0"+month
    if d: day = "0"+day
    return year+""+month+""+day

def write(filename, message):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(filename, "w") as f:
        f.write(message)


def load_links__bak():
    urls = open('urls.csv','r')
    urls = [e.split(',') for e in urls]
    header = urls[0][:-1]
    # for name in header:
    #     print header[0] + repl(name) + ".html"
    # for line in urls[1:3]:
    for line in urls[1:2]:
        for i in range(1,len(line)-1):
            filename = "pages/"+dt(line[0])+"/"+repl(header[i])+".html"
            #content = get_content(line[i])
            content = line[i]
            write(filename, content)
            #print filename

def calc_sentiments__bak():
    # Date handling
    f = open('features.csv','wb')
    writer = csv.writer(f)
    writer.writerow(["date"]+search_terms)
    for date in daterange(datetime.datetime(2014,1,1),END_DATE):
        month,day,year = date.month,date.day,date.year
        if day == 1:
            # monthly
            month2 = 1 if month == 12 else month+1
            year2 = year+1 if month == 12 else year
            app = []
            for term in search_terms:
                # perform sentiment analysis on content
                d1 = search_dt(month,day,year)
                d2 = search_dt(month2,day,year2)
                params = param_maker(term,d1,d2)
                app.append(doc_sentiment(params))
            print app
            writer.writerow([file_dt(date)]+app)
    f.close()

def store_jsons():
    # Date handling
    for date in daterange(START_DATE,END_DATE):
        month,day,year = date.month,date.day,date.year
        if day == 1:
            #content = get_content(line[i])
            content = line[i]
            write(filename, content)
            # monthly
            month2 = 1 if month == 12 else month+1
            year2 = year+1 if month == 12 else year
            app = []
            for term in terms:
                fd = file_dt(date)[:7]
                tkr = term.split()[0]
                filename = "pages/"+fd+"/"+tkr+".json"

                d1 = search_dt(month,day,year)
                d2 = search_dt(month2,day,year2)
                params = param_maker(term,d1,d2)

                r = requests.get(base+".json",params)
                print params['begin_date'], params['fq']
                parsed = json.loads(r.content)
                write(filename, parsed)
