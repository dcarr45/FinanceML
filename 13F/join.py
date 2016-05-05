from pyspark import SparkConf, SparkContext

def process(spark):

    forms = spark.wholeTextFiles('hdfs:///user/carrdp/13F/*/*/parse_file/') \
        .map(lambda (fname, file): agg(fname, file)) \
        .saveAsTextFile('hdfs:///user/carrdp/13F/agged')    

def agg(fname, file):
    year = str(fname.split("/")[-3])
    qtr = str(fname.split("/")[-2])

    data = [eval(str(line)) for line in file.split('\n') if line and 'hdfs://' not in line]

    return (year + qtr, data)

if __name__ == "__main__":

    conf = SparkConf()
    conf.setMaster("spark://10.0.22.241:7077")
    conf.set("spark.executor.memory", "10g")
    conf.set("spark.driver.memory", "10g")
    spark = SparkContext(conf = conf)
    process(spark)
