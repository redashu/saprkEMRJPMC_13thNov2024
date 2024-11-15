from pyspark import SparkContext
import random

sc = SparkContext(appName="WordCountWithSalting")

# Read data
rdd = sc.textFile("hdfs:///hello/a.txt")

# Split into words
words = rdd.flatMap(lambda line: line.split())

# Add salting (randomly partition the occurrences of the same word)
salted_words = words.map(lambda word: (word + "_" + str(random.randint(1, 10)), 1))

# Perform word count with reduceByKey
word_count = salted_words.reduceByKey(lambda a, b: a + b)

# Remove salt by keying by the original word
final_word_count = word_count.map(lambda x: (x[0].split("_")[0], x[1])) \
                             .reduceByKey(lambda a, b: a + b)

# Collect and print the result
for word, count in final_word_count.collect():
    print(f"{word}: {count}")
