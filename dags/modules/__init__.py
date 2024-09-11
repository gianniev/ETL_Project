from .utils import get_default_airflow_args
from .getData import fetch_crypto_data
from .crypto_data import run_pipeline
from .toRedshift import create_table_if_not_exists, send_toRedshift_task
#from .task import create_table_if_not_exists, send_toRedshift_task