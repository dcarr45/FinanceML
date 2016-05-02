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

def calc_sentiments():
    # Date handling
    inf = open('features.csv')
    liness = inf.readlines()
    f = open('features.csv','wb')
    writer = csv.writer(f)
    writer.writerow(["date"]+search_terms)
    for date in daterange(START_DATE,END_DATE):
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

calc_sentiments()
#print search_dt(1,1,2010)

# 20000101SPY.html
# 20000101VIX.html
# 20000101AAPL.html
# 20000101MSFT.html
# 20000101XOM.html
# 20000101JNJ.html
# 20000101GE.html
# 20000101BRKB.html
# 20000101AMZN.html
# 20000101WFC.html
# 20000101JPM.html
# 20000101T.html
# 20000101SPDR_SP_500_ETF_Trust.html
# 20000101CBOE_Volatility_Index.html
# 20000101Apple_Inc.html
# 20000101Microsoft_Corp.html
# 20000101Exxon_Mobil_Corp.html
# 20000101Johnson__Johnson.html
# 20000101General_Electric_Co.html
# 20000101Berkshire_Hathaway_Inc_Cl_B.html
# 20000101Amazoncom_Inc.html
# 20000101Wells_Fargo__Co.html
# 20000101JPMorgan_Chase__Co.html
