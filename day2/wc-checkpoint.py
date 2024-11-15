from pyspark.sql import SparkSession

# Initialize Spark session and context
spark = SparkSession.builder.appName("WordCount").getOrCreate()

# Define storage for checking make sure you have the directory 
spark.sparkContext.setCheckpointDir("hdfs:///common-data/text/checkpoint")

rdd1 = spark.sparkContext.textFile("hdfs:///common-data/text/team2.txt")

# word count code
rdd3 = rdd1.flatMap(lambda line: line.split(" "))
rdd4 = rdd3.map(lambda word: (word,1))
rdd5 = rdd4.reduceByKey(lambda a, b: a + b)


# use other opitons like cache , repartions then -- checkpoint

rdd5.checkpoint() 
# Collect the results and print them
wc = rdd5.collect()
# using for loop to print words and count 
for word,count in wc:
    print(f"{word}: {count}")
    
# stop spark session 
spark.stop()
# Display the top 10 words for verification