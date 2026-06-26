# Databricks notebook source
from pyspark import pipelines as dp
from pyspark.sql.functions import monotonically_increasing_id, col, explode, upper, trim


@dp.table(
    name=f"workspace.silver.dim_language"
)
def silver():
    df = spark.read.table("workspace.bronze.raw_countries")

    df = df.select(explode(col("languages")).alias("languages")).distinct()

    df = df.select(
        monotonically_increasing_id().alias("Id"),
        upper(df.languages.getField("iso639_3")).alias("Code"),
        upper(df.languages.getField("name")).alias("Name"),
    ).filter(trim(col("Code")) != "")

    return df

@dp.table(
    name=f"workspace.gold.dim_language"
)
def gold():
    return spark.read.table("workspace.silver.dim_language")