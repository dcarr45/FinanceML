#from sentiment import *
import os
from loadTickers import get_content

def repl(txt):
    return txt.replace(" ", "_") \
        .replace(".","") \
        .replace("&","")


def dt(txt):
    return txt[:7].replace("-","/")


def write(filename, message):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(filename, "w") as f:
        f.write(message)


def load_links():
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

load_links()


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
