#!/usr/bin/env python

from pyspark import SparkConf, SparkContext

import sys
import os
from bs4 import BeautifulSoup

def extract(spark):
    cusips = set()
    for line in list(open('cusip.txt')):
        cusips.add(line.replace('"','').strip())
    
    forms = spark.textFile('hdfs:///user/carrdp/FinanceML/13F/all_forms/test_forms') \
        .map(lambda form: getInfoTable(form, cusips)) \
        .saveAsTextFile('hdfs:///user/carrdp/FinanceML/13F/res')

def getInfoTable(text, cusips):
    #receives form as indented xml
    soup = BeautifulSoup(text)

    for tag in soup.find_all('infoTable'):
        if tag.cusip.string in cusips
        
    
         

if __name__ == "__main__":
    conf = SparkConf()
    conf.setMaster("spark://10.0.22.241:7077")
    conf.set("spark.executor.memory", "10g")
    conf.set("spark.driver.memory", "10g")
    spark = SparkContext(conf = conf)
    extract(spark)
