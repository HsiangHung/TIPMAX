# TIPMAX

## Motivation

My Insight project is to design a web app, named Tip Max, to help (NYC) taxi drivers to maximize their incomes. It can visualize the pick-up locations, like ![](figures/fig1.png) the tip percentage, defined by tips/fare ![](figures/fig2.png)
and the total fare that passanges paid in the past years. The web is at http://tipmaxnyc.xyz.


## Pipeline

The project pipeline icnludes two parts. I fetched the taxi data from New York city government, which offered 2009-2015 Jun data. The total amount is about 200GB and there are 13 billions events in the data. Also, the data is not ordered in time. So first we can do the batch process to group the data by date. The pipeline is as follows ![](figures/fig3.png)
I chose to use Spark to do batch process to store the taxi data in Cassandra, ordered by time.
