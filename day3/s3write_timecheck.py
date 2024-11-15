from pyspark.sql import SparkSession
import time 
spark = SparkSession.builder \
    .appName("ashuS3ONoMagicptimizedWrite") \
    .config("spark.sql.sources.partitionOverwriteMode", "dynamic") \
    .config("spark.sql.parquet.compression.codec", "snappy") \
    .config("spark.sql.parquet.enableVectorizedReader", "true") \
    .config("spark.hadoop.fs.s3a.fast.upload", "true") \
    .config("spark.hadoop.fs.s3a.fast.upload.buffer", "disk") \
    .getOrCreate()

df = spark.read.csv("s3a://ashu-jpmc-emr-bucket/datasets/customer.csv", header=True, inferSchema=True)
#print schema
df.printSchema()
# printing top 5 row data
df.show(5)

# Perform transformations
df_transformed = df.filter(df["age"] > 25).withColumn("age_group", df["age"] / 10)
# Repartition the DataFrame to optimize the write parallelism
df_transformed = df_transformed.repartition(4, "age_group")  # Partition by "age_group"
# First action: Write the transformed data back to S3 in Parquet format with compression
checkin_time = time.time()
df_transformed.write \
    .mode("overwrite") \
    .option("compression", "snappy") \
    .partitionBy("age_group") \
    .parquet("s3a://ashu-jpmc-emr-bucket/myoutput1/")

checkout_time = time.time()
print(f"Execution of s3 write without Magic writes {checkout_time - checkin_time } seconds")
# Second action: Count the rows in the transformed DataFrame to demonstrate caching and stage reuse
count = df_transformed.count()
print(f"Row count after transformation: {count}")
# Stop the Spark session
spark.stop()
