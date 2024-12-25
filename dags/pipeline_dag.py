from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from pipeline.pipeline import run_pipeline

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'start_date': date(2024, 12, 24),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id = 'pipeline_dag',
    default_args=default_args,
    description = "simple data pipeline DAG for learning airflow",
    schedule_interval='@daily',
    catchup=False # disables backfilling failed runs
) as dag:
    
    task = PythonOperator(
        task_id='run_pipeline',
        python_callable=run_pipeline
    )