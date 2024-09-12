import psycopg2
import os 
import logging
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from modules.crypto_data import run_pipeline
from dotenv import load_dotenv
#from modules import get_default_airflow_args
from modules.toRedshift import create_table_if_not_exists, send_toRedshift_task

# Cargar las variables de entorno
load_dotenv()

logging.info(f"REDSHIFT_HOST: {os.getenv('REDSHIFT_HOST')}")

# Definir los argumentos por defecto para el DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Definir el DAG
with DAG(
    'cryptocurrencies_etl',
    default_args=default_args,
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

    # Task 2
    create_table_task = PythonOperator(
        task_id = 'create_table_task',
        python_callable=create_table_if_not_exists,
        op_kwargs={
            'conn': psycopg2.connect(
                dbname=os.getenv('REDSHIFT_DBNAME'),
                user=os.getenv('REDSHIFT_USER'),
                password=os.getenv('REDSHIFT_PASSWORD'),
                host=os.getenv('REDSHIFT_HOST'),
                port=os.getenv('REDSHIFT_PORT', '5439')
            )
        }
    ) 
    
    # Task 3  
    load_data_task = PythonOperator(
        task_id="send_toRedshift_task",
        python_callable=send_toRedshift_task,
    )

    # Task 4
    send_email_task = PythonOperator(
        task_id="mail_sender_task",
        python_callable=None 
    )



    # Definir las dependencias entre las tareas
    run_pipeline_task >> create_table_task >> load_data_task >> send_email_task



print(os.getenv('REDSHIFT_HOST'))