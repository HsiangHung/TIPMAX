
import sys

# to check if each line has consistent number of row.

hd = open(sys.argv[1])

for line in hd:
    line = line.rstrip().split(',')
    column = len(line)
    print line, len(line)
    break


for line in hd:
    line = line.rstrip().split(',')
    if len(line) != column:
        print 'something is wrong'
        print line, len(line)
        exit()
   
print 'No problem!'
