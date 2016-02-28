#!/bin/bash


## run as ./wgetData.sh https://storage.googleapis.com/tlc-trip-data/2009/yellow_tripdata_2009-02.csv yellow_tripdata_2009-02.csv  yellow_2009-02

wget $1


head -n  3 $2
head -n  1 $2 > Head

echo 'OK'

python countHead.py

tail -n +3 $2 > dataText2


head -n  2 dataText2

head -n -1 dataText2 > dataText

python textrefine.py > $3

rm dataText
rm dataText2

python checktext.py $3
