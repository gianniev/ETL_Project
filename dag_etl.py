import os 
import logging
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from modules.crypto_data import run_pipeline
from dotenv import load_dotenv
from modules import get_default_airflow_args

# Cargar las variables de entorno
load_dotenv()

logging.info(f"REDSHIFT_HOST: {os.getenv('REDSHIFT_HOST')}")


# Definir el DAG
with DAG(
    'cryptocurrencies_etl',
    default_args=get_default_airflow_args,
    description='Extract, Transform and Load crypto data daily',
    schedule_interval="@daily",
    catchup=False,
    tags=['crypto'],  # Añadir etiquetas para mejor organización
) as dag:
    
    args = [f"{datetime.now().strftime('%Y-%m-%d %H')}", os.getcwd()]

    # Task 1
    def execute_pipeline_task():
        return run_pipeline()

    run_pipeline_task = PythonOperator(
        task_id='run_pipeline_task',
        python_callable=execute_pipeline_task,
    )