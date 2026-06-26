# Databricks notebook source
from pyspark import pipelines as dp
from pyspark.sql.functions import monotonically_increasing_id, upper


@dp.table(
    name=f"workspace.silver.dim_country"
)
def silver():
    df = (
        spark.read.table("workspace.bronze.raw_countries").sort("common_name")
    )

    df = df.select(
        monotonically_increasing_id().alias("Id"),
        upper(df.common_name).alias("Name"),
        df.population.alias("Population")
    )

    return df

@dp.table(
    name=f"workspace.gold.dim_country"
)
def gold():
    return spark.read.table("workspace.silver.dim_country")