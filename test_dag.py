from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def print_hello():
    print("Hello from Airflow via Git-Sync!")
    return "Git-sync is working successfully!"

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    'test_git_sync_dag',
    default_args=default_args,
    description='A simple test DAG to verify git-sync and execution',
    schedule=timedelta(days=1),  # <-- Changed from schedule_interval to schedule
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['test', 'git-sync'],
) as dag:

    hello_task = PythonOperator(
        task_id='print_hello_task',
        python_callable=print_hello,
    )