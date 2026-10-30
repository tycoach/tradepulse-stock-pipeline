# Stock Pipeline: Docker + Airflow + PySpark + Postgres

A small data pipeline that runs entirely inside Docker.

```
Stock API  ->  extract  ->  transform (PySpark)  ->  load  ->  validate
                 JSON          Parquet               Postgres     checks
```

## Project layout

| Path | What it does |
|---|---|
| `docker-compose.yml` | Starts Postgres and Airflow together |
| `Dockerfile` | Builds the Airflow image with Java, PySpark and the Postgres driver |
| `dags/stock_pipeline_dag.py` | Tells Airflow which steps to run, in what order |
| `scripts/config.py` | All settings in one place |
| `scripts/extract.py` | Step 1: get prices from the API (or sample files) |
| `scripts/transform.py` | Step 2: clean and calculate with PySpark |
| `scripts/load.py` | Step 3: write to Postgres |
| `scripts/validate.py` | Step 4: check the data landed correctly |
| `data/sample/` | Sample prices, used when there is no API key |
| `sql/check_results.sql` | Queries to explore the result |

## Run it

1. Install and open **Docker Desktop**.
2. In this folder, create your settings file:
   ```
   cp .env.example .env
   ```
   Optional: paste a free [Alpha Vantage key](https://www.alphavantage.co/support/#api-key) into `.env`. Leave it empty to use the sample data.
3. Start everything (the first build takes a few minutes):
   ```
   docker compose up --build
   ```
4. Open **http://localhost:8080** and log in with `admin` / `admin`.
5. Switch on the `stock_pipeline` DAG, then click **Trigger DAG** (the play button).
6. Watch the four tasks turn green. Click a task, then **Logs**, to see what it printed.
7. Check the data in Postgres with any SQL client:
   `host: localhost`, `port: 5433`, `database: stocks`, `user: airflow`, `password: airflow`.
   Then run the queries in `sql/check_results.sql`.

Stop with `Ctrl+C`, or run `docker compose down`. Add `-v` to also delete the database.

## Useful commands

```
docker compose ps                  # what is running
docker compose logs airflow        # Airflow's output
docker compose exec airflow bash   # open a terminal inside the container
docker compose exec airflow python -m scripts.extract   # run one step by hand
```

## If something goes wrong

- **Port 8080 or 5433 already in use:** change the left-hand number in `ports:` in `docker-compose.yml`.
- **Task fails with "API did not return prices":** you hit the free API limit, or the key is wrong. Empty the key in `.env` to use sample data, then restart.
- **Permission denied writing to `data/` (Linux only):** run `chmod -R 777 data`.
- **Changed `.env`:** run `docker compose up -d --force-recreate airflow`.
- **DAG not showing:** wait about a minute, or check `docker compose logs airflow` for a Python error.

## Practice ideas

1. Add a fourth stock (`SYMBOLS` in `.env`) and see it flow through.
2. Add a `ma_20` column in `transform.py`.
3. Add a validation check that no `close` price is above 10,000.
