from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, abs

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Credit Card Fraud Detection") \
    .getOrCreate()

# Load the CSV data
data_path = "hdfs:///ok/cc.csv"  # Update with the actual file path
df = spark.read.csv(data_path, header=True, inferSchema=True)

# Preview the data
df.show()

# Step 3: Calculate the Average Transaction Amount per Customer
avg_transaction_df = df.groupBy("Customer_ID").agg(avg("Amount").alias("Average_Amount"))

# Step 4: Join the original dataset with the average transaction data
df_with_avg = df.join(avg_transaction_df, "Customer_ID")

# Step 5: Calculate deviation from the average and flag possible frauds
# Here, we define "suspicious" as transactions exceeding twice the average amount.
suspicious_transactions = df_with_avg.withColumn(
    "Deviation", abs(col("Amount") - col("Average_Amount"))
).filter(col("Amount") > 2 * col("Average_Amount"))

# Show suspicious transactions
print("Suspicious Transactions (Potential Fraud):")
suspicious_transactions.show()

# Stop the Spark session
spark.stop()
