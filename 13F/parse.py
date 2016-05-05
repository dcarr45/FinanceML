#!/usr/bin/env python

from pyspark import SparkConf, SparkContext
from collections import defaultdict
import urllib2
import re
import sys
from bs4 import BeautifulSoup


def extract(spark, year, qtr):
    cusips = set()
    for line in list(open('cusip.txt')):
        cusips.add(line.replace('"', '').strip())

    forms = spark.wholeTextFiles('hdfs:///user/carrdp/13F/' + year + '/' + qtr + '/*', 1272) \
        .map(lambda (fname, file): parse(file, cusips, fname, year, qtr)) \
    
    forms.cache()

    investors_shares = forms.flatMap(lambda vals: [(cusip, (1, amt)) for (cusip, amt) in vals]) \
        .reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1])) \
        .map(lambda (cusip, (inv, shares)): (cusip, inv, shares, 1.0 * shares / inv)) \
        .saveAsTextFile('hdfs:///user/carrdp/13F/' + year + '/' + qtr + '/parsed')

    '''
    result = num_investors.keyBy(lambda (c, n): c).join(num_shares.keyBy(lambda (c1, n1): c1)) \
        .map(lambda (cusip, ((c1, inv), (c2, shares))): (cusip, inv, shares, 1.0 * shares / inv)) \
        .saveAsTextFile('hdfs:///user/carrdp/13F/2014/Q4/parsed')
    '''

    #TODO:  download market cap and p/e, and eventually open/close
    #       make extensible to 1000+ forms (why isn't it)
    #           Spark streaming?
    #           foreachPartition?
    #       change from S&P to XLK stocks

def parse(file, valid, fname, year, qtr):
    soup = BeautifulSoup(file, "xml")
    try:
        fund = str(soup.find('name').contents)
    except AttributeError:
        pass
    
    try:
        if year == 2013 and (qtr == 'Q3' or qtr == 'Q4') or year > 2013: 
            if str(soup.headerData.submissionType.string).startswith("13F-HR"):
                data = defaultdict(int)

                for tag in soup.find_all('infoTable'):
                    try:
                        cusip = str(tag.cusip.string) 
                        type = str(tag.shrsOrPrnAmt.sshPrnamtType.string)
                        shares = int(tag.shrsOrPrnAmt.sshPrnamt.string.split(".")[0])

                        if cusip in valid and type == "SH":
                            data[cusip] += shares
                    
                    except AttributeError:   
                        data['INTERIOR ERROR'] += 1

                return data.items()

            else:
                return [(fname + ': ' + str(soup.headerData.submissionType.string), 1)]
        else:
           pass 
    
    except AttributeError:
       return [(fname, 10)]
        

if __name__ == "__main__":
    year = sys.argv[1]
    qtr = sys.argv[2]

    conf = SparkConf()
    conf.setMaster("spark://10.0.22.241:7077")
    conf.set("spark.executor.memory", "10g")
    conf.set("spark.driver.memory", "10g")
    spark = SparkContext(conf = conf)
    extract(spark, year, qtr)
