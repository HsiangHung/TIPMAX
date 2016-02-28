#!/bin/bash

python downloadData.py

#python wgetData.py

head -n  1 dataText

tail -n +2 dataText > dataText2

head -n -1 dataText2 > dataText

python textrefine.py > $1

rm dataText
rm dataText2
