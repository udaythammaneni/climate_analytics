# Databricks notebook source
# MAGIC %md
# MAGIC Load Bronze Table

# COMMAND ----------

from pyspark.sql.functions import col

bronze_df = spark.table("climate_analytics.bronze.co2_raw")

# COMMAND ----------

# MAGIC %md
# MAGIC Apply Cleaning Rules

# COMMAND ----------

silver_df = bronze_df \
    .filter(col("country").isNotNull()) \
    .filter(col("year").isNotNull()) \
    .filter(col("iso_code").isNotNull()) \
    .filter(col("co2").isNotNull()) \
    .filter(col("co2") >= 0) \
    .filter(col("year") >= 1950) \
    .dropDuplicates(["country", "year"])

# COMMAND ----------

# MAGIC %md
# MAGIC Data Quality Check

# COMMAND ----------

print("Total Rows After Cleaning:", silver_df.count())

print("Null CO2 Count:",
      silver_df.filter(col("co2").isNull()).count())

print("Negative CO2 Count:",
      silver_df.filter(col("co2") < 0).count())

# COMMAND ----------

# MAGIC %md
# MAGIC Write to Silver Layer

# COMMAND ----------

silver_df.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("climate_analytics.silver.co2_clean")

# COMMAND ----------

# MAGIC %md
# MAGIC Validate Silver

# COMMAND ----------

display(spark.table("climate_analytics.silver.co2_clean").limit(10))

# COMMAND ----------

spark.table("climate_analytics.silver.co2_clean").count()