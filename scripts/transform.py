"""STEP 2 - TRANSFORM: clean the raw JSON with PySpark and calculate new columns."""
import glob
import json
import os

from pyspark.sql import SparkSession, Window
from pyspark.sql import functions as F

from scripts.config import PROCESSED_DIR, RAW_DIR


def get_spark():
    """Start Spark in local mode (runs inside this container, no cluster needed)."""
    return (
        SparkSession.builder.appName("stock_transform")
        .master("local[*]")
        .getOrCreate()
    )


def read_raw_files():
    """Turn every raw JSON file into a flat list of rows (one row per stock per day)."""
    rows = []
    for path in glob.glob(f"{RAW_DIR}/*.json"):
        with open(path) as f:
            data = json.load(f)

        symbol = data["Meta Data"]["2. Symbol"]
        for trade_date, v in data["Time Series (Daily)"].items():
            rows.append(
                (
                    symbol,
                    trade_date,
                    v["1. open"],
                    v["2. high"],
                    v["3. low"],
                    v["4. close"],
                    v["5. volume"],
                )
            )
    return rows


def run_transform():
    spark = get_spark()

    # 1. Load the rows into a Spark DataFrame (everything is text at first)
    columns = ["symbol", "trade_date", "open", "high", "low", "close", "volume"]
    df = spark.createDataFrame(read_raw_files(), columns)
    print(f"Rows read: {df.count()}")

    # 2. Fix the data types
    df = (
        df.withColumn("trade_date", F.to_date("trade_date"))
        .withColumn("open", F.col("open").cast("double"))
        .withColumn("high", F.col("high").cast("double"))
        .withColumn("low", F.col("low").cast("double"))
        .withColumn("close", F.col("close").cast("double"))
        .withColumn("volume", F.col("volume").cast("long"))
    )

    # 3. Remove duplicates (running the pipeline twice gives us the same day twice)
    df = df.dropDuplicates(["symbol", "trade_date"])
    print(f"Rows after removing duplicates: {df.count()}")

    # 4. Remove bad rows
    df = df.dropna(subset=["close"]).filter(F.col("close") > 0)

    # 5. New columns. A "window" = look at each stock separately, in date order.
    w = Window.partitionBy("symbol").orderBy("trade_date")

    df = df.withColumn("prev_close", F.lag("close").over(w))
    df = df.withColumn(
        "daily_return_pct",
        F.round((F.col("close") - F.col("prev_close")) / F.col("prev_close") * 100, 2),
    )
    df = df.withColumn("ma_5", F.round(F.avg("close").over(w.rowsBetween(-4, 0)), 2))

    df = df.drop("prev_close").orderBy("symbol", "trade_date")

    # 6. Save the clean data as Parquet for the next step
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    df.write.mode("overwrite").parquet(f"{PROCESSED_DIR}/daily_prices")
    print(f"Saved {df.count()} clean rows to {PROCESSED_DIR}/daily_prices")

    spark.stop()


if __name__ == "__main__":
    run_transform()
