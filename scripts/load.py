"""STEP 3 - LOAD: read the clean Parquet data and write it into Postgres."""
from pyspark.sql import SparkSession

from scripts.config import (
    DB_PASSWORD,
    DB_USER,
    JDBC_URL,
    PROCESSED_DIR,
    TABLE_NAME,
)


def run_load():
    spark = (
        SparkSession.builder.appName("stock_load")
        .master("local[*]")
        .getOrCreate()
    )

    df = spark.read.parquet(f"{PROCESSED_DIR}/daily_prices")

    # "overwrite" + "truncate" = empty the table and refill it.
    # This means running the pipeline twice will NOT create duplicate rows.
    (
        df.write.format("jdbc")
        .option("url", JDBC_URL)
        .option("dbtable", TABLE_NAME)
        .option("user", DB_USER)
        .option("password", DB_PASSWORD)
        .option("driver", "org.postgresql.Driver")
        .option("truncate", "true")
        .mode("overwrite")
        .save()
    )
    print(f"Loaded {df.count()} rows into {TABLE_NAME}")

    spark.stop()


if __name__ == "__main__":
    run_load()
