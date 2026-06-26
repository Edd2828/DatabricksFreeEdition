# Databricks notebook source
from pyspark import pipelines as dp
from pyspark.sql.functions import col, explode, upper, trim


@dp.table(
    name=f"workspace.silver.bridge_country_currency"
)
def silver():

    df = spark.read.table("workspace.bronze.raw_countries")

    df = df.select(col("common_name"), explode(col("currencies")).alias("currencies")).distinct()

    df = df.select(
        upper(df.common_name).alias("Country"),
        upper(df.currencies.getField("code")).alias("CurrencyCode"),
    ).sort(col("Country"), col("CurrencyCode")).filter(trim(col("CurrencyCode")) != "")

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