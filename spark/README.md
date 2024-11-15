## Tips for spark command 

### launching spark shell locally 

<p> By default it is going to consider Local system as spark master which is like standalone Mode </p>

```
I have no name!@551c674e792a:/opt/bitnami/spark$ spark-shell 
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
24/03/21 05:41:49 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Spark context Web UI available at http://551c674e792a:4040
Spark context available as 'sc' (master = local[*], app id = local-1710999709904).
Spark session available as 'spark'.
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 3.5.1
      /_/
         
Using Scala version 2.12.18 (OpenJDK 64-Bit Server VM, Java 17.0.10)
Type in expressions to have them evaluated.
Type :help for more information.

```

### launching spark shell in remote master 

```
I have no name!@551c674e792a:/opt/bitnami/spark$ spark-shell --master spark://spark-master:7077
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
24/03/21 05:42:51 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Spark context Web UI available at http://551c674e792a:4040
Spark context available as 'sc' (master = spark://spark-master:7077, app id = app-20240321054251-0001).
Spark session available as 'spark'.
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 3.5.1
      /_/
         
Using Scala version 2.12.18 (OpenJDK 64-Bit Server VM, Java 17.0.10)
Type in expressions to have them evaluated.
Type :help for more information.

scala> 


```


## Submiting job to cluster mode -- Make sure you have shared storage where your jar file is available 

```
 spark-submit  --class org.example.spark.BasicDataFrame --master spark://spark-master:7077     --deploy-mode cluster   target/basic-dataframe-maven-1.0-SNAPSHOT.jar


24/03/21 08:09:08 INFO SecurityManager: Changing view acls to: root,spark
24/03/21 08:09:08 INFO SecurityManager: Changing modify acls to: root,spark
24/03/21 08:09:08 INFO SecurityManager: Changing view acls groups to: 
24/03/21 08:09:08 INFO SecurityManager: Changing modify acls groups to: 
24/03/21 08:09:08 INFO SecurityManager: SecurityManager: authentication disabled; ui acls disabled; users with view permissions: root, spark; groups with view permissions: EMPTY; users with modify permissions: root, spark; groups with modify permissions: EMPTY
24/03/21 08:09:08 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
24/03/21 08:09:09 INFO Utils: Successfully started service 'driverClient' on port 35725.
24/03/21 08:09:09 INFO TransportClientFactory: Successfully created connection to spark-master/172.20.0.4:7077 after 13 ms (0 ms spent in bootstraps)
24/03/21 08:09:09 INFO ClientEndpoint: ... waiting before polling master for driver state
24/03/21 08:09:09 INFO ClientEndpoint: Driver successfully submitted as driver-20240321080909-0000
24/03/21 08:09:14 INFO ClientEndpoint: State of driver-20240321080909-0000 is FINISHED
24/03/21 08:09:14 INFO ClientEndpoint: State of driver driver-20240321080909-0000 is FINISHED, exiting spark-submit JVM.
24/03/21 08:09:14 INFO ShutdownHookManager: Shutdown hook called
24/03/21 08:09:14 INFO ShutdownHookManager: Deleting directory /tmp/spark-2ad95139-d377-4139-a034-157eba036026
root@af5b6b91e676:/opt/bitnami/spark/code1# spark-submit  --class org.example.spark.BasicDataFrame --master spark://spark-master:7077     --deploy-mode cluster   target/basic-dataframe-maven-1.0-SNAPSHOT.jar 
24/03/21 08:09:32 INFO SecurityManager: Changing view acls to: root,spark
24/03/21 08:09:32 INFO SecurityManager: Changing modify acls to: root,spark
24/03/21 08:09:32 INFO SecurityManager: Changing view acls groups to: 
24/03/21 08:09:32 INFO SecurityManager: Changing modify acls groups to: 
24/03/21 08:09:32 INFO SecurityManager: SecurityManager: authentication disabled; ui acls disabled; users with view permissions: root, spark; groups with view permissions: EMPTY; users with modify permissions: root, spark; groups with modify permissions: EMPTY
24/03/21 08:09:32 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
24/03/21 08:09:32 INFO Utils: Successfully started service 'driverClient' on port 38699.
24/03/21 08:09:32 INFO TransportClientFactory: Successfully created connection to spark-master/172.20.0.4:7077 after 11 ms (0 ms spent in bootstraps)
24/03/21 08:09:32 INFO ClientEndpoint: ... waiting before polling master for driver state
24/03/21 08:09:32 INFO ClientEndpoint: Driver successfully submitted as driver-20240321080932-0001
24/03/21 08:09:37 INFO ClientEndpoint: State of driver-20240321080932-0001 is FINISHED
24/03/21 08:09:37 INFO ClientEndpoint: State of driver driver-20240321080932-0001 is FINISHED, exiting spark-submit JVM.
24/03/21 08:09:37 INFO ShutdownHookManager: Shutdown hook called
24/03/21 08:09:37 INFO ShutdownHookManager: Deleting directory /tmp/spark-75339966-09dc-4982-bfd4-6e0224633309
```

