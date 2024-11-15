from pyspark import SparkContext
import random

sc = SparkContext(appName="WordCountWithSalting")

# Read data
rdd = sc.textFile("hdfs:///hello/a.txt")

# Split into words
words = rdd.flatMap(lambda line: line.split())
word_pairs = words.map(lambda word: (word, 1))

# Add salting (randomly partition the occurrences of the same word)

hash_partitioner = 10  # Number of partitions (you can adjust this based on your cluster size and data)
partitioned_rdd = word_pairs.partitionBy(hash_partitioner, lambda x: hash(x) % hash_partitioner)

# Perform word count with reduceByKey
word_count = partitioned_rdd.reduceByKey(lambda a, b: a + b)

for word, count in word_count.collect():
    print(f"{word}: {count}")

sc.stop()


#spark-submit  --num-executors 4 --executor-memory 3g  --executor-cores 2 --conf spark.sql.shuffle.partitions=100 --conf spark.io.compression.codec=snappy --conf spark.serializer=org.apache.spark.serializer.KryoSerializer  --master yarn wc1.py 