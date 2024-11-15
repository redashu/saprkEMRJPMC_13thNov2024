## apache spark 3.5 

### some customized ENV 

## Configuration

### Environment variables

#### Customizable environment variables

| Name                                     | Description                                                                      | Default Value                                  |
|------------------------------------------|----------------------------------------------------------------------------------|------------------------------------------------|
| `SPARK_MODE`                             | Spark cluster mode to run (can be master or worker).                             | `master`                                       |
| `SPARK_MASTER_URL`                       | Url where the worker can find the master. Only needed when spark mode is worker. | `spark://spark-master:7077`                    |
| `SPARK_NO_DAEMONIZE`                     | Spark does not run as a daemon.                                                  | `true`                                         |
| `SPARK_RPC_AUTHENTICATION_ENABLED`       | Enable RPC authentication.                                                       | `no`                                           |
| `SPARK_RPC_ENCRYPTION_ENABLED`           | Enable RPC encryption.                                                           | `no`                                           |
| `SPARK_LOCAL_STORAGE_ENCRYPTION_ENABLED` | Enable local storage encryption.                                                 | `no`                                           |
| `SPARK_SSL_ENABLED`                      | Enable SSL configuration.                                                        | `no`                                           |
| `SPARK_SSL_KEYSTORE_FILE`                | Location of the key store.                                                       | `${SPARK_CONF_DIR}/certs/spark-keystore.jks`   |
| `SPARK_SSL_TRUSTSTORE_FILE`              | Location of the key store.                                                       | `${SPARK_CONF_DIR}/certs/spark-truststore.jks` |
| `SPARK_SSL_NEED_CLIENT_AUTH`             | Whether to require client authentication.                                        | `yes`                                          |
| `SPARK_SSL_PROTOCOL`                     | TLS protocol to use.                                                             | `TLSv1.2`                                      |
| `SPARK_METRICS_ENABLED`                  | Whether to enable metrics for Spark.                                             | `false`                                        |

#### Read-only environment variables


| Name                     | Description                            | Value                                   |
|--------------------------|----------------------------------------|-----------------------------------------|
| `SPARK_BASE_DIR`         | Spark installation directory.          | `${BITNAMI_ROOT_DIR}/spark`             |
| `SPARK_CONF_DIR`         | Spark configuration directory.         | `${SPARK_BASE_DIR}/conf`                |
| `SPARK_DEFAULT_CONF_DIR` | Spark default configuration directory. | `${SPARK_BASE_DIR}/conf.default`        |
| `SPARK_WORK_DIR`         | Spark workspace directory.             | `${SPARK_BASE_DIR}/work`                |
| `SPARK_CONF_FILE`        | Spark configuration file path.         | `${SPARK_CONF_DIR}/spark-defaults.conf` |
| `SPARK_LOG_DIR`          | Spark logs directory.                  | `${SPARK_BASE_DIR}/logs`                |
| `SPARK_TMP_DIR`          | Spark tmp directory.                   | `${SPARK_BASE_DIR}/tmp`                 |
| `SPARK_JARS_DIR`         | Spark jar directory.                   | `${SPARK_BASE_DIR}/jars`                |
| `SPARK_INITSCRIPTS_DIR`  | Spark init scripts directory.          | `/docker-entrypoint-initdb.d`           |
| `SPARK_USER`             | Spark user.                            | `spark`                                 |
| `SPARK_DAEMON_USER`      | Spark system user.                     | `spark`                                 |
| `SPARK_DAEMON_GROUP`     | Spark system group.                    | `spark`                                 |



### Security

The Bitnani Apache Spark docker image supports enabling RPC authentication, RPC encryption and local storage encryption easily using the following env vars in all the nodes of the cluster.

```diff
+ SPARK_RPC_AUTHENTICATION_ENABLED=yes
+ SPARK_RPC_AUTHENTICATION_SECRET=RPC_AUTHENTICATION_SECRET
+ SPARK_RPC_ENCRYPTION=yes
+ SPARK_LOCAL_STORAGE_ENCRYPTION=yes
```

### enable SSL 

```
+ SPARK_SSL_ENABLED=yes
+ SPARK_SSL_KEY_PASSWORD=KEY_PASSWORD
+ SPARK_SSL_KEYSTORE_PASSWORD=KEYSTORE_PASSWORD
+ SPARK_SSL_TRUSTSTORE_PASSWORD=TRUSTSTORE_PASSWORD
+ SPARK_SSL_NEED_CLIENT_AUTH=yes
+ SPARK_SSL_PROTOCOL=TLSv1.2

```
