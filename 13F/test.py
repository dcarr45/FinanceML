#!/usr/bin/env python

from pyspark import SparkConf, SparkContext
from collections import defaultdict
import urllib2
import re
from bs4 import BeautifulSoup


def extract(spark):
    cusips = set()
    for line in list(open('cusip.txt')):
        cusips.add(line.replace('"', '').strip())

    forms = spark.wholeTextFiles('hdfs:///user/carrdp/13F/2015/Q2/*', 500) \
        .map(lambda (fname, file): parse(file, cusips, fname)) \
        .saveAsTextFile('hdfs:///user/carrdp/13F/2015/test')    
    '''
    forms.cache()

    investors_shares = forms.flatMap(lambda vals: [(cusip, (1, amt)) for (cusip, amt) in vals]) \
        .reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1])) \
        .map(lambda (cusip, (inv, shares)): (cusip, inv, shares, 1.0 * shares / inv)) \
        .saveAsTextFile('hdfs:///user/carrdp/13F/2015/Q2/parsed') 

    result = num_investors.keyBy(lambda (c, n): c).join(num_shares.keyBy(lambda (c1, n1): c1)) \
        .map(lambda (cusip, ((c1, inv), (c2, shares))): (cusip, inv, shares, 1.0 * shares / inv)) \
        .saveAsTextFile('hdfs:///user/carrdp/13F/2015/Q2/parsed')
    '''

    #TODO:  download market cap and p/e, and eventually open/close
    #       make extensible to 1000+ forms (why isn't it)
    #           Spark streaming?
    #           foreachPartition?
    #       change from S&P to XLK stocks

def parse(file, valid, fname):
    soup = BeautifulSoup(file, "xml")
    try:
        fund = str(soup.find('name').contents)
    except AttributeError:
        return [(fname, 'NO FUND')]
    
    try:
        if str(soup.headerData.submissionType.string).startswith("13F-HR"):
            #data = defaultdict(int)
            data = {}

            for tag in soup.find_all('infoTable'):
                try:
                    cusip = str(tag.cusip.string) 
                    type = str(tag.shrsOrPrnAmt.sshPrnamtType.string)
                    shares = int(tag.shrsOrPrnAmt.sshPrnamt.string.split(".")[0])

                    if cusip == "478160104" and type == "SH":
                        return (str(soup.headerData.filerInfo.filer.credentials.cik.string))
                
                except AttributeError:   
                    data['INTERIOR ERROR'] = 'goo'

            return data.items()

        else:
            return [(fname + '\t' + str(soup.headerData.submissionType.string), 'gooo')]
    except AttributeError:
       return [(fname, 'BAD FORM')]
        

if __name__ == "__main__":

    conf = SparkConf()
    conf.setMaster("spark://10.0.22.241:7077")
    conf.set("spark.executor.memory", "10g")
    conf.set("spark.driver.memory", "10g")
    spark = SparkContext(conf = conf)
    extract(spark)
