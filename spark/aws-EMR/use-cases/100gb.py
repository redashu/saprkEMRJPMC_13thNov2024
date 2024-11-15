from pyspark.sql import SparkSession
from pyspark import SparkConf

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Word Count on 100GB Text Data") \
    .config("spark.executor.memory", "8g") \
    .config("spark.driver.memory", "4g") \
    .config("spark.sql.shuffle.partitions", "200") \
    .config("spark.executor.instances", "6") \
    .config("spark.memory.fraction", "0.6") \
    .getOrCreate()

# Path to the S3 bucket where data is stored
input_path = "s3a://your-bucket-name/your-data/*.txt"  # Update this path with your actual S3 path
output_path = "s3a://your-bucket-name/word-count-output/"  # Update this path for output

# Read the text data from S3
text_rdd = spark.sparkContext.textFile(input_path)

# Perform word count
word_counts = text_rdd.flatMap(lambda line: line.split()) \
                      .map(lambda word: (word, 1)) \
                      .reduceByKey(lambda a, b: a + b)

# Save the result to S3
word_counts.saveAsTextFile(output_path)

# Stop the Spark session
spark.stop()


# spark-submit \
#   --deploy-mode cluster \
#   --master yarn \
#   --num-executors 6 \
#   --executor-memory 8G \
#   --driver-memory 4G \
#   --conf spark.sql.shuffle.partitions=200 \
#   --conf spark.executor.instances=6 \
#   --conf spark.memory.fraction=0.6 \
#   --conf spark.yarn.access.hadoopFileSystems=s3a://your-bucket-name \
#   word_count.py
