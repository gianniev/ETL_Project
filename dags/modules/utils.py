from dotenv import load_dotenv, find_dotenv
from datetime import datetime, timedelta
import os

# Encuentra el archivo .env
dotenv_path = find_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

load_dotenv(dotenv_path) # take enviroment variables from .env file

def get_schema():
    return os.getenv("REDSHIFT_SCHEMA")



def get_credentials():
    url = os.getenv("REDSHIFT_URL")
    user = os.getenv("REDSHIFT_USER")
    pwd = os.getenv("REDSHIFT_PWD")
    port = os.GETENV("REDSHIFT_PORT")
    data_base = os.getenv("REDSHIFT_DB")

    return {
        "dbname": data_base,
        "user": user,
        "password": pwd,
        "host": url,
        "port": port,
    }


def get_default_airflow_args():
    return{
        "owner": "gianni_ev93",
        "depends_on_past": False,
        "start_date": datetime(2023, 1, 1),
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "catch"
        "retry_delay": timedelta(minutes=5),
    }