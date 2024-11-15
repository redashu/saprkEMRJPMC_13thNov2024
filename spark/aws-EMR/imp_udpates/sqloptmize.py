from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg

# Initialize Spark session with optimizations
spark = SparkSession.builder \
    .appName("SparkSQLOptimizations") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .config("spark.sql.adaptive.skewJoin.enabled", "true") \
    .config("spark.sql.shuffle.partitions", "200") \
    .getOrCreate()

# Load sample data for Customers and Orders
customers = spark.read.option("header", "true").csv("hdfs:///path/to/customers.csv")
orders = spark.read.option("header", "true").csv("hdfs:///path/to/orders.csv")

# Caching tables for reuse and faster access
customers.cache()
orders.cache()

# Applying bucketing on Orders table based on 'customer_id' to optimize join performance
orders.write.bucketBy(10, "customer_id").sortBy("customer_id").saveAsTable("bucketed_orders")

# Reading the bucketed data for orders
bucketed_orders = spark.table("bucketed_orders")

# Sample Query with Optimizations
# 1. Join customers with bucketed orders to calculate average order value by customer segment
# 2. Filtering and grouping to show meaningful insights

# Enable the logical and physical plan display for debugging and optimization insight
spark.conf.set("spark.sql.ui.explainMode", "extended")

query = """
    SELECT c.customer_id, c.customer_segment, 
           COUNT(o.order_id) AS total_orders, 
           AVG(o.order_value) AS avg_order_value
    FROM customers AS c
    JOIN bucketed_orders AS o
    ON c.customer_id = o.customer_id
    WHERE o.order_status = 'completed'
    GROUP BY c.customer_id, c.customer_segment
"""

# Execute query with AQE optimizations enabled
result_df = spark.sql(query)

# Displaying physical and logical plans
print("Logical Plan:")
result_df.explain(extended=True)

print("Physical Plan:")
result_df.explain(mode="extended")

# Caching the result for subsequent operations
result_df.cache()

# Show the result
result_df.show(10)

# Perform additional operations on the cached result (if needed)
result_df.filter(col("avg_order_value") > 100).show(10)

# Stop Spark session
spark.stop()
