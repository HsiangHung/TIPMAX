#!/bin/bash
spark-submit --master spark://ip-172-31-2-135:7077 --packages TargetHolding/pyspark-cassandra:0.2.4 --conf spark.cassandra.connection.host=172.31.2.135  yellow2009_cassandra.py hdfs://52.72.109.43:9000/user/yellow/yellow_2009-07

