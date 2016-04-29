#!/usr/bin/env python

from pyspark import SparkConf, SparkContext

import urllib2
from subprocess import call
import os

def download(spark):
    forms = spark.textFile('hdfs:///user/carrdp/FinanceML/13F/Q12015/links10.txt') \
        .repartition(10) \
        .foreachPartition(getForm)

def getForm(links):
    #TODO:  Make connection pool for <65 connections
    #       Threading?

    for link in links:
        out = link.split("/")[-1]
        outfile = open(out, 'w')
        
        try:
            connection = urllib2.urlopen(link)
            file = connection.read()
            connection.close()

            outfile.write(file)
            call(['hadoop', 'fs','-put', out, '/user/carrdp/FinanceML/13F/log/' + out])
            
        except urllib2.URLError as err:
            outfile.write(err.reason)
            call(['hadoop', 'fs','-put', out, '/user/carrdp/FinanceML/13F/log/__' + out])


if __name__ == "__main__":
    conf = SparkConf()
    conf.setMaster("spark://10.0.22.241:7077")
    conf.set("spark.executor.memory", "10g")
    conf.set("spark.driver.memory", "10g")
    spark = SparkContext(conf = conf)
    download(spark)
