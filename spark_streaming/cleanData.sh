#!/bin/bash
tail -n +4 $1 > data
head -n -2 data > $1
rm data
