# Databricks notebook source
from pyspark import pipelines as dp
from pyspark.sql.functions import col, explode


@dp.table(
    name=f"workspace.silver.bridge_country_currency"
)
def silver():
    df = spark.read.table("workspace.default.raw_countries").withColumn("Country", col("name").getField("common"))

    df = df.select(col("Country"), explode(col("currencies"))).distinct().sort(col("Country"), col("key"))

    df = df.select(
        col("Country"),
        col("key").alias("CurrencyCode"),
    )

    return df

@dp.table(
    name=f"workspace.gold.bridge_country_currency"
)
def gold():
    country_currency_df = spark.read.table("workspace.silver.bridge_country_currency")
    country_df = spark.read.table("workspace.silver.dim_country")
    currency_df = spark.read.table("workspace.silver.dim_currency")

    df = (
        country_currency_df
        .join(country_df, country_currency_df.Country == country_df.Name)
        .join(currency_df, country_currency_df.CurrencyCode == currency_df.Code)
    )

    return df.select(
        country_df.Id.alias("CountryId"),
        currency_df.Id.alias("CurrencyId"),
    )