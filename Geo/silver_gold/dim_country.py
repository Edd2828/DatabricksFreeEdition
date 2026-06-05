# Databricks notebook source
from pyspark import pipelines as dp
from pyspark.sql.functions import monotonically_increasing_id, col
from pyspark.sql.types import IntegerType


@dp.table(
    name=f"workspace.silver.dim_country"
)
def silver():
    df = (
        spark.read.table("workspace.default.raw_countries")
        .withColumn("Country", col("name").getField("common"))
        .withColumn("Population", col("population").cast(IntegerType()))
    ).sort("Country")

    df = df.select(
        monotonically_increasing_id().alias("Id"),
        df.Country.alias("Name"),
        df.Population
    )

    return df

@dp.table(
    name=f"workspace.gold.dim_country"
)
def gold():
    return spark.read.table("workspace.silver.dim_country")