package com.example;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.SparkConf;

import java.util.Arrays;
import java.util.List;

public class Demo {
    public static void main(String[] args) {
        // Step 1: Configure Spark
        SparkConf conf = new SparkConf().setAppName("BasicParallelizeExample").setMaster("local[*]");

        // Step 2: Create a Java Spark Context
        JavaSparkContext sc = new JavaSparkContext(conf);

        // Step 3: Create a list of data
        List<Integer> data = Arrays.asList(1, 2, 3, 4, 5);

        // Step 4: Parallelize the list into an RDD
        JavaRDD<Integer> distData = sc.parallelize(data);

        // Step 5: Perform an operation on the RDD (e.g., map and collect the result)
        JavaRDD<Integer> multipliedData = distData.map(x -> x * 2);

        // Step 6: Print the results
        multipliedData.collect().forEach(System.out::println);

        // Step 7: Stop the Spark context
        sc.stop();
    }
}