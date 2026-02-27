from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from datetime import datetime

DATABRICKS_CONN_ID = "databricks_default"

default_args = {
    "owner": "uday",
    "depends_on_past": False,
    "retries": 2
}

with DAG(
    dag_id="co2_emissions_pipeline",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    bronze_task = DatabricksRunNowOperator(
        task_id="run_bronze_job",
        databricks_conn_id=DATABRICKS_CONN_ID,
        job_id=909049220429304
    )

    silver_task = DatabricksRunNowOperator(
        task_id="run_silver_job",
        databricks_conn_id=DATABRICKS_CONN_ID,
        job_id=530257574658272
    )

    gold_task = DatabricksRunNowOperator(
        task_id="run_gold_job",
        databricks_conn_id=DATABRICKS_CONN_ID,
        job_id=62921764999920
    )

    bronze_task >> silver_task >> gold_task