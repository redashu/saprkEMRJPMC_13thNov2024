package com.example;
import java.util.Arrays;

import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;

import scala.Tuple2;





public class Demo {
    public static void main(String[] args) {
        // Step 1: Configure Spark
        SparkConf conf = new SparkConf().setAppName("BasicParallelizeExample").setMaster("local[*]");

        // Step 2: Create a Java Spark Context
        JavaSparkContext sc = new JavaSparkContext(conf);

       

       // Step 2: Read the text file into an RDD
        JavaRDD<String> textFile = sc.textFile("/home/ec2-user/codes/datasets/sample.txt");

        // Step 3: Split each line into words
        JavaRDD<String> words = textFile.flatMap(line -> Arrays.asList(line.split("\\s+")).iterator());

        // Step 4: Map each word to a (word, 1) tuple
        JavaPairRDD<String, Integer> wordPairs = words.mapToPair(word -> new Tuple2<>(word, 1));

        // Step 5: Reduce by key (sum the counts for each word)
        JavaPairRDD<String, Integer> wordCounts = wordPairs.reduceByKey((a, b) -> a + b);

        // Step 6: Collect and print the result
        wordCounts.collect().forEach(tuple -> System.out.println(tuple._1() + ": " + tuple._2()));

        // Step 7: Stop the Spark context
        sc.stop();
    }
}