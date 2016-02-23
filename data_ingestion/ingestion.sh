#spark-submit --jars jars/spark-streaming-kafka-assembly_2.10-1.6.0.jar --master spark://ip-172-31-2-134:7077  $1 localhost:2181 $2

python tick_kafkaproducer.py  52.71.0.86  2009-02-12.csv  1

#spark-submit --jars jars/spark-streaming-kafka-assembly_2.10-1.6.0.jar --master spark://ip-172-31-2-134:7077  --packages TargetHolding/pyspark-cassandra:0.2.4 --conf spark.cassandra.connection.host=172.31.2.134  $1  localhost:2181 $2 