### note: --- in this case you have to check logs in selected worker node only -- under $SPARK_HOME/work directory 

# Apache Spark Cluster Ports and Portals

Apache Spark uses several ports to provide access to different services like the Spark UI, worker nodes, and more. Below is a list of commonly used ports in an Apache Spark cluster and how to access them.

## 1. Master Node Ports

### a. Spark Master Web UI
- **Port:** `8080` (default)
- **Description:** Provides access to the web UI for the Spark master, where you can monitor the status of workers, running jobs, and completed jobs.
- **Access URL:** `http://<master-node-host>:8080`
- **Customization:** You can change this default port by setting the `spark.master.ui.port` configuration in `spark-defaults.conf`.

### b. Spark Master RPC Port
- **Port:** `7077` (default)
- **Description:** This is the RPC (Remote Procedure Call) port that the workers and clients use to communicate with the Spark master.
- **Customization:** This can be configured using the `SPARK_MASTER_PORT` environment variable or in the configuration file.

## 2. Worker Node Ports

### a. Spark Worker Web UI
- **Port:** `8081` (default)
- **Description:** Provides access to the web UI for each worker node. You can view the status of the worker, including its memory and core usage, and the jobs running on that worker.
- **Access URL:** `http://<worker-node-host>:8081`
- **Customization:** You can change this port by setting the `spark.worker.ui.port` configuration.

### b. Spark Worker RPC Port
- **Port:** Random (default) or specified via `SPARK_WORKER_PORT`
- **Description:** This port is used for communication between the worker and the master.

### c. Spark Worker Web UI Bind Address
- **Port:** `4040` for the first job, increments for subsequent jobs
- **Description:** This is the default port for the Spark Web UI on the worker nodes for specific jobs. Each job gets a new port if the previous one is in use.

## 3. Executor Node Ports

### a. Spark Executor Ports
- **Port:** Random (default) or specified via `spark.executor.port`
- **Description:** Executors use these ports to communicate with the Spark driver program. Typically, they are assigned dynamically by the cluster manager.

## 4. Driver Node Ports

### a. Spark Driver Web UI
- **Port:** `4040` (default)
- **Description:** Provides access to the Spark UI for monitoring the Spark driver application and seeing information about running jobs, stages, and tasks.
- **Access URL:** `http://<driver-host>:4040`
- **Customization:** This port can be changed using the `spark.ui.port` configuration. The port increments (4041, 4042, etc.) if 4040 is unavailable due to multiple jobs.

### b. Spark Driver RPC Port
- **Port:** Configurable with `spark.driver.port`
- **Description:** This port is used for communication between the driver and executors.

## 5. Other Ports

### a. BlockManager Port
- **Port:** Random (default) or specified via `spark.blockManager.port`
- **Description:** This is used by Spark's internal BlockManager, which handles the distribution of data blocks between nodes in the cluster.

### b. History Server UI Port
- **Port:** `18080` (default)
- **Description:** If you enable the Spark History Server to view the logs of completed applications, the web UI for the history server runs on this port.
- **Access URL:** `http://<history-server-host>:18080`
- **Customization:** You can change this port by setting the `spark.history.ui.port` configuration.

## Accessing the Spark Portals

To access any of these portals, simply open a web browser and enter the corresponding URL using the hostname or IP of the node and the appropriate port. For example:

- **Master UI:** `http://<master-node-ip>:8080`
- **Worker UI:** `http://<worker-node-ip>:8081`
- **Driver UI (first job):** `http://<driver-node-ip>:4040`
- **History Server UI:** `http://<history-server-ip>:18080`

> **Note:** If you are accessing the Spark cluster from a remote machine, make sure the ports are open and accessible through the network.




