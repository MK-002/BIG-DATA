import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

object IotAnalytics {
  def main(args: Array[String]): Unit = {

    val spark = SparkSession.builder()
      .appName("IotAnalytics")
      .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    val df = spark.read.parquet("hdfs://namenode:9000/data/iot-output")
    df.createOrReplaceTempView("iot_data")

    println("=== ANALYSE SPARK SQL (DATAFRAME) ===")

    val analyticsDf = spark.sql("""
      SELECT 
        deviceId, 
        round(avg(temperature), 2) as avgTemp, 
        round(avg(humidity), 2) as avgHum,
        round(sum(energy_kwh), 2) as totalEnergy,
        min(battery_level) as minBattery
      FROM iot_data 
      GROUP BY deviceId
    """)
    analyticsDf.show()

    println("=== ANALYSE BAS NIVEAU (RDD) ===")
    val rdd = df.rdd
    val countByDevice = rdd
      .map(row => (row.getAs[String]("deviceId"), 1))
      .reduceByKey(_ + _)

    println("Nombre de messages reçus par appareil (via RDD) :")
    countByDevice.collect().foreach { case (device, count) => 
      println(s"Appareil: $device -> Messages: $count")
    }

    val globalStats = df.select(
      countDistinct("deviceId").as("total_sensors"),
      round(avg("temperature"), 2).as("avg_temp_global"),
      round(sum("energy_kwh"), 2).as("total_energy_consumed"),
      round(avg("battery_level"), 1).as("avg_battery_global")
    )

    val deviceStats = analyticsDf 

    println("=== SAUVEGARDE DES RAPPORTS SUR HDFS ===")
    
    globalStats.coalesce(1).write
      .mode("overwrite")
      .option("header", "true")
      .csv("hdfs://namenode:9000/data/kpi-global")

    deviceStats.coalesce(1).write
      .mode("overwrite")
      .option("header", "true")
      .csv("hdfs://namenode:9000/data/kpi-devices")

    println("=== ANALYSE TERMINÉE ET SAUVEGARDÉE ===")
    spark.stop()
  }
}