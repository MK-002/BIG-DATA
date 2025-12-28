import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._
import org.apache.spark.sql.streaming.Trigger

object IotStreaming {

  def main(args: Array[String]): Unit = {

    val schema = new StructType()
      .add("deviceId", StringType)
      .add("temperature", DoubleType)
      .add("humidity", DoubleType)
      .add("energy_kwh", DoubleType)
      .add("battery_level", IntegerType)
      .add("status", StringType)
      .add("timestamp", LongType)

    val spark = SparkSession.builder
      .appName("IotStreaming")
      .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    val df = spark
    .readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:29092") 
    .option("subscribe", "iot-sensors")
    .option("startingOffsets", "earliest")
    .load()


    val jsonDf = df
      .selectExpr("CAST(value AS STRING)")
      .select(from_json(col("value"), schema).as("data"))
      .select("data.*")

    val resultDf = jsonDf
      .withColumn("temperatureF", col("temperature") * 9 / 5 + 32)
      .withColumn("eventTime", to_timestamp(col("timestamp") / 1000))

    resultDf.writeStream
    .format("parquet")
    .option("path", "hdfs://namenode:9000/data/iot-output")
    .option("checkpointLocation", "hdfs://namenode:9000/checkpoints/iot")
    .trigger(Trigger.ProcessingTime("10 seconds"))
    .outputMode("append")
    .start()
    .awaitTermination()
    
  }
}
