import boto3
import pyspark
from pyspark.sql import SparkSession
from io import StringIO

# Step 1: Configure AWS credentials
# Ensure you have configured your AWS credentials using aws configure

# Step 2: Initialize Boto3 S3 client
s3_client = boto3.client('s3')

# Step 3: Download file content from S3
bucket_name = 'delvex-software-center'  # Change this to your bucket name
file_key = 'data.txt'  # Change this to your file key

response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
data = response['Body'].read().decode('utf-8')

# Step 4: Initialize Spark session
spark = SparkSession.builder \
    .appName("WordCountFromS3") \
    .getOrCreate()

# Step 5: Load data into an RDD
lines = spark.sparkContext.parallelize(data.splitlines())

# Step 6: Perform word count
word_counts = (
    lines.flatMap(lambda line: line.split())  # Split lines into words
         .map(lambda word: (word, 1))  # Create pairs of (word, 1)
         .reduceByKey(lambda a, b: a + b)  # Sum counts for each word
)

# Step 7: Collect and print the result
for word, count in word_counts.collect():
    print(f"{word}: {count}")

# Step 8: Stop the Spark session
spark.stop()

