from pyspark.sql import SparkSession

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Spark SQL Optimizations") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.skewJoin.enabled", "true") \
    .config("spark.sql.shuffle.partitions", "200") \
    .getOrCreate()


# Load data from S3
input_path = "s3a://ashu-jpmc-emr-bucket/datasets/customer.csv"  # Update with your S3 bucket path
df = spark.read.csv(input_path, header=True, inferSchema=True)

# Register DataFrame as SQL temporary view
df.createOrReplaceTempView("employee_data")

# Sample SQL Transformation - Using Catalyst Optimizer & AQE
transformed_df = spark.sql("""
    SELECT city, AVG(salary) as avg_salary, COUNT(*) as count
    FROM employee_data
    GROUP BY city
    HAVING COUNT(*) > 5
    ORDER BY avg_salary DESC
""")

# Cache the DataFrame for repeated access
transformed_df.cache()

# Show transformed data
transformed_df.show()

# Write the result to Parquet format back to S3
output_path = "s3a://ashu-jpmc-emr-bucket/outputs/output_employee_data.parquet"  # Update with your output S3 path
transformed_df.write.parquet(output_path)

# Stop the Spark session
spark.stop()
