from ig_utils.Utils import set_catalog
from ig_utils.Tables import drop_object
from ig_utils.Enums import ETL
from ig_utils.Context import ETLContext

from pyspark.sql.functions import explode, col, lit
from pyspark.sql.types import StringType, TimestampType
from delta import DeltaTable

etl_context = ETLContext(ETL.claimsphere)

set_catalog()


def upsert_to_silver(microBatchDF, batchId):
    (
        DeltaTable.forName(spark, "catalog_dev.claimsphere_testing.claim")
        .alias("t")
        .merge(
            microBatchDF.alias("s"),
            "t.id = s.id"
        )
        .whenMatchedUpdateAll()
        .whenNotMatchedInsertAll()
        .execute()
    )

base = etl_context.base_path
delta_lake = etl_context.base_path + '/delta-lake/test/'
checkpoint_path = base + '/checkpoint/'
claim_path = base + '/landing-area/test/claim/'

df = (spark.readStream
  .format("cloudFiles")
  .option("cloudFiles.format", "json")
  .option("cloudFiles.schemaLocation", checkpoint_path)
  .option("cloudFiles.inferColumnTypes", 'true')
  .load(claim_path)
)

primary_key = 'id'
df = df.withColumn("aux", explode(df.items)).select(col('aux'))

def get_column(column_name):
    return col('aux').getItem(column_name).cast(StringType()).alias(column_name)

list_of_columns = [col for col in df.select("aux.*").columns if col != primary_key]

df = df.select(
    col('aux').getItem(primary_key).cast(StringType()).alias(primary_key),
    *(get_column(column) for column in list_of_columns),
    # lit(ingestion_date).cast(TimestampType()).alias('IngestionReferenceInsertedDate')
    )

(
  df.writeStream
  .option("checkpointLocation", checkpoint_path)
  .trigger(availableNow=True)
  .foreachBatch(upsert_to_silver)
  .start()
)