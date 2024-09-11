from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import pandas as pd
import numpy as np
import logging
from dotenv import load_dotenv
from modules.getData import fetch_crypto_data

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_pipeline():
    load_dotenv()

    # Extrar Data de la API desel modulo getdData
    try:
        data = fetch_crypto_data()
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        logging.error(f"Error al obtener datos de la API: {e}")
        return

    if 'data' in data:
        # Proceso de normalización y conversión a DataFrame
        df = pd.json_normalize(data['data'])

        # Filtrar las columnas necesarias
        columns_to_select = ['id', 'name', 'symbol', 'self_reported_market_cap', 'quote.USD.price', 'quote.USD.volume_24h']

        df_filtered = df[columns_to_select]

        # Renombrar columnas para mayor claridad
        df_filtered.columns = ['id', 'name', 'symbol', 'marketcap', 'price', 'volume_24']

        df = df_filtered.head(2000)

        # Convertir los datos a int64
        df = df.replace([np.inf, -np.inf]) # Remplazar valores infinitos por valores nan, luego rellenar con 0
        df['marketcap'] = df['marketcap'].fillna(0).astype('int64')
        df['volume_24'] = df['volume_24'].fillna(0).astype('int64')

        # Mostrar el DataFrame resultante
        num_rows = len(df_filtered)
        num_rows2 = len(df)
        print(f'La Api me extrae un total de filas de:', num_rows)
        print(df.head())
        return df
    else:
        print("No se encontraron datos en la respuesta de la API.")