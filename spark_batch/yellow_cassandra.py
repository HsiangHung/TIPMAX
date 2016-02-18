#
#   deal with 2009 yellow cab data, 
#   note: the batch process includes replace ',,' to ',0,'
#   otherwise it will show error!
#
#  This version considers rearranging the column names to match 
#  the regulation in Cassandra: the column names are alphabetically ordered.
#  e.g. ["pickl", "pickt", "dist", "dropl", "dropt", "fare","paytype","tips", "totalpay"]
#   pickl and pickt are primary keys so are always ahead.
#   but the remaining "dist", "dropl"... are in alphabetical order.
#
# spark-submit --master spark://ip-172-31-2-135:7077 --packages TargetHolding/pyspark-cassandra:0.2.4 --conf spark.cassandra.connection.host=privateIP  $1  $2
#
#   $1=sys.argv[0]: code: green_cassandra.py, $2=sys.argv[1]: input file source: hdfs://public-IP:9000/user/green_2009
#
#
#  before exceuting, need to create keyspace and table:
#  https://sites.google.com/a/insightdatascience.com/dataengineering/devsetups/cassandra-dev
#
#  (1)  cqlsh, and then
#   "CREATE KEYSPACE taxi WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 3};"
#
#  (2)  use taxi; and then
#     "  CREATE Table taxidata (pick_loc text, pick_date text, pick_time text, dist text,  drop_loc text,drop_tdate text, drop_time text, fare text, paytype text, tips text, tipsratio text, totalpay text, ppl_count text,  PRIMARY KEY(pick_date, pick_time) )  WITH CLUSTERING ORDER BY (pick_time ASC);"
#
#
from __future__ import print_function
import sys
from operator import add
from pyspark import SparkContext, SparkConf

import pyspark_cassandra
from pyspark.sql import SQLContext

from datetime import datetime

#import time
#import datetime

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: sort <file>", file=sys.stderr)
        exit(-1)

    sc = SparkContext(appName="Python2009Yellow")
    text = sc.textFile(sys.argv[1], 1)
    #text = sc.textFile("hdfs://52.72.109.43:9000/user/green_2015-01")

    lines = text.flatMap(lambda x: x.replace(",,",",0,").split('\n'))

    ##   1: pick-up timtamp   |      2: drop-off timestamp    |     3: number of passagers      
    ##   4: distance          |    5,6: pick-up location      |  9,10: drop-off location
    ##  11: payment type      |     12: fare                  |    15: tips                  
    ##  17: total pay

    lines = lines.map(lambda x: x.split(',') ).filter(lambda x: float(x[17]) != 0) \
       .map(lambda x: [
           datetime.strptime(x[1].encode('utf-8'),'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d'),\
           int(str(datetime.strptime(x[1],'%Y-%m-%d %H:%M:%S').strftime('%H'))+
                    str(datetime.strptime(x[1],'%Y-%m-%d %H:%M:%S').strftime('%M'))+
                    str(datetime.strptime(x[1],'%Y-%m-%d %H:%M:%S').strftime('%S'))),\
           int(str(datetime.strptime(x[2],'%Y-%m-%d %H:%M:%S').strftime('%H'))+
                    str(datetime.strptime(x[2],'%Y-%m-%d %H:%M:%S').strftime('%M'))+
                    str(datetime.strptime(x[2],'%Y-%m-%d %H:%M:%S').strftime('%S'))),\
           float(x[4]), \
           (float(x[9]),float(x[10])), \
           datetime.strptime(x[2].encode('utf-8'),'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d'),\
           float(x[12]), str(x[11]).lower(), \
           (float(x[5]),float(x[6])), \
           int(x[3]), float(x[15]),float(x[15])/float(x[17]),float(x[17]) ] )

    ## new index assigned:
    ##  0: pick_date              |    1: pick_time           |    2: drop_ time    |  3: distance     
    ##  4: drop-off location      |    5: drop-off date       |    6: fare          |  7: paytype  
    ##  8: pick-up location       |    9: number of passages  |   10: tips          | 11: tipsratio          
    ## 12: totalpay


#    datelist = [('2009-03-27','y_2009_03_27')]


    datelist =list()
    for i in range(0,30):
#        print (i)
        datelist.append(('2009-04-'+str(i+1).zfill(2),'y_2009_04_'+str(i+1).zfill(2)))


#    print (datelist)
#    sc.stop()


    for date, tablename in datelist:

        ## pick-up date filter:
        sortedCount = lines.filter(lambda x : x[0] == date )

        ## payment-type filter:
        sortedCount = sortedCount.filter(lambda x : x[7] == 'credit')

        ## pick-up location filter:
        sortedCount = sortedCount.filter(lambda x :  (x[8][0] != 0.0) &  (x[8][1] != 0) )

        ## pic-up time filter:
        #sortedCount = sortedCount.filter(lambda x:  '21:59:59' > x[1] > '21:00:00')

        #######################################  for cassandra ####################
        sqlContext = SQLContext(sc)
        Ticks = sqlContext.createDataFrame(sortedCount, ["apick_date","bpick_time", "drop_time", "dist","drop_loc",\
            "drop_tdate","fare","paytype", "pick_loc","ppl_count","tips","tipsratio","totalpay"])
        Ticks.write.format("org.apache.spark.sql.cassandra").options(table =tablename, keyspace="taxi_2009").save()
        ##############################  for cassandra ###########################


#    sortedCount.saveAsTextFile("hdfs://52.70.48.150:9000/user/test33")

    # write to local disk:
#    output = sortedCount.collect()
#    index=0
#    for line in output:
       #print (line)
#       print ( "   ".join(repr(x) for x in line))
#       index += 1
#       if index == 20: break

    sc.stop()
