from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, split
from pyspark import StorageLevel

# Initialize Spark session with performance configurations
spark = SparkSession.builder \
    .appName("Optimized Word Count") \
    .config("spark.sql.shuffle.partitions", "200") \
    .config("spark.sql.autoBroadcastJoinThreshold", "10MB") \
    .config("spark.executor.memory", "8g") \
    .config("spark.driver.memory", "4g") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.files.maxPartitionBytes", "134217728") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .config("spark.kryo.registrationRequired", "true") \
    .getOrCreate()

# Read input text data from the local disk (as it's on EMR node, not S3)
input_path = "file:///mnt/wordcount_data.txt"  # Adjust path if needed

# Read the text file into a DataFrame
df = spark.read.text(input_path)

# Perform the word count transformation
words_df = df.select(explode(split(col("value"), "\\s+")).alias("word"))

# Perform the word count aggregation
word_count_df = words_df.groupBy("word").count()

# Cache the word count DataFrame to optimize repeated actions
word_count_df.cache()

# Show the result (in production, you might want to write to a file or database)
word_count_df.show()

# Optionally, checkpoint the DataFrame to optimize shuffle stages and enable fault tolerance
# word_count_df.checkpoint()

# Stop the Spark session after the job is complete
spark.stop()

# spark-submit \
#   --deploy-mode cluster \
#   --master yarn \
#   --conf "spark.sql.shuffle.partitions=200" \
#   --conf "spark.sql.autoBroadcastJoinThreshold=10MB" \
#   --conf "spark.executor.memory=8g" \
#   --conf "spark.driver.memory=4g" \
#   --conf "spark.sql.adaptive.enabled=true" \
#   --conf "spark.sql.files.maxPartitionBytes=134217728" \
#   --conf "spark.serializer=org.apache.spark.serializer.KryoSerializer" \
#   --conf "spark.kryo.registrationRequired=true" \
#   --conf "spark.sql.files.maxPartitionBytes=134217728" \
#   word_count.py
