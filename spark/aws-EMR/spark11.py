# rdd_example.py

from pyspark import SparkContext

# Initialize SparkContext
sc = SparkContext(appName="RDD Example")

# Create an RDD from a list
data = [1, 2, 3, 4, 5, 6]
rdd = sc.parallelize(data)

# Transformations
rdd_map = rdd.map(lambda x: x * 2)  # Multiply each element by 2
rdd_filter = rdd_map.filter(lambda x: x > 5)  # Filter elements greater than 5

# Action
result = rdd_filter.collect()  # Collect results to driver
print("Filtered Results:", result)  # Output: Filtered Results: [6, 8, 10, 12]

# Stop SparkContext
sc.stop()
