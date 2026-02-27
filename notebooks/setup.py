# Databricks notebook source
# MAGIC %md
# MAGIC Create catalog, schema and volume

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE CATALOG IF NOT EXISTS climate_analytics MANAGED LOCATION '<Location/>';
# MAGIC USE CATALOG climate_analytics;
# MAGIC
# MAGIC CREATE SCHEMA IF NOT EXISTS bronze;
# MAGIC CREATE SCHEMA IF NOT EXISTS silver;
# MAGIC CREATE SCHEMA IF NOT EXISTS gold;
# MAGIC
# MAGIC USE SCHEMA bronze; 
# MAGIC CREATE VOLUME IF NOT EXISTS raw;

# COMMAND ----------

# MAGIC %md
# MAGIC Verify File Path

# COMMAND ----------

display(dbutils.fs.ls("/Volumes/climate_analytics/bronze/raw/"))

# COMMAND ----------

# MAGIC %md
# MAGIC Inspect the Dataset

# COMMAND ----------

df_sample = spark.read.csv(
    "/Volumes/climate_analytics/bronze/raw/owid-co2-data.csv",
    header=True,
    inferSchema=True
)

display(df_sample.limit(5))
print(df_sample.printSchema())