# To setup spark on K8s there are couple of methods 


## Method -1 -- all manual steps 

<li> Write dockerfile build , test and push the image </li>
<li> Write K8s manifestfiles for master and workers </li>

## Method 2 -- Using helm 

<li> helm install my-release oci://registry-1.docker.io/bitnamicharts/spark  </li>

### OR 

<li> helm repo add ashu-repo https://charts.bitnami.com/bitnami  </li>
<li> helm install my-spark bitnami/spark --version 9.0.0  </li>

```
helm ls
NAME    	NAMESPACE	REVISION	UPDATED                             	STATUS  	CHART      	APP VERSION
my-spark	default  	1       	2024-04-05 06:59:38.894827 +0530 IST	deployed	spark-9.0.0	3.5.1  

```

### method 3 -- Spark Operator -- Advaned See you in udemy Lector 

## How to submit job in Kubernetes managed Spark 

### client mode

```
spark-submit --master spark://my-spark-master-svc:7077   --class org.apache.spark.examples.SparkPi examples/jars/spark-examples_2.12-3.5.1.jar 10
```

### Cluster mode 

```
 spark-submit --master spark://my-spark-master-svc:7077 --deploy-mode cluster  --class org.apache.sp
ark.examples.SparkPi examples/jars/spark-examples_2.12-3.5.1.jar 10 
```

### we can submit from kubectl cluster mode also --- see in Udemy 

