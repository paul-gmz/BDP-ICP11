import sys
import os

os.environ["SPARK_HOME"] = "C:\\Installations\\spark-2.4.5-bin-hadoop2.7"
os.environ["HADOOP_HOME"]="C:\\Installations\\Hadoop"

from pyspark import SparkContext
from pyspark.streaming import StreamingContext



# Create a local StreamingContext with two working thread and batch interval of 5 second
sc = SparkContext("local[2]", "NetworkedCharacterFrequency")
ssc = StreamingContext(sc, 5)

# Create a DStream that will connect to hostname:port, like localhost:9999
lines = ssc.socketTextStream("localhost", 9999)

# Split each line into words
words = lines.flatMap(lambda line: line.split(" "))

pairs = words.map(lambda word: (len(word), word))
wordCounts = pairs.reduceByKey(lambda x, y: x + "," + y)

wordCounts.pprint()

ssc.start()
ssc.awaitTermination()