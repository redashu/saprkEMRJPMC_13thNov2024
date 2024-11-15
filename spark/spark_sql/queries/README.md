## Spark SQL queries 

## Login to spark sql using shell

```
I have no name!@d23ab36deee7:/opt/bitnami/spark$ spark-sql 
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
24/10/05 05:09:33 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
24/10/05 05:09:35 WARN HiveConf: HiveConf of name hive.stats.jdbc.timeout does not exist
24/10/05 05:09:35 WARN HiveConf: HiveConf of name hive.stats.retries.wait does not exist
24/10/05 05:09:37 WARN ObjectStore: Version information not found in metastore. hive.metastore.schema.verification is not enabled so recording the schema version 2.3.0
24/10/05 05:09:37 WARN ObjectStore: setMetaStoreSchemaVersion called but recording version is disabled: version = 2.3.0, comment = Set by MetaStore UNKNOWN@172.20.0.3
Spark Web UI available at http://d23ab36deee7:4040
Spark master: local[*], Application Id: local-1728104974442
spark-sql (default)> 


```

### checking list of databases 

```
spark-sql (default)> show databases;
default
Time taken: 0.034 seconds, Fetched 1 row(s)
spark-sql (default)> 

```

### By default we have default database which is current also 

### checking current database 

```
select current_database();
default
Time taken: 0.769 seconds, Fetched 1 row(s)
spark-sql (default)> 

```

### Creating a new database 

```
 create database delvexdb;

 ==>
 show databases;
ashudb
default
delvexdb
Time taken: 0.025 seconds, Fetched 3 row(s)
```

### using Database 

```
use delvexdb;
Time taken: 0.021 seconds

```

### Creating a table 

```
CREATE TABLE my_database.people (
    id INT,
    name STRING,
    age INT
);

```

###  printing schema 

```
desc st_info;
id                  	int                 	                    
name                	string              	                    
age                 	int               
```

### Inserting data into table 

```
INSERT INTO people VALUES
(1, 'Alice', 30),
(2, 'Bob', 25),
(3, 'Charlie', 35);

```

### create one more table 

```
-- Create a table for addresses
CREATE TABLE addresses (
    id INT,
    address STRING
);

```

### insert more data 

```
INSERT INTO addresses VALUES
(1, '123 Main St'),
(2, '456 Oak St'),
(3, '789 Pine St');
``

## table Join  (Perform an INNER JOIN on id field)

```
SELECT p.id, p.name, p.age, a.address
FROM people p
JOIN addresses a
ON p.id = a.id;
```

# type of join 

# Types of Joins in Spark SQL

In Spark SQL, a `JOIN` operation is used to combine rows from two or more tables based on a related column between them. The join operation creates a virtual result set, combining the relevant data without altering the original tables.

## 1. Inner Join

An **Inner Join** returns only the matching rows between the two tables based on the specified condition.

```sql
SELECT * FROM table1 
JOIN table2 
ON table1.id = table2.id;
```

## Left Join 

```sql
SELECT * FROM table1 
LEFT JOIN table2 
ON table1.id = table2.id;

```

## Right join 

```sql
SELECT * FROM table1 
RIGHT JOIN table2 
ON table1.id = table2.id;
```

### Full outer Join 

```sql
SELECT * FROM table1 
FULL OUTER JOIN table2 
ON table1.id = table2.id;

```
## Some more Spark sql funcations 

```
Aggregations and Grouping:

Learn how to aggregate data using functions like SUM, COUNT, AVG, MAX, and MIN.
Learn how to use the GROUP BY clause to perform aggregation on groups of data.
Window Functions:

Understand windowing in SQL, which allows you to perform calculations across a set of rows related to the current row.
Learn about RANK, ROW_NUMBER, and other advanced analytical functions.
Filtering and Sorting:

Learn how to filter records using the WHERE clause and sort results using ORDER BY.
Subqueries:

Learn how to write subqueries, which are queries nested inside other queries.
Creating Views:

Understand how to create temporary views and permanent views for easier query management.

```



# Aggregation and Grouping in Spark SQL

In Spark SQL, **aggregation** and **grouping** allow you to perform summary operations on data, such as calculating totals, averages, counts, and more. You can group rows that have the same values in specified columns and aggregate data for each group.

## Common Aggregation Functions:

- `COUNT()` – Counts the number of rows.
- `SUM()` – Sums up the values.
- `AVG()` – Calculates the average of values.
- `MAX()` – Finds the maximum value.
- `MIN()` – Finds the minimum value.

## Example Table: `sales`

Let’s work with a sample table `sales` that stores sales data for different salespersons across regions.

```sql
CREATE TABLE sales (
    salesperson STRING,
    region STRING,
    sales_amount INT
);

-- Insert sample data
INSERT INTO sales VALUES
('Alice', 'North', 500),
('Bob', 'South', 600),
('Alice', 'North', 300),
('Charlie', 'East', 400),
('Bob', 'South', 700);

```
### total sales per person 

```sql
SELECT salesperson, SUM(sales_amount) AS total_sales
FROM sales
GROUP BY salesperson;

```

### Total sales per region 

```sql

SELECT region, SUM(sales_amount) AS total_sales
FROM sales
GROUP BY region;

```

### list of sales person having sales greater than 1000

```sql
SELECT salesperson, SUM(sales_amount) AS total_sales
FROM sales
GROUP BY salesperson
HAVING total_sales > 1000;

```

# Subqueries 

## Using where

```sql
select salesperson,sales_amount 
                    > FROM sales
                    > WHERE sales_amount > (select AVG(sales_amount) from sales);
Bob	600
Bob	700
Time taken: 0.858 seconds, Fetched 2 row(s)

```

### using FROM claus

```sql
select region , avg_sales 
                    > FROM (
                    > Select region , avg(sales_amount) as avg_sales 
                    > FROM sales
                    > GROUP by region ) 
                    > as subquery;
North	400.0
South	650.0
East	400.0
Time taken: 0.546 seconds, Fetched 3 row(s)
```


# Views in Spark SQL

A **view** in Spark SQL is a virtual table that represents the result of a stored query. Views are helpful for simplifying complex queries, improving code reusability, and organizing SQL logic. Unlike physical tables, views do not store data; they store the query that generates the data when needed.

## Types of Views:

1. **Temporary View**:
   - Exists only for the duration of the session.
   - Dropped automatically when the session ends.
   
2. **Global Temporary View**:
   - Accessible across different Spark sessions.
   - Dropped when the Spark application terminates.
   - Stored in the special `global_temp` database.

## Creating a View

You can create a **temporary view** from an existing table or a query. Temporary views are session-scoped and will disappear when the session ends.

```sql
CREATE OR REPLACE TEMP VIEW view_sales AS
SELECT salesperson, region, SUM(sales_amount) AS total_sales
FROM sales
GROUP BY salesperson, region;
```

### query from temp view 

```
SELECT * FROM view_sales;
```

### dropping view 

```sql
DROP VIEW IF EXISTS view_sales;
```

# Global Temporary Views

<p>
A global temporary view is a special type of view that persists across Spark sessions. These views are stored in the global_temp database and remain accessible until the Spark application is stopped.
<p>

## Creating Global temp view 

```sql
CREATE OR REPLACE GLOBAL TEMP VIEW global_sales AS
SELECT salesperson, region, SUM(sales_amount) AS total_sales
FROM sales
GROUP BY salesperson, region;

```

### view 

```sql
SELECT * FROM global_temp.global_sales;
```

