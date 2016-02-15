# TIP MAX

## Motivation

My Insight project is to design a web app, named Tip Max, to help (NYC) taxi drivers to maximize their incomes. It can visualize the pick-up locations, like ![](figures/fig1.png) and the profiles of the tip percentage (defined by tips/fare) 
and the total fare that passanges paid over the New York city in the past years. The latter two features are visualized using heatmap, like ![](figures/fig2.png) The Tip Max is able to help taxi drivers to know the best location to increase their income. The web is available at http://tipmaxnyc.xyz.


##Technical Details

The whole project pipeline icnludes two parts: static pipeline and real-time streaming.

### Static pipeline

For the first part, I fetched the taxi data from the New York city government website, which offered 2009 Jan.- 2015 June data. The total amount is about 200GB and there are 13 billions events in the datasets. Also, the data is not ordered in time. So after loading the clean data (using Pythong to clean data) into the file distributed system HDFS, first we perform the batch processes to group the data by date. The pipeline is as follows ![](figures/fig3.png)
I chose to use Apache Spark to do the batch process and store the time-ordered outcome in the NoSQL database, Cassandra. Cassandra plays a good role to provide high availability in writing. When one wishes to visualize the pick-up locations, tips or fare profiles for a certain date and time, the Flask will query data from Cassandra and shows the profile in MapBox (like previous two figures).

### Real-time streaming process 

![](figures/fig4.png)
The second part is the real-time streaming process. The NYC does not provide live-streaming taxi data. Based on this reason, I engineered the real-time streaming data by repeatedly reading a file (which comes from a historial daily data file) and transporting the messages. In this case we can mock real-time data source and implement Kafka to ingest data. The Python code, tick_kafkaproducer.py, is designed for this function, and, meanwhile, it plays a role as a Kafka producer. On the other hand, the Spark Streaming is running simultaneously, and plays as a Kafka consumer role to fetch the data. 

After collecting data, the Spark streaming filters out the events based on the current (eastern) time, and then we implement the Spark-SQL to do aggregation operations, such as listing top-five high-tip locations and finding averaged/maximum tips during the time window. The time window could be few seconds or a minute, set in Spark Streaming. The aggregated outputs are written into the Cassandra. For the real-time streaming process, with a proper schema, Cassandra is a natural database tool to store time-ordered data.


![](figures/fig5.png)
The above figure shows a mocked real-time result. The averaged tips and max tips are the aggregated outputs from the data ingestion from Kafka and batch process from Spark Streaming filtering out "current time" over the New York city. In reality, the plot needs a minute for a period to update since the data ingestion needs a minute for a cycle. However, the figure, demonstrated above, simulates every few seconds to update the profile. The data aggregated time can be arbitrarily tuned. With these processes, one can further consider to compare the features on different locations, e.g. airports or nearby Time Square, etc.



### Work platform
The entire work is preformed on the AWS using four m4.large instances.
