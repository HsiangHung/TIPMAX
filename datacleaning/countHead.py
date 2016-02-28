import sys

# to check if each line has consistent number of row.

hd = open('Head')

for line in hd:
    line = line.rstrip().split(',')
    column = len(line)
    print line, len(line)
    break

