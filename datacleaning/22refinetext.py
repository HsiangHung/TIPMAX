
## doing if there exists ",,", clean to ","
## usually this means an extra column: eg. yellow_2010-02 and 2010-03
import re
import fileinput

import sys

#hd = open('dataText')
#hd= open('test_taxi.csv')                                                                                              

hd = open(sys.argv[1])

for line in hd:
        line = line.rstrip().replace("\r", " ")
        #newline = line[:-2]
        line = line.replace(",,", ",")
        print line

