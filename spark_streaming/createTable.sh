#!/bin/bash
cqlsh -e'use test; CREATE Table playtest (adate text, btime bigint, cloc_x text, dloc_y text, etips text, fratio text, pay text, PRIMARY KEY (adate, btime), );'
