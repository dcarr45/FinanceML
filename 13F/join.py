from pyspark import SparkConf, SparkContext

def process(spark):

    forms = spark.textFile('hdfs:///user/carrdp/13F/parsed_noempty') \
        .map(lambda line: eval(line))

    num_investors = forms.flatMap(lambda vals: [(cusip, 1) for (cusip, amt, tag) in vals]) \
        .reduceByKey(lambda x, y: x + y)
    
    num_shares = forms.flatMap(lambda vals: [(cusip, amt) for (cusip, amt, tag) in vals]) \
        .reduceByKey(lambda x, y: x + y)

    result = num_investors.keyBy(lambda (c, n): c).join(num_shares.keyBy(lambda (c1, n1): c1)) \
        .map(lambda (cusip, ((c1, inv), (c2, shares))): (cusip, inv, shares, 1.0 * shares / inv)) \
        .saveAsTextFile('hdfs:///user/carrdp/13F/result')

if __name__ == "__main__":

    conf = SparkConf()
    conf.setMaster("spark://10.0.22.241:7077")
    conf.set("spark.executor.memory", "10g")
    conf.set("spark.driver.memory", "10g")
    spark = SparkContext(conf = conf)
    process(spark)
