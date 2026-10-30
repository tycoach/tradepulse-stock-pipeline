"""STEP 1 - EXTRACT: get raw daily prices for each stock and save them as JSON files."""
import json
import os
from datetime import date

import requests

from scripts.config import API_KEY, API_URL, RAW_DIR, SAMPLE_DIR, SYMBOLS


def fetch_from_api(symbol):
    """Call the Alpha Vantage API for one stock."""
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "compact",  # last ~100 days
        "apikey": API_KEY,
    }
    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    # Alpha Vantage returns HTTP 200 even when it refuses us, so check the body.
    if "Time Series (Daily)" not in data:
        raise ValueError(f"API did not return prices for {symbol}: {data}")
    return data


def read_from_sample(symbol):
    """Read the saved sample file for one stock (used when there is no API key)."""
    with open(f"{SAMPLE_DIR}/{symbol}.json") as f:
        return json.load(f)


def run_extract(run_date=None):
    """Save one raw JSON file per stock into the raw folder."""
    run_date = run_date or str(date.today())
    os.makedirs(RAW_DIR, exist_ok=True)

    if API_KEY:
        print("API key found -> calling the live API")
    else:
        print("No API key -> using the sample files")

    for symbol in SYMBOLS:
        data = fetch_from_api(symbol) if API_KEY else read_from_sample(symbol)

        file_path = f"{RAW_DIR}/{symbol}_{run_date}.json"
        with open(file_path, "w") as f:
            json.dump(data, f)
        print(f"Saved {symbol} -> {file_path}")


if __name__ == "__main__":
    run_extract()
