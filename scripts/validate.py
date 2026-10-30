"""STEP 4 - VALIDATE: check the data landed in Postgres correctly. Fail loudly if not."""
import psycopg2

from scripts.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER, SYMBOLS, TABLE_NAME


def run_validate():
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )
    cur = conn.cursor()

    # Check 1: the table has rows
    cur.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
    row_count = cur.fetchone()[0]
    if row_count == 0:
        raise ValueError("Validation failed: the table is empty")

    # Check 2: no missing closing prices
    cur.execute(f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE close IS NULL")
    null_count = cur.fetchone()[0]
    if null_count > 0:
        raise ValueError(f"Validation failed: {null_count} rows have no closing price")

    # Check 3: every stock we asked for is there
    cur.execute(f"SELECT DISTINCT symbol FROM {TABLE_NAME}")
    found = {r[0] for r in cur.fetchall()}
    missing = set(SYMBOLS) - found
    if missing:
        raise ValueError(f"Validation failed: no data for {missing}")

    print(f"Validation passed: {row_count} rows, stocks = {sorted(found)}")
    conn.close()


if __name__ == "__main__":
    run_validate()
