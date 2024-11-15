from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SparkSession
from pyspark.streaming.kafka import KafkaUtils
import json

# Initialize SparkContext and StreamingContext
sc = SparkContext(appName="WeatherStreamingApp")
ssc = StreamingContext(sc, 30)  # 30 seconds batch interval

# Enable Checkpointing for Fault Tolerance
ssc.checkpoint("hdfs://your-hdfs-path/checkpoints")  # This path stores metadata, including WALs

# Function to simulate the processing of weather data
def process_weather_data(rdd):
    if not rdd.isEmpty():
        df = spark.read.json(rdd)
        df.show()

# Example Kafka stream input (assuming we are consuming weather data from Kafka)
kafka_stream = KafkaUtils.createStream(ssc, 'localhost:2181', 'weather-group', {'weather-data': 1})

# Format the stream data (Assume JSON format)
weather_stream = kafka_stream.map(lambda x: x[1])  # Get the message (JSON) from the Kafka stream

# Parse the JSON data
weather_stream.foreachRDD(process_weather_data)

# State update function to compute the running average of temperature and humidity
def update_running_average(new_data, running_avg):
    if running_avg is None:
        running_avg = (0.0, 0.0, 0)  # (sum_temp, sum_humidity, count)
    
    new_sum_temp = running_avg[0] + new_data[0]
    new_sum_humidity = running_avg[1] + new_data[1]
    new_count = running_avg[2] + 1
    
    return (new_sum_temp, new_sum_humidity, new_count)

# Create DStream that simulates temperature and humidity data coming in
def fetch_data_from_stream(line):
    # Assume line is a JSON formatted string like {"timestamp": "2024-11-15T14:00:00Z", "temperature": 22.5, "humidity": 65}
    data = json.loads(line)
    temperature = data['temperature']
    humidity = data['humidity']
    return (temperature, humidity)

# Example input stream with Kafka or other sources
weather_dstream = weather_stream.map(fetch_data_from_stream)

# Use updateStateByKey for stateful processing and running averages
running_avg_stream = weather_dstream.updateStateByKey(update_running_average)

# Print the running average of temperature and humidity every 10 minutes
running_avg_stream.pprint()

# Start the streaming job
ssc.start()
ssc.awaitTermination()

