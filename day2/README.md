## Revision and overview 

### Nodes in EMR

<img src="nodes1.png">

### Instance family types 

<img src="type1.png">

### any one from each team can do that 

```
 1  sudo -i
    2  ls
    3  mkdir  ashutoshh
    4  cd ashutoshh/
    5  yes  "spark is having support of python java scala r"  >ashu.txt
    6  ls -lh  ashu.txt 
    7  hdfs dfs  -ls /
    8  hdfs dfs  -mkidr  /common-data
    9  hdfs dfs  -mkdir   /common-data
   10  hdfs dfs  -ls /
   11  hdfs dfs  -ls /common-data/text
   12  hdfs dfs  -mkdir  /common-data/text
   13  ls
   14  hdfs dfs -copyFromLocal ashu.txt   /common-data/text/
   15  hdfs dfs -ls  /common-data/text
   16  history 

```
## spark bigdata word count example 

<img src="wc1.png">

### spark submit 

```
 spark-submit  --master yarn --num-executors 4 --executor-cores 1  --executor-memory 4g  --conf spark.memory.fraction=0.8 --conf spark.memory.storageFraction=0.2   ashu-wc.py  

```

## Dynamic executor 

```
spark-submit  --master yarn  --conf spark.dynamicAllocation.enabled=true  --conf spark.dynamicAllocation.minExecutors=3  --conf spark.dynamicAllocation.maxExecutors=10    --executor-cores 1  --executor-memory 4g  --conf spark.memory.fraction=0.8 --conf spark.memory.storageFraction=0.2   ashu-wc.py

```
