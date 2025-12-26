from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark.sql.functions import col, sum as _sum, count

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

PROCESSED_PATH = "s3://aws-prod-data-lake-vipul-2025/processed/sales/"
ANALYTICS_PATH = "s3://aws-prod-data-lake-vipul-2025/Analytics/sales_daily/"

# Read processed Parquet data
df = spark.read.parquet(PROCESSED_PATH)

# Create daily sales analytics
analytics_df = (
    df.groupBy("year", "month", "day")
      .agg(
          count("*").alias("total_orders"),
          _sum(col("quantity") * col("price")).alias("total_revenue")
      )
)

# Write analytics data
(
    analytics_df
    .write
    .mode("overwrite")
    .partitionBy("year", "month")
    .parquet(ANALYTICS_PATH)
)

print("Analytics ETL completed successfully")
