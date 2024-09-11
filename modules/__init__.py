from .utils import get_default_airflow_args
from .getData import fetch_crypto_data
from .crypto_data import run_pipeline
#from .toRedshift import send_toRedshift
#from .task import create_table_if_not_exists, send_toRedshift_task