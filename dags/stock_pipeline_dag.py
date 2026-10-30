"""The DAG: tells Airflow WHAT to run and in WHAT ORDER. The real work lives in /scripts."""
from datetime import datetime, timedelta

from airflow.decorators import dag, task

default_args = {
    "owner": "data-engineering",
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}

@dag(
    dag_id="stock_pipeline",
    description="Stock API -> PySpark -> Postgres",
    default_args=default_args,
    start_date=datetime(2026, 10, 1),
    schedule="@daily",
    catchup=False,
)
def stock_pipeline():

    # 1. Capture the run date context variable natively via function parameters
    @task
    def extract(ds=None):
        # Keeps top-level DAG parsing incredibly fast inside the Airflow scheduler
        from scripts.extract import run_extract
        return run_extract(run_date=ds)

    @task
    def transform():
        from scripts.transform import run_transform
        run_transform()

    @task
    def load():
        from scripts.load import run_load
        run_load()

    @task
    def validate():
        from scripts.validate import run_validate
        run_validate()

    # 2. Build the task flow execution order cleanly
    extract() >> transform() >> load() >> validate()

stock_pipeline()
