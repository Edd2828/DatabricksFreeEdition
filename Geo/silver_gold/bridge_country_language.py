# Databricks notebook source
from pyspark import pipelines as dp
from pyspark.sql.functions import col, explode, upper, trim


@dp.table(
    name=f"workspace.silver.bridge_country_language"
)
def silver():
    df = spark.read.table("workspace.bronze.raw_countries")

    df = df.select(col("common_name"), explode(col("languages")).alias("languages")).distinct()

    df = df.select(
        upper(df.common_name).alias("Country"),
        upper(df.languages.getField("iso639_3")).alias("LanguageCode"),
    ).sort(col("Country"), col("LanguageCode")).filter(trim(col("LanguageCode")) != "")

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