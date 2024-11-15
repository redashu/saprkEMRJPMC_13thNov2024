# Spark Performance Optimization with `spark-submit`

## Overview

When submitting a Spark job using `spark-submit`, several configuration options can be utilized to optimize performance, manage resources efficiently, and ensure smooth execution. This document outlines key options to consider when tuning your Spark job for better performance and resource allocation.

## Key Spark-Submit Options for Performance Optimization

### 1. **`--executor-memory`**
   - **Purpose**: Specifies the amount of memory to allocate per executor.
   - **Example**: 
     ```bash
     --executor-memory 8g
     ```
   - **Considerations**: Sufficient memory should be allocated to avoid spills to disk and allow Spark to process larger partitions. This value should be balanced with the number of available executors.

### 2. **`--driver-memory`**
   - **Purpose**: Specifies the amount of memory for the driver node.
   - **Example**: 
     ```bash
     --driver-memory 4g
     ```
   - **Considerations**: Ensure that the driver has enough memory to handle job coordination, task scheduling, and job execution.

### 3. **`--executor-cores`**
   - **Purpose**: Specifies the number of CPU cores per executor.
   - **Example**: 
     ```bash
     --executor-cores 4
     ```
   - **Considerations**: More cores per executor can improve parallelism, but avoid going beyond 5-6 cores to prevent resource contention.

### 4. **`--num-executors`**
   - **Purpose**: Specifies the total number of executors for your job.
   - **Example**: 
     ```bash
     --num-executors 10
     ```
   - **Considerations**: The number of executors should be chosen based on the cluster size and available resources. More executors help with better parallelism.

### 5. **`--conf spark.sql.shuffle.partitions`**
   - **Purpose**: Controls the number of partitions used when shuffling data.
   - **Example**: 
     ```bash
     --conf spark.sql.shuffle.partitions=500
     ```
   - **Considerations**: For operations like `groupBy` or `join`, increasing the number of shuffle partitions can help distribute the load evenly across executors.

### 6. **`--conf spark.default.parallelism`**
   - **Purpose**: Controls the default number of partitions for operations like `reduceByKey`, `join`, etc.
   - **Example**: 
     ```bash
     --conf spark.default.parallelism=200
     ```
   - **Considerations**: Higher parallelism can improve the distribution of tasks, especially for larger datasets.

### 7. **`--conf spark.memory.fraction`**
   - **Purpose**: Controls the fraction of heap memory used for Spark's execution and storage.
   - **Example**: 
     ```bash
     --conf spark.memory.fraction=0.6
     ```
   - **Considerations**: The default value is 0.6, meaning 60% of executor memory is used for Spark operations. You can adjust this based on job requirements.

### 8. **`--conf spark.memory.storageFraction`**
   - **Purpose**: Controls the fraction of executor memory used for storage (caching RDDs).
   - **Example**: 
     ```bash
     --conf spark.memory.storageFraction=0.5
     ```
   - **Considerations**: Higher values help if you're caching data heavily, but may affect operations requiring more memory.

### 9. **`--conf spark.shuffle.compress`**
   - **Purpose**: Enables or disables shuffle compression.
   - **Example**: 
     ```bash
     --conf spark.shuffle.compress=true
     ```
   - **Considerations**: Enabling shuffle compression can reduce I/O during shuffle stages, improving performance with large datasets.

### 10. **`--conf spark.shuffle.spill.compress`**
   - **Purpose**: Controls whether to compress shuffle spill data to disk.
   - **Example**: 
     ```bash
     --conf spark.shuffle.spill.compress=true
     ```
   - **Considerations**: Helps reduce disk I/O during shuffling but adds CPU overhead. Typically used with shuffle compression.

### 11. **`--conf spark.sql.files.maxPartitionBytes`**
   - **Purpose**: Controls the maximum size of each partition for file-based data sources.
   - **Example**: 
     ```bash
     --conf spark.sql.files.maxPartitionBytes=134217728
     ```
   - **Considerations**: Smaller partition sizes can improve parallelism for file-based data sources. Adjust this value based on file size and available resources.

### 12. **`--conf spark.sql.broadcastTimeout`**
   - **Purpose**: Sets the timeout for broadcast joins in Spark SQL.
   - **Example**: 
     ```bash
     --conf spark.sql.broadcastTimeout=3600
     ```
   - **Considerations**: Useful when working with large broadcast joins that might take longer to execute.

### 13. **`--conf spark.sql.autoBroadcastJoinThreshold`**
   - **Purpose**: Controls the maximum size of a table Spark will consider for broadcasting during join operations.
   - **Example**: 
     ```bash
     --conf spark.sql.autoBroadcastJoinThreshold=104857600
     ```
   - **Considerations**: A higher value helps Spark broadcast smaller tables during joins, improving join performance.

### 14. **`--conf spark.sql.adaptive.enabled`**
   - **Purpose**: Enables or disables Spark SQL Adaptive Query Execution (AQE).
   - **Example**: 
     ```bash
     --conf spark.sql.adaptive.enabled=true
     ```
   - **Considerations**: AQE dynamically optimizes query plans based on runtime statistics, improving performance for complex queries with skewed data or large shuffles.

## Example Spark-Submit Command with Performance Options

```bash
spark-submit \
  --deploy-mode cluster \
  --master yarn \
  --executor-memory 8g \
  --driver-memory 4g \
  --executor-cores 4 \
  --num-executors 10 \
  --conf spark.sql.shuffle.partitions=500 \
  --conf spark.sql.autoBroadcastJoinThreshold=104857600 \
  --conf spark.memory.fraction=0.6 \
  --conf spark.shuffle.compress=true \
  --conf spark.shuffle.spill.compress=true \
  --conf spark.sql.adaptive.enabled=true \
  word_count.py
