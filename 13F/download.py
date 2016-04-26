#!/usr/bin/env python

from pyspark import SparkConf, SparkContext

import sys
import os
import urllib2
from bs4 import BeautifulSoup

def extract(spark):
    cusips = set()
    for line in list(open('cusip.txt')):
        cusips.add(line.replace('"','').strip())
    
    forms = spark.textFile('hdfs:///user/carrdp/FinanceML/13F/Q12015/links10.txt') \
        .map(lambda link: getForm(link, cusips)) \
        .saveAsTextFile('hdfs:///user/carrdp/FinanceML/13F/all_forms/testQ1/dir')
        
        #.flatMap(lambda cusips: [(cusip, 1) for (cusip, name) in cusips]) \
        #.reduceByKey(lambda x, y: x + y) \

def getForm(link, cusips):
    file = urllib2.urlopen(link).read()

    #receives form as indented xml
    soup = BeautifulSoup(file, "xml")
    
    shares = []

    for tag in soup.find_all('infoTable'):
        if tag.cusip.string in cusips:
            shares.append((tag.cusip.string, tag.nameOfIssuer.string))
    
    return shares 
    
         

if __name__ == "__main__":
    sys.setrecursionlimit(10000)

    conf = SparkConf()
    conf.setMaster("spark://10.0.22.241:7077")
    conf.set("spark.executor.memory", "10g")
    conf.set("spark.driver.memory", "10g")
    spark = SparkContext(conf = conf)
    extract(spark)
