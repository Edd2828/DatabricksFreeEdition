# Databricks notebook source
from pyspark import pipelines as dp
from pyspark.sql.functions import monotonically_increasing_id, col, explode


@dp.table(
    name=f"workspace.silver.dim_currency"
)
def silver():
    df = spark.read.table("workspace.default.raw_countries")

    df = df.select(explode(col("currencies"))).distinct().sort(col("key"))

    df = df.select(
        monotonically_increasing_id().alias("Id"),
        col("key").alias("Code"),
        col("value.name").alias("Name"),
    )

    return df

@dp.table(
    name=f"workspace.gold.dim_currency"
)
def gold():
    return spark.read.table("workspace.silver.dim_currency")