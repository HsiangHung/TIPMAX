#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
 Counts words in UTF8 encoded, '\n' delimited text received from the network every second.
 Usage: kafka_filter.py <zk> <topic>

 To run this on your local machine, you need to setup Kafka and create a producer first, see
 http://kafka.apache.org/documentation.html#quickstart

 and then run the example
    `$ bin/spark-submit --jars stream-example/jars/spark-streaming-kafka-assembly_2.10-1.6.0.jar 
        --master spark://ip-172-31-2-135:7077  kafka_filter.py localhost:2181 $topic-name`
"""

#  spark-submit --jars stream-example/jars/spark-streaming-kafka-assembly_2.10-1.6.0.jar --master spark://ip-172-31-2-135:7077 kafka_wordcount.py 52.72.109.43(public IP of broker) price_data_part(topic) 

from __future__ import print_function

import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext

from pyspark.streaming.kafka import KafkaUtils

from datetime import datetime

from pyspark_cassandra import streaming

#####################################################
import os
from pyspark.sql import SQLContext, Row

def getSqlContextInstance(sparkContext):
    if ('sqlContextSingletonInstance' not in globals()):
        globals()['sqlContextSingletonInstance'] = SQLContext(sparkContext)
    return globals()['sqlContextSingletonInstance']

#####################################################

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: kafka_filter.py <zk> <topic>", file=sys.stderr)
        exit(-1)

    sc = SparkContext(appName="PythonStreamingKafkaSQL")
    ssc = StreamingContext(sc, 2)

    ##################################################
    zkQuorum, topic = sys.argv[1:]
    kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})
    lines = kvs.map(lambda x: x[1])
    ##################################################

    ##  1: pick-up timtamp       ;   2: drop-off timestamp   ;    5,6 : pick-up location
    ##  7,8 : drop-off location  ;   9: number of passages   ;     10 : distance
    ##  11  : fare               ;  14: tips                 ;     18 : total pay
    ##  19  : payment type
    ##  total 21 arguments

    #lines.pprint()

#    counts = lines.flatMap(lambda line: line.split("\n")) \
#        .map(lambda x: x.split(',') )#.filter(lambda x: float(x[18]) != 0) \
#    counts = lines.flatMap(lambda x: x.split('\n')).map(lambda x: x.split(',') )
    counts = lines.map(lambda x: x.replace('\n','').split(',') ).filter(lambda x: float(x[18]) != 0) \
          .map(lambda x: [
           datetime.strptime(x[1].encode('utf-8'),'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d'),\
           datetime.strptime(x[1].encode('utf-8'),'%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S'),\
           float(x[10]), \
           (float(x[7]),float(x[8])), \
           datetime.strptime(x[2].encode('utf-8'),'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d'),\
           datetime.strptime(x[2].encode('utf-8'),'%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S'),\
           float(x[11]), int(x[19]), (float(x[5]),float(x[6])), \
           int(x[9]), float(x[14]),float(x[14])/float(x[18]),float(x[18]) ] )

    ## new index assigned:
    ##  0,1: pick-up date, time   ;     2: distance           ;  3: drop-off location
    ##  4,5: drop-off date, time  ;     6: fare               ;  7: paytype
    ##  8: pick-up location       ;     9: number of passages ;  10: tips
    ##  11: tipsratio             ;    12: totalpay

    ## pick-up location filter:
    #counts = counts.filter(lambda x :  (-74.0 < x[8][0] < -73.8) &  (41.0 > x[8][1] > 40.7) )

    ## pick-up date filter:
    counts = counts.filter(lambda x : (x[0] == '2015-06-01') or (x[0]=='2015-06-02'))

    ## payment-type filter: (no need, filtered in the static batch procsses)
    #counts = counts.filter(lambda x: x[7] == 1)

datetime.now().strftime("%Y%m%d %H%M%S")
    ## pic-up time filter:
    #counts = counts.filter(lambda x:  '05:59:59' > x[1] > '05:00:00')
#    counts = counts.filter(lambda x:  '21:59:59' > x[1] > '21:00:00')

#    counts.pprint()


    output = counts.map(lambda x:[x[0], x[1], x[11] ] )
    #output.pprint()

    #counts.map(lambda x:{"date":x[0],"time":x[1],"tips":x[11]} ).saveToCassandra("test", "playtest" )
    # save RDD to cassandra 

    #tips = counts.map(lambda x: x[11]).reduce(lambda a,b :a+b)
    #tips.pprint()

    totalcounts = output.count()
    totalcounts.pprint()


    # Convert RDDs of the words DStream to DataFrame and run SQL query
    def process(time, rdd):
        print("========= %s =========" % str(time))

        # Get the singleton instance of SQLContext  
        sqlContext = getSqlContextInstance(rdd.context)

        # Convert RDD[String] to RDD[Row] to DataFrame  
        rowRdd = rdd.map(lambda w: Row(date=w[0], time=w[1], tips=w[2]))
        wordsDataFrame = sqlContext.createDataFrame(rowRdd)
        #wordsDataFrame = sqlContext.createDataFrame(output,["date","time", "tips"])

        # Register as table
        wordsDataFrame.registerTempTable("outputTable")
        #wordsDataFrame.show()

        # Do word count on table using SQL and print it
        testDataFrame = sqlContext.sql("select * from outputTable ORDER BY tips  DESC limit 5")
        summaryDataFrame = sqlContext.sql("select min(tips) as min, max(tips) as max, avg(tips) as avg from outputTable")
        
#        summaryDataFrame.saveToCassandra("test", "playtest" )# save RDD to cassandra

        testDataFrame.write.format("org.apache.spark.sql.cassandra").options(table="playtest",keyspace="test").save(mode="append")

        #testDataFrame.show()
        summaryDataFrame.show()



    output.foreachRDD(process)
    ssc.start()
    ssc.awaitTermination()
