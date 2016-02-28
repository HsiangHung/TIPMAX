#
# Retrieve the webpage as a string
#
#  Python 3.x :
#from urllib import request
#response = request.urlopen("https://storage.googleapis.com/tlc-trip-data/2015/green_tripdata_2015-05.csv")
#  python 2.x :
from urllib2 import urlopen
url = raw_input('Enter : ')
response = urlopen(url)

#response = urlopen("https://storage.googleapis.com/tlc-trip-data/2015/green_tripdata_2015-05.csv")
csv = response.read()
#csv = response.read(4096)

# Save the string to a file
csvstr = str(csv).strip("b'")

lines = csvstr.split("\\n")
f = open("dataText", "w")
for line in lines:
   f.write(line + "\n")
f.close()

