from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, udf
from pyspark.sql.types import StructType, StructField, DoubleType
import joblib
import numpy as np

# Create a SparkSession
spark = SparkSession.builder \
    .appName("KafkaSparkStreamingWithML") \
    .getOrCreate()

# Define the schema for incoming JSON data
# Here we assume each message has a numeric 'feature' field.
schema = StructType([
    StructField("feature", DoubleType(), True)
])

# Load the trained ML model from the mounted directory (/app)
model = joblib.load("/app/price_forecast_model.joblib")

# Broadcast the model to executors (ensuring it is accessible in UDF)
sc = spark.sparkContext
broadcastModel = sc.broadcast(model)

# Define a UDF to perform prediction using the broadcast model
def predict_price(feature):
    # The model expects a 2D array for prediction
    if feature is None:
        return None
    prediction = broadcastModel.value.predict(np.array([[feature]]))
    return float(prediction[0])

predict_price_udf = udf(predict_price, DoubleType())

# Read data from Kafka (ensure Kafka is running on localhost:9092)
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "amazon_products") \
    .option("startingOffsets", "latest") \
    .load()

# Convert the binary 'value' column to string and parse JSON using the schema
data_df = kafka_df.selectExpr("CAST(value AS STRING) as json_str") \
    .select(from_json(col("json_str"), schema).alias("data")) \
    .select("data.*")

# Use the UDF to generate predictions based on the 'feature' field
prediction_df = data_df.withColumn("predicted_price", predict_price_udf(col("feature")))

# Output the streaming predictions to the console
query = prediction_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
