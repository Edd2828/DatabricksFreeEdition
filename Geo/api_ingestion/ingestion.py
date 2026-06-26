# Databricks notebook source
from pyspark.sql.functions import explode, col, row_number
from pyspark.sql.window import Window


df = (
    spark.read.format("json")
    .load("/Volumes/workspace/default/rest_countries/*.json")
).withColumn("_file_modified_time", col("_metadata.file_modification_time"))

df = df.select(
    explode(df.data.objects).alias("raw_objects"),
    col("_file_modified_time"),
)

df = df.select(
    df.raw_objects.names.common.alias("common_name"),
    df.raw_objects.currencies.alias("currencies"),
    df.raw_objects.languages.alias("languages"),
    df.raw_objects.population.alias("population"),
    col("_file_modified_time"),
)

window = Window.partitionBy("common_name").orderBy(col("_file_modified_time").desc())

df = df.withColumn("rownum", row_number().over(window)).filter(col("rownum") == 1).drop("rownum")

df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable("workspace.bronze.raw_countries")