from pyspark.sql import SparkSession
from pyspark import SparkContext

# Initialize Spark session and context
spark = SparkSession.builder \
    .appName("WordCount") \
    .config("spark.sql.shuffle.partitions", "200") \  # Tuning for shuffle partitions
    .config("spark.executor.memory", "8g") \  # Memory per executor
    .config("spark.driver.memory", "4g") \  # Memory for driver
    .getOrCreate()

# Use SparkContext to initialize RDDs
sc = spark.sparkContext

# Define the file path for input data on the local file system (primary node)
# Assuming the data is stored in /mnt/data or another directory on the primary node
input_path = "/mnt/data/word_count_data.txt"  # Adjust this path to where your data is stored on the EMR primary node

# Read the data from the input file (local file system)
text_data = sc.textFile(input_path)

# Perform word count
word_count = (text_data.flatMap(lambda line: line.split())  # Split each line into words
                     .map(lambda word: (word, 1))  # Map each word to (word, 1)
                     .reduceByKey(lambda a, b: a + b))  # Aggregate by key (word)

# Collect the results and print them
results = word_count.collect()

# Display the top 10 words for verification
for word, count in results[:10]:  # Show top 10
    print(f"{word}: {count}")

# Optionally, save the results to an output file on the local file system
output_path = "/mnt/data/output/word_count_results"  # Adjust for output location
word_count.saveAsTextFile(output_path)

# Stop the Spark session when done
spark.stop()

# spark-submit \
#   --deploy-mode cluster \
#   --master yarn \
#   --conf spark.sql.shuffle.partitions=200 \
#   --conf spark.executor.memory=8g \
#   --conf spark.driver.memory=4g \
#   word_count.py
