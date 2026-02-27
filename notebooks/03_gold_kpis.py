# Databricks notebook source
# MAGIC %md
# MAGIC Load Silver Data

# COMMAND ----------

from pyspark.sql.functions import col

silver_df = spark.table("climate_analytics.silver.co2_clean")

# COMMAND ----------

# MAGIC %md
# MAGIC Recalculate Emissions Per Capita

# COMMAND ----------

# DBTITLE 1,Cell 4
from pyspark.sql.functions import try_divide

gold_country_df = silver_df.withColumn(
    "co2_per_capita_calc",
    try_divide(col("co2"), col("population"))
)

# COMMAND ----------

# MAGIC %md
# MAGIC Year-over-Year Growth

# COMMAND ----------

# DBTITLE 1,Cell 6
from pyspark.sql.window import Window
from pyspark.sql.functions import lag, try_divide

windowSpec = Window.partitionBy("country").orderBy("year")

gold_country_df = gold_country_df \
    .withColumn("prev_year_co2", lag("co2").over(windowSpec)) \
    .withColumn(
        "yoy_growth",
        try_divide((col("co2") - col("prev_year_co2")), col("prev_year_co2"))
    )

# COMMAND ----------

# MAGIC %md
# MAGIC Save Country Analytics Table

# COMMAND ----------

# DBTITLE 1,Cell 8
gold_country_df.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("climate_analytics.gold.country_analytics")

# COMMAND ----------

# MAGIC %md
# MAGIC Global Yearly Trend Table

# COMMAND ----------

from pyspark.sql.functions import sum

global_trend_df = silver_df.groupBy("year") \
    .agg(sum("co2").alias("total_global_co2"))

global_trend_df.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("climate_analytics.gold.global_trends")

# COMMAND ----------

# MAGIC %md
# MAGIC Top 10 Polluters

# COMMAND ----------

top_countries_df = silver_df.groupBy("country") \
    .agg(sum("co2").alias("total_co2")) \
    .orderBy(col("total_co2").desc())

top_countries_df.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("climate_analytics.gold.top_polluters")

# COMMAND ----------

# MAGIC %md
# MAGIC Validate Gold Layer

# COMMAND ----------

spark.table("climate_analytics.gold.country_analytics").count()
spark.table("climate_analytics.gold.global_trends").count()
spark.table("climate_analytics.gold.top_polluters").show(10)