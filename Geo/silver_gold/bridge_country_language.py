# Databricks notebook source
from pyspark import pipelines as dp
from pyspark.sql.functions import col, explode


@dp.table(
    name=f"workspace.silver.bridge_country_language"
)
def silver():
    df = spark.read.table("workspace.default.raw_countries").withColumn("Country", col("name").getField("common"))

    df = df.select(col("Country"), explode(col("languages"))).distinct().sort(col("Country"), col("key"))

    df = df.select(
        col("Country"),
        col("key").alias("LanguageCode"),
    )

    return df

@dp.table(
    name=f"workspace.gold.bridge_country_language"
)
def gold():
    country_language_df = spark.read.table("workspace.silver.bridge_country_language")
    country_df = spark.read.table("workspace.silver.dim_country")
    language_df = spark.read.table("workspace.silver.dim_language")

    df = (
        country_language_df
        .join(country_df, country_language_df.Country == country_df.Name)
        .join(language_df, country_language_df.LanguageCode == language_df.Code)
    )

    return df.select(
        country_df.Id.alias("CountryId"),
        language_df.Id.alias("LanguageId"),
    )