from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark.sql.functions import col, year, month, dayofmonth, to_date

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

RAW_PATH = "s3://aws-prod-data-lake-vipul-2025/raw/Sales/"
PROCESSED_PATH = "s3://aws-prod-data-lake-vipul-2025/processed/sales/"
ERROR_PATH = "s3://aws-prod-data-lake-vipul-2025/Error/sales/"

df = spark.read.option("header", "true").csv(RAW_PATH)

df = (
    df.withColumn("order_id", col("order_id").cast("int"))
      .withColumn("quantity", col("quantity").cast("int"))
      .withColumn("price", col("price").cast("double"))
      .withColumn("order_date", to_date(col("order_date")))
)

valid_df = df.filter(
    col("order_id").isNotNull() &
    col("order_date").isNotNull() &
    col("quantity").isNotNull() &
    col("price").isNotNull()
)

error_df = df.subtract(valid_df)

if error_df.count() > 0:
    error_df.write.mode("append").json(ERROR_PATH)

final_df = (
    valid_df
    .withColumn("year", year(col("order_date")))
    .withColumn("month", month(col("order_date")))
    .withColumn("day", dayofmonth(col("order_date")))
)

final_df.write.mode("append") \
    .partitionBy("year", "month", "day") \
    .parquet(PROCESSED_PATH)

print("ETL completed successfully")
