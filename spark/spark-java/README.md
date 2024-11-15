## spark-basic-test folder got ---  "BasicDataFrame.java"

### ON new spark setup --- tested on version spark 3.5.1 and JDK 17 , scala 2.12 

### step 1  -- comiple code -- to create .class file 

```
 javac -cp  "$SPARK_HOME/jars/*"  BasicDataFrame.java
```

### step 2 -- convert into JAR 

```
 jar  cf  BasicDataFrame.jar BasicDataFrame.class
```

### now submit to spark master 

```
spark-submit  --class BasicDataFrame    BasicDataFrame.jar
```

### incase you want to override master details then 

```
spark-submit  --class BasicDataFrame --master "local[*]"   BasicDataFrame.jar
```
