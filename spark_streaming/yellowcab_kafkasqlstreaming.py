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

#spark-submit --jars jars/spark-streaming-kafka-assembly_2.10-1.6.0.jar --master spark://ip-172-31-2-134:7077  --packages TargetHolding/pyspark-cassandra:0.2.4 --conf spark.cassandra.connection.host=172.31.2.134  sqlkafka_filter.py localhost:2181 datatest > test

# the compiler including cassandra and streaming SQL is
#
#spark-submit --jars jars/spark-streaming-kafka-assembly_2.10-1.6.0.jar --master spark://ip-172-31-2-134:7077  --packages TargetHolding/pyspark-cassandra:0.2.4 --conf spark.cassandra.connection.host=172.31.2.134  $1 localhost:2181 $2 > test
## $1: code ;    $2: topic from kafka

from __future__ import print_function

import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext

from pyspark.streaming.kafka import KafkaUtils

from datetime import datetime

from pytz import timezone

from pyspark_cassandra import streaming

#####################################################
import os
from pyspark.sql import SQLContext, Row

def getSqlContextInstance(sparkContext):
    if ('sqlContextSingletonInstance' not in globals()):
        globals()['sqlContextSingletonInstance'] = SQLContext(sparkContext)
    return globals()['sqlContextSingletonInstance']

#####################################################

# intervalt is always larger than the time which reading a whole file
intervalt= 60

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: kafka_filter.py <zk> <topic>", file=sys.stderr)
        exit(-1)

    sc = SparkContext(appName="PythonStreamingKafkaSQL")
    ssc = StreamingContext(sc, intervalt)

    ##################################################
    zkQuorum, topic = sys.argv[1:]
    kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})
    lines = kvs.map(lambda x: x[1])
    ##################################################

    ## new index assigned:
    ##  0: pick_date              |    1: pick_time           |    2: drop_ time    |  3: distance
    ##  4: drop-off location      |    5: drop-off date       |    6: fare          |  7: paytype
    ##  8: pick-up location       |    9: number of passages  |   10: tips          | 11: tipsratio
    ## 12: totalpay

    counts = lines.map(lambda x: x.replace('\n','').replace(' ','').split('|') )

 
    #counts.pprint()

    output = counts.map(lambda x:[x[0].encode('utf-8'), int(x[1]), float(x[8].replace('[','').replace(']','').split(',')[0]), float(x[8].replace('[','').replace(']','').split(',')[1]), float(x[10]), float(x[11]), float(x[12]) ] )
    ## date, pick-time, pick_loc(x), pick_loc(y), tips, tips-ratio, total-fare

 
    ## pic-up time filter:
    #output = output.filter(lambda x:  time2 > x[1] > realtime)

    #output = output.filter(lambda x:  (x[3] == 0.0) & (x[12] != 0))  ## for zero distance but with finite fare
    
    ## pick-up location filter:
    #counts = counts.filter(lambda x :  (-74.0 < x[8][0] < -73.8) &  (41.0 > x[8][1] > 40.7) )  

    #output.pprint()


    # Convert RDDs of the words DStream to DataFrame and run SQL query
    def process(time, rdd):
        print("========= %s =========" % str(time))

        now_time = datetime.now(timezone('US/Eastern'))
        hour = now_time.strftime('%H')
        mins = now_time.strftime('%M')
        sec  = now_time.strftime('%S')

        realtime = int(str(hour)+str(mins)+str(sec))
        time2   =  realtime+100   ## 1min = add 100 in bigint format, data query

        print (realtime, time2)

        ## pic-up time filter:
        rddUpdate = rdd.filter(lambda x:  time2 > x[1] > realtime)


        # Get the singleton instance of SQLContext  
        sqlContext = getSqlContextInstance(rddUpdate.context)

        # Convert RDD[String] to RDD[Row] to DataFrame  
        rowRdd = rddUpdate.map(lambda w: Row(adate=w[0],btime=w[1],cloc_x=w[2],dloc_y=w[3], etips=w[4],\
                            fratio=w[5], pay=w[6]))
        wordsDataFrame = sqlContext.createDataFrame(rowRdd)
        #wordsDataFrame = sqlContext.createDataFrame(output,["date","time", "tips"])

        # Register as table
        wordsDataFrame.registerTempTable("outputTable")
        #wordsDataFrame.show()

        # Do word count on table using SQL and print it
        testDataFrame = sqlContext.sql("select * from outputTable ORDER BY fratio  DESC limit 5")
        summaryDataFrame = sqlContext.sql("select min(fratio) as min, max(fratio) as max, avg(fratio) as avg from outputTable")
        
#        summaryDataFrame.saveToCassandra("test", "playtest" )# save RDD to cassandra

        testDataFrame.write.format("org.apache.spark.sql.cassandra").options(table="playtest",keyspace="test").save(mode="append")

        testDataFrame.show()
        summaryDataFrame.show()



    output.foreachRDD(process)
    ssc.start()
    ssc.awaitTermination()
