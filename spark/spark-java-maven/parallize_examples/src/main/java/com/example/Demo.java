package com.example;
import java.util.Arrays;
import java.util.List;

import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;

public class Demo {
    public static void main(String[] args) {
        // Step 1: Configure Spark
        SparkConf conf = new SparkConf().setAppName("BasicParallelizeExample").setMaster("local[*]");

        // Step 2: Create a Java Spark Context
        JavaSparkContext sc = new JavaSparkContext(conf);

        // Sample data: List of names
        List<String> names = Arrays.asList("Alice", "Bob", "Charlie", "Diana", "Ethan");

        // Create an RDD from the list
        JavaRDD<String> namesRDD = sc.parallelize(names);

        // Use map transformation to convert each name to uppercase
        JavaRDD<String> upperCaseNamesRDD = namesRDD.map(name -> name.toUpperCase());

        // Collect and print the results
        List<String> upperCaseNames = upperCaseNamesRDD.collect();
        System.out.println("Uppercase Names: " + upperCaseNames);

        // Count the number of names in the RDD
        long count = namesRDD.count();
        System.out.println("Count of Names: " + count);

        // Get the first name in the RDD
        String firstName = namesRDD.first();
        System.out.println("First Name: " + firstName);

        // Collect all names in the RDD
        List<String> allNames = namesRDD.collect();
        System.out.println("All Names: " + allNames);
        // Step 7: Stop the Spark context
        sc.stop();
    }
}