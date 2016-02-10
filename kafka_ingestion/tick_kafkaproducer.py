#
#  timing tick every 60 s
#
#  run as "python test_producer.py  52.71.0.86  green_2015-06 1"
#
#
import random
import sys
import six
#from datetime import datetime
from kafka.client import KafkaClient
from kafka.producer import KeyedProducer

import time


starttime=time.time()


class Producer(object):

    def __init__(self, addr):
        self.client = KafkaClient(addr)
        self.producer = KeyedProducer(self.client)

    def produce_msgs(self, source_symbol, file_source):
        hd = open(file_source)
        for line in hd:
            print line
            self.producer.send_messages('datatest', source_symbol, line)
            


if __name__ == "__main__":
    #print 'ok'
    args = sys.argv
    ip_addr = str(args[1])              ## public IP of broker
    file_source = sys.argv[2]           ## data source
    partition_key = str(args[3])        ## pairition key, set =1
    prod = Producer(ip_addr)
    while True:
        print 'tick'
        prod.produce_msgs(partition_key, file_source) 
        time.sleep(60.0 - ((time.time() - starttime) % 60.0))


