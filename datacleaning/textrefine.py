import re
import fileinput

hd = open('dataText')
#hd= open('test_taxi.csv')                                                                                              

for line in hd:
#for line in fileinput.FileInput('dataText',inplace=1):
#    line = filter(lambda x: not re.match(r'^\s*$', x), line)\
#       .rstrip().replace(",,", ",").replace("\r", " ")
#    if line.rstrip():
        line = line.rstrip().replace("\r", " ")
        #newline = line[:-2]
        line = line.replace(",,", ",0,")
        print line

