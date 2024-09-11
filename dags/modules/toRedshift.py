import psycopg2
import os
import logging
from datetime import datetime
import pandas as pd
import psycopg2  
from .utils import get_credentials, get_schema


def create_table_if_not_exists(conn):
    schema = get_schema()
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {schema}.coinmarketcap (
    id INTEGER IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(250),
    symbol VARCHAR(64),
    marketcap BIGINT,
    price DECIMAL(20, 10), 
    volume_24 BIGINT
    ); """
    
    with conn.cursor() as cur:
        cur.execute(create_table_query)
        conn.commit()
    print(f"Table {schema}.coinmarketcap is ready")


def send_toRedshift_task(**context):
    df = context['task_instance'].xcom_pull(task_ids='run_pipeline_task')
    if df is not None and not df.empty:
        # Obtener las credenciales de Redshift desde las variables de entorno
        redshift_credentials = {
            'host': os.getenv('REDSHIFT_HOST'),
            'dbname': os.getenv('REDSHIFT_DBNAME'),
            'user': os.getenv('REDSHIFT_USER'),
            'password': os.getenv('REDSHIFT_PASSWORD'),
            'port': os.getenv('REDSHIFT_PORT', '5439')  # '5439' como valor por defecto
        }

        # Verificar que todas las credenciales estén presentes
        if any(value is None or value == 'default_host' for value in redshift_credentials.values()):
           raise ValueError("Faltan credenciales de Redshift. Revisa las variables de entorno.")

        
        try:
            # Crear conexión a Redshift
            conn = psycopg2.connect(
                dbname=redshift_credentials['dbname'],
                user=redshift_credentials['user'],
                password=redshift_credentials['password'],
                host=redshift_credentials['host'],
                port=redshift_credentials['port']
            )
            cursor = conn.cursor()

            # Verifica los tipo de datos en el Dataframe
            print("DataFrame types:")
            print(df.dtypes)
            print(df[['marketcap', 'volume_24']].max())
            print(df[['marketcap', 'volume_24']].min())


            # Crear tabka si no existe
            create_table_if_not_exists(conn)

            
            # Crear query de insert
            columns = ', '.join([col for col in df.columns if col != 'id'])
            values = ', '.join(['%s'] * len([col for col in df.columns if col != 'id']))
            insert_query = f"INSERT INTO {get_schema()}.coinmarketcap ({columns}) VALUES ({values})"
            

            print("Insert query:")
            print(insert_query)
            
            # Insertar los datos en Redshift
            cursor.executemany(insert_query, df[['name', 'symbol', 'marketcap', 'price', 'volume_24']].values.tolist())            
            conn.commit()

        except Exception as e:
            logging.error(f"Error al insertar datos: {e}")
            raise
        finally:
            cursor.close()
            conn.close()
    else:
        logging.info("El dataframe está vacío. No se enviaron datos a Redshift.")
        
