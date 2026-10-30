-- Runs once, the first time the Postgres container starts.
-- Airflow keeps its own data in the "airflow" database; our stock data goes in "stocks".
CREATE DATABASE stocks;
