from pyspark.sql import SparkSession

# Initialize Spark session with specific configurations for S3
spark = SparkSession.builder \
    .appName("S3OptimizedWrite") \
    .config("spark.sql.sources.partitionOverwriteMode", "dynamic") \
    .config("spark.sql.parquet.compression.codec", "snappy") \
    .config("spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version", "2") \
    .config("spark.sql.parquet.enableVectorizedReader", "true") \
    .config("spark.hadoop.fs.s3a.committer.name", "magic") \
    .config("spark.hadoop.fs.s3a.committer.magic.enabled", "true") \
    .config("spark.hadoop.fs.s3a.fast.upload", "true") \
    .config("spark.hadoop.fs.s3a.fast.upload.buffer", "disk") \
    .getOrCreate()

# Read CSV data from S3
df = spark.read.csv("s3://your-bucket/input-data/sample.csv", header=True, inferSchema=True)

# Perform transformations
df_transformed = df.filter(df["age"] > 25).withColumn("age_group", df["age"] / 10)

# Cache the transformed DataFrame for reuse
df_transformed.cache()

# Repartition the DataFrame to optimize the write parallelism
df_transformed = df_transformed.repartition(4, "age_group")  # Partition by "age_group"

# First action: Write the transformed data back to S3 in Parquet format with compression
df_transformed.write \
    .mode("overwrite") \
    .option("compression", "snappy") \
    .partitionBy("age_group") \
    .parquet("s3://your-bucket/output-data/optimized-parquet")

# Second action: Count the rows in the transformed DataFrame to demonstrate caching and stage reuse
count = df_transformed.count()
print(f"Row count after transformation: {count}")

# Stop the Spark session
spark.stop()