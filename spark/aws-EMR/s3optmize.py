from pyspark.sql import SparkSession

# Initialize Spark session with optimizations for S3 access and Parquet compression
spark = SparkSession.builder \
    .appName("S3OptimizedDataProcessing") \
    .config("spark.sql.parquet.compression.codec", "snappy") \
    .getOrCreate()

# Define S3 input and output paths
input_path = "s3://your-bucket/input-data/"
output_path = "s3://your-bucket/output-data/"

# Read data from S3 (Assuming CSV format)
df = spark.read.csv(input_path, header=True, inferSchema=True)

# Show the original data
print("Original Data:")
df.show()

# Perform a transformation: Filter rows where age is greater than 25
df_transformed = df.filter(df["age"] > 25)

# Repartition the data for better parallelism when processing (e.g., 10 partitions)
df_repartitioned = df_transformed.repartition(10)

# Cache the data for faster access if reused
df_repartitioned.cache()

# Perform some additional transformation (example: adding a new column)
df_transformed_with_column = df_repartitioned.withColumn("new_column", df_repartitioned["age"] * 2)

# Coalesce to a smaller number of partitions before writing to avoid too many small files
df_coalesced = df_transformed_with_column.coalesce(1)

# Write the transformed and optimized data back to S3 as Parquet format with Snappy compression
df_coalesced.write.parquet(output_path, mode="overwrite")

# Stop the Spark session
spark.stop()
