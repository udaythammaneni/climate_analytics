# Databricks notebook source
# MAGIC %md
# MAGIC Read Full CSV

# COMMAND ----------

raw_full_df = spark.read.csv(
    "/Volumes/climate_analytics/bronze/raw/owid-co2-data.csv",
    header=True,
    inferSchema=True
)

# COMMAND ----------

# MAGIC %md
# MAGIC Select Required Columns

# COMMAND ----------

from pyspark.sql.functions import col

bronze_df = raw_full_df.select(
    col("country"),
    col("iso_code"),
    col("year").cast("int"),
    col("co2").cast("double"),
    col("population").cast("long"),
    col("gdp").cast("long"),
    col("co2_per_capita").cast("double")
)

# COMMAND ----------

# MAGIC %md
# MAGIC Add Metadata Columns

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, lit

bronze_df = bronze_df \
    .withColumn("ingestion_timestamp", current_timestamp()) \
    .withColumn("data_source", lit("OWID"))

# COMMAND ----------

# MAGIC %md
# MAGIC Write as Delta Table

# COMMAND ----------

bronze_df.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("climate_analytics.bronze.co2_raw")

# COMMAND ----------

# MAGIC %md
# MAGIC Validate Bronze

# COMMAND ----------

display(spark.table("climate_analytics.bronze.co2_raw").limit(10))

# COMMAND ----------

spark.table("climate_analytics.bronze.co2_raw").count()

# COMMAND ----------

spark.table("climate_analytics.bronze.co2_raw") \
    .filter(col("iso_code").isNull()) \
    .count()