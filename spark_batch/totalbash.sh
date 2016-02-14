#!/bin/bash

# code: $1 "yellow" + year + "_cassandra.py"
# input data source : $2 .../user/yellow/yellow_2009-01
# output cql table (daily) : $3  cassandra table name y_2009_01_01
# output txt table (daily) : $4  text format 

# pseudo code:
# ---- loop for $1 = y_2009_01_01, y_2009_01_02, .... y_2009_01_31  ---
#cqlsh -e' use taxi; CREATE Table y_2009_01_01 (pick_loc text, pick_date text, pick_time text, dist text,  drop_loc text,drop_tdate text, drop_time text, fare text, paytype text, tips text, tipsratio text, totalpay text, ppl_count text,  PRIMARY KEY(pick_date, pick_time) )  WITH CLUSTERING ORDER BY (pick_time ASC);'
# ---- loop is done  --------------------------------------------------
#
#./spark-cassandra.sh yellow2009_cassandra.py hdfs://52.72.109.43:9000/user/yellow/yellow_2009-01 y_2009_01_01
#
# cqlsh -e'use taxi; SELECT * FROM y_2009_01_01' > output.txt
#


cqlsh -e'use taxi_2009; CREATE Table y_2009_02_25 (pick_loc text, pick_date text, apick_time text, dist text,  drop_loc text,drop_tdate text, drop_time text, fare text, paytype text, tips text, tipsratio text, totalpay text, ppl_count text,  PRIMARY KEY (apick_time, drop_time),  );'

