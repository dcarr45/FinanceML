#!/usr/bin/env python

from pyspark import SparkConf, SparkContext

import sys
import os

def extract(spark):
    cusips = set()
    for line in list(open('cusip.txt')):
        cusips.add(line.replace('"','').strip())
    
    forms = spark.textFile('hdfs:///user/carrdp/13F_2015/all_forms/Q1_forms') \
        .map(lambda form = get
    

if __name__ == "__main__":
    conf = SparkConf()
    conf.setMaster("spark://10.0.22.241:7077")
    conf.set("spark.executor.memory", "10g")
    conf.set("spark.driver.memory", "10g")
    spark = SparkContext(conf = conf)
    extract(spark)
