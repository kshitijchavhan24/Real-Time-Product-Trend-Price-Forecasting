from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('amazon_scraper_dag',
          default_args=default_args,
          description='A simple DAG to run the Amazon scraper',
          schedule_interval='@hourly',  # Adjust the schedule as needed
          catchup=False)

run_scraper = BashOperator(
    task_id='run_amazon_scraper',
    bash_command='python /opt/airflow/dags/amazon_scraper.py',
    dag=dag
)
