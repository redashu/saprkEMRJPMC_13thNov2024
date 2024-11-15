## using apache maven you can also built tool and do rest things 

### building jar using maven 

## step 1 

```
mvn package
```

### output 

```
  spark-java-maven git:(master) ls
pom.xml src     target

➜  spark-java-maven git:(master) ls target 
basic-dataframe-maven-1.0-SNAPSHOT.jar generated-sources                      maven-archiver                         test-classes
classes                                generated-test-sources                 maven-status
➜  spark-java-maven git:(master) 


```

### step 2 -- submit job 

```
 spark-submit  --class org.example.spark.BasicDataFrame  target/basic-dataframe-maven-1.0-SNAPSHOT.jar
```
