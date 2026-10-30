"""Shared settings. Every other script imports from here, so change things in ONE place."""
import os

# --- Which stocks to pull -------------------------------------------------
SYMBOLS = os.getenv("SYMBOLS", "AAPL,MSFT,GOOGL").split(",")

# --- API (leave the key empty to use the sample files instead) ------------
API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", "")
API_URL = "https://www.alphavantage.co/query"

# --- Folders (these paths are INSIDE the container) -----------------------
DATA_DIR = "/opt/airflow/data"
SAMPLE_DIR = f"{DATA_DIR}/sample"
RAW_DIR = f"{DATA_DIR}/raw"
PROCESSED_DIR = f"{DATA_DIR}/processed"

# --- Postgres (the host name "postgres" is the service name in docker-compose)
DB_HOST = os.getenv("STOCKS_DB_HOST", "postgres")
DB_PORT = os.getenv("STOCKS_DB_PORT", "5432")
DB_NAME = os.getenv("STOCKS_DB_NAME", "stocks")
DB_USER = os.getenv("STOCKS_DB_USER", "airflow")
DB_PASSWORD = os.getenv("STOCKS_DB_PASSWORD", "airflow")

JDBC_URL = f"jdbc:postgresql://{DB_HOST}:{DB_PORT}/{DB_NAME}"
TABLE_NAME = "daily_prices"
