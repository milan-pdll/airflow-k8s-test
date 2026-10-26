from datetime import datetime
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

IMAGE = "ghcr.io/milan-pdll/spark-py:3.5.0-v2"
PG_SECRET = "postgres-conn"

# Make the Postgres credentials available to driver and executors alike
pg_env = {
    f"spark.kubernetes.{role}.secretKeyRef.{key}": f"{PG_SECRET}:{key}"
    for role in ("driver", "executor")
    for key in ("PG_HOST", "PG_PORT", "PG_DB", "PG_USER", "PG_PASSWORD")
}

with DAG(
    "postgres_usecase_dag",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args={"owner": "data-platform"},
) as dag:
    SparkSubmitOperator(
        task_id="postgres_usecase",
        conn_id="spark_k8s",
        application="local:///opt/spark/jobs/postgres_usecase.py",
        name="postgres-usecase",
        verbose=False,
        conf={
            "spark.kubernetes.container.image": IMAGE,
            "spark.kubernetes.container.image.pullPolicy": "IfNotPresent",
            "spark.kubernetes.namespace": "spark",
            "spark.kubernetes.authenticate.driver.serviceAccountName": "spark-sa",
            "spark.executor.instances": "1",
            "spark.executor.memory": "512m",
            "spark.executor.cores": "1",
            "spark.driver.memory": "512m",
            "spark.eventLog.enabled": "false",
            **pg_env,
        },
    )
