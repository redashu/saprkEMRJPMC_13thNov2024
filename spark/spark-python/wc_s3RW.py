import boto3
import pyspark
from pyspark.sql import SparkSession

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

# Step 6: Split each line into words
words = lines.flatMap(lambda line: line.split())  # This creates a new RDD containing all the words

# Step 7: Create pairs of (word, 1)
word_pairs = words.map(lambda word: (word, 1))  # This creates an RDD of tuples where each tuple is (word, 1)

# Step 8: Sum counts for each word
word_counts = word_pairs.reduceByKey(lambda a, b: a + b)  # This aggregates the counts for each word

# Step 9: Collect word counts and format output
output = word_counts.collect()  # Collect results to the driver
output_formatted = [f"{pair[0]}: {pair[1]}" for pair in output]  # Format output for printing

# Step 10: Print output to the screen
for line in output_formatted:
    print(line)

# Step 11: Write the output back to S3
output_key = 'word_count_output.txt'  # Name of the output file
output_data = '\n'.join(output_formatted)  # Join the output into a single string

# Upload the output to S3
s3_client.put_object(Bucket=bucket_name, Key=output_key, Body=output_data)

# Step 12: Stop the Spark session
spark.stop()

