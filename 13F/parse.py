#!/usr/bin/env python

from pyspark import SparkConf, SparkContext

import sys
import os
import urllib2
import contextlib
from bs4 import BeautifulSoup


def extract(spark):
    cusips = set()
    for line in list(open('cusip.txt')):
        cusips.add(line.replace('"', '').strip())

    forms = spark.textFile('hdfs:///user/carrdp/13F/*/*') \
        .map(lambda link: parse(link, cusips).saveAsTextFile('hdfs:///user/carrdp/13F/parsed')

    forms.cache()

    num_investors = forms.flatMap(lambda vals: [(cusip, 1) for (cusip, amt) in vals]) \ 
        .reduceByKey(lambda x, y: x + y)

    num_shares = forms.flatMap(lambda vals: [(cusip, amt) for (cusip, amt) in vals]) \
        .reduceByKey(lambda x, y: x + y)

    result = num_investors.keyBy(lambda (c, n): c).join(num_shares.keyBy(lambda (c1, n1): c1)) \
        .map(lambda (cusip, ((c1, inv), (c2, shares))): (cusip, inv, shares, 1.0 * shares / inv)) \ 
        .saveAsTextFile('hdfs:///user/carrdp/13F/result')

    #TODO:  download market cap and p/e, and eventually open/close
    #       make extensible to 1000+ forms (why isn't it)
    #           Spark streaming?
    #           foreachPartition?
    #       change from S&P to XLK stocks

def parse(file, cusips):
    soup = BeautifulSoup(file, "xml")

    data = []

    for tag in soup.find_all('infoTable'):
        cusip = tag.cusip.string 
        type = tag.shrsOrPrnAmt.sshPrnamtType.string
        shares = tag.shrsOrPrnAmt.sshPrnamt.string

        if cusip in cusips and str(type) == "SH":
            data.append((str(cusip), int(shares)))

    return data

if __name__ == "__main__":

    conf = SparkConf()
    conf.setMaster("spark://10.0.22.241:7077")
    conf.set("spark.executor.memory", "10g")
    conf.set("spark.driver.memory", "10g")
    spark = SparkContext(conf = conf)
    extract(spark)
