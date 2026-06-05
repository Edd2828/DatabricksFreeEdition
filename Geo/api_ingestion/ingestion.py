# Databricks notebook source
import requests

from pyspark.sql.functions import current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, MapType


BASE_URL = "https://restcountries.com/v3.1/all?"
params = {"fields": ["name", "population", "currencies", "languages"]}

data = requests.get(BASE_URL, params=params).json()

schema = StructType([
    StructField("name", StructType([
        StructField("common", StringType(), True),
        StructField("official", StringType(), True),
    ]), True),
    StructField("currencies", MapType(
        StringType(),
        StructType([
            StructField("name", StringType(), True),
            StructField("symbol", StringType(), True),
        ])), True),
    StructField("languages", MapType(StringType(), StringType()), True),
    StructField("population", StringType(), True),
])

df = spark.createDataFrame(data, schema=schema).withColumn("IngestionDate", current_timestamp())

df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable("raw_countries")