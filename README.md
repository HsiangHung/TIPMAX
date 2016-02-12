# TIPMAX

## Motivation

My Insight project is to design a web app, named Tip Max, to help (NYC) taxi drivers to maximize their incomes. It can visualize the pick-up locations, like ![](figures/fig1.png) the tip percentage, defined by tips/fare ![](figures/fig2.png)
and the total fare that passanges paid profiles over the New York city in the past years. The Tip Max is able to help taxi drivers to know the best location to increase their income. The web is at http://tipmaxnyc.xyz.


## Pipeline

The project pipeline icnludes two parts. I fetched the taxi data from New York city government, which offered 2009-2015 Jun data. The total amount is about 200GB and there are 13 billions events in the data. Also, the data is not ordered in time. So after locaing the data into the distributed file system HDFS, first we perform the batch processes to group the data by date. The pipeline is as follows ![](figures/fig3.png)
I chose to use Spark to do batch process to store the taxi data in Cassandra, ordered by time, and then one can choose a date and time to visualize the distribution.
